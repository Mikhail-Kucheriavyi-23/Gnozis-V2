import sqlite3

from gnosis.reflection.authority import AuthorityRequest
from gnosis.reflection.authority_persistence import (
    load_authority_request,
    save_authority_request,
)


def test_authority_request_roundtrip_preserves_lineage() -> None:
    conn = sqlite3.connect(":memory:")
    request = AuthorityRequest(
        decision="REVIEW",
        rationale=("behavior_changed",),
    )

    request_id = save_authority_request(
        conn,
        "reflection:test",
        "reflection:test:governance:1",
        request,
    )
    restored = load_authority_request(conn, request_id)

    assert restored["request_id"] == request_id
    assert restored["report_id"] == "reflection:test"
    assert restored["decision_id"] == "reflection:test:governance:1"
    assert restored["payload"]["decision"] == "REVIEW"
    assert restored["payload"]["requires_owner_approval"] is True
