"""Generate a reproducible controlled evidence corpus through real persistence."""
from __future__ import annotations

import json
import tempfile
from dataclasses import asdict, is_dataclass
from pathlib import Path

from gnosis.core import Candidate, State, TestResult
from gnosis.core.engine import Engine
from gnosis.instances.instance import Instance
from gnosis.reflection.self_diagnostic import diagnose
from gnosis.reflection.diagnostic_artifact import serialize_artifact
from gnosis.storage import connect, persist_transition, recover_instance, save_candidate, save_instance, verify_durable_graph

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


def _test(state: State, candidate: Candidate) -> TestResult:
    if "bad" in candidate.proposed_state.elements:
        return TestResult(False, ("policy:bad-element",))
    return TestResult(True, ())


def generate() -> None:
    """Execute, persist, recover, and diagnose a controlled Core scenario."""
    instance = Instance.create_root("diagnostic-corpus", State(elements={"n": 0}))
    instance.engine = Engine(
        state=instance.engine.state,
        budget=instance.engine.budget,
        test_fn=_test,
        test_rule_id="test-rule:diagnostic-policy",
    )

    with tempfile.TemporaryDirectory() as tmp:
        db_path = Path(tmp) / "diagnostic.sqlite"
        conn = connect(db_path)
        save_instance(conn, instance)

        for i in range(3):
            candidate = Candidate(
                parent_state_id=instance.engine.state.state_id,
                proposed_state=State(elements={"bad": i}),
                origin="diagnostic-corpus:repeated-rejection",
                seed=i,
            )
            save_candidate(conn, instance, candidate)
            record = instance.engine.step(candidate)
            persist_transition(conn, instance, candidate, record, actor="diagnostic-corpus")

        accepted = Candidate(
            parent_state_id=instance.engine.state.state_id,
            proposed_state=State(elements={"n": 1}),
            origin="diagnostic-corpus:accepted-transition",
            seed=99,
        )
        save_candidate(conn, instance, accepted)
        record = instance.engine.step(accepted)
        persist_transition(conn, instance, accepted, record, actor="diagnostic-corpus")

        verify_durable_graph(conn)
        recovered = recover_instance(conn, instance.instance_id)
        history = recovered.engine.history
        diagnostic = diagnose(history)

        OUT.mkdir(parents=True, exist_ok=True)
        (OUT / "transitions.json").write_text(
            json.dumps([_plain(t) for t in history], ensure_ascii=False, indent=2, sort_keys=True),
            encoding="utf-8",
        )
        (OUT / "metadata.json").write_text(
            json.dumps(
                {
                    "artifact_id": "SELF-DIAGNOSTIC-0001",
                    "scenario": "controlled-persisted-runtime-history",
                    "transition_count": len(history),
                    "generation": "diagnostic_corpus/generate.py",
                    "persistence": "sqlite_round_trip",
                    "test_rule_id": "test-rule:diagnostic-policy",
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
        conn.close()


if __name__ == "__main__":
    generate()
