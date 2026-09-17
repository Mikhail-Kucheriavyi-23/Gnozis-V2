"""Bounded recursive re-evaluation for autonomous evolution candidates."""
from __future__ import annotations

from dataclasses import dataclass
from typing import Callable

from .evaluator import ModelEvidence
from .promotion import PromotionCandidate

EvidenceRunner = Callable[[str, int], ModelEvidence]


@dataclass(frozen=True)
class ReEvaluationResult:
    rounds: tuple[ModelEvidence, ...]
    stable: bool


def reevaluate_candidate(
    candidate: PromotionCandidate,
    runner: EvidenceRunner,
    *,
    max_rounds: int = 3,
) -> ReEvaluationResult:
    if max_rounds < 1:
        raise ValueError("max_rounds must be positive")

    rounds: list[ModelEvidence] = []
    for round_number in range(1, max_rounds + 1):
        evidence = runner(candidate.model_id, round_number)
        rounds.append(evidence)
        if not evidence.passed:
            return ReEvaluationResult(tuple(rounds), False)

    scores = {round_.score for round_ in rounds}
    stable = len(scores) == 1 and candidate.eligible
    return ReEvaluationResult(tuple(rounds), stable)
