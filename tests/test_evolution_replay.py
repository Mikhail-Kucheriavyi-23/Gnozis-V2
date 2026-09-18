from gnosis.core import Candidate, State
from gnosis.evolution.replay import replay_complete, replay_evidence, replay_identity
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


def test_complete_replay_fails_closed_when_provenance_or_audit_is_missing():
    state = State(elements={"a": 1})
    result = run_sandbox(state, _candidate(state), _observer)
    missing_provenance = replay_complete(
        result.execution, None, None, observations=result.execution.observations
    )
    assert not missing_provenance.reproducible
    assert "provenance missing" in missing_provenance.reasons

    missing_audit = replay_complete(
        result.execution, None, None, observations=result.execution.observations
    )
    assert not missing_audit.reproducible
    assert "audit record missing" in missing_audit.reasons


def test_complete_replay_rejects_audit_identity_mismatch():
    state = State(elements={"a": 1})
    result = run_sandbox(state, _candidate(state), _observer)

    class Audit:
        candidate_id = "wrong"
        execution_id = result.execution.candidate_id

    replay = replay_complete(
        result.execution, None, Audit(), observations=result.execution.observations
    )
    assert not replay.reproducible
    assert "provenance missing" in replay.reasons
    assert "audit candidate mismatch" in replay.reasons


def test_complete_replay_rejects_audit_provenance_and_digest_mismatch():
    state = State(elements={"a": 1})
    result = run_sandbox(state, _candidate(state), _observer)

    class Audit:
        candidate_id = result.execution.candidate_id
        execution_id = result.execution.candidate_id
        provenance_id = "wrong-provenance"
        parent_state_digest = "wrong-parent"
        proposed_state_digest = result.execution.proposed_state_digest
        evidence_digest = "wrong-evidence"

    replay = replay_complete(
        result.execution, None, Audit(), observations=result.execution.observations
    )
    assert not replay.reproducible
    assert "audit provenance mismatch" in replay.reasons
    assert "audit parent_state_digest mismatch" in replay.reasons
    assert "audit evidence_digest mismatch" in replay.reasons
