from gnosis.evolution.evaluator import ModelEvidence
from gnosis.evolution.hypothesis import EvolutionHypothesis
from gnosis.evolution.promotion import build_promotion_candidate
from gnosis.reflection.invariant_delta import InvariantDelta


def hypothesis():
    return EvolutionHypothesis(
        hypothesis_id="h1",
        target="reflection",
        rationale=("gap",),
        expected_effects=("improvement",),
        constraints=("no canonical mutation",),
    )


def delta(status):
    return InvariantDelta(
        preserved=("state_integrity",),
        violated=(),
        improved=(),
        unknown=(),
        active_violations={},
        shadow_violations={},
    ) if status == "PRESERVED" else InvariantDelta(
        preserved=(), violated=("state_integrity",), improved=(), unknown=(),
        active_violations={}, shadow_violations={"state_integrity": 1},
    )


def test_promotion_candidate_requires_passed_evidence_and_preserved_invariants():
    evidence = ModelEvidence("h1:model:1", True, 0.9, ("verified",))
    candidate = build_promotion_candidate(hypothesis(), evidence, delta("PRESERVED"))
    assert candidate.eligible is True
    assert candidate.can_promote is True


def test_violation_blocks_promotion():
    evidence = ModelEvidence("h1:model:1", True, 0.9, ("verified",))
    candidate = build_promotion_candidate(hypothesis(), evidence, delta("VIOLATION"))
    assert candidate.eligible is False
    assert candidate.can_promote is False
