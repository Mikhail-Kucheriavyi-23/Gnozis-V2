from gnosis.core import Candidate, Engine, State


def test_custom_test_cannot_bypass_meaningful_change_invariant():
    current = State(elements={"a": 1}, version=0)
    proposed = State(elements={"a": 1}, version=1)
    candidate = Candidate(
        parent_state_id=current.state_id,
        proposed_state=proposed,
        origin="adversarial",
    )

    # Deliberately permissive: the custom predicate must not disable Core invariants.
    engine = Engine(state=current, test_fn=lambda _state, _candidate: True)
    record = engine.step(candidate)

    assert not record.accepted
    assert engine.state.state_id == current.state_id
    assert any("meaningful_change" in reason for reason in record.test_result.reasons)
