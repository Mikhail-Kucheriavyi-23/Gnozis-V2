"""
Verification interface (spec section 6, PROOF-PRESERVING EVOLUTION).

Provides `verify(candidate, state) -> TestResult`. This phase does NOT
integrate a real theorem prover (Lean/Coq/F*) — it runs the registered
invariants and a pluggable Test function, and returns a bool with reasons.

Per spec section 52 (STRICT REPORTING RULE): this is NOT a mathematical
proof. It is invariant-checking + a computable Test predicate. Calling it
"formal verification" would be a false IMPLEMENTED claim.

STATUS: IMPLEMENTED (invariant-based verification)
STATUS: THEORETICAL (external theorem-prover integration hook — interface
        exists as `TestFn`, no Lean/Coq/F* binding implemented)
"""

from __future__ import annotations

from typing import Callable

from .invariants import DEFAULT_INVARIANTS, all_pass, run_invariants
from .types import Candidate, State, TestResult

TestFn = Callable[[State, Candidate], TestResult]


def default_test(current: State, candidate: Candidate) -> TestResult:
    """Baseline Test(candidate) -> bool: passes iff all invariants pass."""
    results = run_invariants(current, candidate, DEFAULT_INVARIANTS)
    if all_pass(results):
        return TestResult(passed=True, reasons=("all invariants satisfied",))
    reasons = tuple(f"{r.name}: {r.detail}" for r in results if not r.ok)
    return TestResult(passed=False, reasons=reasons)


def verify(current: State, candidate: Candidate, test_fn: TestFn = default_test) -> TestResult:
    """Run the Test/verification step. Never mutates state; pure function."""
    return test_fn(current, candidate)
