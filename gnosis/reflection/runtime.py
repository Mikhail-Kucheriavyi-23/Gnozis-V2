"""Runtime entry point for Gnozis self-analysis.

The entry point accepts a canonical Engine instance, reads its existing
history, and returns a reflection report. It never mutates the Engine.
"""

from __future__ import annotations

from typing import Any

from .analyzer import ReflectionAnalyzer, ReflectionReport


def reflect(engine: Any, minimum_repetitions: int = 2) -> ReflectionReport:
    """Run one read-only self-analysis pass over canonical Engine history.

    This is intentionally an external reflection layer: the canonical Core
    remains authoritative and unaware of proposal activation. The returned
    proposals are hypotheses only.
    """
    return ReflectionAnalyzer.from_engine(engine).analyze(
        minimum_repetitions=minimum_repetitions
    )
