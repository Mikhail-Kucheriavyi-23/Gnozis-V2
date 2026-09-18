from gnosis.evolution.provenance import build_provenance, verify_evidence_digest


def test_provenance_accepts_matching_evidence_digest():
    observations = {"metric": 1, "nested": {"ok": True}}
    from gnosis.evolution.provenance import canonical_digest
    digest = canonical_digest(observations)
    result = build_provenance(
        candidate_id="candidate:1",
        parent_state_id="state:1",
        observations=observations,
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
