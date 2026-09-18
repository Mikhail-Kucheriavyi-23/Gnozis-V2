import sqlite3

from gnosis.evolution.audit import make_audit_record, verify_audit_chain
from gnosis.reflection.persistence import (
    append_evolution_audit,
    ensure_reflection_schema,
    list_evolution_audit,
)


def test_audit_chain_is_append_only_and_verifiable():
    conn = sqlite3.connect(":memory:")
    ensure_reflection_schema(conn)
    first = append_evolution_audit(
        conn, event_type="SANDBOX", candidate_id="c1", execution_id="e1",
        payload={"status": "PASS"},
    )
    second = append_evolution_audit(
        conn, event_type="PROVENANCE", candidate_id="c1", execution_id="e1",
        payload={"digest": "abc"},
    )
    records = list_evolution_audit(conn)
    assert len(records) == 2
    assert second.previous_digest == first.record_digest
    assert verify_audit_chain(list(records)) == (True, ())


def test_audit_chain_detects_tampering():
    first = make_audit_record(
        sequence=0, event_type="SANDBOX", candidate_id="c1",
        execution_id="e1", payload={"status": "PASS"},
    )
    tampered = make_audit_record(
        sequence=1, event_type="PROVENANCE", candidate_id="c1",
        execution_id="e1", payload={"digest": "abc"},
        previous_digest=first.record_digest,
    )
    tampered = tampered.__class__(
        sequence=tampered.sequence,
        event_type=tampered.event_type,
        candidate_id=tampered.candidate_id,
        execution_id=tampered.execution_id,
        payload_digest="tampered",
        previous_digest=tampered.previous_digest,
        record_digest=tampered.record_digest,
    )
    valid, reasons = verify_audit_chain([first, tampered])
    assert not valid
    assert "record digest mismatch at 1" in reasons


def test_evolution_chain_survives_sqlite_reopen():
    conn = sqlite3.connect(":memory:")
    ensure_reflection_schema(conn)
    from gnosis.evolution.provenance import EvidenceProvenance
    from gnosis.reflection.persistence import load_evolution_provenance, save_evolution_provenance
    p = EvidenceProvenance(
        execution_id="e-recovery", candidate_id="c-recovery",
        parent_state_id="s-parent", parent_state_digest="pd",
        proposed_state_digest="sd", evidence_digest="ed",
        evaluation_status="PASS", shadow_status="NO_BEHAVIORAL_CHANGE",
        invariant_status="PRESERVED", governance_decision="REVIEW", status="RECORDED",
    )
    pid = save_evolution_provenance(conn, p)
    record = append_evolution_audit(
        conn, event_type="EVOLUTION_RECORDED", candidate_id=p.candidate_id,
        execution_id=p.execution_id, provenance_id=pid,
        parent_state_digest=p.parent_state_digest,
        proposed_state_digest=p.proposed_state_digest,
        evidence_digest=p.evidence_digest, payload={"status": "RECORDED"},
    )
    conn.commit()
    dump = conn.iterdump()
    sql = "\n".join(dump)
    conn.close()
    reopened = sqlite3.connect(":memory:")
    reopened.executescript(sql)
    loaded = load_evolution_provenance(reopened, pid)
    audits = list_evolution_audit(reopened)
    assert loaded["provenance_id"] == pid
    assert audits[0].record_digest == record.record_digest
    assert verify_audit_chain(list(audits)) == (True, ())


def test_recovery_detects_persisted_audit_tampering():
    conn = sqlite3.connect(":memory:")
    ensure_reflection_schema(conn)
    record = append_evolution_audit(
        conn, event_type="EVOLUTION_RECORDED", candidate_id="c",
        execution_id="e", provenance_id="p", parent_state_digest="pd",
        proposed_state_digest="sd", evidence_digest="ed", payload={"x": 1},
    )
    conn.execute("UPDATE evolution_audit SET evidence_digest='tampered'")
    audits = list_evolution_audit(conn)
    ok, reasons = verify_audit_chain(list(audits))
    assert not ok
    assert "record digest mismatch at 0" in reasons
