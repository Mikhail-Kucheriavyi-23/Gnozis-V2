from dataclasses import dataclass

from gnosis.reflection.diagnostic_artifact import build_artifact, serialize_artifact
from gnosis.reflection.self_diagnostic import SelfDiagnostic


@dataclass(frozen=True)
class _DiagnosticReport:
    findings: tuple = ()
    proposals: tuple = ()


def test_artifact_is_read_only_and_machine_readable():
    diagnostic = SelfDiagnostic(
        report=_DiagnosticReport(),
        causal_candidates=(),
        refined_proposals=(),
        limitations=("example limitation",),
    )
    artifact = build_artifact(diagnostic, artifact_id="SELF-DIAGNOSTIC-0001")
    assert artifact["kind"] == "SELF-DIAGNOSTIC"
    assert artifact["artifact_id"] == "SELF-DIAGNOSTIC-0001"
    assert artifact["authority"] == "READ_ONLY"
    assert artifact["limitations"] == ["example limitation"]

    serialized = serialize_artifact(diagnostic, artifact_id="SELF-DIAGNOSTIC-0001")
    assert '"SELF-DIAGNOSTIC-0001"' in serialized
    assert '"READ_ONLY"' in serialized
