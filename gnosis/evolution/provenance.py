"""Tamper-evident provenance for bounded evolution evidence."""
from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass
from typing import Any, Mapping


def canonical_digest(value: Any) -> str:
    """Return a stable SHA-256 digest for JSON-compatible evidence."""
    payload = json.dumps(
        value, ensure_ascii=False, sort_keys=True, separators=(",", ":"), default=str
    )
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()


@dataclass(frozen=True)
class EvidenceProvenance:
    execution_id: str
    candidate_id: str
    parent_state_id: str
    evidence_digest: str
    evaluation_status: str
    shadow_status: str
    invariant_status: str
    governance_decision: str
    status: str = "RECORDED"

    @property
    def provenance_id(self) -> str:
        return "provenance:" + canonical_digest({
            "execution_id": self.execution_id,
            "candidate_id": self.candidate_id,
            "parent_state_id": self.parent_state_id,
            "evidence_digest": self.evidence_digest,
            "evaluation_status": self.evaluation_status,
            "shadow_status": self.shadow_status,
            "invariant_status": self.invariant_status,
            "governance_decision": self.governance_decision,
        })[:24]


def execution_id(candidate_id: str, parent_state_id: str, evidence_digest: str) -> str:
    if not candidate_id or not parent_state_id or not evidence_digest:
        raise ValueError("execution provenance requires candidate, parent state and evidence digest")
    return "execution:" + canonical_digest(
        {"candidate_id": candidate_id, "parent_state_id": parent_state_id, "evidence_digest": evidence_digest}
    )[:24]


def verify_evidence_digest(observations: Mapping[str, Any], expected_digest: str) -> bool:
    if not expected_digest:
        return False
    return canonical_digest(observations) == expected_digest


def build_provenance(
    *,
    candidate_id: str,
    parent_state_id: str,
    observations: Mapping[str, Any],
    evidence_digest: str,
    evaluation_status: str,
    shadow_status: str,
    invariant_status: str,
    governance_decision: str,
) -> EvidenceProvenance:
    if not verify_evidence_digest(observations, evidence_digest):
        raise ValueError("evidence digest mismatch")
    return EvidenceProvenance(
        execution_id=execution_id(candidate_id, parent_state_id, evidence_digest),
        candidate_id=candidate_id,
        parent_state_id=parent_state_id,
        evidence_digest=evidence_digest,
        evaluation_status=evaluation_status,
        shadow_status=shadow_status,
        invariant_status=invariant_status,
        governance_decision=governance_decision,
    )
