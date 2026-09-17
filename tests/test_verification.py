import pytest

from gnosis.core import Candidate, State, TestResult, evaluate, verify


def _candidate() -> tuple[State, Candidate]:
    current = State(elements={"a": 1}, version=0)
    proposed = current.with_elements({"b": 2})
    candidate = Candidate(parent_state_id=current.state_id, proposed_state=proposed, origin="t")
    return current, candidate


def test_default_test_passes_valid_candidate():
    current, candidate = _candidate()
    assert verify(current, candidate) is True
    result = evaluate(current, candidate)
    assert result.passed is True


def test_custom_test_fn_returns_strict_bool():
    current, candidate = _candidate()

    def always_reject(state: State, cand: Candidate) -> bool:
        return False

    assert verify(current, candidate, test_fn=always_reject) is False
    result = evaluate(current, candidate, test_fn=always_reject)
    assert result.passed is False
    assert "custom Test predicate rejected candidate" in result.reasons


@pytest.mark.parametrize("bad_result", ["yes", 1, 0, None, TestResult(passed=False)])
def test_verify_rejects_non_bool_test_results(bad_result):
    current, candidate = _candidate()

    def invalid_test(state: State, cand: Candidate):
        return bad_result

    with pytest.raises(TypeError, match="TestFn must return an actual bool"):
        verify(current, candidate, test_fn=invalid_test)


def test_testresult_still_rejects_non_bool_passed_field():
    with pytest.raises(TypeError, match="TestResult.passed must be an actual bool"):
        TestResult(passed=1)
