"""Deterministic Select stage for Generate -> Test -> Select -> Evolve."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Sequence

from .types import Candidate, State, TestResult
from .verification import TestFn, default_test, evaluate


@dataclass(frozen=True)
class SelectionResult:
    selected: Candidate | None
    evaluated: tuple[tuple[Candidate, TestResult], ...]

    @property
    def rejected(self) -> tuple[Candidate, ...]:
        return tuple(c for c, r in self.evaluated if not r.passed)

    def result_for(self, candidate: Candidate) -> TestResult:
        for c, r in self.evaluated:
            if c is candidate or c.candidate_id == candidate.candidate_id:
                return r
        raise KeyError("candidate not part of this SelectionResult")


def select(
    current: State,
    candidates: Sequence[Candidate],
    test_fn: TestFn = default_test,
) -> SelectionResult:
    """Evaluate every candidate, then choose the smallest passing ID."""
    if not candidates:
        return SelectionResult(selected=None, evaluated=())

    evaluated = tuple((c, evaluate(current, c, test_fn)) for c in candidates)
    passing = [c for c, r in evaluated if r.passed]
    if not passing:
        return SelectionResult(selected=None, evaluated=evaluated)

    chosen = min(passing, key=lambda c: c.candidate_id)
    return SelectionResult(selected=chosen, evaluated=evaluated)
