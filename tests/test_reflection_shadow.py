from gnosis.core import Candidate, State
from gnosis.core.verification import default_test
from gnosis.reflection.shadow import evaluate_shadow


def _candidate(state: State, value: int, seed: int) -> Candidate:
    return Candidate(
        parent_state_id=state.state_id,
        proposed_state=state.with_elements({"x": value}),
        origin="test:shadow",
        seed=seed,
    )


def test_shadow_compares_same_candidate_without_mutating_state():
    state = State(elements={"x": 0})
    candidates = (_candidate(state, 1, 1), _candidate(state, -1, 2))

    def shadow_rule(_state, candidate):
        return candidate.proposed_state.elements.get("x", 0) >= 0

    before = state.state_id
    result = evaluate_shadow(candidates, default_test, shadow_rule)

    assert result.status == "BEHAVIOR_CHANGED"
    assert result.changed_cases == 1
    assert result.regressions == 0
    assert result.improvements == 1
    assert state.state_id == before


def test_shadow_reports_regression_without_activation():
    state = State(elements={"x": 0})
    candidate = _candidate(state, 1, 3)

    def rejecting_rule(_state, _candidate):
        return False

    result = evaluate_shadow((candidate,), default_test, rejecting_rule)

    assert result.status == "REGRESSION"
    assert result.regressions == 1
    assert result.improvements == 0


def test_shadow_empty_input_is_explicit():
    result = evaluate_shadow((), default_test, default_test)
    assert result.status == "NO_INPUT"
    assert result.changed_cases == 0
