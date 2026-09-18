from gnosis.evolution.provenance import build_provenance, verify_evidence_digest


def test_provenance_accepts_matching_evidence_digest():
    observations = {"metric": 1, "nested": {"ok": True}}
    from gnosis.evolution.provenance import canonical_digest
    digest = canonical_digest(observations)
    result = build_provenance(
        candidate_id="candidate:1",
        parent_state_id="state:1",
        observations=observations,
        parent_state_digest="parent-digest",
        proposed_state_digest="proposed-digest",
    candidate_binding_digest="binding-digest",
        evidence_digest=digest,
        evaluation_status="PASS",
        shadow_status="NO_BEHAVIORAL_CHANGE",
        invariant_status="PRESERVED",
        governance_decision="REVIEW",
    )
    assert result.status == "RECORDED"
    assert result.provenance_id.startswith("provenance:")
    assert verify_evidence_digest(observations, digest)


def test_provenance_rejects_tampered_observations():
    observations = {"metric": 1}
    from gnosis.evolution.provenance import canonical_digest
    digest = canonical_digest(observations)
    assert not verify_evidence_digest({"metric": 2}, digest)
    try:
        build_provenance(
            candidate_id="candidate:1",
            parent_state_id="state:1",
            parent_state_digest="parent-digest",
            proposed_state_digest="proposed-digest",
            observations={"metric": 2},
            evidence_digest=digest,
            evaluation_status="PASS",
            shadow_status="NO_BEHAVIORAL_CHANGE",
            invariant_status="PRESERVED",
            governance_decision="REVIEW",
        )
    except ValueError as exc:
        assert "mismatch" in str(exc)
    else:
        raise AssertionError("tampered evidence must be rejected")


def test_provenance_persists_and_reloads_without_activation():
    import sqlite3
    from gnosis.evolution.provenance import canonical_digest
    from gnosis.reflection.persistence import (
        ensure_reflection_schema,
        load_evolution_provenance,
        save_evolution_provenance,
    )
    observations = {"metric": 7}
    provenance = build_provenance(
        candidate_id="candidate:2",
        parent_state_id="state:2",
        parent_state_digest="parent-digest",
        proposed_state_digest="proposed-digest",
        observations=observations,
        evidence_digest=canonical_digest(observations),
        evaluation_status="PASS",
        shadow_status="NO_BEHAVIORAL_CHANGE",
        invariant_status="PRESERVED",
        governance_decision="REVIEW",
    )
    conn = sqlite3.connect(":memory:")
    ensure_reflection_schema(conn)
    stored = save_evolution_provenance(conn, provenance)
    loaded = load_evolution_provenance(conn, stored)
    assert loaded["evidence_digest"] == provenance.evidence_digest
    assert loaded["candidate_id"] == provenance.candidate_id
    assert loaded["status"] == "RECORDED"


def test_crosscheck_accepts_intact_provenance():
    from gnosis.evolution.provenance import (
        canonical_digest,
        crosscheck_provenance,
        execution_id,
    )
    observations = {"metric": 9}
    digest = canonical_digest(observations)
    provenance = build_provenance(
        candidate_id="candidate:3",
        parent_state_id="state:3",
        parent_state_digest="parent-digest",
        proposed_state_digest="proposed-digest",
        observations=observations,
        evidence_digest=digest,
        evaluation_status="PASS",
        shadow_status="NO_BEHAVIORAL_CHANGE",
        invariant_status="PRESERVED",
        governance_decision="REVIEW",
    )
    result = crosscheck_provenance(
        provenance=provenance,
        candidate_id="candidate:3",
        parent_state_id="state:3",
        observations=observations,
        evidence_digest=digest,
        parent_state_digest="parent-digest",
        proposed_state_digest="proposed-digest",
        execution_id_value=execution_id("candidate:3", "state:3", digest, "parent-digest", "proposed-digest"),
        evaluation_status="PASS",
        shadow_status="NO_BEHAVIORAL_CHANGE",
        invariant_status="PRESERVED",
        governance_decision="REVIEW",
    )
    assert result.valid
    assert result.reasons == ()


def test_crosscheck_rejects_chain_mismatch():
    from gnosis.evolution.provenance import canonical_digest, crosscheck_provenance, execution_id
    observations = {"metric": 9}
    digest = canonical_digest(observations)
    provenance = build_provenance(
        candidate_id="candidate:4",
        parent_state_id="state:4",
        parent_state_digest="parent-digest",
        proposed_state_digest="proposed-digest",
        observations=observations,
        evidence_digest=digest,
        evaluation_status="PASS",
        shadow_status="NO_BEHAVIORAL_CHANGE",
        invariant_status="PRESERVED",
        governance_decision="REVIEW",
    )
    result = crosscheck_provenance(
        provenance=provenance,
        candidate_id="candidate:tampered",
        parent_state_id="state:4",
        observations=observations,
        evidence_digest=digest,
        parent_state_digest="parent-digest",
        proposed_state_digest="proposed-digest",
        execution_id_value=execution_id("candidate:tampered", "state:4", digest, "parent-digest", "proposed-digest"),
        evaluation_status="PASS",
        shadow_status="NO_BEHAVIORAL_CHANGE",
        invariant_status="PRESERVED",
        governance_decision="REVIEW",
    )
    assert not result.valid
    assert any("candidate_id mismatch" in reason for reason in result.reasons)


