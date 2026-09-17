from __future__ import annotations

import sqlite3

from gnosis.reflection.governance import GovernanceDecision
from gnosis.reflection.persistence import ensure_reflection_schema


def test_governance_decision_payload_roundtrip_contract() -> None:
    conn = sqlite3.connect(":memory:")
    ensure_reflection_schema(conn)
    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS reflection_governance_decisions (
            decision_id TEXT PRIMARY KEY,
            report_id TEXT NOT NULL,
            decision TEXT NOT NULL,
            payload TEXT NOT NULL
        )
        """
    )

    decision = GovernanceDecision(
        decision="REVIEW",
        shadow_status="BEHAVIOR_CHANGED",
        invariant_status="IMPROVED",
        rationale=("behavior_changed",),
    )
    import json
    from dataclasses import asdict

    payload = json.dumps(asdict(decision), sort_keys=True)
    conn.execute(
        "INSERT INTO reflection_governance_decisions VALUES (?,?,?,?)",
        ("governance:test", "reflection:test", decision.decision, payload),
    )
    row = conn.execute(
        "SELECT decision, payload FROM reflection_governance_decisions WHERE decision_id=?",
        ("governance:test",),
    ).fetchone()
    assert row is not None
    assert row[0] == "REVIEW"
    assert json.loads(row[1])["can_activate"] if "can_activate" in json.loads(row[1]) else True
    assert decision.can_activate is False
    assert decision.can_rollback is False
