from gnosis.core import TestResult, TransitionRecord
from gnosis.evolution.gap import GapDetector, history_from_persisted_transitions


def test_detector_consumes_real_transition_records_without_mutation():
    records = (
        TransitionRecord("s0", "s1", "c1", TestResult(False, ("missing_relation",)), False, "rejected"),
        TransitionRecord("s0", "s2", "c2", TestResult(False, ("missing_relation",)), False, "rejected"),
    )
    observations = history_from_persisted_transitions(records)
    gaps = GapDetector().detect(history=observations)
    assert len(gaps) == 1
    assert gaps[0].trigger_kind == "transition"
    assert gaps[0].source_records[0].startswith("transition:")
    assert records[0].to_state_id == "s1"
