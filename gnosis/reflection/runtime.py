"""Runtime entry points for Gnozis self-analysis.

Reflection remains read-only with respect to canonical Core. The persisted
entry point stores the resulting evidence so later reflection passes can use
prior findings as durable evidence rather than relying on AI conversation
history.
"""

from __future__ import annotations

from dataclasses import dataclass, replace
from datetime import datetime, timezone
from typing import Any

from .analyzer import ReflectionAnalyzer, ReflectionReport
from .counterexample import CounterexampleEngine
from .history import HistoricalFinding, ReflectionHistorySummary, summarize_reflection_history, unresolved_findings
from .persistence import list_reflection_reports, reflection_id, save_reflection_report


@dataclass(frozen=True)
class CumulativeReflectionReport:
    current: ReflectionReport
    history: ReflectionHistorySummary
    recurring_unresolved: tuple[HistoricalFinding, ...]


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


def reflect_with_history(
    engine: Any,
    conn: Any,
    *,
    minimum_repetitions: int = 2,
) -> CumulativeReflectionReport:
    """Run a pass while exposing durable prior reflection evidence.

    Historical evidence is context for analysis only. It does not activate
    proposals, mutate Core, or change the authority of canonical state.
    """
    previous = list_reflection_reports(conn)
    history = summarize_reflection_history(previous)
    recurring = unresolved_findings(previous)
    current = reflect(engine, minimum_repetitions=minimum_repetitions)
    return CumulativeReflectionReport(
        current=current,
        history=history,
        recurring_unresolved=recurring,
    )


def reflect_and_persist(
    engine: Any,
    conn: Any,
    minimum_repetitions: int = 2,
) -> tuple[ReflectionReport, str]:
    """Run reflection, incorporate prior evidence, and persist the new pass."""
    cumulative = reflect_with_history(
        engine,
        conn,
        minimum_repetitions=minimum_repetitions,
    )
    created_at = datetime.now(timezone.utc).isoformat()
    report_key = save_reflection_report(conn, cumulative.current, created_at=created_at)
    return cumulative.current, report_key


def reflection_history_context(conn: Any) -> tuple[dict[str, Any], ...]:
    """Expose persisted reflection evidence for a future analysis layer."""
    return list_reflection_reports(conn)
