import pytest

from gnosis.core import Budget, BudgetExhaustedError


def test_budget_charges_reduce_remaining():
    b = Budget(total=5)
    b.charge(2)
    assert b.remaining == 3
    assert not b.exhausted()


def test_budget_cannot_go_negative():
    # Spec 42: "Budget невозможно отрицательно переполнить"
    b = Budget(total=3)
    b.charge(3)
    assert b.exhausted()
    with pytest.raises(BudgetExhaustedError):
        b.charge(1)
    assert b.remaining == 0  # never negative


def test_negative_cost_rejected():
    b = Budget(total=5)
    with pytest.raises(ValueError):
        b.charge(-1)
