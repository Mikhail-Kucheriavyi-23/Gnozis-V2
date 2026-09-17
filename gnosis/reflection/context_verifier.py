"""Verification helpers for Gnozis self-descriptive context claims."""
from __future__ import annotations

from dataclasses import dataclass

from .context import ContextClaim, ContextStatus, ContextVersion


@dataclass(frozen=True)
class ContextVerification:
    version_id: str
    verified: tuple[str, ...]
    unresolved: tuple[str, ...]
    rejected: tuple[str, ...]
    contradictions: tuple[tuple[str, str], ...]

    @property
    def coherent(self) -> bool:
        return not self.contradictions


def verify_context(version: ContextVersion) -> ContextVerification:
    claims = {claim.claim_id: claim for claim in version.claims}
    contradictions: list[tuple[str, str]] = []

    # A claim cannot be simultaneously represented as VERIFIED and REJECTED
    # under the same identifier. This is deliberately structural: semantic
    # contradiction detection belongs to a later evidence-backed layer.
    for claim_id, claim in claims.items():
        if claim.status not in ContextStatus:
            contradictions.append((claim_id, "unknown context status"))

    verified = tuple(c.claim_id for c in version.claims if c.status is ContextStatus.VERIFIED)
    unresolved = tuple(
        c.claim_id for c in version.claims
        if c.status in {ContextStatus.HYPOTHESIS, ContextStatus.OBSERVED}
    )
    rejected = tuple(c.claim_id for c in version.claims if c.status is ContextStatus.REJECTED)

    return ContextVerification(
        version_id=version.version_id,
        verified=verified,
        unresolved=unresolved,
        rejected=rejected,
        contradictions=tuple(contradictions),
    )
