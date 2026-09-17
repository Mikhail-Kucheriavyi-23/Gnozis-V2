# GNV2-002 — Strict `Test(candidate) -> bool` Runtime Verification

## Task

- TASK-ID: GNV2-002
- BLOCK: Core integrity
- PRIORITY: P0
- STATUS: IMPLEMENTED — RUNTIME VERIFICATION PENDING
- DEPENDS_ON: none

## Objective

Enforce that `Test(candidate)` produces an actual Python `bool` through the `TestResult.passed` contract. Values that are merely truthy/falsy must be rejected.

## Repository evidence

`gnosis/core/types.py::TestResult.__post_init__` explicitly checks `isinstance(self.passed, bool)` and raises `TypeError` otherwise.

`tests/test_test_result_contract.py` contains adversarial cases for:

- `True` / `False` acceptance;
- `1` / `0` rejection;
- `"yes"` / `"True"` rejection;
- empty list rejection;
- `None` rejection;
- float rejection;
- arbitrary object rejection;
- the Python `bool`-is-an-`int` edge case.

## Required runtime evidence

Execute at minimum:

```bash
pytest -q tests/test_test_result_contract.py
```

Then execute the full suite:

```bash
pytest -q
```

Record the exact result and exit code. Do not mark this task DONE from source inspection alone.

## Acceptance

1. `True` and `False` are accepted as actual booleans.
2. All adversarial non-bool inputs listed above raise `TypeError`.
3. The dedicated test file passes in a real pytest runtime.
4. Full regression suite passes.
5. No Core semantics are changed outside this contract.

## Gate

Until runtime evidence exists:

`GNV2-002 != DONE`

No downstream task may use this file as evidence of a passing execution.
