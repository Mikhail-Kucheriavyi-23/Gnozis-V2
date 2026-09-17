# GNV2-PERSIST-003 — Recovery provenance integrity

Status: GAP IDENTIFIED / RUNTIME VERIFICATION PENDING

## Review finding

`recover_instance()` correctly calls `verify_durable_graph()` before loading the instance. The durable graph verifies audit-chain integrity, instance heads, accepted-transition continuity, candidate/state provenance, and fork lineage.

However, the current verifier does not yet independently recompute and validate every persisted `transition_id` from the canonical transition content before accepting the graph. `transition_id()` is deterministic in the persistence implementation, but `verify_durable_graph()` currently checks the transition/candidate relationship without explicitly checking that the stored transition ID equals the recomputed ID.

This is a provenance gap: a tampered transition identifier could potentially remain structurally connected while no longer being the canonical identity of the recorded transition.

## Required invariant

For every persisted transition:

`stored transition_id == transition_id(reconstructed TransitionRecord)`

The verification must also ensure:

- stored `accepted` agrees with reconstructed `TestResult.passed`;
- `candidate_id`, `from_state_id`, and `to_state_id` match the canonical transition content;
- the linked audit event references the same transition ID;
- recovery rejects tampered transition identity before returning an Instance.

## Required adversarial tests

1. mutate `transition_id` only → `verify_durable_graph()` rejects;
2. mutate `accepted` → rejects if identity/content becomes inconsistent;
3. mutate `reasons` → rejects;
4. mutate `test_rule_id` → rejects;
5. mutate `candidate_id` → rejects;
6. mutate audit `transition_id` → rejects;
7. valid transition still recovers after restart.

## Gate

No DONE status until fresh runtime/CI evidence demonstrates rejection of each tampering case and successful recovery of a valid graph.
