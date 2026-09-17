from gnosis.reflection.authority import request_authorization
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
