import pytest

from gnosis.core import Candidate, State
from gnosis.instances.instance import Instance
from gnosis.reflection.gate import run_reflection_gate
from gnosis.storage import connect, save_instance, persist_transition


def test_reflection_gate_reaches_durable_read_only_evidence():
    conn = connect()
    instance = Instance.create_root("user-1", State(elements={"a": 1}))
    save_instance(conn, instance)
    proposed = instance.engine.state.with_elements({"a": 2})
    candidate = Candidate(instance.engine.state.state_id, proposed, "test")
    record = instance.engine.step(candidate)
    persist_transition(conn, instance, candidate, record, actor="test")

    result = run_reflection_gate(instance.engine, conn, instance.instance_id)

    assert result.passed
    assert result.transition_count == 1
    assert result.durable_graph_verified
    assert result.recovery_state_id == instance.engine.state.state_id
    assert result.report_id.startswith("reflection:")
    assert result.artifact["authority"] == "READ_ONLY"
    conn.close()


def test_reflection_gate_fails_closed_without_canonical_history():
    conn = connect()
    instance = Instance.create_root("user-1", State(elements={"a": 1}))
    save_instance(conn, instance)
    result = run_reflection_gate(instance.engine, conn, instance.instance_id)
    assert not result.passed
    assert "canonical Core history is empty" in result.reasons
    conn.close()
