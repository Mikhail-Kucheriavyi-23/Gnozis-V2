"""Self-descriptive context as a verifiable reflection object.

AI_CONTEXT is treated as a claim surface, not as an authority source.
Claims can be observed, verified, rejected, or remain hypotheses. Provenance
is explicit so Gnozis can inspect and evolve its own self-description.
"""
from __future__ import annotations

from dataclasses import dataclass
from enum import Enum


class ContextStatus(str, Enum):
    HYPOTHESIS = "HYPOTHESIS"
    OBSERVED = "OBSERVED"
    VERIFIED = "VERIFIED"
    REJECTED = "REJECTED"


@dataclass(frozen=True)
class ContextClaim:
    claim_id: str
    statement: str
    status: ContextStatus
    provenance: tuple[str, ...] = ()
    evidence_refs: tuple[str, ...] = ()

    @property
    def self_descriptive(self) -> bool:
        return bool(self.claim_id and self.statement and self.provenance)


@dataclass(frozen=True)
class ContextDelta:
    previous_version: str
    current_version: str
    added: tuple[str, ...] = ()
    removed: tuple[str, ...] = ()
    changed: tuple[str, ...] = ()

    @property
    def meaningful(self) -> bool:
        return bool(self.added or self.removed or self.changed)


@dataclass(frozen=True)
class ContextVersion:
    version_id: str
    claims: tuple[ContextClaim, ...]
    parent_version: str | None = None
    delta: ContextDelta | None = None

    def verified_claims(self) -> tuple[ContextClaim, ...]:
        return tuple(c for c in self.claims if c.status is ContextStatus.VERIFIED)

    def unresolved_claims(self) -> tuple[ContextClaim, ...]:
        return tuple(
            c for c in self.claims
            if c.status in {ContextStatus.HYPOTHESIS, ContextStatus.OBSERVED}
        )
