from __future__ import annotations

import hashlib
import json
import sqlite3
from dataclasses import asdict, is_dataclass
from typing import Any

from .analyzer import ReflectionReport
from .counterexample import CounterexampleResult
from .governance import GovernanceDecision
from .invariant_delta import InvariantDelta
from .shadow import ShadowEvaluation
from gnosis.evolution.provenance import EvidenceProvenance, crosscheck_provenance
from gnosis.evolution.audit import EvolutionAuditRecord, make_audit_record


def _json(value: Any) -> str:
    if is_dataclass(value):
        value = asdict(value)
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"))


def reflection_id(report: ReflectionReport) -> str:
    return "reflection:" + hashlib.sha256(_json(report).encode("utf-8")).hexdigest()[:24]


def ensure_reflection_schema(conn: sqlite3.Connection) -> None:
    conn.executescript(
        """
        CREATE TABLE IF NOT EXISTS reflection_reports (
            report_id TEXT PRIMARY KEY,
            created_at TEXT NOT NULL,
            payload TEXT NOT NULL
        );
        CREATE TABLE IF NOT EXISTS reflection_counterexamples (
            result_id TEXT PRIMARY KEY,
            report_id TEXT NOT NULL,
            status TEXT NOT NULL,
            payload TEXT NOT NULL,
            FOREIGN KEY(report_id) REFERENCES reflection_reports(report_id)
        );
        CREATE TABLE IF NOT EXISTS reflection_shadow_assessments (
            assessment_id TEXT PRIMARY KEY,
            report_id TEXT NOT NULL,
            status TEXT NOT NULL,
            payload TEXT NOT NULL,
            FOREIGN KEY(report_id) REFERENCES reflection_reports(report_id)
        );
        CREATE TABLE IF NOT EXISTS reflection_invariant_deltas (
            delta_id TEXT PRIMARY KEY,
            report_id TEXT NOT NULL,
            status TEXT NOT NULL,
            payload TEXT NOT NULL,
            FOREIGN KEY(report_id) REFERENCES reflection_reports(report_id)
        );
        CREATE TABLE IF NOT EXISTS evolution_audit (
            sequence INTEGER PRIMARY KEY,
            event_type TEXT NOT NULL,
            candidate_id TEXT NOT NULL,
            execution_id TEXT NOT NULL,
            provenance_id TEXT NOT NULL,
            parent_state_digest TEXT NOT NULL,
            proposed_state_digest TEXT NOT NULL,
            evidence_digest TEXT NOT NULL,
            payload_digest TEXT NOT NULL,
            previous_digest TEXT NOT NULL,
            record_digest TEXT NOT NULL UNIQUE
        );
        CREATE INDEX IF NOT EXISTS idx_evolution_audit_candidate
            ON evolution_audit(candidate_id);

        CREATE TABLE IF NOT EXISTS evolution_provenance (
            provenance_id TEXT PRIMARY KEY,
            execution_id TEXT NOT NULL,
            candidate_id TEXT NOT NULL,
            parent_state_id TEXT NOT NULL,
            parent_state_digest TEXT NOT NULL,
            proposed_state_digest TEXT NOT NULL,
            evidence_digest TEXT NOT NULL,
            evaluation_status TEXT NOT NULL,
            shadow_status TEXT NOT NULL,
            invariant_status TEXT NOT NULL,
            governance_decision TEXT NOT NULL,
            status TEXT NOT NULL,
            evolution_identity TEXT NOT NULL DEFAULT '',
            proposed_state_content_id TEXT NOT NULL DEFAULT ''
        );
        CREATE INDEX IF NOT EXISTS idx_evolution_provenance_candidate
            ON evolution_provenance(candidate_id);
        CREATE INDEX IF NOT EXISTS idx_evolution_provenance_digest
            ON evolution_provenance(evidence_digest);

        CREATE TABLE IF NOT EXISTS reflection_governance_decisions (
            decision_id TEXT PRIMARY KEY,
            report_id TEXT NOT NULL,
            decision TEXT NOT NULL,
            payload TEXT NOT NULL,
            FOREIGN KEY(report_id) REFERENCES reflection_reports(report_id)
        );
        CREATE INDEX IF NOT EXISTS idx_reflection_counterexamples_report
            ON reflection_counterexamples(report_id);
        CREATE INDEX IF NOT EXISTS idx_reflection_shadow_report
            ON reflection_shadow_assessments(report_id);
        CREATE INDEX IF NOT EXISTS idx_reflection_invariant_delta_report
            ON reflection_invariant_deltas(report_id);
        CREATE INDEX IF NOT EXISTS idx_reflection_governance_report
            ON reflection_governance_decisions(report_id);
        """
    )
    try:
        conn.execute("ALTER TABLE evolution_provenance ADD COLUMN evolution_identity TEXT NOT NULL DEFAULT ''")
    except sqlite3.OperationalError:
        pass
    try:
        conn.execute("ALTER TABLE evolution_provenance ADD COLUMN proposed_state_content_id TEXT NOT NULL DEFAULT ''")
    except sqlite3.OperationalError:
        pass


