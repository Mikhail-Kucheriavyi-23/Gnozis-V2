"""
PATCH defect #1 regression tests — deep immutability.

Each test here is the exact adversarial scenario (A-F) from the PATCH ТЗ
section 2, which previously reproduced v33 defect #8 ("shallow frozen
state"). Before the patch, every one of these either mutated the State's
logical content in place or let a mutable object leak between two
"versions" of State. After the patch, each must fail loudly (TypeError) or
provably leave the original State's content untouched.
"""

import pytest

from gnosis.core import Relation, State


def test_A_nested_dict_mutation_via_accessor_does_not_affect_state():
    s0 = State(elements={"a": {"nested": 1}})
    before_id = s0.state_id
    retrieved = s0.elements  # MappingProxyType, not the caller's original dict

    with pytest.raises(TypeError):
        retrieved["a"]["nested"] = 999  # retrieved["a"] is itself frozen

    assert s0.state_id == before_id
    assert s0.elements["a"]["nested"] == 1


def test_B_direct_top_level_item_assignment_raises_and_state_unchanged():
    s0 = State(elements={"x": 1})
    before_id = s0.state_id

    with pytest.raises(TypeError):
        s0.elements["x"] = 2  # mappingproxy does not support item assignment

    assert s0.state_id == before_id
    assert s0.elements["x"] == 1


def test_C_mutating_nested_object_via_derived_version_does_not_touch_parent():
    s0 = State(elements={"a": {"count": 1}})
    s1 = s0.with_elements({"b": 2})

    with pytest.raises(TypeError):
        s1.elements["a"]["count"] = 999

    assert s0.elements["a"]["count"] == 1
    assert s0.elements == {"a": {"count": 1}}


def test_D_mutating_caller_object_after_passing_it_as_relation_value_has_no_effect():
    shared_list = [1, 2, 3]
    r = Relation(source="x", target="y", relation_type="rel", value=shared_list)
    before_id = r.relation_id

    shared_list.append(999)  # mutate the ORIGINAL object the caller still holds

    assert r.relation_id == before_id
    assert list(r.value) == [1, 2, 3]


def test_E_mutating_retrieved_relation_value_raises_and_relation_unchanged():
    r = Relation(source="x", target="y", relation_type="rel", value=[1, 2, 3])
    before_id = r.relation_id

    # r.value is now a tuple (deep_freeze converts list -> tuple), which has
    # no item-assignment at all; attempting it raises TypeError.
    with pytest.raises(TypeError):
        r.value[0] = 999  # type: ignore[index]

    assert r.relation_id == before_id
    assert r.value == (1, 2, 3)


def test_F_two_state_versions_never_share_a_mutable_substructure():
    s0 = State(elements={"a": {"count": 1}, "shared_list": [1, 2, 3]})
    s1 = s0.with_elements({"b": 2})

    # Adversarial mutation attempts on every nested structure reachable
    # from s1 must fail, proving nothing shared between s0/s1 is mutable —
    # regardless of whether the underlying frozen objects happen to be the
    # same object (`is`) or not. The requirement is "cannot mutate", not
    # "is a different object".
    with pytest.raises(TypeError):
        s1.elements["a"]["count"] = 42
    with pytest.raises(TypeError):
        s1.elements["shared_list"][0] = 42  # tuple: no item assignment

    assert s0.elements["a"]["count"] == 1
    assert s0.elements["shared_list"] == (1, 2, 3)
    assert s1.elements["a"]["count"] == 1
    assert s1.elements["shared_list"] == (1, 2, 3)


def test_set_values_are_frozen_too():
    s0 = State(elements={"tags": {"a", "b", "c"}})
    assert isinstance(s0.elements["tags"], frozenset)
    assert s0.elements["tags"] == frozenset({"a", "b", "c"})


def test_original_mutable_dict_passed_to_constructor_is_not_retained():
    original = {"a": {"nested": 1}}
    s0 = State(elements=original)
    original["a"]["nested"] = 999  # mutate the caller's own object
    original["new_key"] = "should not appear"

    assert s0.elements["a"]["nested"] == 1
    assert "new_key" not in s0.elements
