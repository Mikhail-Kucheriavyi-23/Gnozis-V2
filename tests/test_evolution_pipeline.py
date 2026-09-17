from gnosis.evolution.hypothesis import EvolutionHypothesis
from gnosis.evolution.pipeline import run_experiment
from gnosis.evolution.sandbox import SandboxExperiment, SandboxModel


def test_pipeline_executes_models_and_collects_evidence() -> None:
    hypothesis = EvolutionHypothesis(
        hypothesis_id="h1",
        target="reflection",
        rationale=("gap",),
        expected_effects=("improvement",),
        constraints=("no canonical mutation",),
    )
    models = (
        SandboxModel("a", "h1", "A"),
        SandboxModel("b", "h1", "B"),
    )
    experiment = SandboxExperiment("exp1", hypothesis, models)

    def runner(model):
        return (True, 0.9, ("verified",)) if model.model_id == "b" else (True, 0.4, ("verified",))

    result = run_experiment(experiment, runner)
    assert result.evaluation.best_model().model_id == "b"
