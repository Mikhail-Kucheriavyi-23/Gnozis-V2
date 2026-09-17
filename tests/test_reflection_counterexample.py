from gnosis.core import TestResult, TransitionRecord
from gnosis.reflection import CounterexampleEngine, ReflectionAnalyzer, reflect


def _record(index: int, accepted: bool, candidate_id: str, reason: str) -> TransitionRecord:
    return TransitionRecord(
        from_state_id=f"state:{index}",
        to_state_id=f"state:{index + 1}",
        candidate_id=candidate_id,
        test_result=TestResult(passed=accepted, reasons=(reason,)),
        accepted=accepted,
        reason=reason,
    )


def test_counterexample_is_inconclusive_when_no_accepted_match_exists():
    history = (
        _record(0, False, "c1", "repeated failure"),
        _record(1, False, "c2", "repeated failure"),
    )
    analyzer = ReflectionAnalyzer(history)
    report = analyzer.analyze()
    result = CounterexampleEngine(history).challenge(
        report.findings[0], report.counterexamples[0]
    )
    assert result.status == "INCONCLUSIVE"


def test_counterexample_refutes_unconditional_rejection_hypothesis():
    history = (
        _record(0, False, "same", "repeated failure"),
        _record(1, False, "same", "repeated failure"),
        _record(2, True, "same", "committed"),
    )
    analyzer = ReflectionAnalyzer(history)
    report = analyzer.analyze()
    result = CounterexampleEngine(history).challenge(
        report.findings[0], report.counterexamples[0]
    )
    assert result.status == "REFUTED"
    assert result.evidence_refs == ("transition:2:same",)


def test_runtime_reflection_executes_counterexample_stage_without_mutating_history():
    history = [
        _record(0, False, "c1", "repeated failure"),
        _record(1, False, "c2", "repeated failure"),
    ]

    class EngineLike:
        def __init__(self, history):
            self.history = history

    engine = EngineLike(history)
    report = reflect(engine)

    assert report.counterexample_results[0].status == "INCONCLUSIVE"
    assert engine.history == history
