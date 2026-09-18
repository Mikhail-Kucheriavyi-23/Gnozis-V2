import sqlite3

from gnosis.evolution.provenance import build_provenance, canonical_digest
from gnosis.core.types import State
from gnosis.evolution.recovery import recover_evolution_audit
from gnosis.reflection.persistence import (
    append_evolution_audit,
    ensure_reflection_schema,
    save_evolution_provenance,
)


def _persist(conn):
    observations = {"status": "PASS"}
    state = State(elements={"x": 1})
    p = build_provenance(
        candidate_id="c1", parent_state_id="s1",
        parent_state_digest="pd", proposed_state_digest="sd",
        observations=observations, proposed_state_content_id=state.content_id, evidence_digest=canonical_digest(observations),
        evaluation_status="PASS", shadow_status="NO_BEHAVIORAL_CHANGE",
        invariant_status="PRESERVED", governance_decision="REVIEW",
    )
    pid = save_evolution_provenance(conn, p)
    append_evolution_audit(
        conn, event_type="PROVENANCE", candidate_id=p.candidate_id,
        execution_id=p.execution_id, provenance_id=pid,
        parent_state_digest=p.parent_state_digest,
        proposed_state_digest=p.proposed_state_digest,
        evidence_digest=p.evidence_digest, payload={"status": "PASS"},
    )
    return pid, observations, state


def test_recovery_rebuilds_and_verifies_persisted_chain():
    conn = sqlite3.connect(":memory:")
    ensure_reflection_schema(conn)
    pid, observations, state = _persist(conn)
    report = recover_evolution_audit(conn, provenance_id=pid, observations=observations, proposed_state=state)
    assert report.recovered_records == 1
    assert report.chain_valid
    assert report.replay_valid
    assert report.expected_digest == report.actual_digest
    assert report.reasons == ()


def test_recovery_fails_closed_when_provenance_is_missing():
    conn = sqlite3.connect(":memory:")
    ensure_reflection_schema(conn)
    append_evolution_audit(
        conn, event_type="SANDBOX", candidate_id="c1", execution_id="e1",
        payload={"status": "PASS"},
    )
    report = recover_evolution_audit(conn)
    assert not report.chain_valid
    assert "provenance identity required for trusted recovery" in report.reasons


def test_recovery_fails_closed_on_tampered_persisted_chain():
    conn = sqlite3.connect(":memory:")
    ensure_reflection_schema(conn)
    pid, observations, state = _persist(conn)
    conn.execute("UPDATE evolution_audit SET evidence_digest='tampered'")
    report = recover_evolution_audit(conn, provenance_id=pid, observations=observations, proposed_state=state)
    assert not report.chain_valid
    assert report.reasons


def test_recovery_replay_equality_fails_closed_on_changed_observations():
    conn = sqlite3.connect(":memory:")
    ensure_reflection_schema(conn)
    pid, observations, state = _persist(conn)
    changed = {"status": "CHANGED"}
    report = recover_evolution_audit(conn, provenance_id=pid, observations=changed, proposed_state=state)
    assert report.chain_valid is False
    assert report.replay_valid is False
    assert report.expected_digest != report.actual_digest
    assert "observation digest mismatch" in report.reasons


def test_recovery_replay_fails_when_persisted_state_identity_is_tampered():
    conn = sqlite3.connect(":memory:")
    ensure_reflection_schema(conn)
    pid, observations, state = _persist(conn)
    conn.execute("UPDATE evolution_provenance SET proposed_state_digest='tampered'")
    report = recover_evolution_audit(conn, provenance_id=pid, observations=observations, proposed_state=state)
    assert not report.replay_valid
    assert report.reasons


def test_recovery_rejects_tampered_canonical_evolution_identity():
    conn = sqlite3.connect(":memory:")
    ensure_reflection_schema(conn)
    pid, observations, state = _persist(conn)
    conn.execute("UPDATE evolution_provenance SET evolution_identity='tampered'")
    report = recover_evolution_audit(conn, provenance_id=pid, observations=observations, proposed_state=state)
    assert not report.replay_valid
    assert "recovery evolution identity mismatch" in report.reasons


def test_recovery_rejects_legacy_provenance_without_identity():
    conn = sqlite3.connect(":memory:")
    ensure_reflection_schema(conn)
    pid, observations, state = _persist(conn)
    conn.execute("UPDATE evolution_provenance SET evolution_identity=''")
    report = recover_evolution_audit(conn, provenance_id=pid, observations=observations, proposed_state=state)
    assert not report.replay_valid
    assert "legacy provenance identity is unverified" in report.reasons


def test_recovery_rejects_tampered_proposed_state_content_identity():
    conn = sqlite3.connect(":memory:")
    ensure_reflection_schema(conn)
    observations = {"status": "PASS"}
    state = State(elements={"x": 2})
    p = build_provenance(
        candidate_id="c2", parent_state_id="s2", parent_state_digest="pd2",
        proposed_state_digest="sd2", proposed_state_content_id=state.content_id,
        observations=observations, evidence_digest=canonical_digest(observations),
        evaluation_status="PASS", shadow_status="NO_BEHAVIORAL_CHANGE",
        invariant_status="PRESERVED", governance_decision="REVIEW",
    )
    pid = save_evolution_provenance(conn, p)
    append_evolution_audit(
        conn, event_type="PROVENANCE", candidate_id=p.candidate_id,
        execution_id=p.execution_id, provenance_id=pid,
        parent_state_digest=p.parent_state_digest,
        proposed_state_digest=p.proposed_state_digest,
        evidence_digest=p.evidence_digest, payload={"status": "PASS"},
    )
    conn.execute("UPDATE evolution_provenance SET proposed_state_content_id='tampered'")
    report = recover_evolution_audit(conn, provenance_id=pid, observations=observations, proposed_state=state)
    assert not report.replay_valid
    assert "evolution identity mismatch" in " ".join(report.reasons)
