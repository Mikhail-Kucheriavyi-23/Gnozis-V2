# GNV2-PERSIST-001 — TransitionRecord persistence integrity

Status: IMPLEMENTATION REVIEW / RUNTIME VERIFICATION PENDING

## Scope

Verify the boundary between the Core `TransitionRecord` and durable SQLite history.

## Current implementation reviewed

`gnosis/storage/repositories.py` provides `persist_transition()` and `load_transition_records()`.

The persistence path:

1. checks candidate parent against the transition source;
2. derives a deterministic transition ID from transition content;
3. rejects stale instance heads;
4. persists candidate and transition in one transaction;
5. appends an audit event linked to the transition;
6. updates the instance head only for accepted transitions;
7. commits atomically.

Rejected transitions are persisted as rejected history and must not move the instance head.

## Required runtime evidence

The following must be executed against the current `main`:

- accepted transition survives close/reopen and reloads with the same source, target, candidate and acceptance result;
- rejected transition survives close/reopen with `accepted=False` and preserved reasons/test rule;
- rejected transition does not change `instances.current_state_id`;
- accepted transition changes the current head only after durable transition/audit data is written;
- injected failures at each transaction checkpoint leave no partial durable transition;
- replaying the same transition is idempotent;
- stale instance head is rejected;
- `verify_durable_graph()` succeeds after valid persistence and rejects broken provenance.

## Gate

This file is an implementation/evidence contract only. It does not mark the task DONE.

DONE requires fresh runtime or CI evidence with exit status and the relevant test output recorded.
