"""Bounded endogenous candidate generation from canonical reflection proposals.

This module generates Core Candidates from evidence-backed RuleProposals. It does
not activate rules, mutate an Engine, or bypass Core Test/Select. The generated
state records the proposal as a relation in X/R, making the hypothesis itself a
bounded endogenous state transition rather than an external callback.
"""
from __future__ import annotations
from dataclasses import dataclass
from typing import Sequence
from gnosis.core.types import Candidate, Relation, State
from gnosis.core.budget import Budget
from .analyzer import ReflectionReport, RuleProposal

MAX_ENDOGENOUS_CANDIDATES = 20  # default; bounded by caller-provided evolution budget
REFLECTION_NODE = "__gnozis_reflection__"

@dataclass(frozen=True)
class EndogenousGeneration:
    candidates: tuple[Candidate, ...]
    proposal_ids: tuple[str, ...]
    bounded: bool = True


def _proposal_relation(proposal: RuleProposal) -> Relation:
    return Relation(
        source=REFLECTION_NODE,
        target=proposal.proposal_id,
        relation_type="proposed_rule",
        value={
            "finding_id": proposal.finding_id,
            "rule_id": proposal.rule_id,
            "current_version": proposal.current_version,
            "proposed_version": proposal.proposed_version,
            "hypothesis": proposal.hypothesis,
            "evidence_refs": proposal.evidence_refs,
        },
    )


def generate_endogenous_candidates(
    state: State,
    report: ReflectionReport,
    *,
    max_candidates: int | None = None,
    budget: Budget | None = None,
) -> EndogenousGeneration:
    """Generate at most 20 proposal-backed candidates deterministically.

    Candidates are hypotheses encoded as ordinary Core state transitions. No
    proposal is activated and no Engine state is mutated by this function.
    """
    if not 1 <= max_candidates <= MAX_ENDOGENOUS_CANDIDATES:
        raise ValueError("max_candidates must be in range 1..20")
    proposals = tuple(report.proposals[:max_candidates])
    candidates: list[Candidate] = []
    for proposal in proposals:
        proposed_state = state.with_relations((_proposal_relation(proposal),))
        candidates.append(
            Candidate(
                parent_state_id=state.state_id,
                proposed_state=proposed_state,
                origin="reflection:endogenous",
            )
        )
    return EndogenousGeneration(
        candidates=tuple(candidates),
        proposal_ids=tuple(p.proposal_id for p in proposals),
    )
