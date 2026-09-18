"""Core type contracts for GNOSIS 2.0."""

from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass, field
from enum import Enum
from types import MappingProxyType
from typing import Any, Mapping, Sequence


def deep_freeze(value: Any) -> Any:
    if isinstance(value, Mapping):
        return MappingProxyType({k: deep_freeze(v) for k, v in value.items()})
    if isinstance(value, (list, tuple)):
        return tuple(deep_freeze(v) for v in value)
    if isinstance(value, (set, frozenset)):
        return frozenset(deep_freeze(v) for v in value)
    return value


def _canonical(value: Any) -> Any:
    if isinstance(value, Mapping):
        return {k: _canonical(v) for k, v in value.items()}
    if isinstance(value, (list, tuple)):
        return [_canonical(v) for v in value]
    if isinstance(value, (set, frozenset)):
        return sorted((_canonical(v) for v in value), key=repr)
    return value


def _stable_hash(payload: Any) -> str:
    canonical_payload = _canonical(payload)
    blob = json.dumps(canonical_payload, sort_keys=True, default=str).encode("utf-8")
    return hashlib.sha256(blob).hexdigest()


@dataclass(frozen=True)
class Relation:
    source: str
    target: str
    relation_type: str
    value: Any = None

    def __post_init__(self) -> None:
        object.__setattr__(self, "value", deep_freeze(self.value))

    @property
    def relation_id(self) -> str:
        return _stable_hash({"source": self.source, "target": self.target, "relation_type": self.relation_type, "value": self.value})


@dataclass(frozen=True)
class State:
    elements: Mapping[str, Any] = field(default_factory=dict)
    relations: Sequence[Relation] = field(default_factory=tuple)
    version: int = 0

    def __post_init__(self) -> None:
        object.__setattr__(self, "elements", deep_freeze(dict(self.elements)))
        object.__setattr__(self, "relations", tuple(self.relations))

    @property
    def state_id(self) -> str:
        return _stable_hash({"elements": self.elements, "relations": [r.relation_id for r in self.relations], "version": self.version})

    @property
    def content_id(self) -> str:
        return _stable_hash({"elements": self.elements, "relations": sorted(r.relation_id for r in self.relations)})

    def with_elements(self, elements: Mapping[str, Any]) -> "State":
        merged = dict(self.elements)
        merged.update(elements)
        return State(elements=merged, relations=self.relations, version=self.version + 1)

    def with_relations(self, relations: Sequence[Relation]) -> "State":
        merged = tuple(self.relations) + tuple(relations)
        return State(elements=self.elements, relations=merged, version=self.version + 1)


@dataclass(frozen=True)
class Candidate:
    parent_state_id: str
    proposed_state: State
    origin: str
    seed: int | None = None

    @property
    def candidate_id(self) -> str:
        return _stable_hash({"parent_state_id": self.parent_state_id, "proposed_state_content_id": self.proposed_state.content_id, "origin": self.origin, "seed": self.seed})


    def binding_digest(self, parent_state_digest: str) -> str:
        if not parent_state_digest:
            raise ValueError("parent state digest is required")
        return _stable_hash({
            "candidate_id": self.candidate_id,
            "parent_state_digest": parent_state_digest,
            "proposed_state_content_id": self.proposed_state.content_id,
        })


@dataclass(frozen=True)
class TestResult:
    passed: bool
    reasons: Sequence[str] = field(default_factory=tuple)

    def __post_init__(self) -> None:
        if not isinstance(self.passed, bool):
            raise TypeError(f"TestResult.passed must be an actual bool (True/False), got {type(self.passed).__name__}: {self.passed!r}")
        object.__setattr__(self, "reasons", tuple(self.reasons))


class StopReason(str, Enum):
    BUDGET_EXHAUSTED = "budget_exhausted"
    INVALID_STATE = "invalid_state"
    INVARIANT_VIOLATION = "invariant_violation"
    UNAUTHORIZED_CAPABILITY = "unauthorized_capability"
    CRYPTOGRAPHIC_FAILURE = "cryptographic_failure"
    CORRUPTED_MEMORY = "corrupted_memory"
    EXPLICIT_STOP = "explicit_stop"
    SAFETY_THRESHOLD = "safety_threshold"
    EXECUTION_TIMEOUT = "execution_timeout"
    UNRECOVERABLE_ERROR = "unrecoverable_error"


@dataclass(frozen=True)
class TransitionRecord:
    """Audit record with explicit provenance of the Test rule/policy used."""

    from_state_id: str
    to_state_id: str
    candidate_id: str
    test_result: TestResult
    accepted: bool
    reason: str
    test_rule_id: str = "test-rule:unspecified"

    def __post_init__(self) -> None:
        if self.accepted is not self.test_result.passed:
            raise ValueError(
                "TransitionRecord.accepted must exactly match test_result.passed"
            )
        if not self.reason.strip():
            raise ValueError("TransitionRecord.reason must not be empty")


Agent = None
Instance = None
Capability = None
Message = None
MemoryRecord = None
