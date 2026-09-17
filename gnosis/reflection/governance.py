"""Read-only governance decisions for reflection proposals.

This layer interprets existing ShadowEvaluation and InvariantDelta evidence.
It never activates rules, mutates Core, or performs rollback. A decision is
an evidence classification for a later, explicitly authorized governance
boundary.
"""

from __future__ import annotations

from dataclasses import dataclass

from .invariant_delta import InvariantDelta
from .shadow import ShadowEvaluation


@dataclass(frozen=True)
class GovernanceDecision:
    """Deterministic, non-authoritative classification of proposal evidence."""

    decision: str
    shadow_status: str
    invariant_status: str
    rationale: tuple[str, ...]
    provenance: str = "reflection-governance"

    @property
    def can_activate(self) -> bool:
        """Governance evidence never grants activation authority."""
        return False

    @property
    def can_rollback(self) -> bool:
        """Governance evidence never performs rollback itself."""
        return False


def evaluate_governance(
    evaluation: ShadowEvaluation,
    invariant_delta: InvariantDelta,
) -> GovernanceDecision:
    """Classify existing evidence without changing any canonical state.

    Decision semantics:
    - BLOCK: shadow introduces regressions or invariant violations.
    - HOLD: evidence is insufficient to make a positive classification.
    - REVIEW: evidence is behaviorally changed but has no detected invariant
      regression; a later authorized layer may decide what to do.
    - NO_CHANGE: shadow has no behavioral change and no invariant delta.
    """
    reasons: list[str] = []

    if evaluation.regressions:
        reasons.append(f"shadow_regressions={evaluation.regressions}")
    if invariant_delta.violated:
        reasons.append("invariant_violations=" + ",".join(invariant_delta.violated))
    if invariant_delta.unknown:
        reasons.append(f"unknown_evidence={len(invariant_delta.unknown)}")

    if evaluation.regressions or invariant_delta.violated:
        decision = "BLOCK"
    elif evaluation.status == "NO_INPUT" or invariant_delta.status == "INSUFFICIENT_EVIDENCE":
        decision = "HOLD"
    elif evaluation.status == "BEHAVIOR_CHANGED" or invariant_delta.improved:
        decision = "REVIEW"
    else:
        decision = "NO_CHANGE"

    if not reasons:
        reasons.append("no_detected_regression_or_invariant_delta")

    return GovernanceDecision(
        decision=decision,
        shadow_status=evaluation.status,
        invariant_status=invariant_delta.status,
        rationale=tuple(reasons),
    )
