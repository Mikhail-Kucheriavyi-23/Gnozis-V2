from gnosis.evolution.generator import GenerationPolicy, generate_models
from gnosis.evolution.hypothesis import EvolutionHypothesis


def test_generator_creates_bounded_candidates() -> None:
    hypothesis = EvolutionHypothesis(
        hypothesis_id="h1",
        target="reflection",
        rationale=("observed gap",),
        expected_effects=("reduce regression",),
        constraints=("no canonical mutation",),
    )
    models = generate_models(hypothesis, GenerationPolicy(max_models=5))
    assert len(models) == 3
    assert all(m.hypothesis_id == "h1" for m in models)
    assert len({m.model_id for m in models}) == 3


def test_generator_rejects_unbounded_hypothesis() -> None:
    hypothesis = EvolutionHypothesis(
        hypothesis_id="h2",
        target="reflection",
        rationale=(),
        expected_effects=(),
        constraints=(),
    )
    assert generate_models(hypothesis) == ()
