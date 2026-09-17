"""Executable bounded evolution pipeline."""
from __future__ import annotations

from dataclasses import dataclass
from typing import Callable

from .evaluator import ModelEvidence, SandboxEvaluation, evaluate_experiment
from .sandbox import SandboxExperiment, SandboxModel

Runner = Callable[[SandboxModel], tuple[bool, float, tuple[str, ...]]]


@dataclass(frozen=True)
class EvolutionRun:
    experiment_id: str
    evaluation: SandboxEvaluation


def run_experiment(experiment: SandboxExperiment, runner: Runner) -> EvolutionRun:
    evidence = tuple(
        ModelEvidence(model_id=model.model_id, passed=passed, score=score, reasons=reasons)
        for model in experiment.models
        for passed, score, reasons in (runner(model),)
    )
    evaluation = evaluate_experiment(experiment, evidence)
    return EvolutionRun(experiment_id=experiment.experiment_id, evaluation=evaluation)
