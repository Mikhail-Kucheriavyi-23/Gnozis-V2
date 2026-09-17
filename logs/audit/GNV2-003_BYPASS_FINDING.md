# GNV2-003 — adversarial bypass finding

Status: FINDING — corrective task required

## Finding

`gnosis/core/invariants.py` correctly defines `check_meaningful_change()` and includes it in `DEFAULT_INVARIANTS`.

However, `gnosis/core/verification.py::evaluate()` has two paths:

- `default_test` → `_default_test_result()` → `run_invariants(..., DEFAULT_INVARIANTS)`;
- custom `TestFn` → `verify()` only checks that the custom function returns an actual `bool`.

`gnosis/core/evolution.py::Engine.step()` calls `evaluate(self.state, candidate, self.test_fn)` and commits whenever `result.passed` is true.

Therefore a custom `TestFn` that returns `True` can currently accept a candidate without independently running `DEFAULT_INVARIANTS`, including the `meaningful_change` invariant.

## Consequence

GNV2-003 is implemented for the built-in Test path, but the invariant is not yet an unconditional commit gate for every Engine Test path.

This means GNV2-003 must NOT be marked DONE yet.

## Required corrective task

Make protected Core invariants mandatory at the commit boundary, independent of whether the user-supplied/custom `TestFn` returns `True`.

The intended architecture should remain:

    candidate
      ↓
    protected invariants
      ↓
    Test(candidate) -> bool
      ↓
    commit only if both pass

Do not solve this by weakening the strict bool contract or by duplicating a second State model.

## Required adversarial regression

Construct a content-identical candidate with only a version increment and a custom `TestFn=lambda current, candidate: True`. The Engine must reject it and must not mutate `Engine.state`.

Also verify that a genuine content change can still be accepted when the custom Test returns True and all protected invariants pass.

## Evidence rule

Implementation changes are not DONE until runtime/CI evidence exists for the new regression tests.
