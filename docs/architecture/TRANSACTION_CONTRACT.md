# Persistence Transaction Contract

**Status:** proposed contract for implementation

**Boundary:** storage/repository layer only. Ψ-Core remains unaware of SQL and transaction mechanics.

## Transaction vocabulary

- **Logical operation:** one domain action such as root creation, rejected candidate recording, accepted transition, or fork.
- **Atomic commit:** after a successful commit all required rows are visible; after rollback none of the operation's rows are visible as a new logical result.
- **Current head:** the authoritative persisted state pointer for one instance.
- **Audit event:** immutable evidence of an operation, linked through a global monotonic sequence and SHA-256 chain.

## Connection contract

Every connection must:

1. enable foreign keys and verify that the pragma is active;
2. use explicit transaction boundaries rather than implicit mixed behavior;
3. configure a documented busy timeout;
4. use a documented journal and synchronous mode;
5. rollback on every exception before returning the error;
6. avoid exposing a connection that can write outside repository policy.

The first implementation should use stdlib `sqlite3` and keep SQL confined to storage modules.

## Atomic operations

### T-01 Fresh database initialization

```text
BEGIN
  create schema/version metadata
COMMIT
```

Schema initialization is idempotent only for the same schema version. An incompatible version fails closed; it is not silently migrated by an unrelated repository method.

### T-02 Root instance creation

```text
BEGIN IMMEDIATE
  insert initial state and relation rows
  insert root instance with current_state_id = initial state
  append root-created audit event
COMMIT
```

No root instance without a valid current state may become visible.

### T-03 Rejected candidate

```text
BEGIN IMMEDIATE
  insert parent/proposed states if policy requires deduplicated storage
  insert candidate
  insert transition accepted=false
  append rejected-transition audit event
COMMIT
```

The instance head is unchanged. Candidate and transition are visible together, or neither is visible as a new operation.

### T-04 Accepted transition

```text
BEGIN IMMEDIATE
  lock/validate instance current_state_id = candidate.parent_state_id
  validate candidate and proposed state through the existing Core contract before persistence
  insert proposed state and relation rows
  insert candidate
  insert transition accepted=true with explicit from/to IDs
  allocate audit sequence and append event with prev_hash/event_hash
  update instance current_state_id
  update execution/budget snapshot if this phase persists budget
COMMIT
```

There must be exactly one head advance for one accepted logical transition.

### T-05 Fork

```text
BEGIN IMMEDIATE
  validate parent instance and source state
  insert child instance with parent and generation + 1
  set child current_state_id to isolated cloned state
  append fork audit event
COMMIT
```

Parent head does not change. Child creation cannot be externally observed without its head.

## Audit append contract

Within the same write transaction:

1. read the current last audit sequence/hash under the write lock;
2. compute `sequence = previous + 1`;
3. canonicalize immutable event fields;
4. compute `event_hash = SHA256(canonical_event)`;
5. insert the event with unique sequence and event ID;
6. reject any mismatch or duplicate before commit.

`UPDATE` and `DELETE` on audit events are not part of the normal repository API. Triggers may reject them as defense in depth. Hash verification remains mandatory because database-level constraints cannot detect every payload mutation.

## Failure semantics

| Failure point | Required result |
|---|---|
| Before begin | No operation rows |
| During state insert | Rollback; prior head unchanged |
| During candidate insert | Rollback; no partial candidate/transition pair |
| During transition insert | Rollback; proposed state is not a committed head |
| During audit hash/insert | Rollback; no accepted head advance |
| During head update | Rollback; no visible transition without matching head |
| During commit | SQLite determines all-or-nothing durability; reopen and verify, never guess |
| After commit | New head and full event chain recoverable |

## Read visibility

Readers may observe only committed rows. A repository read that combines multiple tables must either use one read transaction or perform consistency validation before returning a domain object. It must not return a state head assembled from mixed transaction snapshots.

## Concurrency contract

The first implementation must serialize accepted head updates using a write transaction and compare-and-validate the expected current head. A stale candidate must be rejected without moving the head. Concurrent operations on different instances may be serialized initially; optimization is not an acceptance requirement.

Duplicate logical operations must be handled by deterministic IDs and unique constraints. The result must be either idempotent replay of the same operation or explicit duplicate rejection. It must never create two different audit events for the same idempotency key without documentation.

## Append-only enforcement layers

| Threat | Constraint/trigger | Repository behavior | Verification |
|---|---|---|---|
| `UPDATE audit_events` | Reject trigger or restricted DB role where available | No update method | Direct adversarial test plus chain verification |
| `DELETE audit_events` | Reject trigger | No delete method | Direct adversarial test |
| Change `prev_hash` | Hash chain detects | Verification fails | Tamper test |
| Change `event_hash` | Recompute detects | Verification fails | Tamper test |
| Insert in middle | Sequence/unique constraints and chain detect | Verification fails | Reordering test |
| Change sequence | Unique/order/hash checks detect | Verification fails | Sequence tamper test |
| Delete last event | Head/event continuity detects where referenced | Fail closed or documented proven rollback only | Final deletion test |
| Duplicate event | Unique event/idempotency key | Idempotent or reject | Duplicate test |
| Payload substitution | Event hash detects | Fail closed | Payload tamper test |

## Core boundary

Persistence may serialize, store, load, and verify domain objects. It must not:

- select candidates;
- generate candidates;
- decide whether a transition passes Core invariants;
- mutate `Engine.state` directly;
- become a hidden external selector;
- introduce SQL imports into `gnosis/core`.

The accepted transition decision originates in the existing Core engine. The storage adapter receives a committed domain result and persists it atomically.

## Commit proof obligation

For each successful accepted commit, the repository test must prove all of these after reopening the database:

```text
instance.current_state_id == transition.to_state_id
transition.from_state_id == previous_head
candidate.parent_state_id == transition.from_state_id
candidate.proposed_state.state_id == transition.to_state_id
audit event exists and verifies in the chain
```

For each rejected commit, the same test must prove that the instance head is unchanged.
