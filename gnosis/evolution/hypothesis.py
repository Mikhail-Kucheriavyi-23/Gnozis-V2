"""Structured hypotheses for autonomous evolution experiments."""
from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class EvolutionHypothesis:
    """A bounded, testable architectural hypothesis.

    This object describes a proposed change; it does not contain executable
    authority and cannot mutate the canonical Core.
    """

    hypothesis_id: str
    target: str
    rationale: tuple[str, ...]
    expected_effects: tuple[str, ...]
    constraints: tuple[str, ...]

    def is_bounded(self) -> bool:
        return bool(
            self.hypothesis_id.strip()
            and self.target.strip()
            and self.constraints
        )