def save_reflection_report(
    conn: sqlite3.Connection,
    report: ReflectionReport,
    *,
    created_at: str,
    shadow_assessments: tuple[ShadowEvaluation, ...] = (),
) -> str:
    ensure_reflection_schema(conn)
    report_key = reflection_id(report)
    conn.execute(
        "INSERT OR IGNORE INTO reflection_reports(report_id,created_at,payload) VALUES(?,?,?)",
        (report_key, created_at, _json(report)),
    )
    for result in report.counterexample_results:
        save_counterexample(conn, report_key, result)
    for assessment in shadow_assessments:
        save_shadow_assessment(conn, report_key, assessment)
    return report_key


def save_counterexample(conn: sqlite3.Connection, report_id: str, result: CounterexampleResult) -> str:
    ensure_reflection_schema(conn)
    result_id = f"{report_id}:counterexample:{result.candidate_id}"
    conn.execute(
        "INSERT OR REPLACE INTO reflection_counterexamples(result_id,report_id,status,payload) VALUES(?,?,?,?)",
        (result_id, report_id, result.status, _json(result)),
    )
    return result_id


def save_shadow_assessment(conn: sqlite3.Connection, report_id: str, assessment: ShadowEvaluation) -> str:
    ensure_reflection_schema(conn)
    assessment_id = f"{report_id}:shadow:{len(assessment.cases)}:{assessment.status}"
    conn.execute(
        "INSERT OR REPLACE INTO reflection_shadow_assessments(assessment_id,report_id,status,payload) VALUES(?,?,?,?)",
        (assessment_id, report_id, assessment.status, _json(assessment)),
    )
    return assessment_id


def invariant_delta_id(report_id: str, delta: InvariantDelta) -> str:
    return f"{report_id}:invariant-delta:" + hashlib.sha256(_json(delta).encode("utf-8")).hexdigest()[:24]


def save_invariant_delta(conn: sqlite3.Connection, report_id: str, delta: InvariantDelta) -> str:
    ensure_reflection_schema(conn)
    delta_id = invariant_delta_id(report_id, delta)
    conn.execute(
        "INSERT OR IGNORE INTO reflection_invariant_deltas(delta_id,report_id,status,payload) VALUES(?,?,?,?)",
        (delta_id, report_id, delta.status, _json(delta)),
    )
    return delta_id


def load_invariant_delta(conn: sqlite3.Connection, delta_id: str) -> dict[str, Any]:
    ensure_reflection_schema(conn)
    row = conn.execute(
        "SELECT delta_id,report_id,status,payload FROM reflection_invariant_deltas WHERE delta_id=?",
        (delta_id,),
    ).fetchone()
    if row is None:
        raise KeyError(delta_id)
    return {"delta_id": row[0], "report_id": row[1], "status": row[2], "payload": json.loads(row[3]), "raw_payload": row[3]}


def list_invariant_deltas(conn: sqlite3.Connection, report_id: str | None = None) -> tuple[dict[str, Any], ...]:
    ensure_reflection_schema(conn)
    if report_id is None:
        rows = conn.execute("SELECT delta_id,report_id,status,payload FROM reflection_invariant_deltas ORDER BY rowid").fetchall()
    else:
        rows = conn.execute("SELECT delta_id,report_id,status,payload FROM reflection_invariant_deltas WHERE report_id=? ORDER BY rowid", (report_id,)).fetchall()
    return tuple({"delta_id": row[0], "report_id": row[1], "status": row[2], "payload": json.loads(row[3]), "raw_payload": row[3]} for row in rows)


def governance_decision_id(report_id: str, decision: GovernanceDecision) -> str:
    return f"{report_id}:governance:" + hashlib.sha256(_json(decision).encode("utf-8")).hexdigest()[:24]


def save_governance_decision(conn: sqlite3.Connection, report_id: str, decision: GovernanceDecision) -> str:
    ensure_reflection_schema(conn)
    decision_id = governance_decision_id(report_id, decision)
    conn.execute(
        "INSERT OR IGNORE INTO reflection_governance_decisions(decision_id,report_id,decision,payload) VALUES(?,?,?,?)",
        (decision_id, report_id, decision.decision, _json(decision)),
    )
    return decision_id


