"""Deterministic comparison of bounded candidate evidence against a baseline."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Mapping


@dataclass(frozen=True)
class EvaluationResult:
    status: str
    rationale: tuple[str, ...]
    evidence_digest: str


@dataclass(frozen=True)
class Outcome:
    """An explicitly typed measurement used for candidate/baseline comparison."""
    metric: str
    value: float
    direction: str
    uncertainty: float | None
    evidence_digest: str

    def __post_init__(self) -> None:
        if not self.metric.strip():
            raise ValueError("metric must not be empty")
        if self.direction not in {"maximize", "minimize"}:
            raise ValueError("direction must be 'maximize' or 'minimize'")
        if self.uncertainty is not None and self.uncertainty < 0:
            raise ValueError("uncertainty must be non-negative")
        if not self.evidence_digest:
            raise ValueError("evidence_digest is required")

    def normalized_delta(self, baseline: "Outcome") -> float:
        if self.metric != baseline.metric:
            raise ValueError("baseline and candidate metrics must match")
        if self.direction != baseline.direction:
            raise ValueError("baseline and candidate directions must match")
        raw = self.value - baseline.value
        return raw if self.direction == "maximize" else -raw


@dataclass(frozen=True)
class ComparativeEvaluation:
    status: str
    baseline_score: float | None
    candidate_score: float | None
    delta: float | None
    rationale: tuple[str, ...]
    evidence_digest: str

    @property
    def improved(self) -> bool:
        return self.status == "IMPROVED"

    @property
    def regressed(self) -> bool:
        return self.status == "REGRESSION"


def evaluate_observation(
    observations: Mapping[str, Any],
    *,
    evidence_digest: str,
    predicate: str,
) -> EvaluationResult:
    if not evidence_digest:
        return EvaluationResult("INSUFFICIENT_EVIDENCE", ("missing evidence digest",), "")
    if not observations:
        return EvaluationResult(
            "INSUFFICIENT_EVIDENCE",
            ("sandbox produced no observations",),
            evidence_digest,
        )
    if predicate != "observations_present":
        return EvaluationResult(
            "REVIEW",
            ("evidence requires an explicit evaluator implementation",),
            evidence_digest,
        )
    return EvaluationResult(
        "PASS",
        ("sandbox observations are present and digest-linked",),
        evidence_digest,
    )


def evaluate_outcomes(
    *, baseline: Outcome, candidate: Outcome, minimum_delta: float = 0.0
) -> ComparativeEvaluation:
    """Compare typed outcomes; this remains descriptive and non-authoritative."""
    if minimum_delta < 0:
        raise ValueError("minimum_delta must be non-negative")
    if baseline.evidence_digest != candidate.evidence_digest:
        digest = f"{baseline.evidence_digest}:{candidate.evidence_digest}"
    else:
        digest = baseline.evidence_digest
    delta = candidate.normalized_delta(baseline)
    if delta > minimum_delta:
        status = "IMPROVED"
    elif delta < -minimum_delta:
        status = "REGRESSION"
    else:
        status = "NO_MEANINGFUL_CHANGE"
    return ComparativeEvaluation(
        status=status,
        baseline_score=baseline.value,
        candidate_score=candidate.value,
        delta=delta,
        rationale=(f"metric={candidate.metric}", f"direction={candidate.direction}"),
        evidence_digest=digest,
    )


def evaluate_comparative(
    *,
    baseline_score: float | None,
    candidate_score: float | None,
    evidence_digest: str,
    minimum_delta: float = 0.0,
) -> ComparativeEvaluation:
    """Compare two explicit measurements without selecting or activating a candidate."""
    if not evidence_digest:
        return ComparativeEvaluation(
            "INSUFFICIENT_EVIDENCE", baseline_score, candidate_score, None,
            ("missing evidence digest",), "",
        )
    if baseline_score is None or candidate_score is None:
        return ComparativeEvaluation(
            "INSUFFICIENT_EVIDENCE", baseline_score, candidate_score, None,
            ("both baseline and candidate measurements are required",),
            evidence_digest,
        )
    if minimum_delta < 0:
        raise ValueError("minimum_delta must be non-negative")

    delta = candidate_score - baseline_score
    if delta > minimum_delta:
        status = "IMPROVED"
        rationale = ("candidate measurement exceeds baseline by more than minimum_delta",)
    elif delta < -minimum_delta:
        status = "REGRESSION"
        rationale = ("candidate measurement is below baseline by more than minimum_delta",)
    else:
        status = "NO_MEANINGFUL_CHANGE"
        rationale = ("candidate measurement does not exceed the comparison threshold",)

    return ComparativeEvaluation(
        status, baseline_score, candidate_score, delta, rationale, evidence_digest
    )
