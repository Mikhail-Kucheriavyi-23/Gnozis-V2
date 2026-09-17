import sqlite3

import pytest

from gnosis.core import Candidate, State
from gnosis.instances.instance import Instance
from gnosis.storage import (
    connect,
    load_instance,
    persist_transition,
    save_instance,
    verify_audit_chain,
)


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
