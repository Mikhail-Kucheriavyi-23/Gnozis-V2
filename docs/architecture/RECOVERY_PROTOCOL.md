# Persistence Recovery Protocol

**Status:** proposed contract for implementation

**Goal:** after normal restart, crash, or detected corruption, determine one and only one valid system state without silently accepting partial or tampered history.

## Recovery states

The storage layer must report one of these explicit outcomes:

| Recovery result | Meaning | Runtime action |
|---|---|---|
| `RECOVERED` | Schema, heads, states, transitions, and audit chain are valid | Reconstruct instances and continue under documented budget policy |
| `EMPTY_INITIALIZED` | Fresh database with no records | Initialize only through root-creation transaction |
| `RECOVERABLE_ROLLBACK` | Uncommitted SQLite work was rolled back by the engine | Load last committed head and report rollback evidence if available |
| `CORRUPT_FAIL_CLOSED` | Integrity, foreign key, hash, sequence, or head invariant failed | Refuse evolution and require explicit repair procedure |
| `SCHEMA_INCOMPATIBLE` | Migration/version cannot safely load | Refuse startup; do not auto-destruct or reinterpret data |

No recovery path may silently skip a broken middle event or silently rewrite a final event.

## Startup procedure

1. Open the database using the storage factory.
2. Enable and verify `PRAGMA foreign_keys = ON`.
3. Check schema version and required tables, columns, indexes, and triggers.
4. Run SQLite integrity checks appropriate to the deployment mode.
5. Verify all persisted state and relation content hashes.
6. Verify candidate IDs and their parent/proposed state references.
7. Verify transition endpoints, acceptance semantics, and candidate relationships.
8. Verify instance parent references, root generation, generation increments, and current-state heads.
9. Verify the complete audit chain from the fixed genesis hash through the highest sequence.
10. Verify that every current head is a valid state and that accepted transition continuity is consistent.
11. Reconstruct deep-frozen Core objects from canonical storage values.
12. Return `RECOVERED` only if all checks pass.

## Normal accepted transition

Expected durable order:

```text
BEGIN IMMEDIATE
  validate current instance head
  persist proposed state and relations if not already present
  persist candidate
  persist transition accepted=true
  append audit event with next sequence, prev_hash, event_hash
  update instance current_state_id and execution snapshot
COMMIT
```

After reopen, the instance head must equal the transition `to_state_id`, the transition `from_state_id` must equal the previous head, and the audit chain must include the event.

## Crash scenarios

### Crash before `BEGIN`

No new record exists. Recovery returns the prior valid state.

### Crash after `BEGIN` but before writes

SQLite rollback must leave the prior committed state. Recovery returns the prior head.

### Crash after state/candidate writes but before transition/audit/head update

All writes belong to one transaction. SQLite rollback must remove the partial state/candidate rows unless they were independently committed by an explicitly idempotent insertion policy. The instance head must remain unchanged.

### Crash after transition/audit writes but before head update

This situation must be impossible as a visible partial commit: transition, audit event, and head update are one transaction. If a storage failure nevertheless exposes inconsistency, recovery must return `CORRUPT_FAIL_CLOSED`, not guess whether to advance the head.

### Crash after `COMMIT`

All records are durable. Recovery returns the new head and validates the new audit event. Replaying the same logical operation must be idempotent or explicitly rejected as duplicate; it must not create a second semantic transition.

## Corruption scenarios

### Corrupted final audit event

Detect one or more of: invalid JSON/canonical payload, wrong event hash, wrong previous hash, wrong sequence, or invalid referenced resource. Default behavior is `CORRUPT_FAIL_CLOSED`. A future explicit truncation repair may exist only as a separate offline tool with its own audit record; ordinary runtime recovery must not truncate silently.

### Corrupted middle audit event

Always fail closed. A later valid event cannot repair a broken predecessor link. Do not recover by starting a new chain at the next event.

### Missing final event

If the current head references a transition whose audit event is missing, fail closed. If the final event is absent but the current head remains the prior state and all earlier records are valid, recovery may return the prior state only when the database transaction semantics prove that the later operation never committed. The implementation must test this distinction rather than infer it from timestamps.

### Tampered state payload

Recompute `state_id` and reject startup if it differs. Do not load the object and merely flag it in memory.

### Broken instance head

If `current_state_id` is missing or references a nonexistent state, fail closed. Do not select the last state by timestamp.

## Fork and multiple instances

For a fork, recovery must verify:

- child exists exactly once;
- child parent exists;
- child generation equals parent generation plus one;
- child has its own current-state head;
- child and parent state objects are isolated at the domain boundary;
- one instance's accepted transition does not move another instance's head.

A global audit sequence may interleave events from multiple instances. Each event's resource field must identify the instance/resource, and the hash chain must remain global and deterministic.

## Recovery invariants

Recovery is valid only if all of the following hold:

1. Every current head exists and hashes correctly.
2. Every accepted transition's `from_state_id` matches the instance head immediately before it.
3. Every accepted transition's `to_state_id` matches the resulting head.
4. Rejected candidates never become heads.
5. Root instances have no parent and generation zero.
6. Child generations and parent references form an acyclic graph.
7. Every audit sequence is unique and strictly increasing.
8. Every `prev_hash` points to the immediately preceding sequence hash.
9. Every `event_hash` matches its canonical row.
10. No unsupported status or malformed JSON is silently coerced.
11. Reconstructed Core values remain deeply immutable.
12. No secret material appears in persisted fields or audit payloads.

## Recovery output

The recovery result must include at least:

```text
status
schema_version
last_verified_audit_sequence
last_verified_audit_hash
recovered_instance_ids
recovered_heads
warnings
```

Warnings must never downgrade a corrupt state to `RECOVERED`. A warning is for non-fatal documented conditions only.

## Prohibited behavior

Recovery must not choose a state by newest timestamp, ignore an invalid final event, repair a broken middle chain implicitly, delete records automatically, or advance an instance head based solely on an audit event.