def load_governance_decision(conn: sqlite3.Connection, decision_id: str) -> dict[str, Any]:
    ensure_reflection_schema(conn)
    row = conn.execute(
        "SELECT decision_id,report_id,decision,payload FROM reflection_governance_decisions WHERE decision_id=?",
        (decision_id,),
    ).fetchone()
    if row is None:
        raise KeyError(decision_id)
    return {"decision_id": row[0], "report_id": row[1], "decision": row[2], "payload": json.loads(row[3]), "raw_payload": row[3]}


def list_governance_decisions(conn: sqlite3.Connection, report_id: str | None = None) -> tuple[dict[str, Any], ...]:
    ensure_reflection_schema(conn)
    if report_id is None:
        rows = conn.execute("SELECT decision_id,report_id,decision,payload FROM reflection_governance_decisions ORDER BY rowid").fetchall()
    else:
        rows = conn.execute("SELECT decision_id,report_id,decision,payload FROM reflection_governance_decisions WHERE report_id=? ORDER BY rowid", (report_id,)).fetchall()
    return tuple({"decision_id": row[0], "report_id": row[1], "decision": row[2], "payload": json.loads(row[3]), "raw_payload": row[3]} for row in rows)


def load_reflection_report(conn: sqlite3.Connection, stored_report_id: str) -> dict[str, Any]:
    ensure_reflection_schema(conn)
    row = conn.execute("SELECT report_id,created_at,payload FROM reflection_reports WHERE report_id=?", (stored_report_id,)).fetchone()
    if row is None:
        raise KeyError(stored_report_id)
    return {"report_id": row[0], "created_at": row[1], "payload": json.loads(row[2])}


def list_reflection_reports(conn: sqlite3.Connection) -> tuple[dict[str, Any], ...]:
    ensure_reflection_schema(conn)
    rows = conn.execute("SELECT report_id,created_at,payload FROM reflection_reports ORDER BY created_at,report_id").fetchall()
    return tuple({"report_id": row[0], "created_at": row[1], "payload": json.loads(row[2])} for row in rows)


def classify_evolution_provenance(row: dict[str, Any]) -> str:
    """Classify persisted provenance without silently upgrading legacy records."""
    identity = row.get("evolution_identity")
    if identity is None or identity == "":
        return "legacy_unverified"
    return "canonical"


def save_evolution_provenance(conn: sqlite3.Connection, provenance: Any) -> str:
    """Persist immutable provenance metadata; never activates the candidate."""
    ensure_reflection_schema(conn)
    provenance_id = provenance.provenance_id
    evolution_identity = provenance.evolution_identity
    payload = _json(provenance)
    conn.execute(
        """INSERT OR IGNORE INTO evolution_provenance
        (provenance_id,execution_id,candidate_id,parent_state_id,parent_state_digest,proposed_state_digest,evidence_digest,
         evaluation_status,shadow_status,invariant_status,governance_decision,status,evolution_identity)
        VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?)""",
        (
            provenance_id,
            provenance.execution_id,
            provenance.candidate_id,
            provenance.parent_state_id,
            provenance.parent_state_digest,
            provenance.proposed_state_digest,
            provenance.evidence_digest,
            provenance.evaluation_status,
            provenance.shadow_status,
            provenance.invariant_status,
            provenance.governance_decision,
            provenance.status,
            evolution_identity,
            provenance.proposed_state_content_id,
        ),
    )
    return provenance_id


def load_evolution_provenance(conn: sqlite3.Connection, provenance_id: str) -> dict[str, Any]:
    ensure_reflection_schema(conn)
    row = conn.execute(
        """SELECT provenance_id,execution_id,candidate_id,parent_state_id,parent_state_digest,proposed_state_digest,evidence_digest,evolution_identity,
                  evaluation_status,shadow_status,invariant_status,governance_decision,status
           FROM evolution_provenance WHERE provenance_id=?""",
        (provenance_id,),
    ).fetchone()
    if row is None:
        raise KeyError(provenance_id)
    keys = (
        "provenance_id","execution_id","candidate_id","parent_state_id","parent_state_digest","proposed_state_digest","evidence_digest","evolution_identity","proposed_state_content_id",
        "evaluation_status","shadow_status","invariant_status","governance_decision","status",
    )
    return dict(zip(keys, row))


