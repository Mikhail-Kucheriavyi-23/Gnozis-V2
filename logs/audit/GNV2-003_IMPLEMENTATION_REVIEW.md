# GNV2-003 — Reject no-op evolution — implementation review

Status: IMPLEMENTED / RUNTIME VERIFICATION PENDING

## Scope

Prevent a candidate whose mathematical content `(X,R)` is identical to the current state from being accepted merely because its version increases.

## Current implementation

`gnosis/core/invariants.py` contains `check_meaningful_change()` and registers it in `DEFAULT_INVARIANTS`.

The check compares `State.content_id`, which excludes version and is intended to be canonical with respect to content ordering. An identical-content candidate therefore fails the `meaningful_change` invariant even when `version` is incremented.

## Existing adversarial coverage

`tests/test_meaningful_change.py` covers:

1. version-only change is rejected;
2. element-content change is accepted;
3. relation-only change is accepted;
4. dictionary insertion-order changes do not create false evolution;
5. relation ordering does not create false evolution;
6. `content_id` excludes version while `state_id` does not.

## Evidence rule

This document is an implementation review only. It does NOT mark GNV2-003 as DONE.

Required before DONE:

- real runtime execution of the focused test file;
- relevant regression tests;
- actual exit status recorded;
- confirmation that the Engine commit path cannot bypass `DEFAULT_INVARIANTS` for the tested transition path.

## Gate

`DONE` is permitted only after runtime/CI evidence exists. If execution fails, create a corrective task and keep GNV2-003 `IN_PROGRESS`.
