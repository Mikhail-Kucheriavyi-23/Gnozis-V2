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
