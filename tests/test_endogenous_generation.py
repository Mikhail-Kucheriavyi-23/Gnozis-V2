from gnosis.core.types import State
from gnosis.reflection.analyzer import ReflectionReport, RuleProposal
from gnosis.reflection.endogenous import MAX_ENDOGENOUS_CANDIDATES, generate_endogenous_candidates


def proposal(i):
    return RuleProposal(
        proposal_id=f"proposal:{i}", finding_id=f"finding:{i}", target="rule:v1",
        hypothesis="test hypothesis", evidence_refs=(f"evidence:{i}",),
        expected_effect="test", regression_risk="test", required_test="test",
    )


def test_endogenous_generation_is_bounded_and_does_not_mutate_engine_state():
    state = State(elements={"a": 1})
    report = ReflectionReport(proposals=tuple(proposal(i) for i in range(25)))
    result = generate_endogenous_candidates(state, report)
    assert result.bounded
    assert len(result.candidates) == MAX_ENDOGENOUS_CANDIDATES
    assert state.relations == ()
    assert all(c.parent_state_id == state.state_id for c in result.candidates)
    assert all(c.origin == "reflection:endogenous" for c in result.candidates)
    assert all("__gnozis_reflection__" in c.proposed_state.elements for c in result.candidates)


def test_endogenous_generation_is_deterministic_for_same_evidence():
    state = State(elements={"a": 1})
    report = ReflectionReport(proposals=(proposal(1),))
    first = generate_endogenous_candidates(state, report).candidates[0]
    second = generate_endogenous_candidates(state, report).candidates[0]
    assert first.candidate_id == second.candidate_id
    assert first.proposed_state.content_id == second.proposed_state.content_id


def test_endogenous_generation_respects_remaining_budget():
    from gnosis.core.budget import Budget
    state = State(elements={"a": 1})
    report = ReflectionReport(proposals=tuple(proposal(i) for i in range(10)))
    budget = Budget(total=3, spent=1)
    result = generate_endogenous_candidates(state, report, budget=budget)
    assert len(result.candidates) == 2


def test_endogenous_generation_stops_when_budget_exhausted():
    from gnosis.core.budget import Budget
    state = State(elements={"a": 1})
    report = ReflectionReport(proposals=(proposal(1),))
    result = generate_endogenous_candidates(state, report, budget=Budget(total=1, spent=1))
    assert result.candidates == ()


def test_generated_candidates_use_normal_core_test_and_select_path():
    from gnosis.core import Budget, Engine, select
    state = State(elements={"a": 1})
    report = ReflectionReport(proposals=tuple(proposal(i) for i in range(3)))
    generation = generate_endogenous_candidates(state, report, budget=Budget(total=3))
    engine = Engine(state=state, budget=Budget(total=3))
    selection = select(state, generation.candidates, engine.test_fn)
    assert selection.selected is not None
    record = engine.step_select(generation.candidates)
    assert record.accepted
    assert record.candidate_id == selection.selected.candidate_id
    assert engine.state.state_id == selection.selected.proposed_state.state_id
