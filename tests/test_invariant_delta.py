from gnosis.core.invariants import DEFAULT_INVARIANTS
from gnosis.core.types import Candidate, Relation, State
from gnosis.reflection.invariant_delta import analyze_invariant_delta
from gnosis.reflection.shadow import evaluate_shadow


def test_shadow_accepting_invariant_violation_is_classified_as_violation():
    current = State(elements={"a": 1}, version=0)
    proposed = State(
        elements={"a": 1},
        relations=(Relation("a", "missing", "links"),),
        version=1,
    )
    candidate = Candidate(
        parent_state_id=current.state_id,
        proposed_state=proposed,
        origin="test",
    )

    def active_test(_state, _candidate):
        return False

    def shadow_test(_state, _candidate):
        return True

    evaluation = evaluate_shadow((candidate,), active_test, shadow_test)
    delta = analyze_invariant_delta(
        evaluation,
        (candidate,),
        {current.state_id: current},
        DEFAULT_INVARIANTS,
    )

    assert delta.status == "VIOLATION"
    assert "transition_validity" in delta.violated
    assert delta.shadow_violations["transition_validity"] == 1
    assert delta.active_violations == {}


def test_missing_current_state_is_unknown_not_failure():
    current = State(elements={"a": 1}, version=0)
    proposed = current.with_elements({"b": 2})
    candidate = Candidate(
        parent_state_id=current.state_id,
        proposed_state=proposed,
        origin="test",
    )

    def active_test(_state, _candidate):
        return False

    def shadow_test(_state, _candidate):
        return True

    evaluation = evaluate_shadow((candidate,), active_test, shadow_test)
    delta = analyze_invariant_delta(
        evaluation,
        (candidate,),
        {},
        DEFAULT_INVARIANTS,
    )

    assert delta.status == "INSUFFICIENT_EVIDENCE"
    assert candidate.candidate_id in delta.unknown
