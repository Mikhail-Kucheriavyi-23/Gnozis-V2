from gnosis.core import Candidate,State
from gnosis.evolution import evaluate_observation,make_promotion_candidate,run_sandbox
def _candidate(state): return Candidate(parent_state_id=state.state_id,proposed_state=state.with_elements({"b":2}),origin="sandbox-test")
def test_sandbox_produces_digest_linked_evidence():
    state=State(elements={"a":1}); result=run_sandbox(state,_candidate(state),lambda _s,_c:{"metric":1})
    assert result.accepted_for_evaluation and result.execution.status=="COMPLETED" and result.execution.evidence_digest
    assert evaluate_observation(result.execution.observations,evidence_digest=result.execution.evidence_digest,predicate="observations_present").status=="PASS"
def test_sandbox_fails_closed_on_observer_error():
    state=State(elements={"a":1}); result=run_sandbox(state,_candidate(state),lambda _s,_c: (_ for _ in ()).throw(RuntimeError("boom")))
    assert result.execution.status=="FAILED" and not result.accepted_for_evaluation
def test_unknown_evaluator_does_not_claim_pass():
    assert evaluate_observation({"metric":1},evidence_digest="digest",predicate="unknown-policy").status=="REVIEW"
def test_promotion_candidate_cannot_activate():
    p=make_promotion_candidate(candidate_id="candidate:1",evidence_digest="digest",evaluation_status="PASS",shadow_status="BEHAVIOR_CHANGED",invariant_status="IMPROVED",governance_decision="REVIEW")
    assert p.status=="PROPOSED" and p.can_activate is False
def test_sandbox_rejects_stale_parent():
    state=State(elements={"a":1}); candidate=Candidate(parent_state_id="stale",proposed_state=state.with_elements({"b":2}),origin="sandbox-test")
    try: run_sandbox(state,candidate,lambda _s,_c:{"ok":True})
    except ValueError: pass
    else: raise AssertionError("stale parent must be rejected")
