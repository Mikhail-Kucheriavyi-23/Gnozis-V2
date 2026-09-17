from gnosis.core import Candidate, Engine, State


def make_noop_candidate(current: State) -> Candidate:
    proposed = State(elements={"a": 1}, version=current.version + 1)
    return Candidate(
        parent_state_id=current.state_id,
        proposed_state=proposed,
        origin="adversarial",
    )


def test_custom_test_cannot_bypass_meaningful_change_invariant():
    current = State(elements={"a": 1}, version=0)
    candidate = make_noop_candidate(current)

    # Deliberately permissive: the custom predicate must not disable Core invariants.
    engine = Engine(state=current, test_fn=lambda _state, _candidate: True)
    record = engine.step(candidate)

    assert not record.accepted
    assert engine.state.state_id == current.state_id
    assert any("meaningful_change" in reason for reason in record.test_result.reasons)


def test_step_select_cannot_bypass_meaningful_change_invariant():
    current = State(elements={"a": 1}, version=0)
    candidate = make_noop_candidate(current)

    # Select path must use the same protected invariant gate as single-candidate step.
    engine = Engine(state=current, test_fn=lambda _state, _candidate: True)
    record = engine.step_select([candidate])

    assert not record.accepted
    assert engine.state.state_id == current.state_id
    assert "meaningful_change" in record.reason
