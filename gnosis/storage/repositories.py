from __future__ import annotations

import hashlib
import json
import sqlite3
from datetime import datetime, timezone
from collections.abc import Mapping
from typing import Any, Iterable

from gnosis.core import Candidate, Relation, State, TestResult, TransitionRecord
from gnosis.instances.instance import Instance, InstanceStatus
from .database import transaction


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def _plain(value: Any) -> Any:
    if isinstance(value, Mapping):
        return {str(k): _plain(v) for k, v in value.items()}
    if isinstance(value, (list, tuple)):
        return [_plain(v) for v in value]
    if isinstance(value, (set, frozenset)):
        return sorted((_plain(v) for v in value), key=repr)
    return value


def canonical_json(value: Any) -> str:
    return json.dumps(_plain(value), ensure_ascii=False, sort_keys=True, separators=(",", ":"))


def state_payload(state: State) -> str:
    return canonical_json({"elements": state.elements, "version": state.version})


def _decode_payload(payload: str) -> dict[str, Any]:
    value = json.loads(payload)
    if not isinstance(value, dict) or "elements" not in value or "version" not in value:
        raise ValueError("invalid state payload")
    return value


def save_state(conn: sqlite3.Connection, state: State, *, created_at: str | None = None) -> None:
    created_at = created_at or utc_now()
    payload = state_payload(state)
    existing = conn.execute("SELECT version, payload FROM states WHERE state_id = ?", (state.state_id,)).fetchone()
    if existing:
        if existing[0] != state.version or existing[1] != payload:
            raise ValueError("state_id collision or tampered state payload")
        return
    conn.execute(
        "INSERT INTO states(state_id, version, payload, created_at) VALUES (?, ?, ?, ?)",
        (state.state_id, state.version, payload, created_at),
    )
    for order, relation in enumerate(state.relations):
        conn.execute(
            "INSERT INTO relations(state_id, relation_order, relation_id, source_id, target_id, relation_type, value, created_at) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
            (state.state_id, order, relation.relation_id, relation.source, relation.target,
             relation.relation_type, None if relation.value is None else canonical_json(relation.value), created_at),
        )


def load_state(conn: sqlite3.Connection, state_id: str) -> State:
    row = conn.execute("SELECT version, payload FROM states WHERE state_id = ?", (state_id,)).fetchone()
    if row is None:
        raise ValueError(f"state not found: {state_id}")
    payload = _decode_payload(row[1])
    relations: list[Relation] = []
    for rel in conn.execute(
        "SELECT relation_id, source_id, target_id, relation_type, value FROM relations WHERE state_id = ? ORDER BY relation_order",
        (state_id,),
    ):
        value = None if rel[4] is None else json.loads(rel[4])
        relation = Relation(source=rel[1], target=rel[2], relation_type=rel[3], value=value)
        if relation.relation_id != rel[0]:
            raise ValueError(f"relation hash mismatch: {rel[0]}")
        relations.append(relation)
    state = State(elements=payload["elements"], relations=relations, version=payload["version"])
    if state.state_id != state_id:
        raise ValueError(f"state hash mismatch: {state_id}")
    return state


def save_candidate(conn: sqlite3.Connection, candidate: Candidate, *, created_at: str | None = None) -> None:
    created_at = created_at or utc_now()
    save_state(conn, load_state(conn, candidate.parent_state_id) if _exists(conn, "states", candidate.parent_state_id) else _state_from_candidate_parent(candidate), created_at=created_at)
    save_state(conn, candidate.proposed_state, created_at=created_at)
    conn.execute(
        "INSERT OR IGNORE INTO candidates(candidate_id, parent_state_id, candidate_state_id, origin, seed, created_at) VALUES (?, ?, ?, ?, ?, ?)",
        (candidate.candidate_id, candidate.parent_state_id, candidate.proposed_state.state_id, candidate.origin, candidate.seed, created_at),
    )
    row = conn.execute("SELECT parent_state_id, candidate_state_id, origin, seed FROM candidates WHERE candidate_id = ?", (candidate.candidate_id,)).fetchone()
    if row and tuple(row) != (candidate.parent_state_id, candidate.proposed_state.state_id, candidate.origin, candidate.seed):
        raise ValueError("candidate_id collision")


def _state_from_candidate_parent(candidate: Candidate) -> State:
    raise ValueError("parent state must be persisted before candidate")


def _exists(conn: sqlite3.Connection, table: str, key: str) -> bool:
    return conn.execute(f"SELECT 1 FROM {table} WHERE state_id = ?", (key,)).fetchone() is not None


def load_candidate(conn: sqlite3.Connection, candidate_id: str) -> Candidate:
    row = conn.execute("SELECT parent_state_id, candidate_state_id, origin, seed FROM candidates WHERE candidate_id = ?", (candidate_id,)).fetchone()
    if row is None:
        raise ValueError(f"candidate not found: {candidate_id}")
    candidate = Candidate(row[0], load_state(conn, row[1]), row[2], row[3])
    if candidate.candidate_id != candidate_id:
        raise ValueError("candidate hash mismatch")
    return candidate


