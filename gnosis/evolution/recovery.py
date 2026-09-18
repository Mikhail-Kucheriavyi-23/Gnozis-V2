"""Recovery verification for persisted evolution history."""
from __future__ import annotations

import sqlite3
from dataclasses import dataclass
from typing import Any

from .chain_verifier import verify_persisted_chain
from .provenance import canonical_digest, EvidenceProvenance
from ..reflection.persistence import list_evolution_audit, list_evolution_provenance


@dataclass(frozen=True)
class RecoveryReport:
    recovered_records: int
    chain_valid: bool
    replay_valid: bool
    expected_digest: str | None
    actual_digest: str | None
    reasons: tuple[str, ...]


def recover_evolution_audit(
    conn: sqlite3.Connection,
    *,
    provenance_id: str | None = None,
    observations: dict[str, Any] | None = None,
) -> RecoveryReport:
    """Recover persisted evolution and fail closed unless its identity chain verifies."""
    records = list(list_evolution_audit(conn))
    if provenance_id is None:
        if not records:
            return RecoveryReport(0, True, True, None, None, ())
        return RecoveryReport(len(records), False, False, None, None, ("provenance identity required for trusted recovery",))
    rows = list_evolution_provenance(conn, candidate_id=None)
    provenance_rows = [row for row in rows if row["provenance_id"] == provenance_id]
    if not provenance_rows:
        return RecoveryReport(len(records), False, False, None, None, ("provenance record missing",))
    if observations is None:
        return RecoveryReport(len(records), False, False, None, None, ("observations required for independent recovery verification",))
    result = verify_persisted_chain(
        provenance_rows[0],
        [record.__dict__ for record in records],
        observations=observations,
    )
    provenance_row = provenance_rows[0]
    expected_digest = provenance_row["evidence_digest"]
    actual_digest = canonical_digest(observations)
    persisted_identity = provenance_row.get("evolution_identity", "")
    replay_valid = result.valid and actual_digest == expected_digest
    identity_valid = True
    if persisted_identity:
        try:
            recovered_provenance = EvidenceProvenance(
                execution_id=provenance_row["execution_id"],
                candidate_id=provenance_row["candidate_id"],
                parent_state_id=provenance_row["parent_state_id"],
                parent_state_digest=provenance_row["parent_state_digest"],
                proposed_state_digest=provenance_row["proposed_state_digest"],
                evidence_digest=provenance_row["evidence_digest"],
                evaluation_status=provenance_row["evaluation_status"],
                shadow_status=provenance_row["shadow_status"],
                invariant_status=provenance_row["invariant_status"],
                governance_decision=provenance_row["governance_decision"],
            )
            identity_valid = recovered_provenance.evolution_identity == persisted_identity
        except (KeyError, TypeError, ValueError):
            identity_valid = False
    replay_valid = replay_valid and identity_valid
    reasons = list(result.reasons)
    if actual_digest != expected_digest:
        reasons.append("recovery replay digest mismatch")
    if not identity_valid:
        reasons.append("recovery evolution identity mismatch")
    return RecoveryReport(len(records), result.valid, replay_valid, expected_digest, actual_digest, tuple(dict.fromkeys(reasons)))
