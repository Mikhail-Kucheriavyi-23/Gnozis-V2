"""
PATCH defect #3 regression tests — strict Test(candidate) -> bool.

Exact adversarial scenario from the PATCH ТЗ section 4: TestResult(passed=
"yes") previously constructed without error. Now every non-bool value
listed in the ТЗ must raise TypeError at construction, and only True/False
are accepted.

NOTE: written as individual test functions rather than
@pytest.mark.parametrize, because this sandbox has no network access to
install real pytest, and the offline fallback runner used to verify this
PATCH only shims `pytest.raises` (see AUDIT.md / PHASE_PATCH_AUDIT.md).
Under a real pytest install these run identically, just without the
parametrize grouping.
"""

import pytest

from gnosis.core import TestResult


def test_true_is_accepted():
    assert TestResult(passed=True).passed is True


def test_false_is_accepted():
    assert TestResult(passed=False).passed is False


def test_int_one_rejected():
    with pytest.raises(TypeError):
        TestResult(passed=1)


def test_int_zero_rejected():
    with pytest.raises(TypeError):
        TestResult(passed=0)


def test_string_yes_rejected():
    with pytest.raises(TypeError):
        TestResult(passed="yes")


def test_string_true_rejected():
    """Even the string "True" must be rejected — only the actual bool True."""
    with pytest.raises(TypeError):
        TestResult(passed="True")


def test_empty_list_rejected():
    with pytest.raises(TypeError):
        TestResult(passed=[])


def test_none_rejected():
    with pytest.raises(TypeError):
        TestResult(passed=None)


def test_float_rejected():
    with pytest.raises(TypeError):
        TestResult(passed=1.0)


def test_arbitrary_object_rejected():
    with pytest.raises(TypeError):
        TestResult(passed=object())


def test_int_one_specifically_rejected_despite_bool_being_int_subclass():
    """The nuance called out explicitly in the PATCH ТЗ: bool is a subclass
    of int, so isinstance(x, int) would wrongly accept 1/0. The fix must
    check isinstance(x, bool) specifically, which correctly distinguishes
    the literal `1` (type int) from `True` (type bool)."""
    with pytest.raises(TypeError):
        TestResult(passed=1)
    assert TestResult(passed=True).passed is True
