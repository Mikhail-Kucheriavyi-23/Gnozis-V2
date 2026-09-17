# Gnozis-V2 — Task Lifecycle Contract

Status: architecture contract; implementation not yet accepted.

## Purpose

A Task is the durable unit of work that allows Gnozis to continue an analytical or engineering request across different products, agents, and sessions.

A Task is not a chat thread and is not owned by a particular AI terminal.

## Lifecycle

The canonical lifecycle is:

```text
created
  ↓
active
  ├──────────────→ blocked
  │                  ↓
  │               resumed
  │                  ↓
  └──────────────────┘
  ↓
completed
  ↓
verified
  ↓
accepted
```

Alternative terminal states may include:

```text
cancelled
rejected
superseded
```

The exact transition matrix must be enforced by the implementation rather than inferred from UI text.

## State dimensions

Task lifecycle state must remain separate from the Context Snapshot dimensions:

```text
Task lifecycle
Implementation state
Verification state
Acceptance state
```

For example, a task can remain `active` while its current implementation is `implemented` but verification is still `pending`.

## Ownership and actors

A task identifies its owner/principal, but actor identity and authorization are separate concerns.

```text
owner_id
actor_id
capability
```

must not be treated as interchangeable.

An agent may continue a task only when its capabilities authorize the requested operation.

## Claim / handoff

A connected product or agent may request a task continuation without becoming its permanent owner.

Future implementations should support bounded claims such as:

```text
claim(task_id, actor, capability, expiry)
```

The claim should be auditable and should not silently transfer ownership.

A task should remain recoverable if an agent disappears, reaches a limit, or loses access.

## Checkpoint

Long-running work should periodically produce a durable checkpoint containing at least:

```text
task_id
snapshot_id
baseline
current lifecycle state
current implementation state
current verification state
current acceptance state
completed actions
pending actions
blocked actions
next permitted actions
evidence references
actor / producer
sequence
```

A checkpoint is evidence of observed state, not automatic acceptance.

## Resume semantics

When another product requests continuation:

```text
resolve task
   ↓
load latest accepted checkpoint
   ↓
load referenced evidence
   ↓
resolve current capabilities
   ↓
return bounded continuation context
```

The new actor must not infer missing state from an old chat transcript when canonical task state or evidence is available.

## Conflict handling

If two agents produce incompatible updates:

```text
Agent A ─┐
         ├→ evidence / conflict record → resolution
Agent B ─┘
```

The system must preserve both observations until an explicit resolution is recorded. A later write must not silently erase the competing evidence.

## Notifications

A notification is an event about task state, not the task state itself.

Examples:

```text
TASK_BLOCKED
TASK_READY_FOR_REVIEW
TASK_VERIFIED
TASK_ACCEPTED
TASK_ACTION_REQUIRED
```

A notification may contain a compact continuation reference. The recipient must be able to resolve the canonical task state from that reference.

## Cross-product invariant

The same task must retain its identity when accessed through:

```text
AI terminal
mobile application
web interface
work chat
CRM
research tool
engineering tool
```

Products may change presentation and routing, but must not create separate canonical copies of the task.

## Evidence rule

Every material lifecycle transition should be attributable to observable evidence or an explicit human/project action.

The following is insufficient evidence by itself:

```text
"Claude says complete"
"Agent says verified"
"UI shows green"
```

## Safety boundary

Task continuation does not grant new capabilities.

```text
resume(task)
    ≠
execute(anything)
```

Before an operation is executed, the system must independently resolve capability, scope, authorization, and applicable safety constraints.

## Implementation boundary

This contract does not modify Ψ-Core semantics. It defines the durable orchestration/context layer around Core and must remain separable from Core state evolution.

Any implementation that requires changing `gnosis/core/*` must be proposed as a separate explicit architecture task.
