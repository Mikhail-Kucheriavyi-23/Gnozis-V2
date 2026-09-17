"""Execution contract for bounded evolution sandbox experiments.

The executor produces evidence from an actual runner invocation. It has no
reference to canonical Core mutation or promotion authority.
"""
from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass
from typing import Callable, Mapping

from .sandbox import SandboxExperiment, SandboxModel


Observation = Mapping[str, object]
Runner = Callable[[SandboxModel], tuple[Observation, ...]]


@dataclass(frozen=True)
class SandboxExecution:
    experiment_id: str
    model_id: str
    observations: tuple[Observation, ...]
    evidence_digest: str
    executed: bool = True

    @property
    def can_mutate_canonical_core(self) -> bool:
        return False


def execute_model(
    experiment: SandboxExperiment,
    model: SandboxModel,
    runner: Runner,
) -> SandboxExecution:
    """Run one bounded sandbox model and derive an auditable evidence digest."""
    if not experiment.is_bounded():
        raise ValueError("unbounded sandbox experiment")
    if model not in experiment.models:
        raise ValueError("model does not belong to experiment")

    observations = tuple(runner(model))
    canonical = json.dumps(observations, sort_keys=True, separators=(",", ":"), default=str)
    digest = hashlib.sha256(canonical.encode("utf-8")).hexdigest()
    return SandboxExecution(
        experiment_id=experiment.experiment_id,
        model_id=model.model_id,
        observations=observations,
        evidence_digest=digest,
    )
