import sqlite3
import os
import subprocess
import sys
from pathlib import Path

import pytest

from gnosis.core import Candidate, Relation, State, TestResult, TransitionRecord
from gnosis.instances.instance import Instance
from gnosis.storage import (
    StorageCorruptionError,
    append_audit,
    connect,
    load_instance,
    persist_transition,
    recover_instance,
    save_candidate,
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
        conn.execute("INSERT INTO instances(instance_id, owner_id, current_state_id, generation, status, created_at) VALUES ('i', 'u', 'missing', 0, 'active', 'now')")


def test_supported_schema_version_connects(tmp_path: Path):
    path = tmp_path / "supported.sqlite"
    conn = connect(path)
    assert conn.execute("SELECT value FROM schema_meta WHERE key='schema_version'").fetchone()[0] == "4"
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
    conn.execute("INSERT INTO audit_events(event_id, sequence, transition_id, actor, action, resource, result, timestamp, prev_hash, event_hash) VALUES ('e2.5', 2.5, NULL, 'test', 'inserted', 'middle', 'ok', 't2.5', ?, ?)", ("0" * 64, "1" * 64))
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
    transition_id = next(conn.execute("SELECT transition_id FROM transitions WHERE instance_id=?", (instance.instance_id,)))[0]
    conn.execute("DELETE FROM audit_events WHERE transition_id=?", (transition_id,))
    with pytest.raises(StorageCorruptionError, match="audit"):
        verify_durable_graph(conn)


def test_a50_audit_resource_mismatch_fails_durable_graph_verification():
    conn, instance, record = _persisted_transition()
    row = conn.execute("SELECT event_id, sequence, transition_id, actor, action, resource, result, timestamp, prev_hash FROM audit_events WHERE transition_id IS NOT NULL").fetchone()
    conn.execute("DROP TRIGGER audit_events_no_update")
    event = {"event_id": row[0], "sequence": row[1], "transition_id": row[2], "actor": row[3], "action": row[4], "resource": "wrong-resource", "result": row[6], "timestamp": row[7], "prev_hash": row[8]}
    conn.execute("UPDATE audit_events SET resource=?, event_hash=? WHERE event_id=?", ("wrong-resource", _audit_hash(event), row[0]))
    with pytest.raises(StorageCorruptionError, match="audit evidence"):
        verify_durable_graph(conn)


def _rejected_transition_fixture(conn):
    instance = root()
    save_instance(conn, instance)
    proposed = instance.engine.state.with_elements({"b": 2})
    candidate = Candidate(instance.engine.state.state_id, proposed, "rejected")
    record = TransitionRecord(instance.engine.state.state_id, proposed.state_id, candidate.candidate_id, TestResult(False, ("rejected",)), False, "rejected")
    return instance, candidate, record


def test_a08_rejected_candidate_survives_close_reopen_without_head_advance(tmp_path):
    path = tmp_path / "rejected.sqlite"
    conn = connect(path)
    instance, candidate, record = _rejected_transition_fixture(conn)
    persist_transition(conn, instance, candidate, record, actor="u")
    original = instance.engine.state.state_id
    conn.close()
    reopened = connect(path)
    recovered = recover_instance(reopened, instance.instance_id)
    assert recovered.engine.state.state_id == original
    assert verify_durable_graph(reopened)[0] == 2


def test_a28_noop_transition_remains_valid_on_persistence_path():
    conn = connect()
    instance = root()
    save_instance(conn, instance)
    noop = State(elements=instance.engine.state.elements, relations=instance.engine.state.relations, version=instance.engine.state.version + 1)
    candidate = Candidate(instance.engine.state.state_id, noop, "noop")
    record = instance.engine.step(candidate)
    assert record.accepted is False
    persist_transition(conn, instance, candidate, record, actor="u")
    assert recover_instance(conn, instance.instance_id).engine.state.state_id == instance.engine.state.state_id
    assert verify_durable_graph(conn)[0] == 2


def test_a29_rejected_candidate_cannot_become_head_after_close_reopen(tmp_path):
    path = tmp_path / "rejected-head.sqlite"
    conn = connect(path)
    instance, candidate, record = _rejected_transition_fixture(conn)
    persist_transition(conn, instance, candidate, record, actor="u")
    proposed_id = candidate.proposed_state.state_id
    conn.close()
    reopened = connect(path)
    recovered = recover_instance(reopened, instance.instance_id)
    assert recovered.engine.state.state_id != proposed_id
    assert recovered.engine.state.state_id == instance.engine.state.state_id


def test_a02_orphan_relation_is_rejected_by_foreign_key():
    conn = connect()
    with pytest.raises(sqlite3.IntegrityError):
        conn.execute("INSERT INTO relations(state_id, relation_order, relation_id, source_id, target_id, relation_type, value, created_at) VALUES ('missing', 0, 'r', 's', 't', 'x', NULL, 'now')")


def test_a03_orphan_candidate_is_rejected_by_foreign_key():
    conn = connect()
    with pytest.raises(sqlite3.IntegrityError):
        conn.execute("INSERT INTO candidates(candidate_id, parent_state_id, candidate_state_id, origin, seed, created_at) VALUES ('c', 'missing', 'missing', 'test', NULL, 'now')")


def test_a05_state_payload_tamper_fails_closed():
    conn = connect()
    instance = root()
    save_instance(conn, instance)
    conn.execute("UPDATE states SET payload=? WHERE state_id=?", ('{"elements":{"tampered":true},"version":0}', instance.engine.state.state_id))
    with pytest.raises(StorageCorruptionError, match="state hash mismatch"):
        load_instance(conn, instance.instance_id)


def test_a06_relation_tamper_fails_closed():
    conn = connect()
    state = State(elements={"a": 1, "b": 2}, relations=[Relation("a", "b", "link")])
    instance = Instance.create_root("u", state)
    save_instance(conn, instance)
    conn.execute("UPDATE relations SET target_id='tampered' WHERE state_id=?", (state.state_id,))
    with pytest.raises(StorageCorruptionError, match="relation hash mismatch"):
        load_instance(conn, instance.instance_id)


def test_a09_root_atomicity_rolls_back_failed_root_transaction(monkeypatch):
    conn = connect()
    instance = Instance.create_root("u", State(elements={"root": 0}))
    def fail_audit(*args, **kwargs):
        raise RuntimeError("injected root failure")
    monkeypatch.setattr("gnosis.storage.repositories.append_audit", fail_audit)
    with pytest.raises(RuntimeError, match="injected root failure"):
        save_instance(conn, instance)
    assert conn.execute("SELECT count(*) FROM instances").fetchone()[0] == 0
    assert conn.execute("SELECT count(*) FROM states").fetchone()[0] == 0


def test_a13_process_exit_after_commit_reopens_valid_database(tmp_path):
    path = tmp_path / "crash.sqlite"
    script = """
from gnosis.core import Candidate, State
from gnosis.instances.instance import Instance
from gnosis.storage import connect, persist_transition, save_instance
conn = connect(r'{path}')
instance = Instance.create_root('u', State(elements={{'a': 1}}))
save_instance(conn, instance)
proposed = instance.engine.state.with_elements({{'b': 2}})
candidate = Candidate(instance.engine.state.state_id, proposed, 'crash')
record = instance.engine.step(candidate)
persist_transition(conn, instance, candidate, record, actor='u')
conn.close()
""".format(path=path)
    completed = subprocess.run([sys.executable, "-c", script], cwd=Path(__file__).parents[1], check=False)
    assert completed.returncode == 0
    reopened = connect(path)
    rows = reopened.execute("SELECT count(*) FROM transitions").fetchone()[0]
    assert rows == 1
    assert verify_durable_graph(reopened)[0] == 2


def test_a19_delete_final_audit_event_fails_recovery():
    conn, instance, record = _persisted_transition()
    conn.execute("DROP TRIGGER audit_events_no_delete")
    transition_id_value = conn.execute("SELECT transition_id FROM transitions WHERE instance_id=?", (instance.instance_id,)).fetchone()[0]
    conn.execute("DELETE FROM audit_events WHERE transition_id=?", (transition_id_value,))
    with pytest.raises(StorageCorruptionError, match="audit evidence"):
        recover_instance(conn, instance.instance_id)


def test_a25_duplicate_state_id_with_different_payload_is_rejected():
    conn = connect()
    instance = root()
    save_instance(conn, instance)
    with pytest.raises(sqlite3.IntegrityError):
        conn.execute("INSERT INTO states(state_id, version, payload, created_at) VALUES (?, ?, ?, ?)", (instance.engine.state.state_id, 0, '{"elements":{"different":true},"version":0}', 'now'))


def test_a26_duplicate_candidate_id_with_different_payload_is_rejected():
    conn = connect()
    instance = root()
    save_instance(conn, instance)
    proposed = instance.engine.state.with_elements({"b": 2})
    candidate = Candidate(instance.engine.state.state_id, proposed, "test")
    save_candidate(conn, candidate)
    with pytest.raises(sqlite3.IntegrityError):
        conn.execute("INSERT INTO candidates(candidate_id, parent_state_id, candidate_state_id, origin, seed, created_at) VALUES (?, ?, ?, ?, ?, ?)", (candidate.candidate_id, candidate.parent_state_id, candidate.proposed_state.state_id, "other", None, "now"))


def test_a39_unsupported_instance_status_fails_load():
    conn = connect()
    instance = root()
    save_instance(conn, instance)
    conn.execute("PRAGMA foreign_keys=OFF")
    with pytest.raises(sqlite3.IntegrityError, match="CHECK constraint failed"):
        conn.execute("UPDATE instances SET status='unknown' WHERE instance_id=?", (instance.instance_id,))


def test_a46_duplicate_relation_is_rejected_by_primary_key():
    conn = connect()
    state = State(elements={"a": 1, "b": 2}, relations=[Relation("a", "b", "link")])
    instance = Instance.create_root("u", state)
    save_instance(conn, instance)
    relation = state.relations[0]
    with pytest.raises(sqlite3.IntegrityError):
        conn.execute("INSERT INTO relations(state_id, relation_order, relation_id, source_id, target_id, relation_type, value, created_at) VALUES (?, ?, ?, ?, ?, ?, ?, ?)", (state.state_id, 1, relation.relation_id, relation.source, relation.target, relation.relation_type, None, "now"))


def test_a47_read_snapshot_during_active_writer(tmp_path):
    path = tmp_path / "snapshot.sqlite"
    writer = connect(path)
    reader = connect(path)
    instance = root()
    save_instance(writer, instance)
    proposed = instance.engine.state.with_elements({"b": 2})
    writer.execute("BEGIN IMMEDIATE")
    writer.execute("INSERT INTO states(state_id, version, payload, created_at) VALUES (?, ?, ?, ?)", (proposed.state_id, proposed.version, '{"elements":{"b":2},"version":1}', 'now'))
    assert load_instance(reader, instance.instance_id).engine.state.state_id == instance.engine.state.state_id
    writer.rollback()


def test_a48_rollback_reopen_restores_prior_chain(tmp_path):
    path = tmp_path / "rollback-reopen.sqlite"
    conn = connect(path)
    instance = root()
    save_instance(conn, instance)
    original_state_id = instance.engine.state.state_id
    proposed = instance.engine.state.with_elements({"b": 2})
    candidate = Candidate(instance.engine.state.state_id, proposed, "rollback")
    record = instance.engine.step(candidate)
    with pytest.raises(RuntimeError, match="injected failure"):
        persist_transition(conn, instance, candidate, record, actor="u", failure_at="after_transition")
    conn.close()
    reopened = connect(path)
    assert recover_instance(reopened, instance.instance_id).engine.state.state_id == original_state_id
    assert verify_durable_graph(reopened)[0] == 1
