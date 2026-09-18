"""Atomic durable transaction for evolution provenance and audit."""
from __future__ import annotations

import sqlite3
from dataclasses import dataclass
from typing import Any

from .audit import EvolutionAuditRecord, make_audit_record
from .provenance import EvidenceProvenance



@dataclass(frozen=True)
class EvolutionTransactionResult:
    provenance_id: str
    audit_record: EvolutionAuditRecord


def persist_evolution_transaction(
    conn: sqlite3.Connection,
    provenance: EvidenceProvenance,
    *,
    event_type: str,
    payload: dict[str, Any],
) -> EvolutionTransactionResult:
    """Atomically persist provenance and its audit event, or persist neither."""
    conn.executescript("""
        CREATE TABLE IF NOT EXISTS evolution_provenance (
            provenance_id TEXT PRIMARY KEY, execution_id TEXT NOT NULL, candidate_id TEXT NOT NULL,
            parent_state_id TEXT NOT NULL, parent_state_digest TEXT NOT NULL, proposed_state_digest TEXT NOT NULL, evidence_digest TEXT NOT NULL,
            evaluation_status TEXT NOT NULL, shadow_status TEXT NOT NULL,
            invariant_status TEXT NOT NULL, governance_decision TEXT NOT NULL, status TEXT NOT NULL
        );
        CREATE TABLE IF NOT EXISTS evolution_audit (
            sequence INTEGER PRIMARY KEY, event_type TEXT NOT NULL, candidate_id TEXT NOT NULL,
            execution_id TEXT NOT NULL, payload_digest TEXT NOT NULL, previous_digest TEXT NOT NULL,
            record_digest TEXT NOT NULL UNIQUE
        );
    """)
    owns_transaction = conn.in_transaction is False
    try:
        if owns_transaction:
            conn.execute("BEGIN IMMEDIATE")
        row = conn.execute(
            "SELECT sequence, record_digest FROM evolution_audit ORDER BY sequence DESC LIMIT 1"
        ).fetchone()
        sequence = 0 if row is None else row[0] + 1
        previous_digest = "" if row is None else row[1]
        record = make_audit_record(
            sequence=sequence,
            event_type=event_type,
            candidate_id=provenance.candidate_id,
            execution_id=provenance.execution_id,
            payload=payload,
            previous_digest=previous_digest,
        )
        conn.execute(
            """INSERT INTO evolution_provenance
            (provenance_id,execution_id,candidate_id,parent_state_id,parent_state_digest,proposed_state_digest,evidence_digest,
             evaluation_status,shadow_status,invariant_status,governance_decision,status)
            VALUES (?,?,?,?,?,?,?,?,?,?)""",
            (
                provenance.provenance_id, provenance.execution_id,
                provenance.candidate_id, provenance.parent_state_id,
                provenance.parent_state_digest, provenance.proposed_state_digest,
                provenance.evidence_digest, provenance.evaluation_status,
                provenance.shadow_status, provenance.invariant_status,
                provenance.governance_decision, provenance.status,
            ),
        )
        conn.execute(
            """INSERT INTO evolution_audit
            (sequence,event_type,candidate_id,execution_id,payload_digest,previous_digest,record_digest)
            VALUES (?,?,?,?,?,?,?)""",
            (
                record.sequence, record.event_type, record.candidate_id,
                record.execution_id, record.payload_digest,
                record.previous_digest, record.record_digest,
            ),
        )
        if owns_transaction:
            conn.commit()
        return EvolutionTransactionResult(
            provenance_id=provenance.provenance_id,
            audit_record=record,
        )
    except Exception:
        if owns_transaction:
            conn.rollback()
        raise
