# Gnozis-V2 — Context Continuity Runtime Target

Status: architecture target / no runtime implementation in this document.

## Goal

A user must be able to enter Gnozis through any connected product and continue work from durable project state without reconstructing the project manually from a previous conversation.

## Canonical recovery sequence

```text
connected product
      ↓
resolve user/project
      ↓
resolve task (if present)
      ↓
load latest context snapshot
      ↓
load current evidence / verification state
      ↓
load current repository baseline when relevant
      ↓
check permitted capabilities
      ↓
produce current factual state
      ↓
accept new request
```

## Canonical source order

When sources disagree, future runtime should prefer:

1. canonical persisted project/task state;
2. pinned repository state and reproducible runtime evidence;
3. accepted contracts/invariants;
4. independently verified audit evidence;
5. connected-product conversation history.

Conversation history is context assistance, not canonical project state.

## Minimal continuation response

A future connector should be able to obtain at least:

```text
project
active task
current status
last accepted state
last verified evidence
current baseline
blocked items
allowed next operations
```

## Example

```text
User receives notification in work chat.

User opens a different AI terminal and asks:
"What is the real state of this task?"

Terminal sends task_id/project_id through its permitted connector.

Gnozis resolves canonical state and returns:

- task status;
- implementation status;
- verification status;
- latest evidence;
- blockers;
- permitted continuation actions.

The terminal can continue the task without requiring the original chat transcript.
```

## Invariants

- No connected product becomes the canonical owner of project context.
- No notification becomes canonical state merely because it was delivered.
- A product cannot gain authority by possessing a task identifier.
- A context snapshot cannot silently grant capabilities.
- Current facts must be reconstructible from durable evidence.
- Presentation may vary between products; canonical facts may not.

## Relationship to existing contracts

This target builds on the existing Context Continuity Contract and the user/task/capability contracts. It is intentionally a runtime target rather than an implementation mandate.

## Next implementation decomposition

Future implementation should be split into independently auditable phases:

1. Task Envelope value model.
2. Context Snapshot resolver.
3. Task persistence and lifecycle.
4. Capability representation.
5. Read-only cross-terminal status query.
6. Result routing policy.
7. Connector adapters.
8. Authorization and identity enforcement.
9. Notification delivery.

Each phase must preserve Core isolation and existing Persistence semantics unless an explicit architecture task changes them.
