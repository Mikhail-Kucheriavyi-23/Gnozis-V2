"""Versioned, read-only metadata registry for reflection-visible rules."""
from __future__ import annotations

from dataclasses import dataclass
from typing import Mapping


@dataclass(frozen=True)
class RuleMetadata:
    rule_id: str
    rule_version: int
    rule_type: str
    scope: str
    implementation_ref: str
    spec_ref: str
    invariant_refs: tuple[str, ...] = ()
    provenance: str = "reflection-registry"
    status: str = "ACTIVE"


class RuleRegistry:
    """In-memory registry for immutable rule metadata.

    Registry operations only describe rules. They do not execute, activate,
    replace, or mutate any Core rule.
    """

    def __init__(self, rules: Mapping[tuple[str, int], RuleMetadata] | None = None):
        self._rules = dict(rules or {})

    def register(self, rule: RuleMetadata) -> RuleMetadata:
        key = (rule.rule_id, rule.rule_version)
        if key in self._rules:
            raise ValueError(f"rule version already registered: {rule.rule_id}:v{rule.rule_version}")
        if rule.rule_version < 1:
            raise ValueError("rule_version must be >= 1")
        self._rules[key] = rule
        return rule

    def get(self, rule_id: str, rule_version: int) -> RuleMetadata:
        try:
            return self._rules[(rule_id, rule_version)]
        except KeyError as exc:
            raise KeyError(f"unknown rule version: {rule_id}:v{rule_version}") from exc

    def latest(self, rule_id: str) -> RuleMetadata:
        matches = [rule for (rid, _), rule in self._rules.items() if rid == rule_id]
        if not matches:
            raise KeyError(f"unknown rule: {rule_id}")
        return max(matches, key=lambda rule: rule.rule_version)

    def versions(self, rule_id: str) -> tuple[int, ...]:
        return tuple(sorted(version for (rid, version) in self._rules if rid == rule_id))

    def snapshot(self) -> tuple[RuleMetadata, ...]:
        return tuple(self._rules[key] for key in sorted(self._rules))
