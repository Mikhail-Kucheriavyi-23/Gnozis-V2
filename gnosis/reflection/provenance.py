"""Conservative attribution of observations to Core Test rules.

Provenance is evidence, not proof of causality. A reflection pass may attribute
an observed rejection to the exact Test rule identifier recorded by Core, but
must not infer deeper causal ownership when the Core evidence does not expose it.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Sequence

from gnosis.core.types import TransitionRecord


@dataclass(frozen=True)
class RuleAttribution:
    rule_id: str
    transition_ids: tuple[str, ...]
    evidence_refs: tuple[str, ...]
    confidence: str
    basis: str


def attribute_rule(
    transitions: Sequence[TransitionRecord],
    transition_ids: Sequence[str],
) -> tuple[RuleAttribution, ...]:
    """Attribute selected transition evidence to recorded Test rule IDs.

    Only exact provenance recorded on TransitionRecord is used. Multiple rules
    produce separate attributions; no causal ranking is invented.
    """
    wanted = set(transition_ids)
    grouped: dict[str, list[str]] = {}
    for index, transition in enumerate(transitions):
        transition_id = f"transition:{index}:{transition.candidate_id}"
        if transition_id not in wanted:
            continue
        grouped.setdefault(transition.test_rule_id, []).append(transition_id)

    result: list[RuleAttribution] = []
    for rule_id, ids in sorted(grouped.items()):
        confidence = "EXACT_RECORDED_PROVENANCE" if rule_id != "test-rule:unspecified" else "UNSPECIFIED"
        basis = (
            "Core TransitionRecord explicitly recorded the Test rule identifier."
            if confidence != "UNSPECIFIED"
            else "Core transition does not expose a specific Test rule identifier."
        )
        result.append(
            RuleAttribution(
                rule_id=rule_id,
                transition_ids=tuple(ids),
                evidence_refs=tuple(ids),
                confidence=confidence,
                basis=basis,
            )
        )
    return tuple(result)
