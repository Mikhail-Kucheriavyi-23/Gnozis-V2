from gnosis.core.types import Candidate, State, TestResult
from gnosis.reflection.analyzer import RuleProposal
from gnosis.reflection.rules import RuleMetadata, RuleRegistry
from gnosis.reflection.shadow_adapter import evaluate_proposal_shadow


def _candidate(value: int) -> Candidate:
    state = State(elements={"value": value})
    return Candidate(parent_state_id=state.state_id, proposed_state=state, origin="test", seed=value)


def test_rule_proposal_is_evaluated_without_activation() -> None:
    registry = RuleRegistry()
    registry.register(
        RuleMetadata(
            rule_id="test-rule:diagnostic-policy",
            rule_version=1,
            rule_type="test_policy",
            scope="test",
            implementation_ref="test:active",
            spec_ref="test:spec",
        )
    )
    proposal = RuleProposal(
        proposal_id="proposal:shadow:1",
        finding_id="finding:shadow:1",
        target="test-rule:diagnostic-policy",
        hypothesis="accept positive values",
        evidence_refs=("transition:1",),
        expected_effect="one additional accepted candidate",
        regression_risk="negative values must remain rejected",
        required_test="shadow evaluation",
        rule_id="test-rule:diagnostic-policy",
        current_version=1,
        proposed_version=2,
    )

    candidates = (_candidate(-1), _candidate(1))

    def active_test(state, candidate):
        return TestResult(state.elements["value"] > 1, ("active-policy",))

    def shadow_test(state, candidate):
        return TestResult(state.elements["value"] >= 1, ("shadow-policy",))

    assessment = evaluate_proposal_shadow(
        proposal,
        candidates,
        active_test,
        shadow_test,
        registry,
    )

    assert assessment.proposal_id == proposal.proposal_id
    assert assessment.rule_id == proposal.rule_id
    assert assessment.current_version == 1
    assert assessment.proposed_version == 2
    assert len(assessment.candidate_ids) == 2
    assert assessment.evaluation.status == "BEHAVIOR_CHANGED"
    assert assessment.evaluation.improvements == 1
    assert assessment.evaluation.regressions == 0

    # The adapter only evaluates; it must not register or activate v2.
    assert registry.versions(proposal.rule_id) == (1,)
