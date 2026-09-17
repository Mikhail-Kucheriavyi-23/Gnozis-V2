"""Controlled, read-only reflection over canonical Core evidence.

Reflection consumes Core history but has no authority to mutate Core state,
activate rules, or alter invariants.
"""

from .analyzer import (
    CounterexampleCandidate,
    Finding,
    ReflectionAnalyzer,
    ReflectionObservation,
    ReflectionReport,
    RuleProposal,
)
from .counterexample import CounterexampleEngine, CounterexampleResult
from .governance import GovernanceDecision, evaluate_governance
from .history import HistoricalFinding, ReflectionHistorySummary, summarize_reflection_history, unresolved_findings
from .invariant_delta import InvariantDelta, analyze_invariant_delta
from .rules import RuleMetadata, RuleRegistry
from .runtime import reflect
from .shadow import ShadowCase, ShadowEvaluation, evaluate_shadow
from .shadow_adapter import ProposalShadowAssessment, evaluate_proposal_shadow

__all__ = [
    "CounterexampleCandidate",
    "CounterexampleEngine",
    "CounterexampleResult",
    "GovernanceDecision",
    "Finding",
    "HistoricalFinding",
    "ReflectionAnalyzer",
    "ReflectionHistorySummary",
    "ReflectionObservation",
    "ReflectionReport",
    "RuleMetadata",
    "RuleProposal",
    "RuleRegistry",
    "ShadowCase",
    "ShadowEvaluation",
    "evaluate_shadow",
    "ProposalShadowAssessment",
    "evaluate_proposal_shadow",
    "InvariantDelta",
    "analyze_invariant_delta",
    "evaluate_governance",
    "reflect",
    "summarize_reflection_history",
    "unresolved_findings",
]