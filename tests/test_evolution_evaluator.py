from gnosis.evolution.evaluator import ModelEvidence, evaluate_experiment
from gnosis.evolution.hypothesis import EvolutionHypothesis
from gnosis.evolution.sandbox import SandboxExperiment, SandboxModel


def test_evaluator_selects_best_passing_model_without_core_mutation() -> None:
    hypothesis = EvolutionHypothesis(
        hypothesis_id="h1",
        target="reflection",
        rationale=("reduce false proposals",),
        expected_effects=("fewer false proposals",),
        constraints=("preserve_core_invariants",),
    )
    models = (
        SandboxModel("a", "h1", "baseline"),
        SandboxModel("b", "h1", "candidate"),
    )
    experiment = SandboxExperiment("e1", hypothesis, models)

    result = evaluate_experiment(
        experiment,
        (
            ModelEvidence("a", True, 0.4),
            ModelEvidence("b", True, 0.8),
        ),
    )

    assert result.best_model() == models[1]
    assert experiment.can_mutate_canonical_core is False
    assert experiment.is_bounded() is True
