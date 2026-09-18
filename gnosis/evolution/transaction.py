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
    # Schema must already exist. Do not run executescript here: SQLite's executescript
    # can implicitly commit an outer transaction and would violate nested atomicity.
    owns_transaction = not conn.in_transaction
    savepoint = "evolution_atomic"
    try:
        if owns_transaction:
            conn.execute("BEGIN IMMEDIATE")
        else:
            conn.execute(f"SAVEPOINT {savepoint}")
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
            provenance_id=provenance.provenance_id,
            parent_state_digest=provenance.parent_state_digest,
            proposed_state_digest=provenance.proposed_state_digest,
            evidence_digest=provenance.evidence_digest,
            payload=payload,
            previous_digest=previous_digest,
        )
        conn.execute(
            """INSERT INTO evolution_provenance
            (provenance_id,execution_id,candidate_id,parent_state_id,parent_state_digest,proposed_state_digest,evidence_digest,
             evaluation_status,shadow_status,invariant_status,governance_decision,status)
            VALUES (?,?,?,?,?,?,?,?,?,?,?,?)""",
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
            (sequence,event_type,candidate_id,execution_id,provenance_id,parent_state_digest,proposed_state_digest,evidence_digest,payload_digest,previous_digest,record_digest)
            VALUES (?,?,?,?,?,?,?,?,?,?,?)""",
            (
                record.sequence, record.event_type, record.candidate_id,
                record.execution_id, record.provenance_id, record.parent_state_digest,
                record.proposed_state_digest, record.evidence_digest, record.payload_digest,
                record.previous_digest, record.record_digest,
            ),
        )
        stored_provenance = conn.execute(
            "SELECT provenance_id FROM evolution_provenance WHERE provenance_id=?",
            (provenance.provenance_id,),
        ).fetchone()
        stored_audit = conn.execute(
            "SELECT provenance_id,record_digest FROM evolution_audit WHERE sequence=?",
            (record.sequence,),
        ).fetchone()
        if stored_provenance is None or stored_audit is None:
            raise RuntimeError("atomic evolution persistence verification failed")
        if stored_audit[0] != provenance.provenance_id or stored_audit[1] != record.record_digest:
            raise RuntimeError("atomic evolution persistence link mismatch")
        if owns_transaction:
            conn.commit()
        else:
            conn.execute(f"RELEASE SAVEPOINT {savepoint}")
        return EvolutionTransactionResult(
            provenance_id=provenance.provenance_id,
            audit_record=record,
        )
    except Exception:
        if owns_transaction:
            conn.rollback()
        else:
            conn.execute(f"ROLLBACK TO SAVEPOINT {savepoint}")
            conn.execute(f"RELEASE SAVEPOINT {savepoint}")
        raise
