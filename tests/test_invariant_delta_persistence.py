import json

from gnosis.reflection.invariant_delta import InvariantDelta
from gnosis.reflection.persistence import (
    ensure_reflection_schema,
    list_invariant_deltas,
    load_invariant_delta,
    save_invariant_delta,
)
from gnosis.storage import connect


def test_invariant_delta_roundtrip_and_deterministic_identity():
    conn = connect(":memory:")
    delta = InvariantDelta(
        preserved=("state_integrity",),
        violated=("transition_validity",),
        improved=(),
        unknown=(),
        active_violations={"transition_validity": 0},
        shadow_violations={"transition_validity": 1},
    )
    ensure_reflection_schema(conn)

    first_id = save_invariant_delta(conn, "reflection:test", delta)
    second_id = save_invariant_delta(conn, "reflection:test", delta)

    assert first_id == second_id
    stored = load_invariant_delta(conn, first_id)
    assert stored["report_id"] == "reflection:test"
    assert stored["status"] == "VIOLATION"
    assert stored["payload"]["violated"] == ["transition_validity"]
    assert len(list_invariant_deltas(conn, "reflection:test")) == 1

    payload = json.loads(stored["raw_payload"])
    assert payload["provenance"] == "reflection-invariant-delta"
    conn.close()
