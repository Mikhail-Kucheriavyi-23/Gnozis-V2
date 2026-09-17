"""Runtime entry points for Gnozis self-analysis.

Reflection remains read-only with respect to canonical Core. The persisted
entry point stores the resulting evidence so later reflection passes can use
prior findings as durable evidence rather than relying on AI conversation
history.
"""

from __future__ import annotations

from dataclasses import replace
from datetime import datetime, timezone
from typing import Any

from .analyzer import ReflectionAnalyzer, ReflectionReport
from .counterexample import CounterexampleEngine
from .persistence import save_reflection_report


def reflect(engine: Any, minimum_repetitions: int = 2) -> ReflectionReport:
    """Run one read-only self-analysis pass over canonical Engine history."""
    analyzer = ReflectionAnalyzer.from_engine(engine)
    report = analyzer.analyze(minimum_repetitions=minimum_repetitions)
    challenger = CounterexampleEngine(engine.history)
    results = tuple(
        challenger.challenge(finding, candidate)
        for finding, candidate in zip(report.findings, report.counterexamples)
    )
    return replace(report, counterexample_results=results)


def reflect_and_persist(
    engine: Any,
    conn: Any,
    minimum_repetitions: int = 2,
) -> tuple[ReflectionReport, str]:
    """Run reflection and durably store its complete evidence artifact.

    This function deliberately has no activation or mutation path. Persistence
    records what reflection observed and concluded; it does not grant those
    conclusions authority over Core.
    """
    report = reflect(engine, minimum_repetitions=minimum_repetitions)
    created_at = datetime.now(timezone.utc).isoformat()
    report_key = save_reflection_report(conn, report, created_at=created_at)
    return report, report_key
