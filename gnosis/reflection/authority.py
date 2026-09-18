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
