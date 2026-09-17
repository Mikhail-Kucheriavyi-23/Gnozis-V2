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
from .history import HistoricalFinding, ReflectionHistorySummary, summarize_reflection_history, unresolved_findings
from .rules import RuleMetadata, RuleRegistry
from .runtime import reflect
from .shadow import ShadowCase, ShadowEvaluation, evaluate_shadow

__all__ = [
    "CounterexampleCandidate",
    "CounterexampleEngine",
    "CounterexampleResult",
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
    "reflect",
    "summarize_reflection_history",
    "unresolved_findings",
]
