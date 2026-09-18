from gnosis.core import Candidate, State
from gnosis.evolution.replay import replay_evidence, replay_identity
from gnosis.evolution.sandbox import run_sandbox


def _candidate(state):
    return Candidate(
        parent_state_id=state.state_id,
        proposed_state=state.with_elements({"b": 2}),
        origin="replay-test",
    )


def _observer(_state, _candidate):
    return {"metric": 3, "status": "stable"}


def test_replay_reproduces_completed_evidence():
    state = State(elements={"a": 1})
    result = run_sandbox(state, _candidate(state), _observer)
    replay = replay_evidence(result.execution, result.execution.observations)
    assert replay.reproducible
    assert replay.expected_digest == replay.actual_digest


def test_replay_rejects_changed_observations():
    state = State(elements={"a": 1})
    result = run_sandbox(state, _candidate(state), _observer)
    replay = replay_evidence(
        result.execution,
        {"metric": 999, "status": "stable"},
    )
    assert not replay.reproducible
    assert "evidence digest mismatch" in replay.reasons


def test_replay_identity_rejects_wrong_candidate_or_parent():
    state = State(elements={"a": 1})
    result = run_sandbox(state, _candidate(state), _observer)
    assert not replay_identity(
        result.execution,
        candidate_id="tampered",
        parent_state_id=state.state_id,
        parent_state_digest=result.execution.parent_state_digest,
        proposed_state_digest=result.execution.proposed_state_digest,
    ).reproducible
    assert not replay_identity(
        result.execution,
        candidate_id=result.execution.candidate_id,
        parent_state_id="stale",
        parent_state_digest=result.execution.parent_state_digest,
        proposed_state_digest=result.execution.proposed_state_digest,
    ).reproducible
