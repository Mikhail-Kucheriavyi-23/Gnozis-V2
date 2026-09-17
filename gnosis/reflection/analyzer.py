"""Deterministic reflection over canonical Core transition history.

This module is intentionally outside ``gnosis.core``. It can inspect Core
history and produce evidence-linked findings and rule proposals, but it has
no API for changing State, rules, invariants, or persistence authority.

A proposal is a hypothesis, not a patch and not an activation command.
"""

from __future__ import annotations

from collections import Counter
from dataclasses import dataclass, field
from typing import Iterable, Sequence

from gnosis.core.types import TransitionRecord


@dataclass(frozen=True)
class ReflectionObservation:
    """One observed fact derived from canonical Core evidence."""

    observation_id: str
    transition_id: str
    kind: str
    value: str
    evidence_ref: str


@dataclass(frozen=True)
class Finding:
    """A repeatable pattern that may justify a rule investigation."""

    finding_id: str
    claim: str
    observation_ids: tuple[str, ...]
    evidence_refs: tuple[str, ...]
    reproducibility: int
    falsification_condition: str


@dataclass(frozen=True)
class CounterexampleCandidate:
    """Explicit description of how a Finding should be challenged."""

    candidate_id: str
    finding_id: str
    method: str
    success_condition: str


@dataclass(frozen=True)
class RuleProposal:
    """Non-activating proposal for a possible rule improvement."""

    proposal_id: str
    finding_id: str
    target: str
    hypothesis: str
    evidence_refs: tuple[str, ...]
    expected_effect: str
    regression_risk: str
    required_test: str
    status: str = "PROPOSED"


@dataclass(frozen=True)
class ReflectionReport:
    """Complete read-only result of one reflection pass."""

    observations: tuple[ReflectionObservation, ...] = field(default_factory=tuple)
    findings: tuple[Finding, ...] = field(default_factory=tuple)
    counterexamples: tuple[CounterexampleCandidate, ...] = field(default_factory=tuple)
    proposals: tuple[RuleProposal, ...] = field(default_factory=tuple)


class ReflectionAnalyzer:
    """Analyze Core history without changing it.

    The first foundation pass deliberately uses only evidence already exposed
    by ``TransitionRecord``. It does not invent rule identifiers or claim
    causality that the current Core history cannot establish.
    """

    def __init__(self, transitions: Sequence[TransitionRecord]):
        self._transitions = tuple(transitions)

    @classmethod
    def from_engine(cls, engine: object) -> "ReflectionAnalyzer":
        """Build an analyzer from an Engine-like object exposing ``history``."""
        history = getattr(engine, "history", None)
        if history is None:
            raise TypeError("engine must expose canonical Core history")
        return cls(history)

    def observe(self) -> tuple[ReflectionObservation, ...]:
        observations: list[ReflectionObservation] = []
        for index, transition in enumerate(self._transitions):
            transition_id = f"transition:{index}:{transition.candidate_id}"
            observations.append(
                ReflectionObservation(
                    observation_id=f"observation:{index}:outcome",
                    transition_id=transition_id,
                    kind="transition_outcome",
                    value="accepted" if transition.accepted else "rejected",
                    evidence_ref=transition_id,
                )
            )
            if not transition.accepted:
                reason = transition.reason or "unspecified rejection"
                observations.append(
                    ReflectionObservation(
                        observation_id=f"observation:{index}:reason",
                        transition_id=transition_id,
                        kind="rejection_reason",
                        value=reason,
                        evidence_ref=transition_id,
                    )
                )
        return tuple(observations)

    def analyze(self, minimum_repetitions: int = 2) -> ReflectionReport:
        if minimum_repetitions < 2:
            raise ValueError("minimum_repetitions must be >= 2")

        observations = self.observe()
        reason_observations = [o for o in observations if o.kind == "rejection_reason"]
        counts = Counter(o.value for o in reason_observations)

        findings: list[Finding] = []
        counterexamples: list[CounterexampleCandidate] = []
        proposals: list[RuleProposal] = []

        for reason, count in sorted(counts.items()):
            if count < minimum_repetitions:
                continue

            related = tuple(o for o in reason_observations if o.value == reason)
            finding_id = f"finding:repeated-rejection:{abs(hash(reason))}"
            observation_ids = tuple(o.observation_id for o in related)
            evidence_refs = tuple(o.evidence_ref for o in related)

            finding = Finding(
                finding_id=finding_id,
                claim=f"The same rejection reason recurs {count} times in the observed Core history: {reason}",
                observation_ids=observation_ids,
                evidence_refs=evidence_refs,
                reproducibility=count,
                falsification_condition="A sufficiently comparable replay must show that the rejection does not recur under the same stated conditions.",
            )
            findings.append(finding)

            counterexample_id = f"counterexample:{finding_id}"
            counterexamples.append(
                CounterexampleCandidate(
                    candidate_id=counterexample_id,
                    finding_id=finding_id,
                    method="historical_replay_or_boundary_case",
                    success_condition="Produce a comparable case where the suspected repeated rejection condition is absent or produces the expected alternative outcome.",
                )
            )

            proposals.append(
                RuleProposal(
                    proposal_id=f"proposal:{finding_id}",
                    finding_id=finding_id,
                    target="rule_or_test_policy_associated_with_rejection_reason",
                    hypothesis=f"Investigate whether the rule/test policy producing '{reason}' is overly restrictive, underspecified, or correctly rejecting a recurring invalid class.",
                    evidence_refs=evidence_refs,
                    expected_effect="Either demonstrate that the current behavior is justified or identify a narrowly testable rule change.",
                    regression_risk="Changing acceptance criteria may admit invalid transitions; every candidate change must be replayed against existing accepted and rejected evidence.",
                    required_test="Run historical replay plus boundary and adversarial cases before any governance decision.",
                )
            )

        return ReflectionReport(
            observations=observations,
            findings=tuple(findings),
            counterexamples=tuple(counterexamples),
            proposals=tuple(proposals),
        )
