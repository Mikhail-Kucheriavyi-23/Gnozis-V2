# Gnozis-V2 — Task / Proposal Persistence Model

Status: architecture contract; implementation is a separate bounded task.

## Purpose

Make cross-terminal continuation and Core proposal handling durable without turning external products into alternative state machines.

The model separates three things:

```text
Task = what the user/system is trying to accomplish
Proposal = what an agent/product proposes to do
Evidence = what can prove the current state or proposal result
```

None of these is the Ψ-Core State.

## Canonical entities

### Task

A durable unit of work shared across connected products.

Minimum conceptual fields:

```text
task_id
project_id
owner_id
organization_id?
parent_task_id?
title
objective
status
priority
created_at
updated_at
current_checkpoint_id
```

Task status is workflow state, not Core state.

### Task checkpoint

A durable continuation point.

```text
checkpoint_id
task_id
sequence
baseline_ref
implementation_state
verification_state
acceptance_state
objective_snapshot
constraints_snapshot
pending_actions
blocked_actions
capability_refs
evidence_refs
created_at
created_by
```

A checkpoint must be immutable after publication. A new state creates a new checkpoint.

### Proposal

A bounded proposal originating from an external agent, user, connector, or internal analysis layer.

```text
proposal_id
task_id
producer
producer_type
parent_state_id?
proposal_type
payload
scope_ref
capability_refs
evidence_refs
status
created_at
resolved_at?
```

Proposal statuses should distinguish at least:

```text
created
under_review
accepted
rejected
superseded
expired
```

Acceptance of a proposal is not itself a Core state transition unless the proposal passes the Core ingress contract.

### Proposal execution / Core transition reference

A proposal that actually enters Core must reference the resulting canonical transition rather than storing a second state model:

```text
proposal_id
transition_id
from_state_id
to_state_id
verification_evidence_ref
```

This creates traceability:

```text
Task
 ↓
Proposal
 ↓
Candidate
 ↓
Test / Verify
 ↓
Core Transition
 ↓
Evidence
 ↓
Checkpoint
```

## Database boundary

The existing Persistence layer remains the source of truth for existing Core tables and audit events. The future Task/Proposal tables must be additive and must not reinterpret existing Core tables.

Conceptually:

```text
Existing Core persistence
 ├─ states
 ├─ relations
 ├─ candidates
 ├─ instances
 ├─ transitions
 └─ audit_events

User/task layer
 ├─ tasks
 ├─ task_checkpoints
 ├─ proposals
 ├─ proposal_evidence_refs
 └─ task_events
```

Do not create a second `State` table for the user/task layer.

## Cross-terminal continuation

Any connector can resolve:

```text
task_id → latest accepted checkpoint → evidence refs → available capabilities
```

It does not need the original conversation transcript.

Example:

```text
Mobile notification
      ↓
task_id=42
      ↓
checkpoint=17
      ↓
implementation=implemented
verification=verified
acceptance=pending
      ↓
evidence: commit + pytest + audit
      ↓
AI terminal can continue
```

## Concurrency and conflicts

Multiple products may create proposals against the same checkpoint.

They must not silently overwrite each other.

A proposal records the baseline it was derived from. If the canonical Core state has moved on before execution:

```text
proposal.parent_state_id != current_state_id
```

then the proposal is stale and must be rejected or explicitly re-derived. This is analogous to optimistic concurrency control.

Task-level proposals can coexist; Core state cannot have two unverified direct writers.

## Evidence binding

Every accepted proposal should have enough evidence references to reconstruct:

```text
who/what produced it
which task/checkpoint it used
which capabilities were exercised
what artifact or runtime result was produced
what verification occurred
whether acceptance was granted
```

The proposal record must not copy large external documents when an immutable reference is sufficient.

## Authorization boundary

`owner_id` is not authentication and is not authorization.

The persistence model may store ownership and scope, but authorization must be resolved by a separate Identity/Capability layer. This document intentionally does not implement that layer.

## Notification boundary

Notifications reference tasks/events; they do not become canonical state.

```text
notification → task_id → checkpoint/evidence
```

A lost notification therefore does not destroy project state.

## Organization / personal use

The model must support both:

```text
individual user
company / organization
team
```

without duplicating the task engine.

Personal and organizational scopes are represented by explicit ownership/scope metadata and future policy resolution.

## Required invariants before implementation acceptance

1. No second Core State model is introduced.
2. Task lifecycle cannot mutate Ψ-State directly.
3. Proposal execution is bound to an explicit baseline.
4. Stale proposals cannot silently commit.
5. Accepted Core transitions reference their originating proposal when applicable.
6. Evidence references are durable and auditable.
7. Published checkpoints are immutable.
8. Task and proposal persistence is additive to existing Persistence.
9. Existing Core/Persistence tests remain green.
10. Real pytest is required; ad-hoc/offline runners are not sufficient evidence.
11. Implementation, verification, and acceptance remain separate states.
12. External connector access does not grant architectural authority.

## Implementation sequence

When implementation is explicitly authorized:

```text
1. Define exact SQLite DDL and repository API.
2. Add migration/compatibility tests without changing Core semantics.
3. Implement Task repository.
4. Implement immutable Checkpoint repository.
5. Implement Proposal repository.
6. Implement evidence references.
7. Implement stale-baseline detection.
8. Add cross-terminal continuation read path.
9. Add Core proposal-ingress adapter.
10. Run complete real pytest + compileall.
11. Independent adversarial audit.
12. Corrective pass.
13. Independent re-audit.
14. Integration gate.
```

Until step 1 is explicitly assigned, this document is architecture only.
