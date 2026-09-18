"""Append-only audit chain for evolution evidence."""
from __future__ import annotations

import json
from dataclasses import dataclass
from typing import Any, Mapping

from .provenance import canonical_digest


@dataclass(frozen=True)
class EvolutionAuditRecord:
    sequence: int
    event_type: str
    candidate_id: str
    execution_id: str
    provenance_id: str = ""
    parent_state_digest: str = ""
    proposed_state_digest: str = ""
    evidence_digest: str = ""
    payload_digest: str = ""
    previous_digest: str = ""
    record_digest: str = ""


def audit_record_digest(
    *,
    sequence: int,
    event_type: str,
    candidate_id: str,
    execution_id: str,
    provenance_id: str = "",
    parent_state_digest: str = "",
    proposed_state_digest: str = "",
    evidence_digest: str = "",
    payload_digest: str,
    previous_digest: str,
) -> str:
    return canonical_digest({
        "sequence": sequence,
        "event_type": event_type,
        "candidate_id": candidate_id,
        "execution_id": execution_id,
        "provenance_id": provenance_id,
        "parent_state_digest": parent_state_digest,
        "proposed_state_digest": proposed_state_digest,
        "evidence_digest": evidence_digest,
        "payload_digest": payload_digest,
        "previous_digest": previous_digest,
    })


def make_audit_record(
    *,
    sequence: int,
    event_type: str,
    candidate_id: str,
    execution_id: str,
    provenance_id: str = "",
    parent_state_digest: str = "",
    proposed_state_digest: str = "",
    evidence_digest: str = "",
    payload: Mapping[str, Any],
    previous_digest: str = "",
) -> EvolutionAuditRecord:
    if sequence < 0:
        raise ValueError("audit sequence must be non-negative")
    if not event_type or not candidate_id or not execution_id:
        raise ValueError("audit record requires event, candidate and execution identity")
    payload_digest = canonical_digest(payload)
    record_digest = audit_record_digest(
        sequence=sequence,
        event_type=event_type,
        candidate_id=candidate_id,
        execution_id=execution_id,
        provenance_id=provenance_id,
        parent_state_digest=parent_state_digest,
        proposed_state_digest=proposed_state_digest,
        evidence_digest=evidence_digest,
        payload_digest=payload_digest,
        previous_digest=previous_digest,
    )
    return EvolutionAuditRecord(
        sequence=sequence,
        event_type=event_type,
        candidate_id=candidate_id,
        execution_id=execution_id,
        provenance_id=provenance_id,
        parent_state_digest=parent_state_digest,
        proposed_state_digest=proposed_state_digest,
        evidence_digest=evidence_digest,
        payload_digest=payload_digest,
        previous_digest=previous_digest,
        record_digest=record_digest,
    )


def verify_audit_chain(records: list[EvolutionAuditRecord]) -> tuple[bool, tuple[str, ...]]:
    reasons: list[str] = []
    expected_previous = ""
    expected_sequence = 0
    for record in records:
        if record.sequence != expected_sequence:
            reasons.append(f"sequence mismatch at {record.sequence}")
        if record.previous_digest != expected_previous:
            reasons.append(f"previous digest mismatch at {record.sequence}")
        expected = audit_record_digest(
            sequence=record.sequence,
            event_type=record.event_type,
            candidate_id=record.candidate_id,
            execution_id=record.execution_id,
            provenance_id=record.provenance_id,
            parent_state_digest=record.parent_state_digest,
            proposed_state_digest=record.proposed_state_digest,
            evidence_digest=record.evidence_digest,
            payload_digest=record.payload_digest,
            previous_digest=record.previous_digest,
        )
        if record.record_digest != expected:
            reasons.append(f"record digest mismatch at {record.sequence}")
        expected_previous = record.record_digest
        expected_sequence += 1
    return not reasons, tuple(reasons)


@dataclass(frozen=True)
class ProvenanceAuditCrossCheck:
    valid: bool
    reasons: tuple[str, ...]


def crosscheck_provenance_audit(
    provenance: Any,
    audit_record: EvolutionAuditRecord,
) -> ProvenanceAuditCrossCheck:
    """Fail-closed cross-check of all identity-bearing provenance/audit fields."""
    reasons: list[str] = []
    for field in (
        "candidate_id",
        "execution_id",
        "parent_state_digest",
        "proposed_state_digest",
        "evidence_digest",
    ):
        if getattr(provenance, field, None) != getattr(audit_record, field, None):
            reasons.append(f"{field} mismatch")
    expected_provenance_id = getattr(provenance, "provenance_id", None)
    if not expected_provenance_id:
        reasons.append("provenance identity missing")
    elif audit_record.provenance_id != expected_provenance_id:
        reasons.append("provenance_id mismatch")
    expected_record = audit_record_digest(
        sequence=audit_record.sequence,
        event_type=audit_record.event_type,
        candidate_id=audit_record.candidate_id,
        execution_id=audit_record.execution_id,
        provenance_id=audit_record.provenance_id,
        parent_state_digest=audit_record.parent_state_digest,
        proposed_state_digest=audit_record.proposed_state_digest,
        evidence_digest=audit_record.evidence_digest,
        payload_digest=audit_record.payload_digest,
        previous_digest=audit_record.previous_digest,
    )
    if audit_record.record_digest != expected_record:
        reasons.append("audit record digest mismatch")
    return ProvenanceAuditCrossCheck(valid=not reasons, reasons=tuple(dict.fromkeys(reasons)))
