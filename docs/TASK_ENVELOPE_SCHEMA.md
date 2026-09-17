# Gnozis-V2 — Task Envelope Schema

Status: architecture specification / no runtime implementation yet.

## Purpose

Define the smallest portable representation of a user request so that an authorized connected product can create a task and another product can continue it without relying on the originating conversation.

## Canonical envelope

```json
{
  "task_id": "opaque-id",
  "user_id": "opaque-id",
  "project_id": "opaque-id",
  "created_at": "timestamp",
  "objective": "human-readable objective",
  "context_snapshot_id": "opaque-id",
  "baseline_commit": "git-sha-or-null",
  "allowed_scope": [],
  "forbidden_scope": [],
  "required_capabilities": [],
  "acceptance_criteria": [],
  "evidence_required": [],
  "requested_result_channel": [],
  "status": "queued"
}
```

## Required invariants

1. `task_id` uniquely identifies a task within its durable project/user scope.
2. `user_id` and `project_id` are explicit; they must never be inferred from the connected product.
3. `context_snapshot_id` identifies the canonical context used to start or resume the task.
4. `baseline_commit` records the repository state when repository work is involved.
5. `allowed_scope` is bounded; absence of an item does not imply permission.
6. `forbidden_scope` takes precedence over `allowed_scope`.
7. `required_capabilities` describe required operations, not architectural authority.
8. `acceptance_criteria` are explicit and machine-readable where practical.
9. `evidence_required` describes what must be demonstrated before a result can be considered verified.
10. `requested_result_channel` is a routing request, not an authorization grant.
11. `status` describes lifecycle state and must not be treated as proof of correctness.

## Lifecycle

```text
queued
  → resolving
  → executing
  → awaiting_verification
  → blocked
  → completed
  → rejected
  → cancelled
```

Transitions must be validated by the future Task repository. The initial schema intentionally does not implement that repository.

## Cross-terminal continuation

A connected product receiving only `task_id` must be able to resolve:

```text
task
 + canonical context snapshot
 + current evidence
 + current repository baseline
 + current status
 + permitted capabilities
```

It must not need the original chat transcript to reconstruct project facts.

## Separation rules

```text
task_id            ≠ authentication
user_id            ≠ capability
capability         ≠ architectural authority
result_channel     ≠ permission to read all task data
context_snapshot   ≠ mutable task state
status             ≠ verification evidence
```

## Organization use

The same envelope can represent:

- an individual research task;
- a coding task;
- a management request;
- a data-analysis task;
- a CRM/work-chat request;
- a delegated task performed by a future Gnozis agent.

Organization-specific routing and access policy must be layered on top rather than encoded as implicit behavior in the envelope.

## Implementation boundary

This file is a contract only. It does not authorize any new database table, Core mutation, identity mechanism, connector, or agent behavior.

Any implementation must be a separately scoped task and must preserve existing Core and Persistence boundaries.
