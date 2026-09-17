from gnosis.core import TestResult, TransitionRecord
from gnosis.reflection.analyzer import ReflectionAnalyzer


def _record(i: int) -> TransitionRecord:
    return TransitionRecord(
        from_state_id=f"s{i}",
        to_state_id=f"s{i}",
        candidate_id=f"c{i}",
        test_result=TestResult(False, ("policy:repeat",)),
        accepted=False,
        reason="policy:repeat",
        test_rule_id="rule:policy",
    )


def test_analyzer_registers_observed_rule_and_versions_proposal():
    report = ReflectionAnalyzer([_record(0), _record(1)]).analyze()

    assert report.observations[0].rule_id == "rule:policy"
    assert report.observations[0].rule_version == 1
    assert report.findings[0].affected_rule_refs == ("rule:policy:v1",)
    assert report.proposals[0].rule_id == "rule:policy"
    assert report.proposals[0].current_version == 1
    assert report.proposals[0].proposed_version == 2
    assert report.proposals[0].target == "rule:policy:v1"
    assert report.proposals[0].finding_refs == (report.findings[0].finding_id,)
    assert report.proposals[0].counterexample_refs == (report.counterexamples[0].candidate_id,)
