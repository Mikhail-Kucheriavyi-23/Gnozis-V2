# SELF-DIAGNOSTIC-0001 — Verification Gate

## Status

`UNVERIFIED`

This file is a gate, not a diagnostic result. `VERIFIED` must never be written manually in advance.

## Required evidence

The artifact may be considered verified only after a real runtime execution demonstrates all of the following:

1. `diagnostic_corpus/generate.py` executes successfully.
2. The scenario creates exactly 4 `TransitionRecord` objects.
3. Exactly 3 records are rejected and exactly 1 is accepted.
4. Every recovered record preserves `test-rule:diagnostic-policy`.
5. The records survive the SQLite persistence round-trip.
6. `diagnose(recovered_history)` executes on recovered history, not fabricated data.
7. `SELF-DIAGNOSTIC-0001/diagnostic.json` is actually generated.
8. The diagnostic artifact contains findings/provenance/limitations fields required by the reflection contract.

## Verification record

Do not populate this section until the runtime has actually executed.

```text
status: UNVERIFIED
runtime_commit: <unset>
runtime_environment: <unset>
execution_evidence: <unset>
diagnostic_sha256: <unset>
verified_at: <unset>
```

## Architectural rule

Absence of CI evidence is not evidence of failure, and source-code existence is not evidence of successful execution.

Only a real runtime result may move this gate from `UNVERIFIED` to `VERIFIED`.

## Next gate

After verification, inspect the actual diagnostic findings and determine whether they produce a grounded versioned `RuleProposal`. Only then proceed to Shadow Evaluation. Do not enable self-modification.