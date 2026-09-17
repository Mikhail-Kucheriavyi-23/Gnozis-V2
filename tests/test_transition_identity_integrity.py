import pytest

from gnosis.storage.repositories import StorageCorruptionError, transition_id, verify_durable_graph


def test_durable_graph_rejects_transition_id_tampering(persisted_transition):
    conn, instance, record = persisted_transition
    row = conn.execute(
        "SELECT transition_id FROM transitions WHERE instance_id=? ORDER BY created_at, transition_id LIMIT 1",
        (instance.instance_id,),
    ).fetchone()
    assert row is not None
    original = row[0]
    tampered = "f" * 64 if original != "f" * 64 else "e" * 64
    conn.execute(
        "UPDATE transitions SET transition_id=? WHERE transition_id=?",
        (tampered, original),
    )
    with pytest.raises(StorageCorruptionError):
        verify_durable_graph(conn)


def test_transition_identity_function_is_deterministic(persisted_transition):
    _conn, _instance, record = persisted_transition
    assert transition_id(record) == transition_id(record)
