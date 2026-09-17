import pytest

from gnosis.core import State
from gnosis.evolution.evaluator import ModelEvidence
from gnosis.evolution.materialization import CoreVersionDescriptor
from gnosis.evolution.promotion import PromotionCandidate
from gnosis.evolution.promotion_engine import PromotionEngine, PromotionError
from gnosis.evolution.recursive import ReEvaluationResult
from gnosis.evolution.hypothesis import EvolutionHypothesis
from gnosis.reflection.invariant_delta import InvariantDelta


def _fixture():
    current = State(elements={"a": 1}, version=0)
    proposed = current.with_elements({"b": 2})
    hypothesis = EvolutionHypothesis(
        hypothesis_id="h1",
        target="core",
        rationale="validated improvement",
        expected_effects=("b added",),
        constraints=("bounded",),
    )
    evidence = ModelEvidence(
        model_id="h1:model:1", passed=True, score=1.0, reasons=("stable",)
    )
    delta = InvariantDelta(
        preserved=("state-valid",),
        violated=(),
        improved=(),
        unknown=(),
        active_violations={},
        shadow_violations={},
    )
    candidate = PromotionCandidate(
        hypothesis_id=hypothesis.hypothesis_id,
        model_id=evidence.model_id,
        evidence=evidence,
        invariant_delta=delta,
    )
    reevaluation = ReEvaluationResult(
        rounds=(
            ModelEvidence("h1:model:1", True, 1.0, ("stable",)),
            ModelEvidence("h1:model:1", True, 1.0, ("stable",)),
            ModelEvidence("h1:model:1", True, 1.0, ("stable",)),
        ),
        stable=True,
    )
    descriptor = CoreVersionDescriptor(
        version_id=f"{current.state_id}->{proposed.state_id}",
        parent_state_id=current.state_id,
        proposed_state_id=proposed.state_id,
        candidate_model_id=candidate.model_id,
        evidence_rounds=3,
    )
    return current, proposed, candidate, reevaluation, descriptor


def test_promotion_materializes_only_after_all_gates_pass():
    current, proposed, candidate, reevaluation, descriptor = _fixture()

    next_state, result = PromotionEngine().promote(
        current, proposed, candidate, reevaluation, descriptor
    )

    assert next_state is proposed
    assert result.parent_state_id == current.state_id
    assert result.next_state_id == proposed.state_id
    assert result.evidence_rounds == 3


def test_failed_promotion_leaves_parent_unchanged():
    current, proposed, candidate, _, descriptor = _fixture()
    failed = ReEvaluationResult(rounds=(), stable=False)

    with pytest.raises(PromotionError):
        PromotionEngine().promote(current, proposed, candidate, failed, descriptor)

    assert current.state_id != proposed.state_id
    assert current.elements == {"a": 1}


def test_stale_parent_is_rejected():
    current, proposed, candidate, reevaluation, descriptor = _fixture()
    wrong_parent = State(elements={"different": True}, version=0)

    with pytest.raises(PromotionError, match="descriptor parent"):
        PromotionEngine().promote(
            wrong_parent, proposed, candidate, reevaluation, descriptor
        )


def test_descriptor_proposed_state_mismatch_is_rejected():
    current, proposed, candidate, reevaluation, descriptor = _fixture()
    other = proposed.with_elements({"c": 3})

    with pytest.raises(PromotionError, match="descriptor proposed state"):
        PromotionEngine().promote(
            current, other, candidate, reevaluation, descriptor
        )


def test_same_state_cannot_be_promoted():
    current, _, candidate, reevaluation, descriptor = _fixture()
    same = current
    same_descriptor = CoreVersionDescriptor(
        version_id=f"{current.state_id}->{current.state_id}",
        parent_state_id=current.state_id,
        proposed_state_id=current.state_id,
        candidate_model_id=candidate.model_id,
        evidence_rounds=len(reevaluation.rounds),
    )

    with pytest.raises(PromotionError, match="distinct Core state"):
        PromotionEngine().promote(
            current, same, candidate, reevaluation, same_descriptor
        )
