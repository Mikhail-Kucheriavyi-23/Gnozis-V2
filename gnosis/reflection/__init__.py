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
from .runtime import reflect

__all__ = [
    "CounterexampleCandidate",
    "Finding",
    "ReflectionAnalyzer",
    "ReflectionObservation",
    "ReflectionReport",
    "RuleProposal",
    "reflect",
]
