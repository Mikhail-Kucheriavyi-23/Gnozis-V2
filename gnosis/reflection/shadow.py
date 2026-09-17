"""Isolated shadow evaluation for reflection proposals.

A shadow rule is evaluated against the same immutable Candidate inputs as the
active rule. The evaluator never commits state, mutates Engine, or activates a
proposal. It produces a deterministic comparison artifact for later governance.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Sequence

from gnosis.core.types import Candidate, TestResult
from gnosis.core.verification import TestFn, verify


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


def evaluate_shadow(
    candidates: Sequence[Candidate],
    active_test: TestFn,
    shadow_test: TestFn,
) -> ShadowEvaluation:
    """Compare active and proposed Test rules over identical candidates.

    The candidates are treated as immutable evidence. Both rules are invoked
    through the same canonical verification function. No candidate is
    committed and no Engine state is touched.

    ``regressions`` means active accepted while shadow rejects.
    ``improvements`` means active rejected while shadow accepts.
    """
    cases: list[ShadowCase] = []
    regressions = 0
    improvements = 0

    for candidate in candidates:
        active = verify(candidate.proposed_state, candidate, active_test)
        shadow = verify(candidate.proposed_state, candidate, shadow_test)
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
