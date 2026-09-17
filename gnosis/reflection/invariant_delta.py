"""Invariant-delta analysis for isolated shadow evaluations.

This module compares the invariant surface of candidates accepted by the
active rule with the surface accepted by a shadow rule. It does not activate
proposals, mutate Core, or decide governance. Invariants are evaluated using
the existing canonical Core invariant registry/functions.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Mapping, Sequence

from gnosis.core.invariants import InvariantCheck, run_invariants
from gnosis.core.types import Candidate, State

from .shadow import ShadowEvaluation


@dataclass(frozen=True)
class InvariantDelta:
    """Read-only comparison of invariant outcomes across active/shadow sets."""

    preserved: tuple[str, ...]
    violated: tuple[str, ...]
    improved: tuple[str, ...]
    unknown: tuple[str, ...]
    active_violations: Mapping[str, int]
    shadow_violations: Mapping[str, int]
    provenance: str = "reflection-invariant-delta"

    @property
    def status(self) -> str:
        if self.violated:
            return "VIOLATION"
        if self.improved:
            return "IMPROVED"
        if self.unknown:
            return "INSUFFICIENT_EVIDENCE"
        return "PRESERVED"


def _profile(
    candidates: Mapping[str, Candidate],
    accepted_ids: set[str],
    current_states: Mapping[str, State],
    invariants: Sequence[InvariantCheck],
) -> tuple[dict[str, int], set[str]]:
    violations: dict[str, int] = {}
    unknown: set[str] = set()
    for candidate_id in accepted_ids:
        candidate = candidates.get(candidate_id)
        if candidate is None:
            unknown.add(candidate_id)
            continue
        current = current_states.get(candidate.parent_state_id)
        if current is None:
            unknown.add(candidate_id)
            continue
        for result in run_invariants(current, candidate, invariants):
            if not result.ok:
                violations[result.name] = violations.get(result.name, 0) + 1
    return violations, unknown


def analyze_invariant_delta(
    evaluation: ShadowEvaluation,
    candidates: Sequence[Candidate],
    current_states: Mapping[str, State],
    invariants: Sequence[InvariantCheck],
) -> InvariantDelta:
    """Compare invariant violations among active- and shadow-accepted candidates."""
    candidate_map = {candidate.candidate_id: candidate for candidate in candidates}
    active_ids = {case.candidate_id for case in evaluation.cases if case.active.passed}
    shadow_ids = {case.candidate_id for case in evaluation.cases if case.shadow.passed}

    active_violations, active_unknown = _profile(
        candidate_map, active_ids, current_states, invariants
    )
    shadow_violations, shadow_unknown = _profile(
        candidate_map, shadow_ids, current_states, invariants
    )

    violated = tuple(sorted(
        name for name, count in shadow_violations.items()
        if count > active_violations.get(name, 0)
    ))
    improved = tuple(sorted(
        name for name, count in active_violations.items()
        if count > shadow_violations.get(name, 0) and name not in violated
    ))
    preserved = tuple(sorted(
        name for name in set(active_violations) | set(shadow_violations)
        if active_violations.get(name, 0) == shadow_violations.get(name, 0)
    ))

    unknown = tuple(sorted(active_unknown | shadow_unknown))
    return InvariantDelta(
        preserved=preserved,
        violated=violated,
        improved=improved,
        unknown=unknown,
        active_violations=dict(sorted(active_violations.items())),
        shadow_violations=dict(sorted(shadow_violations.items())),
    )
