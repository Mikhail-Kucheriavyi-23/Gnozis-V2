"""Deterministic evaluation contract for sandbox evolution experiments."""
from __future__ import annotations

from dataclasses import dataclass

from .sandbox import SandboxExperiment, SandboxModel


@dataclass(frozen=True)
class ModelEvidence:
    model_id: str
    passed: bool
    score: float
    reasons: tuple[str, ...] = ()


@dataclass(frozen=True)
class SandboxEvaluation:
    experiment_id: str
    evidence: tuple[ModelEvidence, ...]

    def best_model(self) -> SandboxModel | None:
        if not self.evidence:
            return None
        best = max(self.evidence, key=lambda item: (item.passed, item.score))
        if not best.passed:
            return None
        return next((m for m in self._models if m.model_id == best.model_id), None)

    _models: tuple[SandboxModel, ...] = ()


def evaluate_experiment(
    experiment: SandboxExperiment,
    evidence: tuple[ModelEvidence, ...],
) -> SandboxEvaluation:
    """Evaluate supplied deterministic evidence without touching canonical Core."""
    model_ids = {model.model_id for model in experiment.models}
    if any(item.model_id not in model_ids for item in evidence):
        raise ValueError("evidence references unknown sandbox model")
    if len({item.model_id for item in evidence}) != len(evidence):
        raise ValueError("duplicate model evidence")
    return SandboxEvaluation(
        experiment_id=experiment.experiment_id,
        evidence=evidence,
        _models=experiment.models,
    )
