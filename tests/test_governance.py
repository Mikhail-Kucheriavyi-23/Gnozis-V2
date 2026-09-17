from dataclasses import replace

from gnosis.reflection.governance import evaluate_governance
from gnosis.reflection.invariant_delta import InvariantDelta
from gnosis.reflection.shadow import ShadowEvaluation


def _evaluation(*, status="NO_BEHAVIORAL_CHANGE", regressions=0, improvements=0):
    return ShadowEvaluation(
        cases=(),
        changed_cases=0,
        accepted_by_active=0,
        accepted_by_shadow=0,
        regressions=regressions,
        improvements=improvements,
        status=status,
    )


def _delta(*, status="PRESERVED", violated=(), improved=(), unknown=()):
    return InvariantDelta(
        preserved=(),
        violated=tuple(violated),
        improved=tuple(improved),
        unknown=tuple(unknown),
        active_violations={},
        shadow_violations={},
    )


def test_regression_is_blocked_without_activation_authority():
    decision = evaluate_governance(
        _evaluation(status="REGRESSION", regressions=1),
        _delta(),
    )
    assert decision.decision == "BLOCK"
    assert decision.can_activate is False
    assert decision.can_rollback is False


def test_behavior_change_without_violation_requires_review():
    decision = evaluate_governance(
        _evaluation(status="BEHAVIOR_CHANGED", improvements=1),
        _delta(),
    )
    assert decision.decision == "REVIEW"


def test_missing_evidence_is_hold():
    decision = evaluate_governance(
        _evaluation(status="NO_INPUT"),
        _delta(status="INSUFFICIENT_EVIDENCE", unknown=("candidate-1",)),
    )
    assert decision.decision == "HOLD"
