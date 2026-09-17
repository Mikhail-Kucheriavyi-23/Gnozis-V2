import sqlite3
from pathlib import Path

import pytest

from gnosis.core import Candidate, State
from gnosis.instances.instance import Instance
from gnosis.storage import (
    StorageCorruptionError,
    append_audit,
    connect,
    load_instance,
    persist_transition,
    save_instance,
    verify_audit_chain,
    verify_durable_graph,
)
from gnosis.storage.repositories import _audit_hash


def root():
    return Instance.create_root("user-1", State(elements={"a": 1}))


def test_root_round_trip_and_audit_chain():
    conn = connect()
    instance = root()
    save_instance(conn, instance)
    loaded = load_instance(conn, instance.instance_id)
    assert loaded.engine.state.state_id == instance.engine.state.state_id
    assert verify_audit_chain(conn)[0] == 1


def test_accepted_transition_atomically_advances_head():
    conn = connect()
    instance = root()
    save_instance(conn, instance)
    proposed = instance.engine.state.with_elements({"b": 2})
    candidate = Candidate(instance.engine.state.state_id, proposed, "test")
    record = instance.engine.step(candidate)
    persist_transition(conn, instance, candidate, record, actor="test")
    loaded = load_instance(conn, instance.instance_id)
    assert record.accepted
    assert loaded.engine.state.state_id == proposed.state_id
    assert verify_audit_chain(conn)[0] == 2


def test_rejected_transition_does_not_advance_head():
    conn = connect()
    instance = root()
    save_instance(conn, instance)
    proposed = instance.engine.state.with_elements({"b": 2})
    candidate = Candidate(instance.engine.state.state_id, proposed, "test")
    from gnosis.core import TestResult, TransitionRecord
    rejected = TransitionRecord(instance.engine.state.state_id, proposed.state_id, candidate.candidate_id,
                                 TestResult(False, ("rejected",)), False, "rejected")
    persist_transition(conn, instance, candidate, rejected, actor="test")
    assert load_instance(conn, instance.instance_id).engine.state.state_id == instance.engine.state.state_id
    assert verify_audit_chain(conn)[0] == 2


def test_audit_update_and_delete_are_rejected():
    conn = connect()
    instance = root()
    save_instance(conn, instance)
    with pytest.raises(sqlite3.DatabaseError):
        conn.execute("UPDATE audit_events SET result='tampered' WHERE sequence=1")
    with pytest.raises(sqlite3.DatabaseError):
        conn.execute("DELETE FROM audit_events WHERE sequence=1")


def test_audit_payload_tampering_fails_verification():
    conn = connect()
    instance = root()
    save_instance(conn, instance)
    conn.execute("DROP TRIGGER audit_events_no_update")
    conn.execute("UPDATE audit_events SET result='tampered' WHERE sequence=1")
    with pytest.raises(ValueError, match="hash mismatch"):
        verify_audit_chain(conn)


def test_foreign_keys_reject_orphan_instance_state():
    conn = connect()
    with pytest.raises(sqlite3.IntegrityError):
        conn.execute(
            "INSERT INTO instances(instance_id, owner_id, current_state_id, generation, status, created_at) VALUES ('i', 'u', 'missing', 0, 'active', 'now')"
        )


def test_supported_schema_version_connects(tmp_path: Path):
    path = tmp_path / "supported.sqlite"
    conn = connect(path)
    assert conn.execute("SELECT value FROM schema_meta WHERE key='schema_version'").fetchone()[0] == "3"
    conn.close()


@pytest.mark.parametrize("version", ["999", "2"])
def test_incompatible_schema_version_fails_closed_without_modification(tmp_path: Path, version: str):
    path = tmp_path / f"incompatible-{version}.sqlite"
    setup = sqlite3.connect(path)
    setup.execute("CREATE TABLE schema_meta (key TEXT PRIMARY KEY, value TEXT NOT NULL)")
    setup.execute("INSERT INTO schema_meta(key, value) VALUES ('schema_version', ?)", (version,))
    setup.commit()
    before = path.read_bytes()
    setup.close()

    with pytest.raises(RuntimeError, match="incompatible schema version"):
        connect(path)

    assert path.read_bytes() == before
    check = sqlite3.connect(path)
    assert check.execute("SELECT value FROM schema_meta WHERE key='schema_version'").fetchone()[0] == version
    assert check.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='states'").fetchone() is None
    check.close()


