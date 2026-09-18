"""Non-authoritative promotion gate.

A promotion decision is a proof obligation, never an activation authority.
"""
from __future__ import annotations

import hashlib
from dataclasses import dataclass
from typing import Iterable


@dataclass(frozen=True)
class PromotionCandidate:
    candidate_id: str
    evidence_digest: str
    evaluation_status: str
    shadow_status: str
    invariant_status: str
    governance_decision: str
    status: str = "PROPOSED"

    @property
    def can_activate(self) -> bool:
        return False


@dataclass(frozen=True)
class PromotionGate:
    eligible: bool
    reasons: tuple[str, ...]
    status: str = "REVIEW_ONLY"

    @property
    can_activate(self) -> bool:
        return False


REQUIRED_EVALUATION = "PASS"
ALLOWED_SHADOW = frozenset({"NO_BEHAVIORAL_CHANGE", "IMPROVED"})
ALLOWED_INVARIANT = frozenset({"PRESERVED", "IMPROVED"})
ALLOWED_GOVERNANCE = frozenset({"REVIEW", "APPROVE"})


def make_promotion_candidate(
    *,
    candidate_id: str,
    evidence_digest: str,
    evaluation_status: str,
    shadow_status: str,
    invariant_status: str,
    governance_decision: str,
) -> PromotionCandidate:
    if not candidate_id or not evidence_digest:
        raise ValueError("promotion candidate requires candidate_id and evidence_digest")
    raw = "|".join(
        (candidate_id, evidence_digest, evaluation_status, shadow_status,
         invariant_status, governance_decision)
    )
    return PromotionCandidate(
        "promotion:" + hashlib.sha256(raw.encode()).hexdigest()[:24],
        evidence_digest, evaluation_status, shadow_status,
        invariant_status, governance_decision,
    )


def evaluate_promotion_gate(
    candidate: PromotionCandidate,
    *,
    provenance_valid: bool,
    required_evidence: Iterable[str] = (),
) -> PromotionGate:
    reasons: list[str] = []
    if not provenance_valid:
        reasons.append("provenance cross-check failed")
    if candidate.evaluation_status != REQUIRED_EVALUATION:
        reasons.append("evaluation is not PASS")
    if candidate.shadow_status not in ALLOWED_SHADOW:
        reasons.append("shadow result is not acceptable")
    if candidate.invariant_status not in ALLOWED_INVARIANT:
        reasons.append("invariant result is not preserved/improved")
    if candidate.governance_decision not in ALLOWED_GOVERNANCE:
        reasons.append("governance decision is not review/approve")
    missing = tuple(name for name in required_evidence if not name)
    if missing:
        reasons.append("required evidence contains empty identifier")
    return PromotionGate(
        eligible=not reasons,
        reasons=tuple(reasons),
    )
