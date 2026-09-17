import pytest

from gnosis.reflection.rules import RuleMetadata, RuleRegistry


def _rule(version: int) -> RuleMetadata:
    return RuleMetadata(
        rule_id="test-rule:diagnostic-policy",
        rule_version=version,
        rule_type="test_policy",
        scope="diagnostic-corpus",
        implementation_ref="gnosis.core.engine:Engine.test_fn",
        spec_ref="docs/CORE_REFLECTION_R1_TASK.md",
        invariant_refs=("transition-validity",),
    )


def test_registry_enforces_unique_rule_versions_and_exposes_latest():
    registry = RuleRegistry()
    registry.register(_rule(1))
    registry.register(_rule(2))

    assert registry.versions("test-rule:diagnostic-policy") == (1, 2)
    assert registry.latest("test-rule:diagnostic-policy").rule_version == 2
    assert registry.get("test-rule:diagnostic-policy", 1).rule_version == 1

    with pytest.raises(ValueError):
        registry.register(_rule(2))


def test_registry_rejects_invalid_versions_and_unknown_rules():
    registry = RuleRegistry()
    with pytest.raises(ValueError):
        registry.register(_rule(0))
    with pytest.raises(KeyError):
        registry.get("missing-rule", 1)
    with pytest.raises(KeyError):
        registry.latest("missing-rule")


def test_registry_is_descriptive_and_has_no_activation_api():
    registry = RuleRegistry()
    registry.register(_rule(1))
    assert not hasattr(registry, "activate")
    assert registry.snapshot() == (_rule(1),)
