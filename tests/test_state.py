from gnosis.core import Relation, State


def test_state_top_level_reassignment_blocked():
    """Renamed from the misleading `test_state_is_immutable_container`
    (audit finding: that name implied deep immutability but the test only
    checked attribute reassignment). This test covers ONLY reassignment;
    real deep-mutation coverage is in test_immutability_adversarial.py."""
    s = State(elements={"a": 1})
    try:
        s.elements = {"a": 2}  # type: ignore[misc]
        assert False, "State should be immutable"
    except AttributeError:
        pass


def test_with_elements_creates_new_state_and_bumps_version():
    s0 = State(elements={"a": 1}, version=0)
    s1 = s0.with_elements({"b": 2})
    assert s0.elements == {"a": 1}  # original untouched
    assert s1.elements == {"a": 1, "b": 2}
    assert s1.version == s0.version + 1
    assert s0.state_id != s1.state_id


def test_state_id_is_deterministic_for_same_content():
    s1 = State(elements={"a": 1}, version=0)
    s2 = State(elements={"a": 1}, version=0)
    assert s1.state_id == s2.state_id


def test_with_relations_appends_and_bumps_version():
    s0 = State(elements={"a": 1, "b": 2})
    rel = Relation(source="a", target="b", relation_type="linked")
    s1 = s0.with_relations([rel])
    assert rel in s1.relations
    assert s1.version == s0.version + 1


def test_relation_id_stable_for_identical_content():
    r1 = Relation(source="a", target="b", relation_type="x", value=1)
    r2 = Relation(source="a", target="b", relation_type="x", value=1)
    assert r1.relation_id == r2.relation_id
