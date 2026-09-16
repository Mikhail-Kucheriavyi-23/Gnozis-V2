"""
PATCH defect #5 regression tests — Select stage.

Before the PATCH, `Engine` had no path that accepted more than one
Candidate at once — Select did not exist in runtime, only in documentation.
`gnosis.core.select.select` and `Engine.step_select` close that gap.
"""

from gnosis.core import Candidate, Engine, State, select


def make_current():
    return State(elements={"a": 1}, version=0)


def make_candidate(current: State, key: str, value) -> Candidate:
    proposed = current.with_elements({key: value})
    return Candidate(parent_state_id=current.state_id, proposed_state=proposed, origin="test")


def test_select_with_multiple_passing_candidates_picks_exactly_one_deterministically():
    current = make_current()
    c1 = make_candidate(current, "b", 1)
    c2 = make_candidate(current, "c", 2)
    c3 = make_candidate(current, "d", 3)

    result = select(current, [c1, c2, c3])
    assert result.selected is not None
    assert result.selected in (c1, c2, c3)

    # Determinism: same set, different input order -> same selection.
    result_reordered = select(current, [c3, c1, c2])
    assert result_reordered.selected.candidate_id == result.selected.candidate_id


def test_select_removes_failed_candidates():
    current = make_current()
    good = make_candidate(current, "b", 1)
    # Content-identical to current except version bump -> fails meaningful_change
    bad = Candidate(
        parent_state_id=current.state_id,
        proposed_state=State(elements=dict(current.elements), version=current.version + 1),
        origin="bad",
    )

    result = select(current, [good, bad])
    assert result.selected.candidate_id == good.candidate_id
    assert bad in result.rejected
    assert good not in result.rejected


def test_select_returns_none_when_all_candidates_fail():
    current = make_current()
    bad1 = Candidate(
        parent_state_id=current.state_id,
        proposed_state=State(elements=dict(current.elements), version=current.version + 1),
        origin="bad1",
    )
    bad2 = Candidate(
        parent_state_id="wrong-parent",
        proposed_state=current.with_elements({"x": 1}),
        origin="bad2",
    )
    result = select(current, [bad1, bad2])
    assert result.selected is None
    assert set(c.candidate_id for c in result.rejected) == {bad1.candidate_id, bad2.candidate_id}


def test_select_with_empty_candidate_list_returns_none():
    current = make_current()
    result = select(current, [])
    assert result.selected is None
    assert result.evaluated == ()


def test_select_has_no_global_mutable_state_between_calls():
    """Two independent select() calls on unrelated states/candidates must
    not interfere with each other — pure function, no shared selector."""
    current_a = State(elements={"a": 1})
    current_b = State(elements={"z": 9})
    cand_a = make_candidate(current_a, "b", 1)
    cand_b = make_candidate(current_b, "y", 1)

    result_a = select(current_a, [cand_a])
    result_b = select(current_b, [cand_b])

    assert result_a.selected.candidate_id == cand_a.candidate_id
    assert result_b.selected.candidate_id == cand_b.candidate_id


def test_engine_step_select_commits_the_selected_candidate():
    engine = Engine(state=make_current())
    c1 = make_candidate(engine.state, "b", 1)
    c2 = make_candidate(engine.state, "c", 2)

    record = engine.step_select([c1, c2])
    assert record.accepted
    assert engine.state.state_id in (c1.proposed_state.state_id, c2.proposed_state.state_id)
    assert engine.budget.spent == 1  # one round, one charge


def test_engine_step_select_leaves_state_untouched_when_nothing_passes():
    engine = Engine(state=make_current())
    before_id = engine.state.state_id
    noop_candidate = Candidate(
        parent_state_id=engine.state.state_id,
        proposed_state=State(elements=dict(engine.state.elements), version=engine.state.version + 1),
        origin="attacker",
    )
    record = engine.step_select([noop_candidate])
    assert not record.accepted
    assert engine.state.state_id == before_id


def test_full_vertical_slice_generate_test_select_evolve():
    """Psi0 -> Generate(multiple) -> Test -> Select -> Evolve -> Psi1,
    exercised end to end through the Engine."""
    engine = Engine(state=make_current())
    psi0_id = engine.state.state_id

    candidates = [make_candidate(engine.state, f"k{i}", i) for i in range(5)]
    record = engine.step_select(candidates)

    assert record.accepted
    assert record.from_state_id == psi0_id
    assert engine.state.state_id == record.to_state_id
    assert engine.state.state_id != psi0_id
