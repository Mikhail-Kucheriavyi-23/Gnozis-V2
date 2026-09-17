"""Generate a reproducible controlled evidence corpus through real persistence."""
from __future__ import annotations

import json
import tempfile
from dataclasses import asdict, is_dataclass
from pathlib import Path

from gnosis.core import Candidate, Engine, State
from gnosis.instances.instance import Instance
from gnosis.reflection.diagnostic_artifact import serialize_artifact
from gnosis.reflection.self_diagnostic import diagnose
from gnosis.storage import (
    connect,
    load_transition_records,
    persist_transition,
    save_instance,
    verify_durable_graph,
)

OUT = Path(__file__).parent / "SELF-DIAGNOSTIC-0001"


def _plain(value):
    if is_dataclass(value):
        return {k: _plain(v) for k, v in asdict(value).items()}
    if isinstance(value, (tuple, list)):
        return [_plain(v) for v in value]
    if isinstance(value, dict):
        return {str(k): _plain(v) for k, v in value.items()}
    return value


def _test(state: State, candidate: Candidate) -> bool:
    return "bad" not in candidate.proposed_state.elements


def generate() -> None:
    """Execute, persist, recover, and diagnose a controlled Core scenario."""
    instance = Instance.create_root("diagnostic-corpus", State(elements={"n": 0}))
    instance.engine = Engine(
        state=instance.engine.state,
        budget=instance.engine.budget,
        test_fn=_test,
        test_rule_id="test-rule:diagnostic-policy",
    )

    with tempfile.TemporaryDirectory(prefix="gnozis-diagnostic-") as tmp:
        db_path = Path(tmp) / "diagnostic.sqlite"
        conn = connect(db_path)
        save_instance(conn, instance)

        for i in range(3):
            candidate = Candidate(
                parent_state_id=instance.engine.state.state_id,
                proposed_state=State(elements={"bad": i}, version=1),
                origin="diagnostic-corpus:repeated-rejection",
                seed=i,
            )
            record = instance.engine.step(candidate)
            persist_transition(conn, instance, candidate, record, actor="diagnostic-corpus")

        accepted = Candidate(
            parent_state_id=instance.engine.state.state_id,
            proposed_state=State(elements={"n": 1}, version=1),
            origin="diagnostic-corpus:accepted-transition",
            seed=99,
        )
        record = instance.engine.step(accepted)
        persist_transition(conn, instance, accepted, record, actor="diagnostic-corpus")

        verify_durable_graph(conn)
        recovered_history = load_transition_records(conn, instance.instance_id)
        assert len(recovered_history) == 4
        assert sum(not record.accepted for record in recovered_history) == 3
        assert sum(record.accepted for record in recovered_history) == 1
        assert all(record.test_rule_id == "test-rule:diagnostic-policy" for record in recovered_history)

        diagnostic = diagnose(recovered_history)
        OUT.mkdir(parents=True, exist_ok=True)
        (OUT / "transitions.json").write_text(
            json.dumps([_plain(t) for t in recovered_history], ensure_ascii=False, indent=2, sort_keys=True),
            encoding="utf-8",
        )
        (OUT / "metadata.json").write_text(
            json.dumps(
                {
                    "artifact_id": "SELF-DIAGNOSTIC-0001",
                    "scenario": "controlled-persisted-runtime-history",
                    "transition_count": len(recovered_history),
                    "accepted_count": 1,
                    "rejected_count": 3,
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