def _three_event_chain():
    conn = connect()
    root_instance = root()
    save_instance(conn, root_instance)
    append_audit(conn, actor="test", action="one", resource="r1", result="ok", timestamp="t1", event_key="e1")
    append_audit(conn, actor="test", action="two", resource="r2", result="ok", timestamp="t2", event_key="e2")
    append_audit(conn, actor="test", action="three", resource="r3", result="ok", timestamp="t3", event_key="e3")
    return conn


def test_a16_middle_audit_event_corruption_fails_verification():
    conn = _three_event_chain()
    conn.execute("DROP TRIGGER audit_events_no_update")
    conn.execute("UPDATE audit_events SET result='tampered' WHERE event_id='e2'")
    with pytest.raises(StorageCorruptionError, match="hash mismatch"):
        verify_audit_chain(conn)


def test_a17_prev_hash_tampering_fails_verification():
    conn = _three_event_chain()
    conn.execute("DROP TRIGGER audit_events_no_update")
    conn.execute("UPDATE audit_events SET prev_hash=? WHERE event_id='e2'", ("f" * 64,))
    with pytest.raises(StorageCorruptionError, match="sequence/link mismatch"):
        verify_audit_chain(conn)


def test_a18_sequence_tampering_fails_verification():
    conn = _three_event_chain()
    conn.execute("DROP TRIGGER audit_events_no_update")
    conn.execute("UPDATE audit_events SET sequence=5 WHERE event_id='e2'")
    conn.execute("UPDATE audit_events SET sequence=3 WHERE event_id='e3'")
    conn.execute("UPDATE audit_events SET sequence=4 WHERE event_id='e2'")
    with pytest.raises(StorageCorruptionError, match="sequence/link mismatch"):
        verify_audit_chain(conn)


def test_a20_inserting_audit_event_into_middle_fails_verification():
    conn = _three_event_chain()
    conn.execute(
        "INSERT INTO audit_events(event_id, sequence, transition_id, actor, action, resource, result, timestamp, prev_hash, event_hash) "
        "VALUES ('e2.5', 2.5, NULL, 'test', 'inserted', 'middle', 'ok', 't2.5', ?, ?)",
        ("0" * 64, "1" * 64),
    )
    with pytest.raises(StorageCorruptionError, match="sequence/link mismatch"):
        verify_audit_chain(conn)


def _persisted_transition():
    conn = connect()
    instance = root()
    save_instance(conn, instance)
    proposed = instance.engine.state.with_elements({"b": 2})
    candidate = Candidate(instance.engine.state.state_id, proposed, "test")
    record = instance.engine.step(candidate)
    persist_transition(conn, instance, candidate, record, actor="test")
    return conn, instance, record


def test_a42_missing_audit_evidence_fails_durable_graph_verification():
    conn, instance, record = _persisted_transition()
    conn.execute("DROP TRIGGER audit_events_no_delete")
    conn.execute("DELETE FROM audit_events WHERE transition_id=?", (record and next(conn.execute("SELECT transition_id FROM transitions WHERE instance_id=?", (instance.instance_id,)))[0],))
    with pytest.raises(StorageCorruptionError, match="audit"):
        verify_durable_graph(conn)


def test_a50_audit_resource_mismatch_fails_durable_graph_verification():
    conn, instance, record = _persisted_transition()
    row = conn.execute(
        "SELECT event_id, sequence, transition_id, actor, action, resource, result, timestamp, prev_hash FROM audit_events WHERE transition_id IS NOT NULL"
    ).fetchone()
    conn.execute("DROP TRIGGER audit_events_no_update")
    event = {
        "event_id": row[0], "sequence": row[1], "transition_id": row[2],
        "actor": row[3], "action": row[4], "resource": "wrong-resource",
        "result": row[6], "timestamp": row[7], "prev_hash": row[8],
    }
    conn.execute("UPDATE audit_events SET resource=?, event_hash=? WHERE event_id=?", ("wrong-resource", _audit_hash(event), row[0]))
    with pytest.raises(StorageCorruptionError, match="audit evidence"):
        verify_durable_graph(conn)
