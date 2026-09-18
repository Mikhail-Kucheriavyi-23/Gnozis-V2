import sqlite3

from gnosis.evolution.chain_verifier import verify_persisted_chain
from gnosis.evolution.provenance import EvidenceProvenance, build_provenance, canonical_digest
from gnosis.reflection.persistence import append_evolution_audit, ensure_reflection_schema, save_evolution_provenance, list_evolution_audit


def test_independent_verifier_accepts_persisted_chain():
    conn = sqlite3.connect(":memory:")
    ensure_reflection_schema(conn)
    observations = {"result": "ok"}
    p = build_provenance(
        candidate_id="c", parent_state_id="s", parent_state_digest="pd",
        proposed_state_digest="sd", observations=observations,
        evidence_digest=canonical_digest(observations),
        evaluation_status="PASS", shadow_status="NO_BEHAVIORAL_CHANGE",
        invariant_status="PRESERVED", governance_decision="REVIEW",
    )
    pid = save_evolution_provenance(conn, p)
    append_evolution_audit(
        conn, event_type="EVOLUTION_RECORDED", candidate_id="c", execution_id=p.execution_id,
        provenance_id=pid, parent_state_digest="pd", proposed_state_digest="sd",
        evidence_digest=p.evidence_digest, payload={"status": "RECORDED"},
    )
    rows = list_evolution_audit(conn)
    provenance_row = {
        "provenance_id": pid, "execution_id": p.execution_id, "candidate_id": "c",
        "parent_state_id": "s", "parent_state_digest": "pd",
        "proposed_state_digest": "sd", "evidence_digest": p.evidence_digest,
        "evaluation_status": "PASS", "shadow_status": "NO_BEHAVIORAL_CHANGE",
        "invariant_status": "PRESERVED", "governance_decision": "REVIEW",
        "status": "RECORDED",
    }
    audit_rows = [row.__dict__ for row in rows]
    result = verify_persisted_chain(provenance_row, audit_rows, observations=observations)
    assert result.valid, result.reasons


def test_independent_verifier_fails_closed_on_tampered_persisted_data():
    observations = {"result": "ok"}
    provenance = {
        "provenance_id": "provenance:wrong",
        "execution_id": "e", "candidate_id": "c", "parent_state_id": "s",
        "parent_state_digest": "pd", "proposed_state_digest": "sd",
        "evidence_digest": canonical_digest(observations),
        "evaluation_status": "PASS", "shadow_status": "NO_BEHAVIORAL_CHANGE",
        "invariant_status": "PRESERVED", "governance_decision": "REVIEW",
        "status": "RECORDED",
    }
    result = verify_persisted_chain(provenance, [], observations=observations)
    assert not result.valid
    assert "audit chain missing" in result.reasons


def test_persisted_provenance_carries_canonical_evolution_identity():
    conn = sqlite3.connect(":memory:")
    ensure_reflection_schema(conn)
    observations = {"result": "ok"}
    p = build_provenance(
        candidate_id="c", parent_state_id="s", parent_state_digest="pd",
        proposed_state_digest="sd", observations=observations,
        evidence_digest=canonical_digest(observations), evaluation_status="PASS",
        shadow_status="NO_BEHAVIORAL_CHANGE", invariant_status="PRESERVED",
        governance_decision="REVIEW",
    )
    from gnosis.reflection.persistence import save_evolution_provenance, load_evolution_provenance
    pid = save_evolution_provenance(conn, p)
    row = load_evolution_provenance(conn, pid)
    assert row["evolution_identity"] == p.evolution_identity
