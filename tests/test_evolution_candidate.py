from gnosis.core import Candidate, State


def test_candidate_id_binds_parent_proposed_content_origin_and_seed():
    parent = State(elements={"a": 1})
    proposed = parent.with_elements({"b": 2})
    base = Candidate(
        parent_state_id=parent.state_id,
        proposed_state=proposed,
        origin="generator-a",
        seed=7,
    )
    assert base.candidate_id == Candidate(
        parent_state_id=parent.state_id,
        proposed_state=proposed,
        origin="generator-a",
        seed=7,
    ).candidate_id

    assert base.candidate_id != Candidate(
        parent_state_id=parent.state_id,
        proposed_state=proposed,
        origin="generator-b",
        seed=7,
    ).candidate_id
    assert base.candidate_id != Candidate(
        parent_state_id=parent.state_id,
        proposed_state=proposed,
        origin="generator-a",
        seed=8,
    ).candidate_id
    assert base.candidate_id != Candidate(
        parent_state_id=parent.state_id,
        proposed_state=parent.with_elements({"c": 3}),
        origin="generator-a",
        seed=7,
    ).candidate_id


def test_candidate_binding_digest_binds_parent_state_content_digest():
    parent = State(elements={"a": 1})
    candidate = Candidate(
        parent_state_id=parent.state_id,
        proposed_state=parent.with_elements({"b": 2}),
        origin="generator-a",
        seed=7,
    )
    digest = candidate.binding_digest(parent.content_id)
    assert digest
    assert digest != candidate.binding_digest("wrong-parent-digest")
