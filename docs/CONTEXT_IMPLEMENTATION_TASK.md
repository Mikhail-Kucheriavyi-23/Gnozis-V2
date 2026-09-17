# Gnozis-V2 — Context Implementation Task

## Status

`TASK SPECIFICATION — IMPLEMENTATION AUTHORIZED ONLY WITHIN THIS SCOPE`

This task implements the first runtime slice defined by `docs/CONTEXT_CONTRACT.md`.

## Objective

Create a durable, terminal-independent TaskContext layer so an authorized client can create, read, update, and reconstruct a task without relying on conversation history.

## Scope

Implement only:

```text
context types
context repository
create/update/read
optimistic revision protection
context reconstruction / handoff
contract tests
```

## Required semantic fields

The implementation must represent the contract fields:

```text
context_id
project_id
task_id
organization_scope?
user_scope
objective
current_task_state
required_inputs[]
context_references[]
evidence_references[]
implementation_state
verification_state
unresolved_findings[]
next_permitted_action
available_capabilities[]
allowed_data_sources[]
allowed_output_destinations[]
created_at
updated_at
revision
```

The exact storage representation may be chosen by the implementer, but semantics must not be silently removed.

## Required invariants

### 1. Identity

`context_id` uniquely identifies one durable context.

`task_id` must not silently identify unrelated contexts across projects.

### 2. Revision control

Every successful update increments `revision`.

An update with `expected_revision != current revision` must fail without modifying the stored record.

No last-write-wins overwrite is permitted.

### 3. Recovery

Close/reopen of the storage layer must preserve the complete canonical context.

A fresh client must be able to reconstruct the task from durable context alone.

### 4. State separation

The implementation must preserve separate values for:

```text
current_task_state
implementation_state
verification_state
```

A reported implementation must not automatically become verified or accepted.

### 5. Scope explicitness

Every context must have an explicit `user_scope`.

Organization scope may be absent for a personal task.

No context may silently inherit arbitrary connected-source data.

### 6. Capability semantics

`available_capabilities` describe possible operations only.

They must not be interpreted by this layer as authentication, authorization, or permission grants.

### 7. Core isolation

No writes to:

```text
gnosis/core/*
gnosis/instances/*
states
relations
candidates
transitions
instances.current_state_id
```

No imports of Core execution machinery are required for this phase.

### 8. Memory isolation

Do not import, modify, or depend on the unaccepted Memory implementation.

Context may contain evidence references as opaque identifiers/metadata only.

### 9. Connector isolation

Do not implement GitHub, Drive, chat, CRM, Internet Bridge, or AI-provider adapters in this phase.

The context layer stores routing declarations; it does not execute external delivery or data retrieval.

## Allowed repository changes

Preferred new namespace:

```text
gnosis/context/
```

Allowed tests:

```text
tests/test_context_*.py
```

A focused documentation update may be made only if required to describe the actual implementation.

Do not modify:

```text
gnosis/core/*
gnosis/instances/*
gnosis/storage/repositories.py
gnosis/storage/__init__.py
gnosis/memory/*
identity/authentication/authorization
Internet Bridge
```

If persistence integration genuinely requires a change outside the allowed files, stop and report the exact dependency instead of expanding scope silently.

## Required API shape

Names may differ if semantics remain equivalent, but the implementation must provide operations equivalent to:

```python
create_context(context) -> stored_context
get_context(context_id) -> stored_context
update_context(context_id, expected_revision, patch) -> stored_context
reconstruct_context(context_id) -> ContextHandoff
```

`ContextHandoff` must expose at least:

```text
objective
current state
implementation state
verification state
evidence references
unresolved findings
allowed data sources
available capabilities
allowed output destinations
next permitted action
revision
```

## Mandatory tests

At minimum:

1. create and read round-trip;
2. complete field preservation;
3. close/reopen recovery;
4. update increments revision;
5. stale revision is rejected;
6. rejected stale update leaves bytes/state unchanged;
7. reconstruction from a fresh repository/client;
8. separate user scopes do not merge implicitly;
9. organization and personal contexts remain distinguishable;
10. capability declarations do not grant permission;
11. evidence references remain references rather than copied hidden state;
12. Core boundary test;
13. Memory boundary test;
14. no connector execution from Context;
15. invalid task-state / verification-state combinations are rejected where the contract defines them;
16. full existing regression suite remains green.

## Acceptance evidence

The implementation report must include:

```text
changed files
exact commit SHA
real test command
real test result
compileall result
Core isolation evidence
Memory isolation evidence
revision-conflict evidence
recovery evidence
known limitations
```

A custom/offline test shim may be included as supplementary evidence but cannot replace real pytest.

## Independent verification

After implementation, a different agent must perform a read-only audit against the pinned commit/artifact.

The auditor must independently verify at least:

```text
source scope
schema/storage behavior
revision atomicity
recovery
scope separation
Core isolation
Memory isolation
connector isolation
real pytest
compileall
```

Any finding that affects an invariant requires corrective implementation and re-audit before acceptance.

## Explicit non-goals

This phase does NOT implement:

- authentication;
- authorization;
- encryption;
- cryptographic integrity;
- Memory acceptance;
- Internet Bridge;
- external connector execution;
- autonomous AI agents;
- Core evolution changes;
- routing/delivery execution;
- organization-wide policy enforcement.

## Success condition

The phase is successful when a new terminal can resolve a durable TaskContext and answer:

```text
What is the task?
What is its actual current state?
What is implemented?
What is verified?
What evidence exists?
What remains unresolved?
What may be accessed?
What may be done next?
```

without access to the previous AI conversation, while preserving all declared boundaries.
