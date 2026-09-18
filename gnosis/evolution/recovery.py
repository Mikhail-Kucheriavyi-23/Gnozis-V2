"""Recovery verification for persisted evolution history."""
from __future__ import annotations

import sqlite3
from dataclasses import dataclass
from typing import Any

from .chain_verifier import verify_persisted_chain
from .provenance import canonical_digest, crosscheck_provenance
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
    expected_digest = provenance_rows[0]["evidence_digest"]
    actual_digest = canonical_digest(observations)
    provenance_check = crosscheck_provenance(
        provenance=provenance_rows[0],
        candidate_id=provenance_rows[0]["candidate_id"],
        parent_state_id=provenance_rows[0]["parent_state_id"],
        parent_state_digest=provenance_rows[0]["parent_state_digest"],
        proposed_state_digest=provenance_rows[0]["proposed_state_digest"],
        observations=observations,
        evidence_digest=provenance_rows[0]["evidence_digest"],
        execution_id_value=provenance_rows[0]["execution_id"],
        evaluation_status=provenance_rows[0]["evaluation_status"],
        shadow_status=provenance_rows[0]["shadow_status"],
        invariant_status=provenance_rows[0]["invariant_status"],
        governance_decision=provenance_rows[0]["governance_decision"],
    )
    replay_valid = result.valid and provenance_check.valid and actual_digest == expected_digest
    reasons = list(result.reasons)
    reasons.extend(provenance_check.reasons)
    if actual_digest != expected_digest:
        reasons.append("recovery replay digest mismatch")
    return RecoveryReport(len(records), result.valid, replay_valid, expected_digest, actual_digest, tuple(dict.fromkeys(reasons)))
