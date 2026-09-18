"""Deterministic endogenous capability-gap detection.

This module is deliberately outside Core. It derives hypotheses from supplied
history/evidence but has no mutation or authorization API.
"""
from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass
from typing import Any, Mapping, Sequence


def _digest(value: Any) -> str:
    payload = json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"), default=str)
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()


@dataclass(frozen=True)
class GapHypothesis:
    gap_id: str
    source_records: tuple[str, ...]
    trigger_kind: str
    description: str
    conditions: tuple[str, ...] = ()
    counterevidence: tuple[str, ...] = ()
    status: str = "HYPOTHESIS"
    provenance: str = "endogenous-gap-detector"


class GapDetector:
    """Find repeated unresolved patterns without naming the desired capability."""

    def detect(
        self,
        *,
        history: Sequence[Mapping[str, Any]],
        evidence: Sequence[Mapping[str, Any]] = (),
        tensions: Sequence[Mapping[str, Any]] = (),
        forecast_errors: Sequence[Mapping[str, Any]] = (),
        minimum_repetitions: int = 2,
    ) -> tuple[GapHypothesis, ...]:
        if minimum_repetitions < 2:
            raise ValueError("minimum_repetitions must be >= 2")

        records = tuple(history) + tuple(evidence) + tuple(tensions) + tuple(forecast_errors)
        groups: dict[str, list[tuple[str, Mapping[str, Any]]]] = {}
        for index, record in enumerate(records):
            kind = str(record.get("kind", record.get("type", "unknown")))
            status = str(record.get("status", record.get("outcome", ""))).upper()
            reason = str(record.get("reason", record.get("pattern", record.get("error", "")))).strip()
            if not reason:
                continue
            unresolved = status in {"FAILED", "REJECTED", "REGRESSION", "UNRESOLVED", "INCONCLUSIVE", "ERROR"} or bool(record.get("unresolved", False))
            if not unresolved:
                continue
            key = f"{kind}|{reason}"
            ref = str(record.get("record_id", f"record:{index}"))
            groups.setdefault(key, []).append((ref, record))

        result: list[GapHypothesis] = []
        for key in sorted(groups):
            items = groups[key]
            if len(items) < minimum_repetitions:
                continue
            kind, reason = key.split("|", 1)
            refs = tuple(ref for ref, _ in items)
            raw = {"kind": kind, "reason": reason, "source_records": refs}
            gap_id = "gap:" + _digest(raw)[:24]
            counter = tuple(str(item.get("counterevidence", "")) for _, item in items if item.get("counterevidence"))
            result.append(
                GapHypothesis(
                    gap_id=gap_id,
                    source_records=refs,
                    trigger_kind=kind,
                    description=f"Repeated unresolved pattern: {reason}",
                    conditions=(f"pattern_kind={kind}", f"minimum_repetitions={minimum_repetitions}"),
                    counterevidence=counter,
                )
            )
        return tuple(result)


def history_from_persisted_transitions(records: Sequence[Any]) -> tuple[dict[str, Any], ...]:
    """Convert canonical TransitionRecord objects into detector observations.

    This adapter is read-only: it does not reconstruct or mutate Core state.
    The detector consumes only explicit transition evidence and preserves the
    transition candidate/state identities as source references.
    """
    observations: list[dict[str, Any]] = []
    for record in records:
        accepted = bool(getattr(record, "accepted"))
        test_result = getattr(record, "test_result", None)
        reasons = tuple(getattr(test_result, "reasons", ())) if test_result is not None else ()
        status = "ACCEPTED" if accepted else "REJECTED"
        for reason in reasons or (getattr(record, "reason", "unspecified"),):
            observations.append({
                "record_id": f"transition:{record.candidate_id}:{record.from_state_id}:{record.to_state_id}:{reason}",
                "kind": "transition",
                "status": status,
                "reason": str(reason),
                "candidate_id": record.candidate_id,
                "from_state_id": record.from_state_id,
                "to_state_id": record.to_state_id,
                "test_rule_id": getattr(record, "test_rule_id", "test-rule:unspecified"),
                "unresolved": not accepted,
            })
    return tuple(observations)
