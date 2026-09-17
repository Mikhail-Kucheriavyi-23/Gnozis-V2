from gnosis.reflection.context import ContextClaim, ContextStatus, ContextVersion
from gnosis.reflection.context_verifier import verify_context


def test_context_verifier_classifies_claims() -> None:
    version = ContextVersion(
        version_id="ctx1",
        claims=(
            ContextClaim("v", "verified", ContextStatus.VERIFIED, ("test",)),
            ContextClaim("h", "hypothesis", ContextStatus.HYPOTHESIS, ("proposal",)),
            ContextClaim("r", "rejected", ContextStatus.REJECTED, ("test",)),
        ),
    )
    result = verify_context(version)
    assert result.coherent is True
    assert result.verified == ("v",)
    assert result.unresolved == ("h",)
    assert result.rejected == ("r",)