def transition_id(record: TransitionRecord) -> str:
    raw = canonical_json({"candidate_id": record.candidate_id, "from": record.from_state_id, "to": record.to_state_id, "accepted": record.accepted, "reasons": record.test_result.reasons})
    return hashlib.sha256(raw.encode()).hexdigest()


def _audit_hash(event: dict[str, Any]) -> str:
    return hashlib.sha256(canonical_json(event).encode()).hexdigest()


def append_audit(conn: sqlite3.Connection, *, actor: str, action: str, resource: str, result: str, timestamp: str | None = None) -> str:
    timestamp = timestamp or utc_now()
    row = conn.execute("SELECT sequence, event_hash FROM audit_events ORDER BY sequence DESC LIMIT 1").fetchone()
    sequence = 1 if row is None else int(row[0]) + 1
    prev_hash = "0" * 64 if row is None else row[1]
    event_id = hashlib.sha256(canonical_json({"sequence": sequence, "actor": actor, "action": action, "resource": resource, "result": result, "timestamp": timestamp}).encode()).hexdigest()
    event = {"event_id": event_id, "sequence": sequence, "actor": actor, "action": action, "resource": resource, "result": result, "timestamp": timestamp, "prev_hash": prev_hash}
    event_hash = _audit_hash(event)
    conn.execute(
        "INSERT INTO audit_events(event_id, sequence, actor, action, resource, result, timestamp, prev_hash, event_hash) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)",
        (event_id, sequence, actor, action, resource, result, timestamp, prev_hash, event_hash),
    )
    return event_hash


def verify_audit_chain(conn: sqlite3.Connection) -> tuple[int, str]:
    previous = "0" * 64
    last = (0, previous)
    for row in conn.execute("SELECT event_id, sequence, actor, action, resource, result, timestamp, prev_hash, event_hash FROM audit_events ORDER BY sequence"):
        if row[1] != last[0] + 1 or row[7] != previous:
            raise ValueError("audit chain link or sequence mismatch")
        event = {"event_id": row[0], "sequence": row[1], "actor": row[2], "action": row[3], "resource": row[4], "result": row[5], "timestamp": row[6], "prev_hash": row[7]}
        if _audit_hash(event) != row[8]:
            raise ValueError(f"audit event hash mismatch: {row[0]}")
        previous = row[8]
        last = (row[1], previous)
    return last


def save_instance(conn: sqlite3.Connection, instance: Instance, *, actor: str | None = None) -> None:
    with transaction(conn):
        save_state(conn, instance.engine.state)
        conn.execute(
            "INSERT INTO instances(instance_id, parent_instance_id, owner_id, current_state_id, generation, status, created_at) VALUES (?, ?, ?, ?, ?, ?, ?)",
            (instance.instance_id, instance.parent_instance_id, instance.owner_id, instance.engine.state.state_id, instance.generation, instance.status.value, instance.created_at),
        )
        append_audit(conn, actor=actor or instance.owner_id, action="instance.create", resource=instance.instance_id, result="accepted")


def load_instance(conn: sqlite3.Connection, instance_id: str) -> Instance:
    row = conn.execute("SELECT instance_id, owner_id, current_state_id, parent_instance_id, generation, status, created_at FROM instances WHERE instance_id = ?", (instance_id,)).fetchone()
    if row is None:
        raise ValueError(f"instance not found: {instance_id}")
    from gnosis.core import Engine
    instance = Instance(instance_id=row[0], owner_id=row[1], engine=Engine(load_state(conn, row[2])), parent_instance_id=row[3], generation=row[4], status=InstanceStatus(row[5]), created_at=row[6])
    return instance


def persist_transition(conn: sqlite3.Connection, instance: Instance, candidate: Candidate, record: TransitionRecord, *, actor: str) -> None:
    if candidate.parent_state_id != record.from_state_id:
        raise ValueError("candidate parent does not match transition source")
    with transaction(conn):
        db_instance = load_instance(conn, instance.instance_id)
        if db_instance.engine.state.state_id != record.from_state_id:
            raise ValueError("stale instance head")
        save_candidate(conn, candidate)
        tid = transition_id(record)
        conn.execute(
            "INSERT INTO transitions(transition_id, candidate_id, from_state_id, to_state_id, accepted, reasons, created_at) VALUES (?, ?, ?, ?, ?, ?, ?)",
            (tid, candidate.candidate_id, record.from_state_id, record.to_state_id, int(record.accepted), canonical_json(record.test_result.reasons), utc_now()),
        )
        append_audit(conn, actor=actor, action="transition.commit" if record.accepted else "transition.reject", resource=instance.instance_id, result="accepted" if record.accepted else "rejected")
        if record.accepted:
            conn.execute("UPDATE instances SET current_state_id = ? WHERE instance_id = ?", (record.to_state_id, instance.instance_id))
