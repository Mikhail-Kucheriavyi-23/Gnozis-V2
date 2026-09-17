from __future__ import annotations

import json
import sqlite3
from dataclasses import asdict, is_dataclass
from typing import Any

from .counterexample import CounterexampleResult
from .models import ReflectionReport
from .shadow import ShadowAssessment


def _json(value: Any) -> str:
    if is_dataclass(value):
        value = asdict(value)
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"))


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
        CREATE INDEX IF NOT EXISTS idx_reflection_counterexamples_report
            ON reflection_counterexamples(report_id);
        CREATE INDEX IF NOT EXISTS idx_reflection_shadow_report
            ON reflection_shadow_assessments(report_id);
        """
    )


def save_reflection_report(
    conn: sqlite3.Connection,
    report: ReflectionReport,
    *,
    created_at: str,
) -> str:
    ensure_reflection_schema(conn)
    payload = _json(report)
    conn.execute(
        "INSERT OR IGNORE INTO reflection_reports(report_id,created_at,payload) VALUES(?,?,?)",
        (report.report_id, created_at, payload),
    )
    for result in getattr(report, "counterexamples", ()):
        save_counterexample(conn, report.report_id, result)
    for assessment in getattr(report, "shadow_assessments", ()):
        save_shadow_assessment(conn, report.report_id, assessment)
    return report.report_id


def save_counterexample(
    conn: sqlite3.Connection,
    report_id: str,
    result: CounterexampleResult,
) -> str:
    ensure_reflection_schema(conn)
    payload = _json(result)
    conn.execute(
        "INSERT OR REPLACE INTO reflection_counterexamples(result_id,report_id,status,payload) VALUES(?,?,?,?)",
        (result.result_id, report_id, result.status, payload),
    )
    return result.result_id


def save_shadow_assessment(
    conn: sqlite3.Connection,
    report_id: str,
    assessment: ShadowAssessment,
) -> str:
    ensure_reflection_schema(conn)
    payload = _json(assessment)
    conn.execute(
        "INSERT OR REPLACE INTO reflection_shadow_assessments(assessment_id,report_id,status,payload) VALUES(?,?,?,?)",
        (assessment.assessment_id, report_id, assessment.status, payload),
    )
    return assessment.assessment_id


def load_reflection_report(conn: sqlite3.Connection, report_id: str) -> dict[str, Any]:
    ensure_reflection_schema(conn)
    row = conn.execute(
        "SELECT report_id,created_at,payload FROM reflection_reports WHERE report_id=?",
        (report_id,),
    ).fetchone()
    if row is None:
        raise KeyError(report_id)
    return {"report_id": row[0], "created_at": row[1], "payload": json.loads(row[2])}
