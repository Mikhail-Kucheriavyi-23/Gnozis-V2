"""Deterministic replay and evidence-integrity checks for evolution experiments."""
from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Mapping

from .provenance import canonical_digest, verify_evidence_digest
from .sandbox import SandboxExecution


@dataclass(frozen=True)
class ReplayResult:
    reproducible: bool
    reasons: tuple[str, ...]
    expected_digest: str | None = None
    actual_digest: str | None = None


def replay_evidence(
    execution: SandboxExecution,
    observations: Mapping[str, Any],
) -> ReplayResult:
    """Recompute evidence identity without executing or activating anything."""
    actual = canonical_digest(observations)
    reasons: list[str] = []
    if actual != execution.evidence_digest:
        reasons.append("evidence digest mismatch")
    if not verify_evidence_digest(observations, execution.evidence_digest):
        reasons.append("evidence verification failed")
    return ReplayResult(
        reproducible=not reasons,
        reasons=tuple(reasons),
        expected_digest=execution.evidence_digest,
        actual_digest=actual,
    )


def replay_identity(
    execution: SandboxExecution,
    *,
    candidate_id: str,
    parent_state_id: str,
    parent_state_digest: str,
    proposed_state_digest: str,
) -> ReplayResult:
    """Check that replay inputs still identify the same execution."""
    reasons: list[str] = []
    if execution.candidate_id != candidate_id:
        reasons.append("candidate identity mismatch")
    if execution.parent_state_id != parent_state_id:
        reasons.append("parent state identity mismatch")
    if execution.parent_state_digest != parent_state_digest:
        reasons.append("parent state digest mismatch")
    if execution.proposed_state_digest != proposed_state_digest:
        reasons.append("proposed state digest mismatch")
    return ReplayResult(reproducible=not reasons, reasons=tuple(reasons))
