import pytest
import sqlite3

from gnosis.core import State, TestResult, TransitionRecord
from gnosis.evolution import SandboxBudget, run_runtime_slice
from gnosis.evolution.evaluator import Outcome, assess_evidence_sufficiency, assess_replicated_evidence, evaluate_comparative, evaluate_outcomes
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


def test_runtime_slice_shadow_evaluation_is_non_authoritative():
    conn = sqlite3.connect(":memory:")
    ensure_reflection_schema(conn)
    state = State(elements={"a": 1})

    def active(_state, _candidate):
        return False

    def shadow(_state, _candidate):
        return True

    result = run_runtime_slice(
        conn=conn,
        state=state,
        transitions=_history(),
        observe=_observer,
        active_test=active,
        shadow_test=shadow,
    )

    assert result.shadow is not None
    assert result.shadow.status == "BEHAVIOR_CHANGED"
    assert result.shadow.improvements == 1
    assert result.provenance.shadow_status == "BEHAVIOR_CHANGED"
    assert result.capability.can_activate is False
    assert result.transaction.audit_record.event_type == "BOUNDED_RUNTIME_EVIDENCE"


def test_comparative_evaluator_distinguishes_improvement_regression_and_no_change():
    digest = "evidence-digest"
    assert evaluate_comparative(
        baseline_score=1.0, candidate_score=1.2, evidence_digest=digest, minimum_delta=0.1
    ).status == "IMPROVED"
    assert evaluate_comparative(
        baseline_score=1.0, candidate_score=0.8, evidence_digest=digest, minimum_delta=0.1
    ).status == "REGRESSION"
    assert evaluate_comparative(
        baseline_score=1.0, candidate_score=1.05, evidence_digest=digest, minimum_delta=0.1
    ).status == "NO_MEANINGFUL_CHANGE"


def test_comparative_evaluator_refuses_missing_measurements():
    result = evaluate_comparative(
        baseline_score=None, candidate_score=1.0, evidence_digest="e"
    )
    assert result.status == "INSUFFICIENT_EVIDENCE"


def test_typed_outcome_respects_metric_direction():
    baseline = Outcome("latency", 10.0, "minimize", 0.5, "b")
    candidate = Outcome("latency", 8.0, "minimize", 0.4, "c")
    result = evaluate_outcomes(baseline=baseline, candidate=candidate, minimum_delta=1.0)
    assert result.status == "IMPROVED"
    assert result.delta == 2.0


def test_typed_outcome_rejects_mismatched_metric():
    baseline = Outcome("accuracy", 0.8, "maximize", None, "b")
    candidate = Outcome("latency", 0.2, "maximize", None, "c")
    with pytest.raises(ValueError, match="metrics"):
        evaluate_outcomes(baseline=baseline, candidate=candidate)


def test_evidence_sufficiency_requires_independent_uncertain_measurements():
    baseline = Outcome("accuracy", 0.80, "maximize", 0.01, "baseline")
    candidate = Outcome("accuracy", 0.84, "maximize", 0.01, "candidate")
    result = assess_evidence_sufficiency(
        baseline=baseline, candidate=candidate, minimum_delta=0.02, min_confidence=0.65
    )
    assert result.sufficient is True
    assert result.status == "SUFFICIENT"


def test_evidence_sufficiency_rejects_shared_or_missing_evidence():
    shared_a = Outcome("accuracy", 0.80, "maximize", 0.01, "same")
    shared_b = Outcome("accuracy", 0.84, "maximize", 0.01, "same")
    assert assess_evidence_sufficiency(baseline=shared_a, candidate=shared_b).sufficient is False

    missing = Outcome("accuracy", 0.84, "maximize", None, "candidate")
    baseline = Outcome("accuracy", 0.80, "maximize", 0.01, "baseline")
    assert assess_evidence_sufficiency(baseline=baseline, candidate=missing).sufficient is False


