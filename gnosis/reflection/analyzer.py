"""Deterministic reflection over canonical Core transition history.

This module is intentionally outside ``gnosis.core``. It can inspect Core
history and produce evidence-linked findings and rule proposals, but it has
no API for changing State, rules, invariants, or persistence authority.

A proposal is a hypothesis, not a patch and not an activation command.
"""

from __future__ import annotations

import hashlib
from collections import Counter
from dataclasses import dataclass, field
from typing import Sequence

from gnosis.core.types import TransitionRecord
from .rules import RuleMetadata, RuleRegistry


@dataclass(frozen=True)
class ReflectionObservation:
    """One observed fact derived from canonical Core evidence."""

    observation_id: str
    transition_id: str
    kind: str
    value: str
    evidence_ref: str
    rule_id: str = "test-rule:unspecified"
    rule_version: int = 1
    provenance: str = "canonical-transition-record"


@dataclass(frozen=True)
class Finding:
    """A repeatable pattern that may justify a rule investigation."""

    finding_id: str
    claim: str
    observation_ids: tuple[str, ...]
    evidence_refs: tuple[str, ...]
    reproducibility: int
    falsification_condition: str
    affected_rule_refs: tuple[str, ...] = ()
    status: str = "OPEN"
    provenance: str = "reflection-analyzer"


@dataclass(frozen=True)
class CounterexampleCandidate:
    """Explicit description of how a Finding should be challenged."""

    candidate_id: str
    finding_id: str
    method: str
    success_condition: str
    evidence_refs: tuple[str, ...] = ()
    provenance: str = "reflection-analyzer"


@dataclass(frozen=True)
class RuleProposal:
    """Non-activating proposal for a possible rule/version improvement."""

    proposal_id: str
    finding_id: str
    target: str
    hypothesis: str
    evidence_refs: tuple[str, ...]
    expected_effect: str
    regression_risk: str
    required_test: str
    status: str = "PROPOSED"
    rule_id: str = "test-rule:unspecified"
    current_version: int = 1
    proposed_version: int = 2
    finding_refs: tuple[str, ...] = ()
    counterexample_refs: tuple[str, ...] = ()
    expected_effects: tuple[str, ...] = ()
    possible_regressions: tuple[str, ...] = ()
    test_plan: str = ""
    provenance: str = "reflection-analyzer"


@dataclass(frozen=True)
class ReflectionReport:
    """Complete read-only result of one reflection pass."""

    observations: tuple[ReflectionObservation, ...] = field(default_factory=tuple)
    findings: tuple[Finding, ...] = field(default_factory=tuple)
    counterexamples: tuple[CounterexampleCandidate, ...] = field(default_factory=tuple)
    proposals: tuple[RuleProposal, ...] = field(default_factory=tuple)
    counterexample_results: tuple[object, ...] = field(default_factory=tuple)


