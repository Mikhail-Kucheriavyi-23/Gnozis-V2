"""Recovery verification for persisted evolution history."""
from __future__ import annotations

import sqlite3
from dataclasses import dataclass

from .audit import EvolutionAuditRecord, verify_audit_chain
from ..reflection.persistence import list_evolution_audit


@dataclass(frozen=True)
class RecoveryReport:
    recovered_records: int
    chain_valid: bool
    reasons: tuple[str, ...]


def recover_evolution_audit(conn: sqlite3.Connection) -> RecoveryReport:
    """Reconstruct the audit chain solely from durable SQLite records."""
    records = list(list_evolution_audit(conn))
    valid, reasons = verify_audit_chain(records)
    return RecoveryReport(
        recovered_records=len(records),
        chain_valid=valid,
        reasons=reasons,
    )
