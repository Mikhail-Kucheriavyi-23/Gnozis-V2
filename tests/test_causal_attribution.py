from gnosis.core import TestResult, TransitionRecord
from gnosis.reflection.analyzer import Finding, RuleProposal
from gnosis.reflection.causal import attribute_finding, refine_proposal_target


def _record(i: int, rule: str) -> TransitionRecord:
    return TransitionRecord(
        from_state_id=f"s{i}",
        to_state_id=f"s{i}",
        candidate_id=f"c{i}",
        test_result=TestResult(False, ("rejected",)),
        accepted=False,
        reason="rejected",
        test_rule_id=rule,
    )


def test_finding_gets_exact_rule_attribution():
    finding = Finding(
        finding_id="finding:1",
        claim="repeat",
        observation_ids=(),
        evidence_refs=("transition:0:c0", "transition:1:c1"),
        reproducibility=2,
        falsification_condition="replay differs",
    )
    causal = attribute_finding(finding, (_record(0, "rule:nonnegative"), _record(1, "rule:nonnegative")))
    assert causal.target_rule_ids == ("rule:nonnegative",)
    assert causal.confidence == "EXACT_RECORDED_PROVENANCE"


def test_proposal_target_is_refined_only_from_exact_provenance():
    proposal = RuleProposal("p1", "finding:1", "unknown", "investigate", (), "effect", "risk", "test")
    finding = Finding("finding:1", "repeat", (), ("transition:0:c0",), 2, "replay")
    causal = attribute_finding(finding, (_record(0, "rule:budget"),))
    refined = refine_proposal_target(proposal, causal)
    assert refined.target == "test-rule:rule:budget"
