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
    parent_state_digest: str
    proposed_state_digest: str
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
            "parent_state_digest": self.parent_state_digest,
            "proposed_state_digest": self.proposed_state_digest,
            "evidence_digest": self.evidence_digest,
            "evaluation_status": self.evaluation_status,
            "shadow_status": self.shadow_status,
            "invariant_status": self.invariant_status,
            "governance_decision": self.governance_decision,
        })[:24]


def execution_id(candidate_id: str, parent_state_id: str, evidence_digest: str, parent_state_digest: str = "", proposed_state_digest: str = "") -> str:
    if not candidate_id or not parent_state_id or not evidence_digest:
        raise ValueError("execution provenance requires candidate, parent state and evidence digest")
    return "execution:" + canonical_digest(
        {"candidate_id": candidate_id, "parent_state_id": parent_state_id, "parent_state_digest": parent_state_digest, "proposed_state_digest": proposed_state_digest, "evidence_digest": evidence_digest}
    )[:24]


def verify_evidence_digest(observations: Mapping[str, Any], expected_digest: str) -> bool:
    if not expected_digest:
        return False
    return canonical_digest(observations) == expected_digest


def build_provenance(
    *,
    candidate_id: str,
    parent_state_id: str,
    parent_state_digest: str,
    proposed_state_digest: str,
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
        execution_id=execution_id(candidate_id, parent_state_id, evidence_digest, parent_state_digest, proposed_state_digest),
        candidate_id=candidate_id,
        parent_state_id=parent_state_id,
        parent_state_digest=parent_state_digest,
        proposed_state_digest=proposed_state_digest,
        evidence_digest=evidence_digest,
        evaluation_status=evaluation_status,
        shadow_status=shadow_status,
        invariant_status=invariant_status,
        governance_decision=governance_decision,
    )


@dataclass(frozen=True)
class ProvenanceCrossCheck:
    valid: bool
    reasons: tuple[str, ...]


def crosscheck_provenance(
    *,
    provenance: EvidenceProvenance,
    candidate_id: str,
    parent_state_id: str,
    parent_state_digest: str,
    proposed_state_digest: str,
    observations: Mapping[str, Any],
    evidence_digest: str,
    execution_id_value: str,
    evaluation_status: str,
    shadow_status: str,
    invariant_status: str,
    governance_decision: str,
) -> ProvenanceCrossCheck:
    """Verify every identity-bearing link before provenance can be trusted."""
    reasons: list[str] = []
    if provenance.candidate_id != candidate_id:
        reasons.append("candidate_id mismatch")
    if provenance.parent_state_id != parent_state_id:
        reasons.append("parent_state_id mismatch")
    if provenance.parent_state_digest != parent_state_digest:
        reasons.append("parent_state_digest mismatch")
    if provenance.proposed_state_digest != proposed_state_digest:
        reasons.append("proposed_state_digest mismatch")
    if provenance.evidence_digest != evidence_digest:
        reasons.append("evidence_digest mismatch")
    if provenance.execution_id != execution_id_value:
        reasons.append("execution_id mismatch")
    if provenance.evaluation_status != evaluation_status:
        reasons.append("evaluation_status mismatch")
    if provenance.shadow_status != shadow_status:
        reasons.append("shadow_status mismatch")
    if provenance.invariant_status != invariant_status:
        reasons.append("invariant_status mismatch")
    if provenance.governance_decision != governance_decision:
        reasons.append("governance_decision mismatch")
    if not verify_evidence_digest(observations, evidence_digest):
        reasons.append("observation digest mismatch")
    expected_execution = execution_id(candidate_id, parent_state_id, evidence_digest, parent_state_digest, proposed_state_digest)
    if execution_id_value != expected_execution:
        reasons.append("execution identity mismatch")
    expected_provenance = EvidenceProvenance(
        execution_id=execution_id_value,
        candidate_id=candidate_id,
        parent_state_id=parent_state_id,
        parent_state_digest=parent_state_digest,
        proposed_state_digest=proposed_state_digest,
        evidence_digest=evidence_digest,
        evaluation_status=evaluation_status,
        shadow_status=shadow_status,
        invariant_status=invariant_status,
        governance_decision=governance_decision,
        status=provenance.status,
    )
    if provenance.provenance_id != expected_provenance.provenance_id:
        reasons.append("provenance identity mismatch")
    return ProvenanceCrossCheck(valid=not reasons, reasons=tuple(reasons))
