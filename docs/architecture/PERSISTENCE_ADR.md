# Persistence Architecture Decision Record

**Status:** proposed contract for implementation

**Baseline:** GNOSIS-V2 `origin/main` at `050a3e4359d90acdbc98cf2b7657e83385b2c458`

**Scope:** Persistence + Append-Only Audit Log. No production code is authorized by this document.

## Decision summary

| Question | Decision | Rationale |
|---|---|---|
| Current state | Add explicit `current_state_id` to the persisted instance head, preferably in a separate `instance_heads` table or as a nullable FK on `instances` if schema evolution remains simple | Restart recovery must not infer the live head from ambiguous history joins |
| Current event hash | Store both `prev_hash` and `event_hash` | A previous hash alone detects chain-link changes but cannot prove the current payload was unchanged |
| Transition endpoints | Persist explicit `from_state_id` and `to_state_id` on `transitions` | Recovery and audit inspection must not depend on derived joins |
| Ordering | Use a DB-assigned monotonic `sequence` within the audit log; hash the sequence | Timestamp is metadata, not a total order |
| Budget/history | Persist committed transition/audit history; persist a budget snapshot only if the phase requires resumable execution, otherwise restart with an explicit documented budget policy | `Engine.history` is not durable; silent budget reset would be an undocumented semantic change |
| Driver | Use stdlib `sqlite3` for the first local phase; isolate it behind storage repositories | Preserves zero Core dependencies and keeps the first phase small; SQLAlchemy remains a future adapter option |

## Decision 1 — Instance current state

The persistence model must expose one authoritative current-state pointer per instance. Recommended schema evolution is:

```text
instances(instance_id, ..., current_state_id FK -> states.state_id)
```

If preserving the existing table shape is preferred, use:

```text
instance_heads(instance_id PK/FK, current_state_id FK, updated_at)
```

The implementation must choose one, document it in the migration/schema, and never maintain two competing heads. Root creation writes the initial state and head atomically. Accepted transition updates the head in the same transaction as the transition and audit rows.

## Decision 2 — Audit hashes

`audit_events` must contain:

```text
event_id       TEXT PRIMARY KEY
event_hash     TEXT NOT NULL UNIQUE
prev_hash      TEXT NOT NULL
action         TEXT NOT NULL
actor          TEXT NOT NULL
resource       TEXT NOT NULL
result         TEXT NOT NULL
sequence       INTEGER NOT NULL UNIQUE
timestamp      TEXT NOT NULL
```

The exact names may follow the schema migration convention, but the semantics are mandatory. `event_hash` is SHA-256 over canonical serialized event fields including `prev_hash` and `sequence`. The first event uses a fixed documented genesis hash. No event is considered verified merely because its `prev_hash` points to a valid predecessor.

## Decision 3 — Transition endpoints

`transitions` must explicitly store:

```text
transition_id  TEXT PRIMARY KEY
candidate_id   TEXT NOT NULL FK
from_state_id  TEXT NOT NULL FK
 to_state_id   TEXT NOT NULL FK
accepted       INTEGER NOT NULL CHECK (accepted IN (0, 1))
reasons        TEXT NOT NULL
created_at     TEXT NOT NULL
```

For rejected transitions, `to_state_id` is the proposed state ID if the candidate state was persisted, while the instance head remains `from_state_id`. For the special no-candidate record, use an explicit nullable candidate or a documented sentinel; do not overload a normal candidate ID.

## Decision 4 — Ordering

Audit order is defined by `sequence`, not by timestamp or lexical `event_id`. The writer allocates the next sequence inside the same write transaction that appends the event. The hash covers `sequence`, so reordering is detectable.

For multiple instances, the first phase uses one database-wide audit sequence. Per-instance ordering may be added later, but it must not replace the global chain without an explicit architectural decision.

## Decision 5 — Budget and durable history

Durable history is the `transitions` plus `audit_events` records, not the in-memory `Engine.history` list. The repository must reconstruct domain history from durable records when requested.

Budget semantics require an explicit implementation choice. Recommended first-phase contract: persist `budget_remaining` and `budget_consumed` in an instance execution snapshot whenever a commit is made. If budget persistence is deferred, restart must not silently claim continuity; it must use a documented fresh-run policy and mark that policy in recovery metadata. A phase claiming exact resumability must persist the budget snapshot.

## Decision 6 — sqlite3 versus SQLAlchemy

Use `sqlite3` for this phase. Storage modules may depend on the standard library; `gnosis/core` remains dependency-free. Repositories own SQL, serialization, transaction handling, and connection pragmas. SQLAlchemy is not prohibited forever, but introducing it now would enlarge the dependency surface without solving an acceptance criterion.

Required connection behavior includes foreign keys enabled per connection, explicit transaction handling, a documented busy timeout, and a testable journal/synchronous policy. WAL may be enabled only with tests covering the chosen deployment mode.

## Rejected alternatives

- Inferring current state solely from the last transition: ambiguous for roots, rejected candidates, forks, and crashes.
- Storing only previous hashes: insufficient to detect payload tampering.
- Using timestamps as order: not total, not reliable under concurrency.
- Storing only `Engine.history`: process-local and lost on restart.
- Putting SQL imports in `gnosis/core`: violates the dependency boundary.
- Treating `actor`, `origin`, or `owner_id` as authorization: identity/capability layers are not implemented.

## Implementation gate

Claude should not reinterpret these six questions independently during implementation. Any deviation requires a new ADR amendment and must be reviewed before code is treated as conforming.

## Hardening amendment — implementation candidate

The hardening candidate adds three persistence relationships needed to make the provenance contract executable: `instances.root_state_id` identifies the validated root state; `instances.budget_total` and `instances.budget_spent` preserve restart budget state; and `transitions.instance_id` plus `audit_events.transition_id` make instance/event provenance explicit.

The schema version is `3`. These additions do not change Ψ-Core semantics. They strengthen the storage graph so recovery can verify `Instance → State → Transition → Candidate → AuditEvent` rather than relying on foreign-key existence alone.

`load_instance()` is a low-level loader. The fail-closed recovery entry point is `recover_instance()`, which runs `verify_durable_graph()` before reconstruction. Callers must use `recover_instance()` for restart recovery.

The implementation also defines a narrow test-only `failure_at` seam on `persist_transition()` for transaction-boundary tests. It is not a business rule and does not alter the normal commit path.
