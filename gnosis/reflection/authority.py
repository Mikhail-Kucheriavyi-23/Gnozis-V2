"""Non-authoritative boundary for proposed Core evolution.

This module deliberately stops before activation. Governance can create a
request describing what would need explicit owner authorization, but the
request itself carries no execution capability and cannot mutate Core.
"""

from __future__ import annotations

from dataclasses import dataclass

from .governance import GovernanceDecision


@dataclass(frozen=True)
class AuthorityRequest:
    """A request for explicit authorization, not an authorization token."""

    decision: str
    rationale: tuple[str, ...]
    provenance: str = "reflection-authority-boundary"
    requires_owner_approval: bool = True

    @property
    def authorized(self) -> bool:
        """The request itself never grants authority."""
        return False

    @property
    def can_activate(self) -> bool:
        """No activation capability crosses this boundary."""
        return False

    @property
    def can_rollback(self) -> bool:
        """No rollback capability crosses this boundary."""
        return False


def request_authorization(decision: GovernanceDecision) -> AuthorityRequest:
    """Translate a governance classification into an explicit approval request."""
    return AuthorityRequest(
        decision=decision.decision,
        rationale=decision.rationale,
    )


@dataclass(frozen=True)
class ExecutionAuthorization:
    """Authorization bound to one exact evolution provenance."""
    request_provenance: str
    owner_approved: bool = False
    evolution_identity: str = ""

    @property
    def can_execute(self) -> bool:
        return (
            self.owner_approved
            and bool(self.request_provenance)
            and bool(self.evolution_identity)
        )


def require_execution_authorization(
    auth: ExecutionAuthorization | None,
    *,
    request_provenance: str,
    evolution_identity: str,
) -> None:
    """Fail closed unless authorization exactly matches the requested evolution."""
    if (
        auth is None
        or not auth.can_execute
        or auth.request_provenance != request_provenance
        or auth.evolution_identity != evolution_identity
    ):
        raise PermissionError("execution authorization does not match evolution")


@dataclass(frozen=True)
class ExecutionIntentSnapshot:
    """Immutable identity snapshot of the exact evolution authorized for execution."""
    provenance_id: str
    execution_id: str
    parent_state_id: str
    parent_state_digest: str
    evolution_identity: str
    candidate_binding_digest: str
    proposed_state_content_id: str

    @classmethod
    def from_provenance(cls, provenance: object) -> "ExecutionIntentSnapshot":
        return cls(
            provenance_id=str(provenance.provenance_id),
            execution_id=str(provenance.execution_id),
            parent_state_id=str(provenance.parent_state_id),
            parent_state_digest=str(provenance.parent_state_digest),
            evolution_identity=str(provenance.evolution_identity),
            candidate_binding_digest=str(provenance.candidate_binding_digest),
            proposed_state_content_id=str(provenance.proposed_state_content_id),
        )

    def matches_provenance(self, provenance: object) -> bool:
        return self == type(self).from_provenance(provenance)


def require_execution_intent_snapshot(
    snapshot: ExecutionIntentSnapshot | None,
    provenance: object,
) -> None:
    """Fail closed unless the immutable snapshot exactly matches current provenance."""
    if snapshot is None or not snapshot.matches_provenance(provenance):
        raise PermissionError("execution intent snapshot does not match evolution")


@dataclass(frozen=True)
class ExecutionCommitRequest:
    """All pre-commit identity material required for one authorized execution."""
    authorization: ExecutionAuthorization
    intent_snapshot: ExecutionIntentSnapshot
    request_provenance: str
    evolution_identity: str
    provenance: object


def require_execution_commit(request: ExecutionCommitRequest) -> None:
    """Fail closed unless authorization, identity and freshness all agree."""
    require_execution_authorization(
        request.authorization,
        request_provenance=request.request_provenance,
        evolution_identity=request.evolution_identity,
    )
    if request.authorization.evolution_identity != request.intent_snapshot.evolution_identity:
        raise PermissionError("execution commit identity mismatch")
    require_execution_intent_snapshot(request.intent_snapshot, request.provenance)
