"""Isolated shadow evaluation for reflection proposals."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Sequence

from gnosis.core.types import Candidate, TestResult
from gnosis.core.verification import TestFn


@dataclass(frozen=True)
class ShadowCase:
    candidate_id: str
    active: TestResult
    shadow: TestResult

    @property
    def changed(self) -> bool:
        return self.active.passed != self.shadow.passed or self.active.reasons != self.shadow.reasons


@dataclass(frozen=True)
class ShadowEvaluation:
    cases: tuple[ShadowCase, ...]
    changed_cases: int
    accepted_by_active: int
    accepted_by_shadow: int
    regressions: int
    improvements: int
    status: str


def _evaluate_policy(test_fn: TestFn, candidate: Candidate) -> TestResult:
    """Evaluate only the policy predicate; Core invariants are analyzed separately."""
    result = test_fn(candidate.proposed_state, candidate)
    if not isinstance(result, bool):
        raise TypeError(
            "Shadow TestFn must return an actual bool (True/False), "
            f"got {type(result).__name__}: {result!r}"
        )
    if result:
        return TestResult(True, ("shadow policy passed",))
    return TestResult(False, ("shadow policy rejected candidate",))


def evaluate_shadow(
    candidates: Sequence[Candidate],
    active_test: TestFn,
    shadow_test: TestFn,
) -> ShadowEvaluation:
    """Compare policy outcomes without activating a rule or bypassing Core at commit time."""
    cases: list[ShadowCase] = []
    regressions = 0
    improvements = 0

    for candidate in candidates:
        active = _evaluate_policy(active_test, candidate)
        shadow = _evaluate_policy(shadow_test, candidate)
        case = ShadowCase(candidate.candidate_id, active, shadow)
        cases.append(case)
        if active.passed and not shadow.passed:
            regressions += 1
        elif not active.passed and shadow.passed:
            improvements += 1

    accepted_active = sum(case.active.passed for case in cases)
    accepted_shadow = sum(case.shadow.passed for case in cases)
    changed = sum(case.changed for case in cases)

    if not cases:
        status = "NO_INPUT"
    elif regressions:
        status = "REGRESSION"
    elif improvements:
        status = "BEHAVIOR_CHANGED"
    else:
        status = "NO_BEHAVIORAL_CHANGE"

    return ShadowEvaluation(
        cases=tuple(cases),
        changed_cases=changed,
        accepted_by_active=accepted_active,
        accepted_by_shadow=accepted_shadow,
        regressions=regressions,
        improvements=improvements,
        status=status,
    )
