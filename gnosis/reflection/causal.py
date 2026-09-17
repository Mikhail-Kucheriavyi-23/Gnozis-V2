"""Conservative causal candidates for reflection.

This layer connects repeated findings to exact Test-rule provenance already
recorded by Core. It does not infer causality beyond that evidence.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Sequence

from gnosis.core.types import TransitionRecord

from .analyzer import Finding, RuleProposal
from .provenance import RuleAttribution, attribute_rule


@dataclass(frozen=True)
class CausalCandidate:
    finding_id: str
    attributions: tuple[RuleAttribution, ...]
    target_rule_ids: tuple[str, ...]
    confidence: str
    basis: str


def attribute_finding(
    finding: Finding,
    transitions: Sequence[TransitionRecord],
) -> CausalCandidate:
    attributions = attribute_rule(transitions, finding.evidence_refs)
    exact = tuple(a.rule_id for a in attributions if a.confidence == "EXACT_RECORDED_PROVENANCE")
    if exact:
        confidence = "EXACT_RECORDED_PROVENANCE"
        basis = "Finding evidence maps directly to Test rule identifiers recorded by Core."
    else:
        confidence = "UNSPECIFIED"
        basis = "Finding evidence does not expose a specific Test rule identifier."
    return CausalCandidate(
        finding_id=finding.finding_id,
        attributions=attributions,
        target_rule_ids=exact,
        confidence=confidence,
        basis=basis,
    )


def refine_proposal_target(
    proposal: RuleProposal,
    causal: CausalCandidate,
) -> RuleProposal:
    """Return a proposal whose target is precise only when provenance is exact."""
    if not causal.target_rule_ids:
        return proposal
    target = "test-rule:" + ",".join(causal.target_rule_ids)
    hypothesis = (
        f"Investigate whether {target} is responsible for the repeated finding; "
        "test a narrowly scoped change against the recorded evidence before any governance decision."
    )
    return RuleProposal(
        proposal_id=proposal.proposal_id,
        finding_id=proposal.finding_id,
        target=target,
        hypothesis=hypothesis,
        evidence_refs=proposal.evidence_refs,
        expected_effect=proposal.expected_effect,
        regression_risk=proposal.regression_risk,
        required_test=proposal.required_test,
        status=proposal.status,
    )
