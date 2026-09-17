# Gnozis-V2 — Context Continuity Contract

## Purpose

Gnozis-V2 is a user-facing architecture in which the durable project context belongs to Gnozis, not to a particular AI product, terminal, chat session, GitHub workspace, or Google Drive session.

A connected AI is replaceable. A project context must remain recoverable.

This contract defines the minimum semantics required for a new or returning AI to continue work from the current durable project state without reconstructing the project from prior conversation history.

## Core principle

```text
AI product != project memory
AI product != project state
connector != authority
conversation history != source of truth
```

The canonical repository and accepted durable project artifacts outrank any individual AI session.

## Context Continuity model

```text
USER
  ↓
AI TERMINAL / PRODUCT
  ↓
CONNECTOR
  ↓
CONTEXT CONTINUITY
  ├── Identity scope
  ├── Current project state
  ├── Active task
  ├── Accepted decisions
  ├── Pending decisions
  ├── Evidence
  ├── Provenance
  ├── Authority scope
  └── Recovery point
  ↓
Ψ-Core / durable project state
```

Connectors are access paths. They are not independent sources of architectural truth.

## ContextSnapshot

A `ContextSnapshot` is a recoverable projection of the durable project state needed by an authorized agent to continue a task.

It is **not** a second Ψ-Core `State` model.

Minimum logical fields:

```text
context_id
user_scope
project_scope
current_task
current_project_state
accepted_decisions
pending_decisions
active_agents
authority_scope
relevant_memory
 evidence_refs
provenance
last_verified
recovery_point
```

The physical representation may change during implementation. These are contract semantics, not a mandatory database schema.

## ContextRequest

A context request must identify the scope required to recover work. Conceptually:

```text
ContextRequest
├── user_scope
├── project_scope
├── task_scope (optional)
├── agent_identity (when available)
└── requested_evidence_depth
```

An implementation must not silently widen the requested scope.

## ContextResponse

A context response must distinguish at least:

```text
IMPLEMENTATION
VERIFICATION
ACCEPTANCE
AUTHORITY
EVIDENCE
NEXT PERMITTED ACTION
```

These states must never be collapsed into a single `status` value.

Example:

```text
Implementation: IMPLEMENTED
Verification: VERIFIED_BY_TESTS
Acceptance: NOT_ACCEPTED
Authority: implementation-only / bounded
Next permitted action: independent re-audit
Evidence: commit + test/audit references
```

## Evidence and provenance

A contextual statement must be traceable to durable evidence whenever it is presented as a verified fact.

Evidence precedence remains:

1. current source;
2. reproducible runtime behavior and real tests/CI;
3. accepted contracts/invariants;
4. independent audit evidence;
5. AI reports and proposals.

A conversation message alone is not sufficient evidence of repository state.

## Memory boundary

Memory stores durable information relevant to project continuity. Context selects and presents the subset required for the current task.

```text
Memory
  ↓ projection
ContextSnapshot
  ↓ interpretation
AI session
```

Memory must not become a second Core state machine.

Context must not silently mutate Core state merely because an agent requested context.

## Core boundary

The authoritative Ψ-Core state remains separate from contextual projections.

```text
Ψ-Core State
    = authoritative system state

ContextSnapshot
    = recoverable agent-facing projection
```

A context request is read/recovery behavior unless a separate explicitly authorized task permits a state-changing operation.

## Authority boundary

Receiving context does not grant authority to modify the project.

```text
access
  ↓
identity/scope
  ↓
context recovery
  ↓
explicit task
  ↓
bounded capability
  ↓
execution
  ↓
verification
  ↓
gate
```

GitHub, Google Drive, AI-terminal, or other connector access is an operational capability only.

## Continuation invariant

If two authorized AI products request the same current project context for the same user/project/task scope, they should receive semantically equivalent current state, evidence, authority and next-action information, subject only to interface-specific presentation.

The project must not depend on which AI product happened to hold the previous conversation.

## Recovery invariant

A new AI must be able to reconstruct the active work state from durable project artifacts without access to the previous AI's conversation history.

At minimum it must recover:

```text
current HEAD
active phase
implementation state
verification state
acceptance state
role assignment
allowed scope
forbidden scope
latest tested commit
open findings
next permitted action
```

## Runtime feedback

Real interaction with connected AI systems is part of the development strategy.

Runtime observations may expose missing requirements, useful interfaces, or incorrect assumptions. They do not automatically become canonical architecture. New architectural requirements must be explicitly documented and gated.

## Practical acceptance test

The first practical test of this contract is deliberately simple:

1. Start a fresh AI session with no prior Gnozis conversation history.
2. Give it access to the canonical repository.
3. Point it to `AI_CONTEXT.md`, `STATUS.md`, `docs/AI_HANDOFF_PROTOCOL.md`, `docs/MULTI_AGENT_BUILD_STRATEGY.md`, `AGENT_ROLES.md`, and this contract.
4. Ask:

   > Continue Gnozis from the current confirmed state. Do not rely on previous conversation history. First recover the project context and report the next permitted action.

5. The AI must reconstruct the current baseline from repository evidence.
6. It must not claim Memory is accepted merely because a Memory artifact exists outside `main`.
7. It must not restart Persistence.
8. It must identify the current Memory corrective/re-audit sequence and its scope.
9. It must wait for or execute only an explicitly assigned bounded task.

This test validates **context recovery**, not autonomous authority.

## Future implementation direction

A future implementation may expose explicit operations equivalent to:

```text
RecoverContext(user, project, task?)
GetEvidence(context_id, reference)
GetCurrentTask(context_id)
GetAuthority(context_id)
```

These names are conceptual until an implementation phase is explicitly authorized.

No API, database schema, Identity system, encryption layer, Bridge, or Core modification is implied by this document.

## Current scope

This contract is an architectural/documentation layer only.

It does not accept or merge the Memory artifact, does not implement authentication/authorization, does not implement encryption, and does not declare Gnozis autonomous or federated.
