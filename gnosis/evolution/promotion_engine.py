"""Evidence-gated materialization of the next Core version.

The engine is the first evolution component allowed to materialize a proposed
Core_(n+1), but it deliberately does not write canonical persistence. The
operation is atomic at the domain boundary: every precondition is validated
before the caller receives the new immutable State. A failed promotion leaves
the supplied current State untouched.
"""
from __future__ import annotations

from dataclasses import dataclass

from gnosis.core.types import State

from .materialization import CoreVersionDescriptor
from .promotion import PromotionCandidate
from .recursive import ReEvaluationResult


@dataclass(frozen=True)
class PromotionResult:
    """Immutable evidence that a Core transition was materialized."""

    parent_state_id: str
    next_state_id: str
    version_id: str
    candidate_model_id: str
    evidence_rounds: int
    provenance: str = "evolution-promotion-engine"


class PromotionError(ValueError):
    """Raised when an evolution proposal cannot cross the promotion gate."""


class PromotionEngine:
    """Materialize Core_(n+1) only after every promotion gate passes.

    This class has no persistence, subprocess, git, or authority side effect.
    Canonical persistence is a later integration boundary. The engine accepts
    an already constructed immutable proposed State and returns a new immutable
    result; it never mutates the supplied parent State.
    """

    def promote(
        self,
        current_state: State,
        proposed_state: State,
        candidate: PromotionCandidate,
        reevaluation: ReEvaluationResult,
        descriptor: CoreVersionDescriptor,
    ) -> tuple[State, PromotionResult]:
        self._validate(
            current_state=current_state,
            proposed_state=proposed_state,
            candidate=candidate,
            reevaluation=reevaluation,
            descriptor=descriptor,
        )

        # State is frozen/deep-frozen by the Core type contract. Returning the
        # exact proposed object makes materialization atomic at this boundary:
        # no partially-mutated parent can escape on failure.
        return proposed_state, PromotionResult(
            parent_state_id=current_state.state_id,
            next_state_id=proposed_state.state_id,
            version_id=descriptor.version_id,
            candidate_model_id=candidate.model_id,
            evidence_rounds=len(reevaluation.rounds),
        )

    @staticmethod
    def _validate(
        *,
        current_state: State,
        proposed_state: State,
        candidate: PromotionCandidate,
        reevaluation: ReEvaluationResult,
        descriptor: CoreVersionDescriptor,
    ) -> None:
        if not candidate.can_promote:
            raise PromotionError("promotion candidate is not eligible")
        if not reevaluation.stable:
            raise PromotionError("promotion candidate did not pass stable re-evaluation")
        if not descriptor.ready:
            raise PromotionError("Core version descriptor is not ready")
        if descriptor.parent_state_id != current_state.state_id:
            raise PromotionError("descriptor parent does not match current Core state")
        if descriptor.proposed_state_id != proposed_state.state_id:
            raise PromotionError("descriptor proposed state does not match proposed Core state")
        if descriptor.candidate_model_id != candidate.model_id:
            raise PromotionError("descriptor model does not match promotion candidate")
        if descriptor.evidence_rounds != len(reevaluation.rounds):
            raise PromotionError("descriptor evidence round count does not match re-evaluation")
        if proposed_state.state_id == current_state.state_id:
            raise PromotionError("promotion must materialize a distinct Core state")
        if candidate.evidence.model_id != candidate.model_id:
            raise PromotionError("candidate evidence model mismatch")
