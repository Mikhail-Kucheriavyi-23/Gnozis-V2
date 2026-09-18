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
