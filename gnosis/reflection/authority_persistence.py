"""Persistent provenance for non-authoritative evolution requests."""

from __future__ import annotations

import hashlib
import json
import sqlite3
from dataclasses import asdict

from .authority import AuthorityRequest


def authority_request_id(report_id: str, request: AuthorityRequest) -> str:
    payload = json.dumps(asdict(request), sort_keys=True, separators=(",", ":"))
    digest = hashlib.sha256(payload.encode("utf-8")).hexdigest()[:24]
    return f"{report_id}:authority:{digest}"


def ensure_authority_schema(conn: sqlite3.Connection) -> None:
    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS reflection_authority_requests (
            request_id TEXT PRIMARY KEY,
            report_id TEXT NOT NULL,
            decision_id TEXT NOT NULL,
            request_payload TEXT NOT NULL
        )
        """
    )
    conn.execute(
        "CREATE INDEX IF NOT EXISTS idx_authority_report ON reflection_authority_requests(report_id)"
    )


def save_authority_request(
    conn: sqlite3.Connection,
    report_id: str,
    decision_id: str,
    request: AuthorityRequest,
) -> str:
    ensure_authority_schema(conn)
    request_id = authority_request_id(report_id, request)
    conn.execute(
        """
        INSERT OR IGNORE INTO reflection_authority_requests
        (request_id, report_id, decision_id, request_payload)
        VALUES (?, ?, ?, ?)
        """,
        (
            request_id,
            report_id,
            decision_id,
            json.dumps(asdict(request), sort_keys=True, separators=(",", ":")),
        ),
    )
    return request_id


def load_authority_request(conn: sqlite3.Connection, request_id: str) -> dict[str, object]:
    ensure_authority_schema(conn)
    row = conn.execute(
        """
        SELECT request_id, report_id, decision_id, request_payload
        FROM reflection_authority_requests
        WHERE request_id=?
        """,
        (request_id,),
    ).fetchone()
    if row is None:
        raise KeyError(request_id)
    return {
        "request_id": row[0],
        "report_id": row[1],
        "decision_id": row[2],
        "payload": json.loads(row[3]),
        "raw_payload": row[3],
    }
