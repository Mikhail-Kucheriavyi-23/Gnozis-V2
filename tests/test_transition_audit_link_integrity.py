import pytest

from gnosis.storage.repositories import StorageCorruptionError, verify_durable_graph


def test_transition_audit_link_tampering_is_rejected(persisted_transition):
    conn, instance, _record = persisted_transition
    row = conn.execute(
        "SELECT transition_id FROM transitions WHERE instance_id=? LIMIT 1",
        (instance.instance_id,),
    ).fetchone()
    assert row is not None
    transition_id = row[0]
    other = "f" * 64
    conn.execute("DROP TRIGGER audit_events_no_update")
    conn.execute("UPDATE audit_events SET transition_id=? WHERE transition_id=?", (other, transition_id))
    with pytest.raises((StorageCorruptionError, ValueError, RuntimeError)):
        verify_durable_graph(conn)


def test_transition_audit_link_is_valid_for_persisted_transition(persisted_transition):
    conn, _instance, _record = persisted_transition
    verify_durable_graph(conn)
