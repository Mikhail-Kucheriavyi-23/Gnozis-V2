from gnosis.core.types import State
from gnosis.evolution.evaluator import ModelEvidence
from gnosis.evolution.hypothesis import EvolutionHypothesis
from gnosis.evolution.materialization import materialize_descriptor
from gnosis.evolution.promotion import build_promotion_candidate
from gnosis.evolution.recursive import reevaluate_candidate
from gnosis.reflection.invariant_delta import InvariantDelta


def make_candidate():
    h = EvolutionHypothesis("h1", "reflection", ("gap",), ("improvement",), ("bounded",))
    evidence = ModelEvidence("h1:model:1", True, 0.9, ("verified",))
    delta = InvariantDelta(preserved=("state_integrity",), violated=(), improved=(), unknown=(), active_violations={}, shadow_violations={})
    return build_promotion_candidate(h, evidence, delta)


def test_materialization_is_only_a_version_descriptor():
    current = State(elements={"x": 1})
    proposed = State(elements={"x": 2}, version=1)
    candidate = make_candidate()
    reevaluation = reevaluate_candidate(candidate, lambda model, r: ModelEvidence(model, True, 0.9, ()), max_rounds=3)
    descriptor = materialize_descriptor(current, proposed, candidate, reevaluation)
    assert descriptor.parent_state_id == current.state_id
    assert descriptor.proposed_state_id == proposed.state_id
    assert descriptor.ready is True


def test_unstable_candidate_cannot_materialize():
    current = State(elements={"x": 1})
    proposed = State(elements={"x": 2}, version=1)
    candidate = make_candidate()
    reevaluation = reevaluate_candidate(candidate, lambda model, r: ModelEvidence(model, r < 2, 0.9, ()), max_rounds=3)
    try:
        materialize_descriptor(current, proposed, candidate, reevaluation)
    except ValueError as exc:
        assert "stable re-evaluation" in str(exc)
    else:
        raise AssertionError("unstable candidate must not materialize")
