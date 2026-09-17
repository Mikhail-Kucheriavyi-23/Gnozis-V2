import pytest

from gnosis.storage.repositories import StorageCorruptionError, verify_audit_chain


def test_audit_event_payload_tampering_is_rejected(persisted_transition):
    conn, _instance, _record = persisted_transition
    row = conn.execute("SELECT event_id FROM audit_events ORDER BY sequence LIMIT 1").fetchone()
    assert row is not None
    conn.execute("UPDATE audit_events SET result='tampered' WHERE event_id=?", (row[0],))
    with pytest.raises(StorageCorruptionError, match="audit event hash mismatch"):
        verify_audit_chain(conn)


def test_audit_event_hash_tampering_is_rejected(persisted_transition):
    conn, _instance, _record = persisted_transition
    row = conn.execute("SELECT event_id FROM audit_events ORDER BY sequence LIMIT 1").fetchone()
    assert row is not None
    conn.execute("UPDATE audit_events SET event_hash=? WHERE event_id=?", ("f" * 64, row[0]))
    with pytest.raises(StorageCorruptionError):
        verify_audit_chain(conn)


def test_audit_prev_hash_tampering_is_rejected(persisted_transition):
    conn, _instance, _record = persisted_transition
    rows = conn.execute("SELECT event_id FROM audit_events ORDER BY sequence").fetchall()
    assert len(rows) >= 2
    conn.execute("UPDATE audit_events SET prev_hash=? WHERE event_id=?", ("a" * 64, rows[1][0]))
    with pytest.raises(StorageCorruptionError, match="sequence/link mismatch"):
        verify_audit_chain(conn)
