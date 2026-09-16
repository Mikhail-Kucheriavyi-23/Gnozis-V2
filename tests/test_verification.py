from gnosis.core import Candidate, State, TestResult, verify


def test_default_test_passes_valid_candidate():
    current = State(elements={"a": 1}, version=0)
    proposed = current.with_elements({"b": 2})
    candidate = Candidate(parent_state_id=current.state_id, proposed_state=proposed, origin="t")
    result = verify(current, candidate)
    assert result.passed


def test_custom_test_fn_is_used_when_provided():
    current = State(elements={"a": 1}, version=0)
    proposed = current.with_elements({"b": 2})
    candidate = Candidate(parent_state_id=current.state_id, proposed_state=proposed, origin="t")

    def always_reject(state: State, cand: Candidate) -> TestResult:
        return TestResult(passed=False, reasons=("custom policy rejects everything",))

    result = verify(current, candidate, test_fn=always_reject)
    assert not result.passed
    assert "custom policy rejects everything" in result.reasons
