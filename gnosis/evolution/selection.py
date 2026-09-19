"""Bounded, non-authoritative selection over sufficient evidence."""

from __future__ import annotations

from dataclasses import dataclass

from .evaluator import ComparativeEvaluation, EvidenceSufficiency


@dataclass(frozen=True)
class SelectionResult:
    status: str
    candidate_id: str
    rationale: tuple[str, ...]

    @property
    def selected_for_review(self) -> bool:
        return self.status == "ACCEPT_FOR_REVIEW"


def select_for_review(
    *,
    candidate_id: str,
    comparison: ComparativeEvaluation,
    sufficiency: EvidenceSufficiency,
) -> SelectionResult:
    """Select evidence for human/governance review, never for activation."""
    if not candidate_id:
        raise ValueError("candidate_id is required")
    if not sufficiency.sufficient:
        return SelectionResult(
            "INSUFFICIENT",
            candidate_id,
            ("evidence is not sufficient for selection",),
        )
    if comparison.status != "IMPROVED":
        return SelectionResult(
            "REJECT",
            candidate_id,
            (f"comparison status is {comparison.status}",),
        )
    return SelectionResult(
        "ACCEPT_FOR_REVIEW",
        candidate_id,
        ("candidate exceeded baseline with sufficient evidence; review remains required",),
    )
