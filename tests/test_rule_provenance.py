from gnosis.core import Candidate, Engine, State
from gnosis.reflection.provenance import attribute_rule


def test_engine_records_test_rule_provenance():
    state = State(elements={"n": 0})
    engine = Engine(state=state, test_rule_id="rule:nonnegative")
    proposed = state.with_elements({"n": 1})
    record = engine.step(Candidate(state.state_id, proposed, "test"))
    assert record.test_rule_id == "rule:nonnegative"


def test_attribution_uses_only_recorded_provenance():
    state = State(elements={"n": 0})
    engine = Engine(state=state, test_rule_id="rule:nonnegative")
    rejected = state.with_elements({"n": -1})
    engine.test_fn = lambda _state, _candidate: __import__("gnosis.core").core.TestResult(False, ("rejected",))
    record = engine.step(Candidate(state.state_id, rejected, "test"))
    transition_id = f"transition:0:{record.candidate_id}"
    result = attribute_rule(engine.history, (transition_id,))
    assert len(result) == 1
    assert result[0].rule_id == "rule:nonnegative"
    assert result[0].confidence == "EXACT_RECORDED_PROVENANCE"
