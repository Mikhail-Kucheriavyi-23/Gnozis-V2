from gnosis.evolution.gap import GapDetector
from gnosis.evolution.capability import CapabilitySynthesizer


def _history():
    return (
        {"record_id": "r1", "kind": "transition", "status": "REJECTED", "reason": "missing_relation"},
        {"record_id": "r2", "kind": "transition", "status": "REJECTED", "reason": "missing_relation"},
    )


def test_gap_is_endogenously_derived_and_deterministic():
    first = GapDetector().detect(history=_history())
    second = GapDetector().detect(history=_history())
    assert first == second
    assert len(first) == 1
    assert first[0].source_records == ("r1", "r2")


def test_gap_changes_when_relevant_evidence_changes():
    base = GapDetector().detect(history=_history())
    changed = GapDetector().detect(history=(
        {"record_id": "r1", "kind": "transition", "status": "REJECTED", "reason": "different"},
        {"record_id": "r2", "kind": "transition", "status": "REJECTED", "reason": "different"},
    ))
    assert base[0].gap_id != changed[0].gap_id


def test_caller_does_not_name_capability():
    gap = GapDetector().detect(history=_history())[0]
    capability = CapabilitySynthesizer().synthesize(gap)[0]
    assert capability.source_gap_id == gap.gap_id
    assert capability.can_activate is False
    assert capability.status == "PROPOSED"


def test_missing_dependency_is_explicit():
    gap = GapDetector().detect(history=_history())[0]
    capability = CapabilitySynthesizer().synthesize(gap, available_operations=("observe",))[0]
    assert capability.missing_dependencies == ("record",)
