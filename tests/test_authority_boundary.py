import pytest
from gnosis.reflection.authority import ExecutionAuthorization, request_authorization, require_execution_authorization
from gnosis.reflection.governance import GovernanceDecision


def test_authority_request_requires_owner_and_grants_no_capability() -> None:
    decision = GovernanceDecision(
        decision="REVIEW",
        shadow_status="BEHAVIOR_CHANGED",
        invariant_status="PRESERVED",
        rationale=("behavior_changed",),
    )

    request = request_authorization(decision)

    assert request.requires_owner_approval is True
    assert request.authorized is False
    assert request.can_activate is False
    assert request.can_rollback is False
    assert request.decision == "REVIEW"
    assert request.rationale == ("behavior_changed",)


def test_execution_authorization_fails_closed_without_explicit_owner_approval():
    with pytest.raises(PermissionError, match="execution authorization required"):
        require_execution_authorization(None, request_provenance="p", evolution_identity="e")
    auth = ExecutionAuthorization(request_provenance="p", owner_approved=False)
    with pytest.raises(PermissionError, match="execution authorization required"):
        require_execution_authorization(auth, request_provenance="p", evolution_identity="e")


def test_execution_authorization_requires_nonempty_provenance():
    auth = ExecutionAuthorization(request_provenance="", owner_approved=True)
    with pytest.raises(PermissionError, match="execution authorization required"):
        require_execution_authorization(auth)


def test_execution_authorization_must_match_exact_evolution():
    auth = ExecutionAuthorization(request_provenance="p", evolution_identity="e", owner_approved=True)
    require_execution_authorization(auth, request_provenance="p", evolution_identity="e")
    with pytest.raises(PermissionError, match="does not match evolution"):
        require_execution_authorization(auth, request_provenance="other", evolution_identity="e")
    with pytest.raises(PermissionError, match="does not match evolution"):
        require_execution_authorization(auth, request_provenance="p", evolution_identity="other")