class ReflectionAnalyzer:
    """Analyze Core history without changing it.

    The analyzer uses only rule identifiers recorded by Core. Version 1
    metadata is registered as the current reflection-visible version unless a
    caller supplies an explicit registry. This does not activate or mutate a
    Core rule.
    """

    def __init__(self, transitions: Sequence[TransitionRecord], registry: RuleRegistry | None = None):
        self._transitions = tuple(transitions)
        self._registry = registry or RuleRegistry()
        self._ensure_rule_metadata()

    def _ensure_rule_metadata(self) -> None:
        for transition in self._transitions:
            rule_id = transition.test_rule_id
            if rule_id == "test-rule:unspecified":
                continue
            try:
                self._registry.get(rule_id, 1)
            except KeyError:
                self._registry.register(
                    RuleMetadata(
                        rule_id=rule_id,
                        rule_version=1,
                        rule_type="test_policy",
                        scope="canonical-core-transition",
                        implementation_ref="core:TransitionRecord.test_rule_id",
                        spec_ref="docs/CORE_REFLECTION_R1_TASK.md",
                        provenance="observed-from-canonical-transition",
                    )
                )

    @classmethod
    def from_engine(cls, engine: object, registry: RuleRegistry | None = None) -> "ReflectionAnalyzer":
        """Build an analyzer from an Engine-like object exposing ``history``."""
        history = getattr(engine, "history", None)
        if history is None:
            raise TypeError("engine must expose canonical Core history")
        return cls(history, registry=registry)

    @property
    def rule_registry(self) -> RuleRegistry:
        return self._registry

    def observe(self) -> tuple[ReflectionObservation, ...]:
        observations: list[ReflectionObservation] = []
        for index, transition in enumerate(self._transitions):
            transition_id = f"transition:{index}:{transition.candidate_id}"
            rule_id = transition.test_rule_id
            rule_version = 1
            observations.append(
                ReflectionObservation(
                    observation_id=f"observation:{index}:outcome",
                    transition_id=transition_id,
                    kind="transition_outcome",
                    value="accepted" if transition.accepted else "rejected",
                    evidence_ref=transition_id,
                    rule_id=rule_id,
                    rule_version=rule_version,
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
                        rule_id=rule_id,
                        rule_version=rule_version,
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
            reason_key = hashlib.sha256(reason.encode("utf-8")).hexdigest()[:16]
            finding_id = f"finding:repeated-rejection:{reason_key}"
            observation_ids = tuple(o.observation_id for o in related)
            evidence_refs = tuple(o.evidence_ref for o in related)
            affected_rule_refs = tuple(sorted({f"{o.rule_id}:v{o.rule_version}" for o in related if o.rule_id != "test-rule:unspecified"}))

            finding = Finding(
                finding_id=finding_id,
                claim=f"The same rejection reason recurs {count} times in the observed Core history: {reason}",
                observation_ids=observation_ids,
                evidence_refs=evidence_refs,
                reproducibility=count,
                falsification_condition="A sufficiently comparable replay must show that the rejection does not recur under the same stated conditions.",
                affected_rule_refs=affected_rule_refs,
            )
            findings.append(finding)

            counterexample_id = f"counterexample:{finding_id}"
            counterexamples.append(
                CounterexampleCandidate(
                    candidate_id=counterexample_id,
                    finding_id=finding_id,
                    method="historical_replay_or_boundary_case",
                    success_condition="Produce a comparable case where the suspected repeated rejection condition is absent or produces the expected alternative outcome.",
                    evidence_refs=evidence_refs,
                )
            )

            rule_ids = sorted({o.rule_id for o in related if o.rule_id != "test-rule:unspecified"}) or ["test-rule:unspecified"]
            for rule_id in rule_ids:
                current_version = self._registry.latest(rule_id).rule_version if rule_id != "test-rule:unspecified" else 1
                proposals.append(
                    RuleProposal(
                        proposal_id=f"proposal:{finding_id}:{rule_id}",
                        finding_id=finding_id,
                        target=f"{rule_id}:v{current_version}",
                        hypothesis=f"Investigate whether the rule/test policy producing '{reason}' is overly restrictive, underspecified, or correctly rejecting a recurring invalid class.",
                        evidence_refs=evidence_refs,
                        expected_effect="Either demonstrate that the current behavior is justified or identify a narrowly testable rule change.",
                        regression_risk="Changing acceptance criteria may admit invalid transitions; every candidate change must be replayed against existing accepted and rejected evidence.",
                        required_test="Run historical replay plus boundary and adversarial cases before any governance decision.",
                        rule_id=rule_id,
                        current_version=current_version,
                        proposed_version=current_version + 1,
                        finding_refs=(finding_id,),
                        counterexample_refs=(counterexample_id,),
                        expected_effects=("Preserve valid accepted transitions while testing the suspected restriction.",),
                        possible_regressions=("Admission of previously rejected invalid transitions.",),
                        test_plan="Run historical replay, boundary cases, adversarial cases, and invariant checks before governance.",
                    )
                )

        return ReflectionReport(
            observations=observations,
            findings=tuple(findings),
            counterexamples=tuple(counterexamples),
            proposals=tuple(proposals),
        )
