"""
Resource budget enforcement (spec section 8).

No autonomous cycle runs unbounded. Every atomic operation has a cost;
when the budget is exhausted, execution stops hard (StopReason.BUDGET_EXHAUSTED).

STATUS: IMPLEMENTED
"""

from __future__ import annotations

from dataclasses import dataclass

DEFAULT_BUDGET = 20


class BudgetExhaustedError(RuntimeError):
    """Raised when an operation is attempted with insufficient budget."""


@dataclass
class Budget:
    total: int = DEFAULT_BUDGET
    spent: int = 0

    @property
    def remaining(self) -> int:
        return self.total - self.spent

    def charge(self, cost: int) -> None:
        if cost < 0:
            raise ValueError("operation cost cannot be negative")
        if self.remaining - cost < 0:
            raise BudgetExhaustedError(
                f"insufficient budget: remaining={self.remaining}, cost={cost}"
            )
        self.spent += cost

    def exhausted(self) -> bool:
        return self.remaining <= 0
