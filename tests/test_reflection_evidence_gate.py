from gnosis.core.invariants import DEFAULT_INVARIANTS
from gnosis.core.types import Candidate, State
from gnosis.reflection.evidence_gate import run_reflection_evidence_gate


def test_evidence_gate_produces_review_without_authority():
    current = State(elements={"a": 1})
    candidates = [Candidate(current.state_id, current.with_elements({"a": 2}), "c1")]
    result = run_reflection_evidence_gate(candidates, lambda s,c: True, lambda s,c: False, {current.state_id: current}, DEFAULT_INVARIANTS)
    assert result.passed
    assert result.shadow.regressions == 1
    assert result.governance.decision == "BLOCK"
    assert not result.governance.can_activate
    assert not result.governance.can_rollback


def test_evidence_gate_fails_closed_on_empty_input():
    result = run_reflection_evidence_gate([], lambda s,c: True, lambda s,c: True, {}, DEFAULT_INVARIANTS)
    assert result.passed
    assert result.governance.decision == "HOLD"
    assert not result.governance.can_activate
