# AI Context Checkpoint — 2026-09-17

## Verified HEAD at this checkpoint

`main` → `ea75f48e7d7b76570443df59e19bfa22d88e09f8`

## Architectural change

Closed the previously identified connection gap between `RuleProposal` and the existing isolated `ShadowEvaluation` mechanism.

New adapter:

`gnosis/reflection/shadow_adapter.py`

Public API:

`evaluate_proposal_shadow(proposal, candidates, active_test, shadow_test, registry)`

The adapter:

- validates that the proposal's current rule/version exists in `RuleRegistry`;
- requires `proposed_version > current_version`;
- receives the concrete shadow Test function explicitly rather than turning proposal text into executable code;
- evaluates active and shadow rules over the same immutable Candidate evidence;
- returns `ProposalShadowAssessment` containing proposal/rule/version lineage, candidate IDs and the existing `ShadowEvaluation`;
- does not activate, register, mutate Core, mutate State, or mutate persistence.

The adapter is exported from `gnosis.reflection`.

## Test added

`tests/test_shadow_adapter.py`

The deterministic test verifies:

- proposal lineage is preserved;
- two identical Candidate inputs are evaluated;
- one improvement is detected;
- no regression is detected;
- RuleRegistry remains at version 1, proving that shadow evaluation did not activate version 2.

## Runtime status

The test has been added but has NOT been executed in a verified runtime in this checkpoint. Do not claim PASS until CI/runtime evidence is inspected.

## Next architectural gate

Do not activate proposals and do not implement self-modification.

Next: independently verify this adapter/test, then design `InvariantDelta` around the existing `ShadowEvaluation` and the actual Core invariants. `InvariantDelta` must remain read-only and must distinguish preserved, violated, improved and unknown evidence.
