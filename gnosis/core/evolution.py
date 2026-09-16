"""
Evolution engine (spec sections 2-4): the only path from State to State'.

    Candidate -> Test -> Verification -> Commit

There is NO direct-mutation path. `Engine.step()`/`Engine.step_select()` are
the only entry points that can advance `self.state`, and both always go
through `verify()` first. This is what spec section 4 calls out explicitly:

    Never: Candidate -> direct Core mutation.

The engine also enforces Budget (section 8) and raises a hard
StopCondition (section 9) for the two conditions actually implemented —
see StopReason in types.py for the IMPLEMENTED-NOW vs RESERVED split.

PATCH — GENERATE / "ENDOGENOUS" HONESTY (audit defect, PATCH section 6)
--------------------------------------------------------------------------
The pre-PATCH docstring here called `GenerateFn` an "endogenous generator
hook". That was inaccurate: `run()` receives `generate_fn` as a plain
argument supplied by the CALLER on every invocation. That is exactly the
pattern spec section 3 calls out and prohibits:

    "External Controller -> tells Core what to evolve."

This slice does NOT implement an internal/endogenous generator — Generate
is, honestly, caller-supplied today. Fixing this for real (a generator that
is part of the Core's own cycle rather than an injected callback) is
Phase 9 scope (population/mutation) and is explicitly OUT of scope for this
PATCH (PATCH section 14: "не менять фундаментальную модель... не создавать
альтернативный evolution engine"). `GenerateFn`/`run()` are kept as-is,
functionally, but no longer described as endogenous.

PATCH — SELECT (audit defect #5)
--------------------------------------------------------------------------
`step_select()` adds the missing Select stage: given multiple candidates,
Test is applied to each (via gnosis.core.select.select), failing ones are
discarded, and exactly one passing candidate is committed via the same
verify()-gated path as `step()`. See select.py for the selection rule.

PATCH — INVARIANT-FAILURE SEMANTICS (audit defect, PATCH section 7)
--------------------------------------------------------------------------
Explicit, documented choice: invariant failure on a single candidate is a
REJECT-AND-CONTINUE (Variant A), not a hard stop of the Engine. Only
budget exhaustion and an invalid parent-state reference are hard stops
(StopCondition/StopReason) here. See invariants.py module docstring for
the fuller reasoning and for what remains out of scope (state corruption,
security failure, unrecoverable error — all MISSING, not silently folded
into this behavior).

STATUS: IMPLEMENTED (single-candidate step, multi-candidate step_select)
STATUS: MISSING (population-based evolution / mutation — Phase 9)
STATUS: NOT ENDOGENOUS (Generate is caller-supplied; see note above)
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Callable, Sequence

from .budget import Budget, BudgetExhaustedError
from .select import SelectionResult, select
from .types import Candidate, State, StopReason, TestResult, TransitionRecord
from .verification import TestFn, default_test, verify

# Generate(state) -> Candidate. NOT endogenous in this slice: the caller
# supplies this function to `run()` on every invocation. See module
# docstring PATCH note above — do not describe this as an internal/
# endogenous generator elsewhere in the codebase or docs.
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

    STEP_COST: int = 1

    def _charge_step(self) -> None:
        if self.budget.exhausted():
            raise StopCondition(StopReason.BUDGET_EXHAUSTED, "no budget remaining before step")
        try:
            self.budget.charge(self.STEP_COST)
        except BudgetExhaustedError as exc:
            raise StopCondition(StopReason.BUDGET_EXHAUSTED, str(exc)) from exc

    def step(self, candidate: Candidate) -> TransitionRecord:
        """Single-candidate path: (caller-supplied) Generate -> Test ->
        Evolve. No Select stage here by construction (only one candidate);
        use step_select() when there is more than one candidate to choose
        among.
        """
        self._charge_step()

        if candidate.parent_state_id != self.state.state_id:
            raise StopCondition(
                StopReason.INVALID_STATE,
                f"candidate parent {candidate.parent_state_id} does not match "
                f"current state {self.state.state_id}",
            )

        result = verify(self.state, candidate, self.test_fn)

        record = TransitionRecord(
            from_state_id=self.state.state_id,
            to_state_id=candidate.proposed_state.state_id,
            candidate_id=candidate.candidate_id,
            test_result=result,
            accepted=result.passed,
            reason="committed" if result.passed else "rejected: " + "; ".join(result.reasons),
        )
        self.history.append(record)

        if not result.passed:
            # Rejected candidates never touch self.state — this IS the
            # "no direct Core mutation" guarantee, enforced structurally.
            # Per PATCH section 7: this is Variant A (reject-and-continue),
            # not a hard stop. See module docstring.
            return record

        self.state = candidate.proposed_state
        return record

    def step_select(self, candidates: Sequence[Candidate]) -> TransitionRecord:
        """Multi-candidate path: (caller-supplied) Generate -> Test ->
        Select -> Evolve, in one round (PATCH defect #5).

        All candidates are Tested; the deterministic Select rule
        (gnosis.core.select.select) picks at most one passing candidate;
        that one candidate is committed through the same verify()-gated
        path as step(). If no candidate passes, or the list is empty, the
        Engine state is left untouched and a rejection record is returned
        — this is still Variant A (reject-and-continue), not a hard stop.
        """
        self._charge_step()

        result: SelectionResult = select(self.state, candidates, self.test_fn)

        if result.selected is None:
            reasons: tuple[str, ...]
            if not result.evaluated:
                reasons = ("no candidates supplied to step_select",)
            else:
                reasons = tuple(
                    f"{c.candidate_id}: " + "; ".join(r.reasons) for c, r in result.evaluated
                )
            failed_result = TestResult(passed=False, reasons=reasons)
            record = TransitionRecord(
                from_state_id=self.state.state_id,
                to_state_id=self.state.state_id,
                candidate_id="<none-selected>",
                test_result=failed_result,
                accepted=False,
                reason="no candidate passed Test/Select",
            )
            self.history.append(record)
            return record

        selected = result.selected
        if selected.parent_state_id != self.state.state_id:
            raise StopCondition(
                StopReason.INVALID_STATE,
                f"selected candidate parent {selected.parent_state_id} does not match "
                f"current state {self.state.state_id}",
            )

        selected_result = result.result_for(selected)
        record = TransitionRecord(
            from_state_id=self.state.state_id,
            to_state_id=selected.proposed_state.state_id,
            candidate_id=selected.candidate_id,
            test_result=selected_result,
            accepted=True,
            reason=f"committed via select (out of {len(candidates)} candidates)",
        )
        self.history.append(record)
        self.state = selected.proposed_state
        return record

    def run(self, generate_fn: GenerateFn, max_steps: int | None = None) -> list[TransitionRecord]:
        """Run repeated (caller-supplied) Generate -> step cycles until
        budget exhausted, an explicit max_steps limit, or a StopCondition
        is raised. See module docstring: generate_fn is NOT endogenous."""
        steps_taken = 0
        records: list[TransitionRecord] = []
        while not self.budget.exhausted():
            if max_steps is not None and steps_taken >= max_steps:
                break
            candidate = generate_fn(self.state)
            try:
                records.append(self.step(candidate))
            except StopCondition:
                raise
            steps_taken += 1
        return records
