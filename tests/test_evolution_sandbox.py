from gnosis.evolution.hypothesis import EvolutionHypothesis
from gnosis.evolution.sandbox import SandboxExperiment, SandboxModel


def test_sandbox_is_bounded_and_cannot_mutate_canonical_core() -> None:
    hypothesis = EvolutionHypothesis(
        hypothesis_id="h1",
        target="reflection.rule",
        rationale=("observed regression",),
        expected_effects=("reduce regression",),
        constraints=("preserve state integrity",),
    )
    experiment = SandboxExperiment(
        experiment_id="exp1",
        hypothesis=hypothesis,
        models=(SandboxModel("m1", "h1", "candidate architecture"),),
    )

    assert experiment.is_bounded() is True
    assert experiment.can_mutate_canonical_core is False
