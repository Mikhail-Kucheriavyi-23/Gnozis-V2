"""Deterministic, authority-free capability hypothesis synthesis."""
from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass
from typing import Sequence

from .gap import GapHypothesis


def _digest(value: object) -> str:
    payload = json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"), default=str)
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()


@dataclass(frozen=True)
class CapabilityHypothesis:
    capability_id: str
    source_gap_id: str
    target_conflicts: tuple[str, ...]
    mechanism: str
    expected_effects: tuple[str, ...]
    possible_side_effects: tuple[str, ...]
    test_strategy: str
    resource_bound: int
    available_operations: tuple[str, ...]
    missing_dependencies: tuple[str, ...] = ()
    provenance_refs: tuple[str, ...] = ()
    counterevidence: tuple[str, ...] = ()
    status: str = "PROPOSED"

    @property
    def can_activate(self) -> bool:
        return False


class CapabilitySynthesizer:
    """Turn a GapHypothesis into bounded capability proposals.

    Templates are intentionally simple for the first runtime milestone.
    """

    def synthesize(
        self,
        gap: GapHypothesis,
        *,
        available_operations: Sequence[str] = (),
        resource_bound: int = 1,
    ) -> tuple[CapabilityHypothesis, ...]:
        if resource_bound < 1 or resource_bound > 20:
            raise ValueError("resource_bound must be in range 1..20")

        operations = tuple(sorted(set(str(x) for x in available_operations)))
        mechanism = "bounded-observation-and-retry"
        required = ("observe", "record")
        missing = tuple(op for op in required if op not in operations)
        capability_id = "capability:" + _digest({
            "gap_id": gap.gap_id,
            "mechanism": mechanism,
            "operations": operations,
            "resource_bound": resource_bound,
        })[:24]
        return (CapabilityHypothesis(
            capability_id=capability_id,
            source_gap_id=gap.gap_id,
            target_conflicts=gap.source_records,
            mechanism=mechanism,
            expected_effects=("reduce recurrence of the source unresolved pattern",),
            possible_side_effects=("additional observation cost", "new evidence may expose a different gap"),
            test_strategy="run bounded sandbox observation against a comparable historical case",
            resource_bound=resource_bound,
            available_operations=operations,
            missing_dependencies=missing,
            provenance_refs=gap.source_records,
            counterevidence=gap.counterevidence,
        ),)