def list_evolution_provenance(
    conn: sqlite3.Connection, candidate_id: str | None = None
) -> tuple[dict[str, Any], ...]:
    ensure_reflection_schema(conn)
    if candidate_id is None:
        rows = conn.execute(
            "SELECT provenance_id,execution_id,candidate_id,parent_state_id,parent_state_digest,proposed_state_digest,evidence_digest,evolution_identity,"
            "evaluation_status,shadow_status,invariant_status,governance_decision,status "
            "FROM evolution_provenance ORDER BY rowid"
        ).fetchall()
    else:
        rows = conn.execute(
            "SELECT provenance_id,execution_id,candidate_id,parent_state_id,parent_state_digest,proposed_state_digest,evidence_digest,"
            "evaluation_status,shadow_status,invariant_status,governance_decision,status "
            "FROM evolution_provenance WHERE candidate_id=? ORDER BY rowid",
            (candidate_id,),
        ).fetchall()
    keys = (
        "provenance_id","execution_id","candidate_id","parent_state_id","parent_state_digest","proposed_state_digest","evidence_digest","evolution_identity",
        "evaluation_status","shadow_status","invariant_status","governance_decision","status",
    )
    return tuple(dict(zip(keys, row)) for row in rows)


def crosscheck_stored_provenance(
    conn: sqlite3.Connection,
    provenance_id: str,
    *,
    observations: dict[str, Any],
) -> Any:
    """Re-validate stored identity/evidence links against supplied observations."""
    row = load_evolution_provenance(conn, provenance_id)
    provenance = EvidenceProvenance(
        execution_id=row["execution_id"],
        candidate_id=row["candidate_id"],
        parent_state_id=row["parent_state_id"],
        parent_state_digest=row["parent_state_digest"],
        proposed_state_digest=row["proposed_state_digest"],
        evidence_digest=row["evidence_digest"],
        evaluation_status=row["evaluation_status"],
        shadow_status=row["shadow_status"],
        invariant_status=row["invariant_status"],
        governance_decision=row["governance_decision"],
        status=row["status"],
    )
    return crosscheck_provenance(
        provenance=provenance,
        candidate_id=row["candidate_id"],
        parent_state_id=row["parent_state_id"],
        parent_state_digest=row["parent_state_digest"],
        proposed_state_digest=row["proposed_state_digest"],
        observations=observations,
        evidence_digest=row["evidence_digest"],
        execution_id_value=row["execution_id"],
        evaluation_status=row["evaluation_status"],
        shadow_status=row["shadow_status"],
        invariant_status=row["invariant_status"],
        governance_decision=row["governance_decision"],
    )


def append_evolution_audit(
    conn: sqlite3.Connection,
    *,
    event_type: str,
    candidate_id: str,
    execution_id: str,
    provenance_id: str = "",
    parent_state_digest: str = "",
    proposed_state_digest: str = "",
    evidence_digest: str = "",
    payload: dict[str, Any],
) -> EvolutionAuditRecord:
    """Append exactly one record; prior audit records are never updated."""
    ensure_reflection_schema(conn)
    row = conn.execute(
        "SELECT sequence, record_digest FROM evolution_audit ORDER BY sequence DESC LIMIT 1"
    ).fetchone()
    sequence = 0 if row is None else row[0] + 1
    previous_digest = "" if row is None else row[1]
    record = make_audit_record(
        sequence=sequence,
        event_type=event_type,
        candidate_id=candidate_id,
        execution_id=execution_id,
        provenance_id=provenance_id,
        parent_state_digest=parent_state_digest,
        proposed_state_digest=proposed_state_digest,
        evidence_digest=evidence_digest,
        payload=payload,
        previous_digest=previous_digest,
    )
    conn.execute(
        """INSERT INTO evolution_audit
        (sequence,event_type,candidate_id,execution_id,provenance_id,parent_state_digest,proposed_state_digest,evidence_digest,payload_digest,previous_digest,record_digest)
        VALUES (?,?,?,?,?,?,?,?,?,?,?)""",
        (record.sequence, record.event_type, record.candidate_id, record.execution_id, record.provenance_id,
         record.parent_state_digest, record.proposed_state_digest, record.evidence_digest,
         record.payload_digest, record.previous_digest, record.record_digest),
    )
    return record


def list_evolution_audit(conn: sqlite3.Connection) -> tuple[EvolutionAuditRecord, ...]:
    ensure_reflection_schema(conn)
    rows = conn.execute(
        """SELECT sequence,event_type,candidate_id,execution_id,provenance_id,
                  parent_state_digest,proposed_state_digest,evidence_digest,payload_digest,
                  previous_digest,record_digest
           FROM evolution_audit ORDER BY sequence"""
    ).fetchall()
    return tuple(EvolutionAuditRecord(*row) for row in rows)
