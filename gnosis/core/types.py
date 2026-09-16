"""
Core type contracts for GNOSIS 2.0.

Per spec section 7 (TYPE SAFETY): State, Relation, Candidate, Transition,
TestResult, Capability, Agent, Instance, Message, MemoryRecord, AuditEvent
must not be mixed without explicit conversion.

PATCH (audit remediation) — DEFECT #1: REAL DEEP IMMUTABILITY
--------------------------------------------------------------------------
The original Phase 1 slice used `frozen=True` and a single-level
`dict(...)`/`tuple(...)` copy in `__post_init__`. That only blocks
*reassigning* `state.elements`; it does NOT block mutating the dict/list/set
CONTENTS reachable through `.elements`, `.relations`, or `Relation.value`.
An adversarial audit proved this reproduces v33 defect #8 ("shallow frozen
state") — see docs/PATCH_NOTES.md and tests/test_immutability_adversarial.py.

Fix: `deep_freeze()` recursively converts every Mapping into a
`types.MappingProxyType` wrapping a freshly-built dict of recursively-frozen
values, every list/tuple into a tuple of recursively-frozen values, and
every set/frozenset into a frozenset of recursively-frozen values. This
happens once, at construction time, on a *copy* of whatever the caller
passed in — so:
  - the caller's original object is never retained internally (mutating it
    afterward cannot affect the frozen State/Relation);
  - the exposed `.elements`/`.relations`/`Relation.value` are themselves
    immutable containers, so `state.elements['x'] = 1` raises TypeError
    instead of silently succeeding;
  - two State "versions" produced via `with_elements`/`with_relations` may
    share references to already-frozen (hence safe-to-share) substructures,
    but never share a mutable one.

Scalars (str/int/float/bool/None) and already-immutable custom types are
passed through unchanged — this does not attempt to freeze arbitrary
third-party mutable objects, only the dict/list/set cases the audit
actually exercised (PATCH section 2 scope).

STATUS: IMPLEMENTED (State, Relation, Candidate, TestResult, TransitionRecord)
STATUS: THEORETICAL (Agent, Instance, Capability, Message, MemoryRecord —
        reserved names, NOT type contracts; see note near bottom and STATUS.md)
"""

from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass, field
from enum import Enum
from types import MappingProxyType
from typing import Any, Mapping, Sequence


def deep_freeze(value: Any) -> Any:
    """Recursively convert dict/list/tuple/set into immutable equivalents,
    built from fresh containers (never the caller's original objects).
    Leaves everything else (scalars, already-frozen dataclasses, etc.)
    untouched."""
    if isinstance(value, Mapping):
        return MappingProxyType({k: deep_freeze(v) for k, v in value.items()})
    if isinstance(value, (list, tuple)):
        return tuple(deep_freeze(v) for v in value)
    if isinstance(value, (set, frozenset)):
        return frozenset(deep_freeze(v) for v in value)
    return value


def _canonical(value: Any) -> Any:
    """Convert a (possibly deep-frozen) value into plain JSON-serializable
    builtins for hashing. MappingProxyType/frozenset are not directly
    JSON-serializable, so this is required even after deep_freeze.
    `json.dumps(..., sort_keys=True)` handles key ordering for nested
    dicts recursively, so this function does not need to sort dict keys
    itself — only sets need explicit ordering, since JSON has no set type
    and set iteration order is not content-stable."""
    if isinstance(value, Mapping):
        return {k: _canonical(v) for k, v in value.items()}
    if isinstance(value, (list, tuple)):
        return [_canonical(v) for v in value]
    if isinstance(value, (set, frozenset)):
        return sorted((_canonical(v) for v in value), key=repr)
    return value


def _stable_hash(payload: Any) -> str:
    """Deterministic content hash used for state/relation identity.

    Canonicalizes first (handles MappingProxyType/frozenset from
    deep_freeze), then serializes with sorted keys so identical logical
    content always hashes the same way, independent of dict insertion
    order or frozen-container wrapping.
    """
    canonical_payload = _canonical(payload)
    blob = json.dumps(canonical_payload, sort_keys=True, default=str).encode("utf-8")
    return hashlib.sha256(blob).hexdigest()


@dataclass(frozen=True)
class Relation:
    """An immutable relation between two entities in X.

    source/target are opaque identifiers into the State's element space.
    `relation_type` and `value` carry the semantic content. `value` is
    deep-frozen at construction (PATCH defect #1, scenarios D/E): mutating
    an object the caller passed as `value` after construction, or mutating
    whatever `.value` returns, cannot change this Relation.
    """

    source: str
    target: str
    relation_type: str
    value: Any = None

    def __post_init__(self) -> None:
        object.__setattr__(self, "value", deep_freeze(self.value))

    @property
    def relation_id(self) -> str:
        return _stable_hash(
            {
                "source": self.source,
                "target": self.target,
                "relation_type": self.relation_type,
                "value": self.value,
            }
        )


