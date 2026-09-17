from gnosis.reflection.context import ContextClaim, ContextStatus, ContextVersion


def test_context_claim_requires_provenance_to_be_self_descriptive() -> None:
    claim = ContextClaim(
        claim_id="c1",
        statement="AI_CONTEXT is part of the self-description surface",
        status=ContextStatus.HYPOTHESIS,
        provenance=("architecture-decision",),
    )
    assert claim.self_descriptive is True


def test_context_version_separates_verified_and_unresolved_claims() -> None:
    version = ContextVersion(
        version_id="ctx1",
        claims=(
            ContextClaim("v", "verified claim", ContextStatus.VERIFIED, ("test",)),
            ContextClaim("h", "open hypothesis", ContextStatus.HYPOTHESIS, ("proposal",)),
            ContextClaim("o", "observed claim", ContextStatus.OBSERVED, ("observation",)),
        ),
    )
    assert [c.claim_id for c in version.verified_claims()] == ["v"]
    assert [c.claim_id for c in version.unresolved_claims()] == ["h", "o"]
