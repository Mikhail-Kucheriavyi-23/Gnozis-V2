import sqlite3
import pytest

from gnosis.evolution.provenance import build_provenance, canonical_digest
from gnosis.evolution.transaction import persist_evolution_transaction
from gnosis.reflection.persistence import ensure_reflection_schema


def _provenance():
    observations = {"metric": 13}
    return build_provenance(
        candidate_id="candidate:tx",
        parent_state_id="state:tx",
        observations=observations,
        evidence_digest=canonical_digest(observations),
        evaluation_status="PASS",
        shadow_status="NO_BEHAVIORAL_CHANGE",
        invariant_status="PRESERVED",
        governance_decision="REVIEW",
    )


def test_evolution_transaction_commits_provenance_and_audit_together():
    conn = sqlite3.connect(":memory:")
    ensure_reflection_schema(conn)
    result = persist_evolution_transaction(
        conn, _provenance(), event_type="PROVENANCE", payload={"status": "RECORDED"}
    )
    assert conn.execute("SELECT count(*) FROM evolution_provenance").fetchone()[0] == 1
    assert conn.execute("SELECT count(*) FROM evolution_audit").fetchone()[0] == 1
    assert result.audit_record.candidate_id == "candidate:tx"


def test_evolution_transaction_rolls_back_both_records_on_failure(monkeypatch):
    conn = sqlite3.connect(":memory:")
    ensure_reflection_schema(conn)
    original = conn.execute

    def fail_on_audit(sql, params=()):
        if "INSERT INTO evolution_audit" in sql:
            raise sqlite3.IntegrityError("simulated audit failure")
        return original(sql, params)

    monkeypatch.setattr(conn, "execute", fail_on_audit)
    with pytest.raises(sqlite3.IntegrityError):
        persist_evolution_transaction(
            conn, _provenance(), event_type="PROVENANCE", payload={"status": "RECORDED"}
        )
    assert conn.execute("SELECT count(*) FROM evolution_provenance").fetchone()[0] == 0
    assert conn.execute("SELECT count(*) FROM evolution_audit").fetchone()[0] == 0
