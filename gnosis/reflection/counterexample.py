"""Deterministic counterexample evaluation for reflection findings.

The counterexample layer is deliberately evidence-based and non-mutating. It
can challenge a repeated-rejection finding using the canonical transition
history, but it cannot alter Core state or activate a proposal.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Sequence

from gnosis.core.types import TransitionRecord

from .analyzer import CounterexampleCandidate, Finding


@dataclass(frozen=True)
class CounterexampleResult:
    candidate_id: str
    status: str
    evidence_refs: tuple[str, ...]
    explanation: str


class CounterexampleEngine:
    """Challenge reflection findings using only canonical historical evidence.

    The first executable challenge is intentionally conservative. For a
    repeated-rejection finding it searches for an accepted transition whose
    candidate identifier is the same. Such evidence can refute the simplistic
    hypothesis that the candidate class is unconditionally rejected.

    Absence of such evidence is INCONCLUSIVE, never proof that the finding is
    true. More powerful replay/boundary/mutation challenges belong to later
    reflection phases.
    """

    def __init__(self, transitions: Sequence[TransitionRecord]):
        self._transitions = tuple(transitions)

    def challenge(
        self,
        finding: Finding,
        candidate: CounterexampleCandidate,
    ) -> CounterexampleResult:
        related_ids = set(finding.observation_ids)
        rejected_candidate_ids = {
            record.candidate_id
            for record in self._transitions
            if f"observation:{self._transitions.index(record)}:reason" in related_ids
        }

        accepted = tuple(
            record
            for record in self._transitions
            if record.accepted and record.candidate_id in rejected_candidate_ids
        )

        if accepted:
            refs = tuple(
                f"transition:{self._transitions.index(record)}:{record.candidate_id}"
                for record in accepted
            )
            return CounterexampleResult(
                candidate_id=candidate.candidate_id,
                status="REFUTED",
                evidence_refs=refs,
                explanation="Historical evidence contains an accepted transition with a candidate identifier associated with the finding.",
            )

        return CounterexampleResult(
            candidate_id=candidate.candidate_id,
            status="INCONCLUSIVE",
            evidence_refs=tuple(finding.evidence_refs),
            explanation="No historical accepted transition was found that satisfies this conservative counterexample criterion; the finding is not proven.",
        )