@dataclass(frozen=True)
class State:
    """Immutable Core State: Psi = (X, R).

    X (elements) is a mapping of element_id -> arbitrary JSON-serializable
    payload. R (relations) is a tuple of Relation objects. State is the
    single source of truth (spec section 1) — nothing else is allowed to
    silently become a second authoritative state.

    Both `elements` and `relations` are deep-frozen at construction (PATCH
    defect #1): nested dict/list/set content is copied into fresh
    MappingProxyType/tuple/frozenset structures, so no caller-held
    reference — before or after construction — can mutate this State's
    logical content.
    """

    elements: Mapping[str, Any] = field(default_factory=dict)
    relations: Sequence[Relation] = field(default_factory=tuple)
    version: int = 0

    def __post_init__(self) -> None:
        object.__setattr__(self, "elements", deep_freeze(dict(self.elements)))
        object.__setattr__(self, "relations", tuple(self.relations))

    @property
    def state_id(self) -> str:
        """Full identity, including `version`. Used for parent-matching
        (Engine.step checks candidate.parent_state_id == state.state_id) —
        deliberately version-sensitive, unlike `content_id` below."""
        return _stable_hash(
            {
                "elements": self.elements,
                "relations": [r.relation_id for r in self.relations],
                "version": self.version,
            }
        )

    @property
    def content_id(self) -> str:
        """PATCH defect #2 (identity/no-op evolution): content-only hash,
        deliberately EXCLUDING `version` and independent of relation
        ordering (relation ids are sorted before hashing). Two States with
        identical elements/relations but different `version` have the SAME
        content_id — this is exactly the case the meaningful-change
        invariant (invariants.py::check_meaningful_change) rejects."""
        return _stable_hash(
            {
                "elements": self.elements,
                "relations": sorted(r.relation_id for r in self.relations),
            }
        )

    def with_elements(self, elements: Mapping[str, Any]) -> "State":
        merged = dict(self.elements)
        merged.update(elements)
        return State(elements=merged, relations=self.relations, version=self.version + 1)

    def with_relations(self, relations: Sequence[Relation]) -> "State":
        merged = tuple(self.relations) + tuple(relations)
        return State(elements=self.elements, relations=merged, version=self.version + 1)


@dataclass(frozen=True)
class Candidate:
    """A proposed next state, not yet committed to Core.

    Per spec section 4 (SAFE SELF-MODIFICATION), a Candidate can NEVER
    mutate Core directly. It must pass through Test -> Verification ->
    Commit (see evolution.py / verification.py).
    """

    parent_state_id: str
    proposed_state: State
    origin: str  # e.g. "generator:default", "agent:<id>", "user:<id>"
    seed: int | None = None

    @property
    def candidate_id(self) -> str:
        return _stable_hash(
            {
                "parent_state_id": self.parent_state_id,
                "proposed_state_id": self.proposed_state.state_id,
                "origin": self.origin,
                "seed": self.seed,
            }
        )


@dataclass(frozen=True)
class TestResult:
    """Result of running Test(candidate) -> bool, with reasons kept for audit.

    PATCH defect #3 (STRICT Test(candidate) -> bool): `passed` is validated
    at construction to be an actual `bool`. Python's `bool` is a subclass of
    `int`, so this checks `isinstance(passed, bool)` specifically —
    `isinstance(1, bool)` is False even though `isinstance(True, int)` is
    True — which correctly rejects 1/0/"yes"/[]/None while accepting only
    True/False. This was previously unenforced (a plain type hint), which
    let `TestResult(passed="yes")` be constructed silently.
    """

    passed: bool
    reasons: Sequence[str] = field(default_factory=tuple)

    def __post_init__(self) -> None:
        if not isinstance(self.passed, bool):
            raise TypeError(
                f"TestResult.passed must be an actual bool (True/False), "
                f"got {type(self.passed).__name__}: {self.passed!r}"
            )
        object.__setattr__(self, "reasons", tuple(self.reasons))


class StopReason(str, Enum):
    """Hard stop conditions (spec section 9).

    PATCH defect #8: this enum still names all 10 conditions from the
    spec, but only two are actually ever raised in this slice. See
    STATUS.md / docs/PATCH_NOTES.md for the explicit IMPLEMENTED-NOW vs
    RESERVED split — declaring a name here is not a claim that it fires.
    """

    # --- IMPLEMENTED NOW (actually raised by gnosis/core/evolution.py) ---
    BUDGET_EXHAUSTED = "budget_exhausted"
    INVALID_STATE = "invalid_state"

    # --- RESERVED / FUTURE (named per spec section 9; no code path raises
    #     these yet — they require layers (Capability, Identity, Memory,
    #     Bridge) that don't exist in this slice) ---
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
    """Audit-relevant record of a single committed state transition."""

    from_state_id: str
    to_state_id: str
    candidate_id: str
    test_result: TestResult
    accepted: bool
    reason: str


# --- Forward-declared, NOT implemented in this slice (see STATUS.md) -------
# PATCH defect #10: these are RESERVED NAMES, not type contracts. Assigning
# `None` does not create a Protocol/ABC usable for isinstance checks or type
# hints — it is only a placeholder so later phases (Agent Layer, Instances,
# Memory, Federation, Bridge) don't have to invent these names from
# scratch. The previous docstring here overstated this as a "fixed
# contract to implement against"; that language has been removed per the
# audit finding. No Agent/Capability/Message architecture is added in this
# PATCH (out of scope per PATCH sections 10/14).
Agent = None            # RESERVED NAME — Phase 5, not a type
Instance = None         # RESERVED NAME — Phase 3 (real Instance lives in gnosis.instances.instance.Instance)
Capability = None       # RESERVED NAME — Phase 5/8, not a type
Message = None          # RESERVED NAME — Phase 5/7, not a type
MemoryRecord = None     # RESERVED NAME — Phase 4, not a type
