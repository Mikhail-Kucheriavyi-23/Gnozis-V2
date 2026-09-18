"""Recovery verification for persisted evolution history."""
from __future__ import annotations

import sqlite3
from dataclasses import dataclass
from typing import Any

from .chain_verifier import verify_persisted_chain
from ..reflection.persistence import list_evolution_audit, list_evolution_provenance


@dataclass(frozen=True)
class RecoveryReport:
    recovered_records: int
    chain_valid: bool
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
            return RecoveryReport(0, True, ())
        return RecoveryReport(
            recovered_records=len(records),
            chain_valid=False,
            reasons=("provenance identity required for trusted recovery",),
        )
    rows = list_evolution_provenance(conn, candidate_id=None)
    provenance_rows = [row for row in rows if row["provenance_id"] == provenance_id]
    if not provenance_rows:
        return RecoveryReport(len(records), False, ("provenance record missing",))
    if observations is None:
        return RecoveryReport(len(records), False, ("observations required for independent recovery verification",))
    result = verify_persisted_chain(
        provenance_rows[0],
        [record.__dict__ for record in records],
        observations=observations,
    )
    return RecoveryReport(len(records), result.valid, result.reasons)
