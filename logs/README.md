# logs/ — PLACEHOLDER, NOT A FUNCTIONING COMPONENT

Audit finding (PATCH section 9): `logs/audit`, `logs/evolution`,
`logs/security` are empty directories. **Nothing in this codebase writes
to them.** They exist only to reserve the layout named in the master spec
(section 38).

The only thing that currently records transitions is
`gnosis.core.evolution.Engine.history` — an in-process Python list. It is
lost when the process exits. It is **not a persistent audit log, it is**
**not hash-chained, and it must not be described as "audit-complete" or
as satisfying spec section 39 (auditability) or section 10 (logs) until a
real writer exists here.

Building the real logging system (append-only, hash-chained, matching the
`audit_events` table in `docs/DATABASE_SCHEMA.md`) is future work, tracked
in `STATUS.md`, and is explicitly out of scope for the current PATCH
(PATCH section 9: "не требуется строить полноценную persistent logging
system").
