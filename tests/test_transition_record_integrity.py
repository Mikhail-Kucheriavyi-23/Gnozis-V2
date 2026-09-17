import pytest

from gnosis.core import TestResult, TransitionRecord


def test_transition_record_cannot_claim_acceptance_when_test_failed():
    with pytest.raises(ValueError):
        TransitionRecord(
            from_state_id="s0",
            to_state_id="s1",
            candidate_id="c1",
            test_result=TestResult(passed=False, reasons=("invariant failed",)),
            accepted=True,
            reason="committed",
        )


def test_transition_record_cannot_claim_rejection_when_test_passed():
    with pytest.raises(ValueError):
        TransitionRecord(
            from_state_id="s0",
            to_state_id="s1",
            candidate_id="c1",
            test_result=TestResult(passed=True),
            accepted=False,
            reason="rejected",
        )


def test_transition_record_acceptance_matches_test_result():
    accepted = TransitionRecord(
        from_state_id="s0",
        to_state_id="s1",
        candidate_id="c1",
        test_result=TestResult(passed=True),
        accepted=True,
        reason="committed",
    )
    rejected = TransitionRecord(
        from_state_id="s0",
        to_state_id="s0",
        candidate_id="c2",
        test_result=TestResult(passed=False, reasons=("invariant failed",)),
        accepted=False,
        reason="rejected: invariant failed",
    )
    assert accepted.accepted is True
    assert rejected.accepted is False
