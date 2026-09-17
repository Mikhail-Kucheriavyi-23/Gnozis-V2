from gnosis.evolution.evaluator import ModelEvidence
from gnosis.evolution.hypothesis import EvolutionHypothesis
from gnosis.evolution.promotion import build_promotion_candidate
from gnosis.evolution.recursive import reevaluate_candidate
from gnosis.reflection.invariant_delta import InvariantDelta


def candidate():
    h = EvolutionHypothesis("h1", "reflection", ("gap",), ("improvement",), ("bounded",))
    evidence = ModelEvidence("h1:model:1", True, 0.9, ("verified",))
    delta = InvariantDelta(
        preserved=("state_integrity",), violated=(), improved=(), unknown=(),
        active_violations={}, shadow_violations={},
    )
    return build_promotion_candidate(h, evidence, delta)


def test_recursive_reevaluation_requires_stable_rounds():
    result = reevaluate_candidate(
        candidate(),
        lambda model_id, round_number: ModelEvidence(model_id, True, 0.9, (f"round:{round_number}",)),
        max_rounds=3,
    )
    assert result.stable is True
    assert len(result.rounds) == 3


def test_recursive_reevaluation_stops_on_failed_round():
    result = reevaluate_candidate(
        candidate(),
        lambda model_id, round_number: ModelEvidence(model_id, round_number < 2, 0.9, ()),
        max_rounds=3,
    )
    assert result.stable is False
    assert len(result.rounds) == 2
