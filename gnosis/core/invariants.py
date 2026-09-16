"""
Protected Core invariants (spec section 5).

Every candidate transition must pass ALL registered invariants before it can
be committed. This module implements the subset of invariants that are
actually checkable at this phase: Core State integrity, type safety on the
transition, and transition validity (no orphan relations).

Capability enforcement, audit integrity, memory isolation, identity
integrity and cryptographic verification are NOT implemented here — they
belong to later phases (Agent/Memory/Federation) and are listed as
THEORETICAL in STATUS.md. This module must not claim to check them.

STATUS: IMPLEMENTED (state_integrity, transition_validity, monotonic_version,
        meaningful_change — the last one added by PATCH to close audit
        defect #2, identity/no-op transitions)
STATUS: MISSING (capability_enforcement, identity_integrity,
        cryptographic_verification, memory_isolation, audit_integrity —
        no Agent/Memory/Identity layer exists yet in this slice)

PATCH — INVARIANT-FAILURE SEMANTICS (audit finding, section 7 of PATCH ТЗ):
A failing invariant here (any of the four in DEFAULT_INVARIANTS) results in
Engine.step() REJECTING that one candidate and continuing to run normally
(Variant A). It does NOT raise StopCondition/StopReason.INVARIANT_VIOLATION
and does NOT halt the Engine. This is a deliberate, now-documented choice,
distinct from:
  - corruption of the current authoritative State (no detection exists —
    MISSING);
  - a security/capability failure (no Capability layer exists — MISSING);
  - an unrecoverable engine failure (no such condition is raised — MISSING).
These four are NOT the same thing and must not be conflated. Only
candidate-local invariant failure (this module) is implemented.
"""

from __future__ import annotations

from typing import Callable, Sequence

from .types import Candidate, State

InvariantCheck = Callable[[State, Candidate], "InvariantResult"]


class InvariantResult:
    def __init__(self, ok: bool, name: str, detail: str = ""):
        self.ok = ok
        self.name = name
        self.detail = detail

    def __repr__(self) -> str:
        status = "OK" if self.ok else "VIOLATION"
        return f"<Invariant {self.name}: {status} {self.detail}>".strip()


def check_state_integrity(current: State, candidate: Candidate) -> InvariantResult:
    """The candidate must actually descend from the current state."""
    if candidate.parent_state_id != current.state_id:
        return InvariantResult(
            False,
            "state_integrity",
            f"candidate parent {candidate.parent_state_id} != current {current.state_id}",
        )
    return InvariantResult(True, "state_integrity")


def check_transition_validity(current: State, candidate: Candidate) -> InvariantResult:
    """Every relation in the proposed state must reference an existing element.

    Prevents a transition from silently introducing dangling references,
    which would corrupt the single source of truth (spec section 1).
    """
    proposed = candidate.proposed_state
    known_elements = set(proposed.elements.keys())
    for rel in proposed.relations:
        if rel.source not in known_elements or rel.target not in known_elements:
            return InvariantResult(
                False,
                "transition_validity",
                f"relation {rel.relation_id} references unknown element(s)",
            )
    return InvariantResult(True, "transition_validity")


def check_monotonic_version(current: State, candidate: Candidate) -> InvariantResult:
    """Proposed state's version must strictly increase from current."""
    if candidate.proposed_state.version <= current.version:
        return InvariantResult(
            False,
            "monotonic_version",
            f"proposed version {candidate.proposed_state.version} <= current {current.version}",
        )
    return InvariantResult(True, "monotonic_version")


def check_meaningful_change(current: State, candidate: Candidate) -> InvariantResult:
    """PATCH defect #2 (identity/no-op evolution, v33 recidive #3).

    The audit proved that a candidate whose `elements`/`relations` are
    byte-for-byte identical to the current state, but whose `version` is
    bumped by 1, passed every previous invariant and got committed as a
    "real" state transition — even though nothing about the mathematical
    content of Psi=(X,R) actually changed.

    This invariant compares `State.content_id`, which is deliberately
    version-independent and relation-order-independent (see
    types.py::State.content_id). A candidate is rejected here iff its
    proposed state's content is identical to the current state's content,
    regardless of what `version` claims. Changing `elements` OR `relations`
    (even a single key, even relation ordering that changes the actual
    relation set) makes content_id differ and this check passes.
    """
    if candidate.proposed_state.content_id == current.content_id:
        return InvariantResult(
            False,
            "meaningful_change",
            "proposed state has identical content to current state "
            "(identity/no-op transition — only version or non-content "
            "metadata differs)",
        )
    return InvariantResult(True, "meaningful_change")


DEFAULT_INVARIANTS: Sequence[InvariantCheck] = (
    check_state_integrity,
    check_transition_validity,
    check_monotonic_version,
    check_meaningful_change,
)


def run_invariants(
    current: State,
    candidate: Candidate,
    invariants: Sequence[InvariantCheck] = DEFAULT_INVARIANTS,
) -> list[InvariantResult]:
    return [inv(current, candidate) for inv in invariants]


def all_pass(results: Sequence[InvariantResult]) -> bool:
    return all(r.ok for r in results)
