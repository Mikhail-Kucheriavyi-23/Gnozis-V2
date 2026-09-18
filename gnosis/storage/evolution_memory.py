"""Append-only durable memory of endogenous evolution attempts."""
from __future__ import annotations
from dataclasses import dataclass
import hashlib
import json
from typing import Any
from .repositories import canonical_json, utc_now, StorageCorruptionError

@dataclass(frozen=True)
class EvolutionMemoryRecord:
    memory_id: str
    instance_id: str
    candidate_id: str
    transition_id: str
    state_id: str
    proposal_id: str | None
    outcome: str
    evidence: tuple[str, ...]
    created_at: str

    @property
    def digest(self) -> str:
        return hashlib.sha256(canonical_json({
            "memory_id": self.memory_id, "instance_id": self.instance_id,
            "candidate_id": self.candidate_id, "transition_id": self.transition_id,
            "state_id": self.state_id, "proposal_id": self.proposal_id,
            "outcome": self.outcome, "evidence": self.evidence,
            "created_at": self.created_at,
        }).encode()).hexdigest()


def append_evolution_memory(conn, *, instance_id: str, candidate_id: str, transition_id: str,
                            state_id: str, proposal_id: str | None, outcome: str,
                            evidence: tuple[str, ...] | list[str], created_at: str | None = None) -> EvolutionMemoryRecord:
    if outcome not in {"accepted", "rejected", "inconclusive"}:
        raise ValueError("invalid evolution memory outcome")
    evidence_tuple = tuple(str(x) for x in evidence)
    timestamp = created_at or utc_now()
    raw = {"instance_id": instance_id, "candidate_id": candidate_id, "transition_id": transition_id,
           "state_id": state_id, "proposal_id": proposal_id, "outcome": outcome,
           "evidence": evidence_tuple, "created_at": timestamp}
    memory_id = hashlib.sha256(canonical_json(raw).encode()).hexdigest()
    record = EvolutionMemoryRecord(memory_id, instance_id, candidate_id, transition_id, state_id,
                                   proposal_id, outcome, evidence_tuple, timestamp)
    conn.execute("""INSERT INTO evolution_memory(memory_id,instance_id,candidate_id,transition_id,state_id,proposal_id,outcome,evidence,created_at)
                    VALUES(?,?,?,?,?,?,?,?,?)
                    ON CONFLICT(memory_id) DO NOTHING""",
                 (record.memory_id, record.instance_id, record.candidate_id, record.transition_id,
                  record.state_id, record.proposal_id, record.outcome, canonical_json(record.evidence), record.created_at))
    return record


def load_evolution_memory(conn, instance_id: str, *, limit: int = 100) -> tuple[EvolutionMemoryRecord, ...]:
    if limit < 1:
        raise ValueError("limit must be >= 1")
    rows = conn.execute("""SELECT memory_id,instance_id,candidate_id,transition_id,state_id,proposal_id,outcome,evidence,created_at
                          FROM evolution_memory WHERE instance_id=? ORDER BY created_at,memory_id LIMIT ?""", (instance_id, limit)).fetchall()
    records=[]
    for row in rows:
        try: evidence=tuple(json.loads(row[7]))
        except (TypeError, json.JSONDecodeError) as exc: raise StorageCorruptionError("malformed evolution memory evidence") from exc
        rec=EvolutionMemoryRecord(*row[:7], evidence, row[8])
        if rec.memory_id != rec.digest:
            raise StorageCorruptionError("evolution memory digest mismatch")
        records.append(rec)
    return tuple(records)
