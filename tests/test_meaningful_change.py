"""
PATCH defect #2 regression tests — identity/no-op evolution rejection.

Exact adversarial scenario from the PATCH ТЗ section 3 / from the original
audit: a candidate with identical elements/relations but a bumped version
must now be REJECTED by check_meaningful_change, where it was previously
ACCEPTED.
"""

from gnosis.core import (
    Candidate,
    Relation,
    State,
    all_pass,
    check_meaningful_change,
    run_invariants,
)


def test_version_only_change_is_rejected():
    """The exact scenario the audit reproduced: same elements, same
    relations, version+1 -> must now fail check_meaningful_change."""
    current = State(elements={"a": 1}, version=1)
    proposed = State(elements={"a": 1}, version=2)  # content-identical
    candidate = Candidate(
        parent_state_id=current.state_id, proposed_state=proposed, origin="test"
    )

    result = check_meaningful_change(current, candidate)
    assert not result.ok

    results = run_invariants(current, candidate)
    assert not all_pass(results)
    names = {r.name for r in results if not r.ok}
    assert "meaningful_change" in names


def test_element_content_change_is_accepted():
    current = State(elements={"a": 1}, version=1)
    proposed = current.with_elements({"a": 2})  # actual content change
    candidate = Candidate(
        parent_state_id=current.state_id, proposed_state=proposed, origin="test"
    )
    assert check_meaningful_change(current, candidate).ok


def test_relation_only_change_is_accepted():
    current = State(elements={"a": 1, "b": 2}, version=1)
    proposed = current.with_relations([Relation(source="a", target="b", relation_type="x")])
    candidate = Candidate(
        parent_state_id=current.state_id, proposed_state=proposed, origin="test"
    )
    assert check_meaningful_change(current, candidate).ok


def test_dict_key_insertion_order_does_not_create_false_evolution():
    """Same canonical content, different insertion order -> same content_id,
    so a version-bump-only candidate built from the reordered dict is still
    correctly rejected as a no-op."""
    current = State(elements={"a": 1, "b": 2}, version=1)
    reordered_same_content = State(elements={"b": 2, "a": 1}, version=2)
    candidate = Candidate(
        parent_state_id=current.state_id,
        proposed_state=reordered_same_content,
        origin="test",
    )
    assert current.content_id == reordered_same_content.content_id
    assert not check_meaningful_change(current, candidate).ok


def test_relation_ordering_does_not_create_false_evolution():
    r1 = Relation(source="a", target="b", relation_type="x")
    r2 = Relation(source="b", target="a", relation_type="y")
    current = State(elements={"a": 1, "b": 2}, relations=(r1, r2), version=1)
    reordered = State(elements={"a": 1, "b": 2}, relations=(r2, r1), version=2)
    assert current.content_id == reordered.content_id


def test_content_id_excludes_version_but_state_id_does_not():
    s_v1 = State(elements={"a": 1}, version=1)
    s_v2 = State(elements={"a": 1}, version=2)
    assert s_v1.content_id == s_v2.content_id
    assert s_v1.state_id != s_v2.state_id
