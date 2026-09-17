"""Promotion candidate contract for recursive autonomous evolution.

A promotion candidate is descriptive evidence, not executable authority.
Canonical Core promotion is intentionally a later, explicit stage.
"""
from __future__ import annotations

from dataclasses import dataclass

from gnosis.reflection.invariant_delta import InvariantDelta

from .evaluator import ModelEvidence
from .hypothesis import EvolutionHypothesis


@dataclass(frozen=True)
class PromotionCandidate:
    hypothesis_id: str
    model_id: str
    evidence: ModelEvidence
    invariant_delta: InvariantDelta
    provenance: str = "evolution-promotion-candidate"

    @property
    def eligible(self) -> bool:
        return (
            self.invariant_delta.status in {"PRESERVED", "IMPROVED"}
            and self.invariant_delta.status != "INSUFFICIENT_EVIDENCE"
            and self.evidence.passed
        )

    @property
    def can_promote(self) -> bool:
        return self.eligible


def build_promotion_candidate(
    hypothesis: EvolutionHypothesis,
    evidence: ModelEvidence,
    invariant_delta: InvariantDelta,
) -> PromotionCandidate:
    if evidence.model_id not in {f"{hypothesis.hypothesis_id}:model:{i}" for i in range(1, 4)}:
        raise ValueError("evidence does not belong to a bounded hypothesis model")
    return PromotionCandidate(
        hypothesis_id=hypothesis.hypothesis_id,
        model_id=evidence.model_id,
        evidence=evidence,
        invariant_delta=invariant_delta,
    )
