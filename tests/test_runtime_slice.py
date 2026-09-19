import sqlite3

from gnosis.core import State, TestResult, TransitionRecord
from gnosis.evolution import SandboxBudget, run_runtime_slice
from gnosis.reflection.persistence import ensure_reflection_schema, load_evolution_provenance


def _history():
    return (
        TransitionRecord(
            "s0", "s1", "c1", TestResult(False, ("missing_relation",)), False, "rejected"
        ),
        TransitionRecord(
            "s0", "s2", "c2", TestResult(False, ("missing_relation",)), False, "rejected"
        ),
    )


def _observer(_state, candidate):
    return {
        "candidate_id": candidate.candidate_id,
        "capability_present": "__gnozis_capability__" in candidate.proposed_state.elements,
    }


def _failing_observer(_state, _candidate):
    raise RuntimeError("observer failure")


def test_runtime_slice_completes_and_persists_evidence_without_core_mutation():
    conn = sqlite3.connect(":memory:")
    ensure_reflection_schema(conn)
    state = State(elements={"a": 1})
    before_id = state.state_id
    before_content = state.content_id

    result = run_runtime_slice(
        conn=conn,
        state=state,
        transitions=_history(),
        observe=_observer,
        sandbox_budget=SandboxBudget(timeout_seconds=1.0),
    )

    assert result.gap.source_records
    assert result.capability.source_gap_id == result.gap.gap_id
    assert result.sandbox.accepted_for_evaluation
    assert result.sandbox.execution.status == "COMPLETED"
    assert result.evaluation.status == "PASS"
    assert result.capability.can_activate is False
    assert result.provenance.governance_decision == "REVIEW"
    assert result.transaction.provenance_id == result.provenance.provenance_id
    assert state.state_id == before_id
    assert state.content_id == before_content
    assert "__gnozis_capability__" not in state.elements

    stored = load_evolution_provenance(conn, result.provenance.provenance_id)
    assert stored["evolution_identity"] == result.provenance.evolution_identity
    assert stored["candidate_id"] == result.candidate.candidate_id


def test_runtime_slice_records_failed_sandbox_as_non_authoritative_evidence():
    conn = sqlite3.connect(":memory:")
    ensure_reflection_schema(conn)
    state = State(elements={"a": 1})

    result = run_runtime_slice(
        conn=conn,
        state=state,
        transitions=_history(),
        observe=_failing_observer,
    )

    assert result.sandbox.execution.status == "FAILED"
    assert not result.sandbox.accepted_for_evaluation
    assert result.evaluation.status == "REJECTED"
    assert result.provenance.governance_decision == "REVIEW"
    assert result.capability.can_activate is False
