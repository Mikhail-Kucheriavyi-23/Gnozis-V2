"""Stable, read-only self-diagnostic artifact serialization."""
from __future__ import annotations

import json
from dataclasses import asdict, is_dataclass
from typing import Any

from .self_diagnostic import SelfDiagnostic


def _plain(value: Any) -> Any:
    if is_dataclass(value):
        return {k: _plain(v) for k, v in asdict(value).items()}
    if isinstance(value, tuple):
        return [_plain(v) for v in value]
    if isinstance(value, list):
        return [_plain(v) for v in value]
    if isinstance(value, dict):
        return {str(k): _plain(v) for k, v in value.items()}
    return value


def build_artifact(diagnostic: SelfDiagnostic, *, artifact_id: str) -> dict[str, Any]:
    """Build a machine-readable diagnostic artifact without granting mutation authority."""
    return {
        "artifact_id": artifact_id,
        "kind": "SELF-DIAGNOSTIC",
        "version": 1,
        "report": _plain(diagnostic.report),
        "causal_candidates": _plain(diagnostic.causal_candidates),
        "refined_proposals": _plain(diagnostic.refined_proposals),
        "limitations": list(diagnostic.limitations),
        "authority": "READ_ONLY",
    }


def serialize_artifact(diagnostic: SelfDiagnostic, *, artifact_id: str) -> str:
    return json.dumps(
        build_artifact(diagnostic, artifact_id=artifact_id),
        ensure_ascii=False,
        sort_keys=True,
        indent=2,
    )
