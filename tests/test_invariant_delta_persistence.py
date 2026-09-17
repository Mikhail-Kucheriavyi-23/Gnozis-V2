import json

from gnosis.reflection.analyzer import ReflectionReport
from gnosis.reflection.invariant_delta import InvariantDelta
from gnosis.reflection.persistence import (
    list_invariant_deltas,
    load_invariant_delta,
    save_invariant_delta,
    save_reflection_report,
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

    report_id = save_reflection_report(
        conn,
        ReflectionReport(),
        created_at="2026-09-17T00:00:00Z",
    )
    first_id = save_invariant_delta(conn, report_id, delta)
    second_id = save_invariant_delta(conn, report_id, delta)

    assert first_id == second_id
    stored = load_invariant_delta(conn, first_id)
    assert stored["report_id"] == report_id
    assert stored["status"] == "VIOLATION"
    assert stored["payload"]["violated"] == ["transition_validity"]
    assert len(list_invariant_deltas(conn, report_id)) == 1

    payload = json.loads(stored["raw_payload"])
    assert payload["provenance"] == "reflection-invariant-delta"
    conn.close()