def test_stored_provenance_crosscheck_detects_tampering():
    import sqlite3
    from gnosis.evolution.provenance import canonical_digest
    from gnosis.reflection.persistence import (
        crosscheck_stored_provenance,
        ensure_reflection_schema,
        save_evolution_provenance,
    )
    observations = {"metric": 11}
    digest = canonical_digest(observations)
    provenance = build_provenance(
        candidate_id="candidate:5",
        parent_state_id="state:5",
        parent_state_digest="parent-digest",
        proposed_state_digest="proposed-digest",
        observations=observations,
        evidence_digest=digest,
        evaluation_status="PASS",
        shadow_status="NO_BEHAVIORAL_CHANGE",
        invariant_status="PRESERVED",
        governance_decision="REVIEW",
    )
    conn = sqlite3.connect(":memory:")
    ensure_reflection_schema(conn)
    stored = save_evolution_provenance(conn, provenance)
    assert crosscheck_stored_provenance(conn, stored, observations=observations).valid
    result = crosscheck_stored_provenance(conn, stored, observations={"metric": 999})
    assert not result.valid
    assert any("observation digest mismatch" in reason for reason in result.reasons)


def test_promotion_gate_is_review_only_even_when_eligible():
    from gnosis.evolution.promotion import evaluate_promotion_gate, make_promotion_candidate
    candidate = make_promotion_candidate(
        candidate_id="candidate:6",
        evidence_digest="digest",
        evaluation_status="PASS",
        shadow_status="IMPROVED",
        invariant_status="PRESERVED",
        governance_decision="APPROVE",
    )
    gate = evaluate_promotion_gate(candidate, provenance_valid=True)
    assert gate.eligible
    assert gate.status == "REVIEW_ONLY"
    assert gate.can_activate is False
    assert candidate.can_activate is False


def test_promotion_gate_fails_closed_on_provenance():
    from gnosis.evolution.promotion import evaluate_promotion_gate, make_promotion_candidate
    candidate = make_promotion_candidate(
        candidate_id="candidate:7",
        evidence_digest="digest",
        evaluation_status="PASS",
        shadow_status="NO_BEHAVIORAL_CHANGE",
        invariant_status="PRESERVED",
        governance_decision="APPROVE",
    )
    gate = evaluate_promotion_gate(candidate, provenance_valid=False)
    assert not gate.eligible
    assert "provenance cross-check failed" in gate.reasons


def test_promotion_gate_rejects_unsafe_statuses():
    from gnosis.evolution.promotion import evaluate_promotion_gate, make_promotion_candidate
    candidate = make_promotion_candidate(
        candidate_id="candidate:8",
        evidence_digest="digest",
        evaluation_status="REVIEW",
        shadow_status="BEHAVIOR_CHANGED",
        invariant_status="REGRESSED",
        governance_decision="REJECT",
    )
    gate = evaluate_promotion_gate(candidate, provenance_valid=True)
    assert not gate.eligible
    assert len(gate.reasons) == 4


def test_crosscheck_rejects_state_digest_mismatch():
    from gnosis.evolution.provenance import canonical_digest, crosscheck_provenance, execution_id
    observations = {"metric": 12}
    digest = canonical_digest(observations)
    provenance = build_provenance(
        candidate_id="candidate:state-bind",
        parent_state_id="state:bind",
        parent_state_digest="parent-digest",
        proposed_state_digest="proposed-digest",
        observations=observations,
        evidence_digest=digest,
        evaluation_status="PASS",
        shadow_status="NO_BEHAVIORAL_CHANGE",
        invariant_status="PRESERVED",
        governance_decision="REVIEW",
    )
    result = crosscheck_provenance(
        provenance=provenance,
        candidate_id="candidate:state-bind",
        parent_state_id="state:bind",
        parent_state_digest="wrong-parent",
        proposed_state_digest="proposed-digest",
        observations=observations,
        evidence_digest=digest,
        execution_id_value=execution_id("candidate:state-bind", "state:bind", digest, "wrong-parent", "proposed-digest"),
        evaluation_status="PASS",
        shadow_status="NO_BEHAVIORAL_CHANGE",
        invariant_status="PRESERVED",
        governance_decision="REVIEW",
    )
    assert not result.valid
    assert "parent_state_digest mismatch" in result.reasons


def test_state_content_identity_is_canonical_and_version_independent():
    from gnosis.core.types import State
    a = State(elements={"b": 2, "a": {"x": 1}}, version=1)
    b = State(elements={"a": {"x": 1}, "b": 2}, version=99)
    assert a.content_id == b.content_id
    assert a.state_id != b.state_id


def test_state_content_identity_changes_with_content():
    from gnosis.core.types import State
    a = State(elements={"x": 1})
    b = State(elements={"x": 2})
    assert a.content_id != b.content_id
