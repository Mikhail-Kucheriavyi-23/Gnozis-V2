"""Governed adapter from a RuleProposal to isolated ShadowEvaluation.

The adapter closes the reflection-to-shadow gap without activating proposals.
It requires explicit rule metadata, candidate evidence, and both active and
shadow Test functions. The proposal remains a hypothesis; this module only
produces a lineage-bearing evaluation artifact.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Sequence

from gnosis.core.types import Candidate

from .analyzer import RuleProposal
from .rules import RuleRegistry
from .shadow import ShadowEvaluation, evaluate_shadow
from gnosis.core.verification import TestFn


@dataclass(frozen=True)
class ProposalShadowAssessment:
    proposal_id: str
    rule_id: str
    current_version: int
    proposed_version: int
    candidate_ids: tuple[str, ...]
    evaluation: ShadowEvaluation
    provenance: str = "reflection-shadow-adapter"


def evaluate_proposal_shadow(
    proposal: RuleProposal,
    candidates: Sequence[Candidate],
    active_test: TestFn,
    shadow_test: TestFn,
    registry: RuleRegistry,
) -> ProposalShadowAssessment:
    """Evaluate one proposal against immutable candidate evidence.

    The registry must contain the proposal's current rule version. The
    proposed version must be strictly newer. The caller supplies the concrete
    shadow Test function explicitly; the proposal itself never becomes code.
    No Engine, State, RuleRegistry, or persistence state is mutated.
    """
    current = registry.get(proposal.rule_id, proposal.current_version)
    if proposal.proposed_version <= proposal.current_version:
        raise ValueError("proposed_version must be greater than current_version")
    if current.rule_id != proposal.rule_id:
        raise ValueError("proposal rule_id does not match registry metadata")

    candidate_tuple = tuple(candidates)
    evaluation = evaluate_shadow(candidate_tuple, active_test, shadow_test)
    return ProposalShadowAssessment(
        proposal_id=proposal.proposal_id,
        rule_id=proposal.rule_id,
        current_version=proposal.current_version,
        proposed_version=proposal.proposed_version,
        candidate_ids=tuple(candidate.candidate_id for candidate in candidate_tuple),
        evaluation=evaluation,
    )
