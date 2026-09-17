"""
Verification interface (spec section 6, PROOF-PRESERVING EVOLUTION).

The canonical Test predicate is strictly:

    Test(state, candidate) -> bool

`verify()` is the public predicate boundary and rejects every non-`bool`
return value. `evaluate()` is the diagnostic envelope used by the runtime to
retain reasons/evidence without weakening the mathematical Test contract.

This phase does NOT integrate a real theorem prover (Lean/Coq/F*). It performs
invariant checking plus a computable Test predicate. Calling it "formal
verification" would be a false IMPLEMENTED claim.
"""

from __future__ import annotations

from typing import Callable

from .invariants import DEFAULT_INVARIANTS, all_pass, run_invariants
from .types import Candidate, State, TestResult

# Canonical mathematical/runtime contract: Test must return an actual bool.
TestFn = Callable[[State, Candidate], bool]


def _default_test_result(current: State, candidate: Candidate) -> TestResult:
    """Produce diagnostic evidence for the built-in invariant Test."""
    results = run_invariants(current, candidate, DEFAULT_INVARIANTS)
    if all_pass(results):
        return TestResult(passed=True, reasons=("all invariants satisfied",))
    reasons = tuple(f"{r.name}: {r.detail}" for r in results if not r.ok)
    return TestResult(passed=False, reasons=reasons)


def default_test(current: State, candidate: Candidate) -> bool:
    """Baseline Test predicate: true iff all registered invariants pass."""
    return _default_test_result(current, candidate).passed


def verify(current: State, candidate: Candidate, test_fn: TestFn = default_test) -> bool:
    """Run the canonical Test predicate and enforce a strict bool result."""
    result = test_fn(current, candidate)
    if not isinstance(result, bool):
        raise TypeError(
            "TestFn must return an actual bool (True/False), "
            f"got {type(result).__name__}: {result!r}"
        )
    return result


def evaluate(
    current: State,
    candidate: Candidate,
    test_fn: TestFn = default_test,
) -> TestResult:
    """Return diagnostic evidence for a strict Test predicate.

    The built-in predicate retains detailed invariant reasons. Custom TestFn
    implementations expose only their boolean result at this boundary; a
    failed custom predicate receives a deterministic generic reason rather
    than introducing a second return-type contract.
    """
    if test_fn is default_test:
        return _default_test_result(current, candidate)

    passed = verify(current, candidate, test_fn)
    return TestResult(
        passed=passed,
        reasons=(
            "custom Test predicate rejected candidate",
        ) if not passed else (
            "custom Test predicate passed",
        ),
    )
