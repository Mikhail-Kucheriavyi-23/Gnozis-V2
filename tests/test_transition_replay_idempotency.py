import pytest

from gnosis.core import Candidate, TestResult, TransitionRecord
from gnosis.storage import StorageCorruptionError, connect, persist_transition, save_instance, verify_durable_graph
from gnosis.instances.instance import Instance
from gnosis.core import State


def test_same_transition_replay_is_idempotent():
    conn = connect()
    instance = Instance.create_root("user-1", State(elements={"a": 1}))
    save_instance(conn, instance)
    proposed = instance.engine.state.with_elements({"b": 2})
    candidate = Candidate(instance.engine.state.state_id, proposed, "replay-test")
    record = instance.engine.step(candidate)

    persist_transition(conn, instance, candidate, record, actor="test")
    transition_count = conn.execute("SELECT COUNT(*) FROM transitions").fetchone()[0]
    audit_count = conn.execute("SELECT COUNT(*) FROM audit_events WHERE transition_id IS NOT NULL").fetchone()[0]
    head = conn.execute("SELECT current_state_id FROM instances WHERE instance_id=?", (instance.instance_id,)).fetchone()[0]

    persist_transition(conn, instance, candidate, record, actor="test")

    assert conn.execute("SELECT COUNT(*) FROM transitions").fetchone()[0] == transition_count
    assert conn.execute("SELECT COUNT(*) FROM audit_events WHERE transition_id IS NOT NULL").fetchone()[0] == audit_count
    assert conn.execute("SELECT current_state_id FROM instances WHERE instance_id=?", (instance.instance_id,)).fetchone()[0] == head
    verify_durable_graph(conn)


def test_same_transition_id_with_conflicting_content_is_rejected():
    conn = connect()
    instance = Instance.create_root("user-1", State(elements={"a": 1}))
    save_instance(conn, instance)
    proposed = instance.engine.state.with_elements({"b": 2})
    candidate = Candidate(instance.engine.state.state_id, proposed, "replay-test")
    record = instance.engine.step(candidate)
    persist_transition(conn, instance, candidate, record, actor="test")

    conflicting = TransitionRecord(
        from_state_id=record.from_state_id,
        to_state_id=record.to_state_id,
        candidate_id=record.candidate_id,
        test_result=TestResult(False, ("conflicting",)),
        accepted=False,
        reason="conflicting replay",
        test_rule_id=record.test_rule_id,
    )
    with pytest.raises((ValueError, StorageCorruptionError)):
        persist_transition(conn, candidate= candidate, instance=instance, record=conflicting, actor="test")
