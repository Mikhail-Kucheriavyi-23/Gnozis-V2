"""Runtime entry point for Gnozis self-analysis.

The entry point accepts a canonical Engine instance, reads its existing
history, and returns a reflection report. It never mutates the Engine.
"""

from __future__ import annotations

from dataclasses import replace
from typing import Any

from .analyzer import ReflectionAnalyzer, ReflectionReport
from .counterexample import CounterexampleEngine


def reflect(engine: Any, minimum_repetitions: int = 2) -> ReflectionReport:
    """Run one read-only self-analysis pass over canonical Engine history.

    The pass observes history, creates findings/proposals, and immediately
    executes the conservative historical counterexample challenge. Results
    remain evidence only: nothing can activate or mutate Core.
    """
    analyzer = ReflectionAnalyzer.from_engine(engine)
    report = analyzer.analyze(minimum_repetitions=minimum_repetitions)
    challenger = CounterexampleEngine(engine.history)
    results = tuple(
        challenger.challenge(finding, candidate)
        for finding, candidate in zip(report.findings, report.counterexamples)
    )
    return replace(report, counterexample_results=results)
