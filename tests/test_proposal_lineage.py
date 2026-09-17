from gnosis.reflection.proposal_lineage import evolve_proposal


def test_initial_proposal_has_no_parent():
    result = evolve_proposal(
        finding_id="finding:1",
        current_proposal_id="proposal:1",
        prior_proposals=(),
        evidence_refs=("transition:1",),
    )
    assert result.parent_proposal_id is None
    assert result.relation == "INITIAL"


def test_rejected_proposal_creates_refinement_lineage():
    result = evolve_proposal(
        finding_id="finding:1",
        current_proposal_id="proposal:2",
        prior_proposals=({
            "finding_id": "finding:1",
            "proposal_id": "proposal:1",
            "status": "REJECTED",
        },),
        evidence_refs=("transition:2",),
    )
    assert result.parent_proposal_id == "proposal:1"
    assert result.relation == "REFINEMENT_AFTER_REJECTION"


def test_unresolved_proposal_requires_additional_evidence():
    result = evolve_proposal(
        finding_id="finding:1",
        current_proposal_id="proposal:2",
        prior_proposals=({
            "finding_id": "finding:1",
            "proposal_id": "proposal:1",
            "status": "PROPOSED",
        },),
    )
    assert result.relation == "REVISION_OF_UNRESOLVED"
    assert "additional evidence" in result.rationale
