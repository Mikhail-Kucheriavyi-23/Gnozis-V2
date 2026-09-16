from gnosis.core import (
    Candidate,
    Relation,
    State,
    all_pass,
    run_invariants,
)


def make_current():
    return State(elements={"a": 1}, version=0)


def test_valid_candidate_passes_all_invariants():
    current = make_current()
    proposed = current.with_elements({"b": 2})
    candidate = Candidate(
        parent_state_id=current.state_id, proposed_state=proposed, origin="test"
    )
    results = run_invariants(current, candidate)
    assert all_pass(results)


def test_candidate_with_wrong_parent_fails_state_integrity():
    current = make_current()
    other = State(elements={"z": 9}, version=0)
    proposed = other.with_elements({"b": 2})
    candidate = Candidate(
        parent_state_id=other.state_id,  # does not match `current`
        proposed_state=proposed,
        origin="test",
    )
    results = run_invariants(current, candidate)
    assert not all_pass(results)
    names = {r.name for r in results if not r.ok}
    assert "state_integrity" in names


def test_candidate_with_dangling_relation_fails_transition_validity():
    current = make_current()
    proposed_state = State(
        elements={"a": 1},
        relations=(Relation(source="a", target="does_not_exist", relation_type="x"),),
        version=1,
    )
    candidate = Candidate(
        parent_state_id=current.state_id, proposed_state=proposed_state, origin="test"
    )
    results = run_invariants(current, candidate)
    assert not all_pass(results)
    names = {r.name for r in results if not r.ok}
    assert "transition_validity" in names


def test_candidate_with_non_increasing_version_fails():
    current = make_current()
    proposed_state = State(elements={"a": 1, "b": 2}, version=0)  # same version
    candidate = Candidate(
        parent_state_id=current.state_id, proposed_state=proposed_state, origin="test"
    )
    results = run_invariants(current, candidate)
    assert not all_pass(results)
    names = {r.name for r in results if not r.ok}
    assert "monotonic_version" in names
