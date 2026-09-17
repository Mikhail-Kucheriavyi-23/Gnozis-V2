from __future__ import annotations

import hashlib
import json
import sqlite3
from dataclasses import asdict, is_dataclass
from typing import Any

from .analyzer import ReflectionReport
from .counterexample import CounterexampleResult
from .shadow import ShadowEvaluation


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


def load_reflection_report(conn: sqlite3.Connection, stored_report_id: str) -> dict[str, Any]:
    ensure_reflection_schema(conn)
    row = conn.execute(
        "SELECT report_id,created_at,payload FROM reflection_reports WHERE report_id=?",
        (stored_report_id,),
    ).fetchone()
    if row is None:
        raise KeyError(stored_report_id)
    return {"report_id": row[0], "created_at": row[1], "payload": json.loads(row[2])}


def list_reflection_reports(conn: sqlite3.Connection) -> tuple[dict[str, Any], ...]:
    ensure_reflection_schema(conn)
    rows = conn.execute(
        "SELECT report_id,created_at,payload FROM reflection_reports ORDER BY created_at,report_id"
    ).fetchall()
    return tuple(
        {"report_id": row[0], "created_at": row[1], "payload": json.loads(row[2])}
        for row in rows
    )
