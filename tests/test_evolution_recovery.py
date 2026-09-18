import sqlite3

from gnosis.evolution.recovery import recover_evolution_audit
from gnosis.reflection.persistence import append_evolution_audit, ensure_reflection_schema


def test_recovery_rebuilds_and_verifies_audit_from_sqlite():
    conn = sqlite3.connect(":memory:")
    ensure_reflection_schema(conn)
    append_evolution_audit(
        conn, event_type="SANDBOX", candidate_id="c1", execution_id="e1",
        payload={"status": "PASS"},
    )
    append_evolution_audit(
        conn, event_type="PROVENANCE", candidate_id="c1", execution_id="e1",
        payload={"digest": "abc"},
    )
    report = recover_evolution_audit(conn)
    assert report.recovered_records == 2
    assert report.chain_valid
    assert report.reasons == ()


def test_recovery_detects_persisted_tampering():
    conn = sqlite3.connect(":memory:")
    ensure_reflection_schema(conn)
    append_evolution_audit(
        conn, event_type="SANDBOX", candidate_id="c1", execution_id="e1",
        payload={"status": "PASS"},
    )
    conn.execute("UPDATE evolution_audit SET payload_digest='tampered' WHERE sequence=0")
    report = recover_evolution_audit(conn)
    assert not report.chain_valid
    assert "record digest mismatch at 0" in report.reasons
