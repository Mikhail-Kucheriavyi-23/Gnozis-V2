"""
Select (PATCH defect #5): closes the gap between the documented cycle

    Generate -> Test -> Select -> Evolve

and the pre-PATCH Engine, which only ever accepted a single pre-formed
Candidate (no Select stage existed in runtime at all).

Given multiple candidates, Test is applied to each; failing ones are
discarded; exactly one candidate is chosen among the passing ones by an
explicit, deterministic rule — NOT a global selector, NOT an external
model, NOT mutable shared state.

Selection rule (documented per PATCH section 5 as an explicit, minimal,
temporary mechanism — the master spec does not yet define a scoring
criterion, so nothing "intelligent" is invented here): among candidates
that pass Test, choose the one with the lexicographically smallest
`candidate_id` (a content-addressed hash). This is:
  - deterministic — same candidate set always yields the same choice,
    regardless of the order the caller supplies them in;
  - testable — pure function of (current, candidates), no I/O, no clock;
  - explicit — the rule is exactly "min by candidate_id", nothing implicit.

STATUS: IMPLEMENTED (minimal deterministic selection rule)
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Sequence

from .types import Candidate, State, TestResult
from .verification import TestFn, default_test, verify


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
    """Test every candidate, then deterministically choose one passing
    candidate (or None if the list is empty or none pass)."""
    if not candidates:
        return SelectionResult(selected=None, evaluated=())

    evaluated = tuple((c, verify(current, c, test_fn)) for c in candidates)
    passing = [c for c, r in evaluated if r.passed]
    if not passing:
        return SelectionResult(selected=None, evaluated=evaluated)

    chosen = min(passing, key=lambda c: c.candidate_id)
    return SelectionResult(selected=chosen, evaluated=evaluated)
