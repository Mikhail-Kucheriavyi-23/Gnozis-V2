"""End-to-end read-only gate for canonical Core -> persistence -> reflection evidence."""
from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from gnosis.storage import recover_instance, verify_durable_graph

from .diagnostic_artifact import build_artifact
from .persistence import reflection_id
from .runtime import reflect_with_history
from .self_diagnostic import diagnose


@dataclass(frozen=True)
class ReflectionGateResult:
    passed: bool
    instance_id: str
    transition_count: int
    durable_graph_verified: bool
    recovery_state_id: str
    report_id: str
    artifact: dict[str, Any]
    reasons: tuple[str, ...] = ()


def run_reflection_gate(engine: Any, conn: Any, instance_id: str, *, minimum_repetitions: int = 2) -> ReflectionGateResult:
    """Verify that one canonical execution history reaches durable reflection evidence.

    This function is observational only: it does not commit Core state, issue authority,
    activate proposals, or modify rules/invariants.
    """
    reasons: list[str] = []
    history = tuple(getattr(engine, "history", ()))
    if not history:
        reasons.append("canonical Core history is empty")

    try:
        durable = verify_durable_graph(conn)
        durable_ok = instance_id in durable
    except Exception as exc:
        durable_ok = False
        reasons.append(f"durable graph verification failed: {type(exc).__name__}")

    try:
        recovered = recover_instance(conn, instance_id)
        recovery_state_id = recovered.engine.state.state_id
    except Exception as exc:
        recovery_state_id = ""
        reasons.append(f"recovery failed: {type(exc).__name__}")

    if history and recovery_state_id and recovery_state_id != engine.state.state_id:
        reasons.append("recovered state does not match canonical engine state")

    try:
        cumulative = reflect_with_history(engine, conn, minimum_repetitions=minimum_repetitions)
        report = cumulative.current
        diagnostic = diagnose(history, minimum_repetitions=minimum_repetitions)
        artifact = build_artifact(diagnostic, artifact_id=reflection_id(report))
        report_id = reflection_id(report)
    except Exception as exc:
        report_id = ""
        artifact = {}
        reasons.append(f"reflection evidence generation failed: {type(exc).__name__}")

    if not durable_ok:
        reasons.append("instance is not proven durable")
    if artifact.get("authority") != "READ_ONLY":
        reasons.append("diagnostic artifact is not explicitly read-only")

    return ReflectionGateResult(
        passed=not reasons,
        instance_id=instance_id,
        transition_count=len(history),
        durable_graph_verified=durable_ok,
        recovery_state_id=recovery_state_id,
        report_id=report_id,
        artifact=artifact,
        reasons=tuple(reasons),
    )
