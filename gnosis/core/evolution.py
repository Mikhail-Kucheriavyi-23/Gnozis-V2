"""Evolution engine: Candidate -> Test -> Verification -> Commit."""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Callable, Sequence

from .budget import Budget, BudgetExhaustedError
from .select import SelectionResult, select
from .types import Candidate, State, StopReason, TestResult, TransitionRecord
from .verification import TestFn, default_test, verify

GenerateFn = Callable[[State], Candidate]


class StopCondition(RuntimeError):
    def __init__(self, reason: StopReason, detail: str = ""):
        self.reason = reason
        self.detail = detail
        super().__init__(f"{reason.value}: {detail}".strip())


@dataclass
class Engine:
    state: State
    budget: Budget = field(default_factory=Budget)
    test_fn: TestFn = default_test
    history: list[TransitionRecord] = field(default_factory=list)
    test_rule_id: str = "test-rule:default"

    STEP_COST: int = 1

    def _charge_step(self) -> None:
        if self.budget.exhausted():
            raise StopCondition(StopReason.BUDGET_EXHAUSTED, "no budget remaining before step")
        try:
            self.budget.charge(self.STEP_COST)
        except BudgetExhaustedError as exc:
            raise StopCondition(StopReason.BUDGET_EXHAUSTED, str(exc)) from exc

    def step(self, candidate: Candidate) -> TransitionRecord:
        self._charge_step()
        if candidate.parent_state_id != self.state.state_id:
            raise StopCondition(StopReason.INVALID_STATE, f"candidate parent {candidate.parent_state_id} does not match current state {self.state.state_id}")
        result = verify(self.state, candidate, self.test_fn)
        record = TransitionRecord(
            from_state_id=self.state.state_id,
            to_state_id=candidate.proposed_state.state_id,
            candidate_id=candidate.candidate_id,
            test_result=result,
            accepted=result.passed,
            reason="committed" if result.passed else "rejected: " + "; ".join(result.reasons),
            test_rule_id=self.test_rule_id,
        )
        self.history.append(record)
        if result.passed:
            self.state = candidate.proposed_state
        return record

    def step_select(self, candidates: Sequence[Candidate]) -> TransitionRecord:
        self._charge_step()
        result: SelectionResult = select(self.state, candidates, self.test_fn)
        if result.selected is None:
            reasons: tuple[str, ...]
            if not result.evaluated:
                reasons = ("no candidates supplied to step_select",)
            else:
                reasons = tuple(f"{c.candidate_id}: " + "; ".join(r.reasons) for c, r in result.evaluated)
            failed_result = TestResult(passed=False, reasons=reasons)
            record = TransitionRecord(
                from_state_id=self.state.state_id,
                to_state_id=self.state.state_id,
                candidate_id="<none-selected>",
                test_result=failed_result,
                accepted=False,
                reason="no candidate passed Test/Select",
                test_rule_id=self.test_rule_id,
            )
            self.history.append(record)
            return record
        selected = result.selected
        if selected.parent_state_id != self.state.state_id:
            raise StopCondition(StopReason.INVALID_STATE, f"selected candidate parent {selected.parent_state_id} does not match current state {self.state.state_id}")
        selected_result = result.result_for(selected)
        record = TransitionRecord(
            from_state_id=self.state.state_id,
            to_state_id=selected.proposed_state.state_id,
            candidate_id=selected.candidate_id,
            test_result=selected_result,
            accepted=True,
            reason=f"committed via select (out of {len(candidates)} candidates)",
            test_rule_id=self.test_rule_id,
        )
        self.history.append(record)
        self.state = selected.proposed_state
        return record

    def run(self, generate_fn: GenerateFn, max_steps: int | None = None) -> list[TransitionRecord]:
        steps_taken = 0
        records: list[TransitionRecord] = []
        while not self.budget.exhausted():
            if max_steps is not None and steps_taken >= max_steps:
                break
            candidate = generate_fn(self.state)
            records.append(self.step(candidate))
            steps_taken += 1
        return records