def test_selection_requires_sufficient_improvement_and_stays_review_only():
    from gnosis.evolution.evaluator import ComparativeEvaluation, EvidenceSufficiency
    from gnosis.evolution.selection import select_for_review

    comparison = ComparativeEvaluation(
        "IMPROVED", 1.0, 1.2, 0.2, ("improved",), "e"
    )
    sufficient = EvidenceSufficiency("SUFFICIENT", 0.99, ("sufficient",))
    result = select_for_review(
        candidate_id="candidate-1",
        comparison=comparison,
        sufficiency=sufficient,
    )
    assert result.status == "ACCEPT_FOR_REVIEW"
    assert result.selected_for_review is True


def test_selection_rejects_insufficient_or_non_improving_evidence():
    from gnosis.evolution.evaluator import ComparativeEvaluation, EvidenceSufficiency
    from gnosis.evolution.selection import select_for_review

    comparison = ComparativeEvaluation(
        "IMPROVED", 1.0, 1.2, 0.2, ("improved",), "e"
    )
    insufficient = EvidenceSufficiency("INSUFFICIENT", 0.4, ("uncertain",))
    assert select_for_review(
        candidate_id="candidate-1", comparison=comparison, sufficiency=insufficient
    ).status == "INSUFFICIENT"

    no_change = ComparativeEvaluation(
        "NO_MEANINGFUL_CHANGE", 1.0, 1.0, 0.0, ("same",), "e"
    )
    sufficient = EvidenceSufficiency("SUFFICIENT", 0.99, ("sufficient",))
    assert select_for_review(
        candidate_id="candidate-1", comparison=no_change, sufficiency=sufficient
    ).status == "REJECT"


def test_runtime_slice_integrates_outcome_sufficiency_and_review_selection():
    conn = sqlite3.connect(":memory:")
    ensure_reflection_schema(conn)
    state = State(elements={"a": 1})

    result = run_runtime_slice(
        conn=conn,
        state=state,
        transitions=_history(),
        observe=_observer,
        baseline_outcome=Outcome("accuracy", 0.80, "maximize", 0.01, "baseline"),
        candidate_outcome=Outcome("accuracy", 0.84, "maximize", 0.01, "candidate"),
        minimum_delta=0.02,
        min_confidence=0.65,
    )

    assert result.comparison is not None
    assert result.comparison.status == "IMPROVED"
    assert result.sufficiency is not None
    assert result.sufficiency.status == "SUFFICIENT"
    assert result.selection is not None
    assert result.selection.status == "ACCEPT_FOR_REVIEW"
    assert result.capability.can_activate is False
    assert result.transaction.audit_record.event_type == "BOUNDED_RUNTIME_EVIDENCE"


def test_replicated_evidence_requires_independent_repetitions_and_clears_conservative_bound():
    baselines = (
        Outcome("accuracy", 0.80, "maximize", 0.01, "b1"),
        Outcome("accuracy", 0.81, "maximize", 0.01, "b2"),
    )
    candidates = (
        Outcome("accuracy", 0.84, "maximize", 0.01, "c1"),
        Outcome("accuracy", 0.85, "maximize", 0.01, "c2"),
    )
    result = assess_replicated_evidence(
        baselines=baselines, candidates=candidates, minimum_repetitions=2, minimum_delta=0.01
    )
    assert result.status == "SUFFICIENT"
    assert result.repetitions == 2
    assert result.conservative_delta_lower_bound == pytest.approx(0.02)


def test_replicated_evidence_rejects_insufficient_or_non_independent_repetitions():
    baseline = Outcome("accuracy", 0.80, "maximize", 0.01, "same")
    candidate = Outcome("accuracy", 0.84, "maximize", 0.01, "same")
    result = assess_replicated_evidence(
        baselines=(baseline,), candidates=(candidate,), minimum_repetitions=2
    )
    assert result.status == "INSUFFICIENT"

    b1 = Outcome("accuracy", 0.80, "maximize", 0.01, "b1")
    c1 = Outcome("accuracy", 0.84, "maximize", 0.01, "c1")
    b2 = Outcome("accuracy", 0.82, "maximize", 0.02, "b2")
    c2 = Outcome("accuracy", 0.83, "maximize", 0.02, "c2")
    result = assess_replicated_evidence(
        baselines=(b1, b2), candidates=(c1, c2), minimum_repetitions=2, minimum_delta=0.0
    )
    assert result.status == "INSUFFICIENT"
