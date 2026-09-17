"""Describe a proposed Core version without mutating canonical Core.

Materialization here means constructing an immutable version descriptor. The
actual canonical write remains a separate operation after recursive evidence
has established eligibility.
"""
from __future__ import annotations

from dataclasses import dataclass

from gnosis.core.types import State

from .promotion import PromotionCandidate
from .recursive import ReEvaluationResult


@dataclass(frozen=True)
class CoreVersionDescriptor:
    version_id: str
    parent_state_id: str
    proposed_state_id: str
    candidate_model_id: str
    evidence_rounds: int
    provenance: str = "evolution-materialization"

    @property
    def ready(self) -> bool:
        return self.evidence_rounds > 0


def materialize_descriptor(
    current_state: State,
    proposed_state: State,
    candidate: PromotionCandidate,
    reevaluation: ReEvaluationResult,
) -> CoreVersionDescriptor:
    if not candidate.can_promote:
        raise ValueError("promotion candidate is not eligible")
    if not reevaluation.stable:
        raise ValueError("promotion candidate did not pass stable re-evaluation")
    return CoreVersionDescriptor(
        version_id=f"{current_state.state_id}->{proposed_state.state_id}",
        parent_state_id=current_state.state_id,
        proposed_state_id=proposed_state.state_id,
        candidate_model_id=candidate.model_id,
        evidence_rounds=len(reevaluation.rounds),
    )
