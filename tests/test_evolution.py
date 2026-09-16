import pytest

from gnosis.core import Budget, Candidate, Engine, State, StopCondition, StopReason


def initial_state():
    return State(elements={"a": 1}, version=0)


def test_valid_step_commits_new_state():
    engine = Engine(state=initial_state())
    proposed = engine.state.with_elements({"b": 2})
    candidate = Candidate(
        parent_state_id=engine.state.state_id, proposed_state=proposed, origin="test"
    )
    record = engine.step(candidate)
    assert record.accepted
    assert engine.state.state_id == proposed.state_id
    assert engine.budget.spent == 1


def test_rejected_candidate_never_mutates_core_state():
    """SECURITY TEST (spec 42): an invalid candidate must NOT change state,
    even partially. This is the structural proof that there is no
    Candidate -> direct Core mutation path."""
    engine = Engine(state=initial_state())
    before_id = engine.state.state_id

    # proposed_state has a dangling relation -> fails transition_validity
    from gnosis.core import Relation

    bad_proposed = State(
        elements={"a": 1},
        relations=(Relation(source="a", target="ghost", relation_type="x"),),
        version=1,
    )
    candidate = Candidate(
        parent_state_id=engine.state.state_id, proposed_state=bad_proposed, origin="attacker"
    )
    record = engine.step(candidate)

    assert not record.accepted
    assert engine.state.state_id == before_id  # unchanged
    assert engine.state is not bad_proposed


def test_candidate_from_stale_parent_is_rejected():
    engine = Engine(state=initial_state())
    stale_parent = "not-the-real-state-id"
    proposed = engine.state.with_elements({"b": 2})
    candidate = Candidate(parent_state_id=stale_parent, proposed_state=proposed, origin="test")
    with pytest.raises(StopCondition) as excinfo:
        engine.step(candidate)
    assert excinfo.value.reason == StopReason.INVALID_STATE


def test_budget_exhaustion_is_a_hard_stop():
    engine = Engine(state=initial_state(), budget=Budget(total=1))
    proposed = engine.state.with_elements({"b": 2})
    candidate = Candidate(
        parent_state_id=engine.state.state_id, proposed_state=proposed, origin="test"
    )
    engine.step(candidate)  # spends the only budget unit
    assert engine.budget.exhausted()

    proposed2 = engine.state.with_elements({"c": 3})
    candidate2 = Candidate(
        parent_state_id=engine.state.state_id, proposed_state=proposed2, origin="test"
    )
    with pytest.raises(StopCondition) as excinfo:
        engine.step(candidate2)
    assert excinfo.value.reason == StopReason.BUDGET_EXHAUSTED


def test_run_stops_when_budget_exhausted_without_exception_from_generator():
    engine = Engine(state=initial_state(), budget=Budget(total=3))

    def generate(state: State) -> Candidate:
        proposed = state.with_elements({f"k{state.version}": state.version})
        return Candidate(parent_state_id=state.state_id, proposed_state=proposed, origin="gen")

    records = engine.run(generate)
    assert len(records) == 3
    assert all(r.accepted for r in records)
    assert engine.budget.exhausted()
