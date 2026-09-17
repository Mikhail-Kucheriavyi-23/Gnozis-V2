"""Bounded sandbox contract for autonomous evolution experiments."""
from __future__ import annotations

from dataclasses import dataclass

from .hypothesis import EvolutionHypothesis


@dataclass(frozen=True)
class SandboxModel:
    model_id: str
    hypothesis_id: str
    description: str


@dataclass(frozen=True)
class SandboxExperiment:
    experiment_id: str
    hypothesis: EvolutionHypothesis
    models: tuple[SandboxModel, ...]

    @property
    def can_mutate_canonical_core(self) -> bool:
        return False

    def is_bounded(self) -> bool:
        return self.hypothesis.is_bounded() and bool(self.models)
