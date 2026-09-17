"""Deterministic bounded generation of candidate evolution models."""
from __future__ import annotations

from dataclasses import dataclass

from .hypothesis import EvolutionHypothesis
from .sandbox import SandboxModel


@dataclass(frozen=True)
class GenerationPolicy:
    max_models: int = 3
    require_constraints: bool = True


def generate_models(
    hypothesis: EvolutionHypothesis,
    policy: GenerationPolicy = GenerationPolicy(),
) -> tuple[SandboxModel, ...]:
    if policy.max_models < 1:
        return ()
    if policy.require_constraints and not hypothesis.is_bounded():
        return ()

    count = min(policy.max_models, 3)
    return tuple(
        SandboxModel(
            model_id=f"{hypothesis.hypothesis_id}:model:{i}",
            hypothesis_id=hypothesis.hypothesis_id,
            description=f"bounded candidate {i} for target {hypothesis.target}",
        )
        for i in range(1, count + 1)
    )
