from gnosis.evolution.execution import execute_model
from gnosis.evolution.generator import generate_models
from gnosis.evolution.hypothesis import EvolutionHypothesis
from gnosis.evolution.sandbox import SandboxExperiment


def test_execution_runs_runner_and_produces_digest() -> None:
    hypothesis = EvolutionHypothesis(
        hypothesis_id="h1",
        target="reflection",
        rationale=("observed gap",),
        expected_effects=("reduce regression",),
        constraints=("no canonical mutation",),
    )
    models = generate_models(hypothesis)
    experiment = SandboxExperiment("exp1", hypothesis, models)

    def runner(model):
        return ({"model": model.model_id, "result": "ok"},)

    result = execute_model(experiment, models[0], runner)

    assert result.executed is True
    assert result.observations[0]["result"] == "ok"
    assert result.evidence_digest
    assert result.can_mutate_canonical_core is False
