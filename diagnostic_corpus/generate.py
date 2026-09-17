"""Generate a reproducible controlled evidence corpus from actual Core execution."""
from __future__ import annotations

import json
from dataclasses import asdict, is_dataclass
from pathlib import Path

from gnosis.core.engine import Engine
from gnosis.reflection.self_diagnostic import diagnose
from gnosis.reflection.diagnostic_artifact import serialize_artifact

OUT = Path(__file__).parent / "SELF-DIAGNOSTIC-0001"


def _plain(value):
    if is_dataclass(value):
        return {k: _plain(v) for k, v in asdict(value).items()}
    if isinstance(value, tuple):
        return [_plain(v) for v in value]
    if isinstance(value, list):
        return [_plain(v) for v in value]
    if isinstance(value, dict):
        return {str(k): _plain(v) for k, v in value.items()}
    return value


def generate() -> None:
    """Execute the controlled Core scenario and export its actual history.

    The generator is intentionally read-only with respect to the repository:
    it writes only the diagnostic corpus directory.
    """
    engine = Engine()
    # The workflow remains the canonical executable scenario. This generator
    # deliberately consumes the resulting runtime history rather than hand
    # authoring TransitionRecord values.
    diagnostic = diagnose(engine.history)
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / "transitions.json").write_text(
        json.dumps([_plain(t) for t in engine.history], ensure_ascii=False, indent=2, sort_keys=True),
        encoding="utf-8",
    )
    (OUT / "metadata.json").write_text(
        json.dumps(
            {
                "artifact_id": "SELF-DIAGNOSTIC-0001",
                "scenario": "controlled-runtime-history",
                "transition_count": len(engine.history),
                "generation": "diagnostic_corpus/generate.py",
            },
            ensure_ascii=False,
            indent=2,
            sort_keys=True,
        ),
        encoding="utf-8",
    )
    (OUT / "diagnostic.json").write_text(
        serialize_artifact(diagnostic, artifact_id="SELF-DIAGNOSTIC-0001"),
        encoding="utf-8",
    )


if __name__ == "__main__":
    generate()
