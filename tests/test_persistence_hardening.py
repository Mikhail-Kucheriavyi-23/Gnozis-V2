import json
import sqlite3

import pytest

from gnosis.core import Candidate, State, TestResult, TransitionRecord
from gnosis.instances.instance import Instance
from gnosis.storage import (
    SecretMaterialError,
    StorageCorruptionError,
    append_audit,
    connect,
    load_instance,
    persist_transition,
    recover_instance,
    save_instance,
    verify_durable_graph,
)


def test_orphan_transition_is_rejected_by_schema():
    conn = connect()
    instance = Instance.create_root("u", State(elements={"a": 1}))
    save_instance(conn, instance)
    with pytest.raises(sqlite3.IntegrityError):
        conn.execute("INSERT INTO transitions(transition_id, instance_id, candidate_id, from_state_id, to_state_id, accepted, reasons, created_at) VALUES ('t', ?, NULL, ?, ?, 1, '[]', 'now')", (instance.instance_id, instance.engine.state.state_id, instance.engine.state.state_id))


def test_audit_event_replay_is_idempotent():
    conn = connect()
    first = append_audit(conn, actor="u", action="x", resource="r", result="ok", timestamp="fixed", event_key="request-1")
    second = append_audit(conn, actor="u", action="x", resource="r", result="ok", timestamp="fixed", event_key="request-1")
    assert first == second
    assert conn.execute("SELECT count(*) FROM audit_events").fetchone()[0] == 1


def test_conflicting_audit_replay_is_rejected():
    conn = connect()
    append_audit(conn, actor="u", action="x", resource="r", result="ok", event_key="request-1")
    with pytest.raises(StorageCorruptionError):
        append_audit(conn, actor="u", action="x", resource="other", result="ok", event_key="request-1")


def test_secret_bearing_state_is_rejected_before_write():
    conn = connect()
    instance = Instance.create_root("u", State(elements={"api_key": "do-not-store"}))
    with pytest.raises(SecretMaterialError):
        save_instance(conn, instance)
    assert conn.execute("SELECT count(*) FROM states").fetchone()[0] == 0


def test_budget_and_history_survive_restart():
    conn = connect()
    instance = Instance.create_root("u", State(elements={"a": 1}))
    save_instance(conn, instance)
    proposed = instance.engine.state.with_elements({"b": 2})
    candidate = Candidate(instance.engine.state.state_id, proposed, "test")
    record = instance.engine.step(candidate)
    persist_transition(conn, instance, candidate, record, actor="u")
    recovered = load_instance(conn, instance.instance_id)
    assert recovered.engine.budget.spent == instance.engine.budget.spent
    assert verify_durable_graph(conn)[0] == 2


def test_head_without_transition_fails_graph_verification():
    conn = connect()
    instance = Instance.create_root("u", State(elements={"a": 1}))
    save_instance(conn, instance)
    # Valid state row but an unauthorized head move.
    proposed = instance.engine.state.with_elements({"b": 2})
    conn.execute("INSERT INTO states(state_id, version, payload, created_at) VALUES (?, ?, ?, ?)", (proposed.state_id, proposed.version, json.dumps({"elements": {"b": 2}, "version": proposed.version}, separators=(",", ":")), "now"))
    conn.execute("UPDATE instances SET current_state_id=? WHERE instance_id=?", (proposed.state_id, instance.instance_id))
    with pytest.raises(StorageCorruptionError):
        verify_durable_graph(conn)


@pytest.mark.parametrize("point", ["before_begin", "after_begin", "after_candidate", "after_transition", "after_audit", "after_head", "before_commit"])
def test_fault_injection_rolls_back_transition(point):
    conn = connect()
    instance = Instance.create_root("u", State(elements={"a": 1}))
    save_instance(conn, instance)
    original_state_id = instance.engine.state.state_id
    proposed = instance.engine.state.with_elements({"b": 2})
    candidate = Candidate(instance.engine.state.state_id, proposed, "test")
    record = instance.engine.step(candidate)
    with pytest.raises(RuntimeError, match="injected failure"):
        persist_transition(conn, instance, candidate, record, actor="u", failure_at=point)
    assert load_instance(conn, instance.instance_id).engine.state.state_id == original_state_id
    assert verify_durable_graph(conn)[0] == 1


def test_recover_instance_runs_graph_validation():
    conn = connect()
    instance = Instance.create_root("u", State(elements={"a": 1}))
    save_instance(conn, instance)
    assert recover_instance(conn, instance.instance_id).instance_id == instance.instance_id


def test_after_commit_failure_leaves_committed_transition_durable():
    conn = connect()
    instance = Instance.create_root("u", State(elements={"a": 1}))
    save_instance(conn, instance)
    proposed = instance.engine.state.with_elements({"b": 2})
    candidate = Candidate(instance.engine.state.state_id, proposed, "test")
    record = instance.engine.step(candidate)
    with pytest.raises(RuntimeError, match="injected failure"):
        persist_transition(conn, instance, candidate, record, actor="u", failure_at="after_commit")
    assert load_instance(conn, instance.instance_id).engine.state.state_id == proposed.state_id
    assert verify_durable_graph(conn)[0] == 2
