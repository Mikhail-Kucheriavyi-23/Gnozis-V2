from gnosis.storage.repositories import verify_durable_graph


def test_valid_transition_identity_is_accepted(persisted_transition):
    conn, _instance, _record = persisted_transition
    sequence, _last_hash = verify_durable_graph(conn)
    assert sequence >= 1
