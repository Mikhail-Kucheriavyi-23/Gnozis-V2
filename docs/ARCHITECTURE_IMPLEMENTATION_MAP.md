# Gnozis-V2 — Architecture Implementation Map

Status: working architecture map; implementation stages require explicit tasks and independent verification.

## Goal

Gnozis is being built as a user-facing architecture in which a person or organization can continue the same work from different connected products without losing canonical task state, context, evidence, or capability boundaries.

Users may range from managers and programmers to engineers, scientists and physicists working with large analytical datasets. The interface must remain separate from Ψ-Core.

## Canonical layers

```text
Connected products
  ├─ AI terminals
  ├─ mobile app
  ├─ web UI
  ├─ work chat / bot
  ├─ CRM
  └─ research / engineering tools
          ↓
Connector / Adapter
          ↓
Capability + Scope
          ↓
Task / Context / Evidence
          ↓
Workspace / Proposal
          ↓
Ψ-Core boundary
          ↓
Candidate → Test → Verify → Commit
          ↓
Durable state + audit
```

## Existing foundations

### Persistence

Persistence is already in `main` and is the durable foundation for Core state, transitions, instances and audit semantics. New user-facing layers must not create a second persistence system.

### Memory

The current Memory implementation remains unaccepted until its corrective pass and independent re-audit complete. It must not be treated as canonical production Memory yet.

### Core

`gnosis/core/*` remains the semantic source of truth for Ψ evolution. Tasks, connectors, notifications, transcripts and orchestration must not silently become a second Core.

## Required architectural components

### 1. Task layer

Canonical durable task identity and lifecycle. See `docs/TASK_LIFECYCLE_CONTRACT.md`.

Future minimum entities:

```text
Task
TaskCheckpoint
TaskEvent
TaskEvidenceRef
TaskClaim
TaskConflict
```

### 2. Context layer

Portable continuation context assembled from canonical task state rather than chat history.

A Context Snapshot should identify at least:

```text
snapshot_id
task_id
baseline
implementation_state
verification_state
acceptance_state
completed
pending
blocked
next_permitted_actions
evidence_refs
capability_refs
producer
sequence
```

### 3. Evidence layer

Evidence must be addressable independently of the product that produced it: commit/diff, test result, artifact + SHA-256, audit report, human decision, runtime observation, or external document.

An AI statement is not equivalent to evidence.

### 4. Capability / Connector layer

Connectors translate product-specific operations into bounded Gnozis operations. Repository or Drive access does not itself grant architectural authority.

### 5. Routing / notification layer

Notifications reference canonical tasks and evidence; they are not authoritative state.

Examples: work chat → `TASK_READY_FOR_REVIEW`; mobile → `TASK_BLOCKED`; AI terminal → `continue(task_id)`; CRM → task result/action request.

### 6. Workspace / proposal layer

External products may produce observations, analyses, candidate actions and artifacts without directly mutating Ψ-Core:

```text
external observation
      ↓
proposal
      ↓
Core-compatible candidate
      ↓
Test
      ↓
Verify
      ↓
Commit
```

## User and organization model

The system should not create separate architectures for manager, programmer, engineer, scientist, physicist or company. Users differ primarily through capabilities, connected products, data scopes, tasks, policies and output preferences.

A company may use Gnozis as an analytical/CRM coordination layer while individual users connect personal tools and determine which information may be routed to which task or analysis context. Personal and organizational connectors must remain distinguishable, with explicit sharing.

## Core integration boundary

```text
Task state        ≠ Ψ State
Context snapshot  ≠ Ψ State
Memory            ≠ Ψ State
Connector state   ≠ Ψ State
Notification      ≠ Ψ State
Agent transcript  ≠ Ψ State
```

Only the Core's accepted transition mechanism may commit semantic Core evolution.

## Practical continuation scenario

```text
1. User receives TASK_ACTION_REQUIRED in a work chat.
2. User opens any connected AI terminal.
3. Terminal resolves task_id.
4. Gnozis loads the latest accepted checkpoint + evidence.
5. Capability/scope is resolved for that terminal.
6. Terminal receives bounded continuation context.
7. User asks for the real current status.
8. Terminal reports canonical state and evidence, not a reconstructed guess.
9. If work is requested, a bounded proposal/action is created.
10. Verification and acceptance remain explicit.
```

The same task may then be resumed from mobile, web, another AI terminal, CRM or research tooling.

## Parallel implementation tracks

### Track A — Core-facing architecture

1. Preserve Ψ-Core boundary.
2. Formalize candidate/proposal ingress.
3. Define task-to-Core transition references.
4. Define evidence references for accepted Core transitions.
5. Define a bounded execution interface without embedding connectors into Core.

### Track B — User continuity

1. Task entities.
2. Checkpoints.
3. Portable Context Snapshot.
4. Evidence reference model.
5. Continuation/resume contract.
6. Notification references.

### Track C — Connectors

1. Generic connector contract.
2. Capability resolution.
3. Scope resolution.
4. GitHub adapter.
5. Google Drive adapter.
6. AI-terminal adapter.
7. Chat/mobile adapters.

Adapters remain replaceable and are not canonical data stores.

### Track D — Organization / routing

1. Personal vs organization scope.
2. Routing policies.
3. Recipient/output policies.
4. Routing audit.
5. Company/CRM integration boundary.

## Safe work vs explicit architecture gates

Safe to design or implement without changing Ψ-Core semantics:

- task/checkpoint data model;
- context snapshot schema;
- evidence reference schema;
- connector/capability interfaces;
- routing/notification event schema;
- read-only continuation API;
- architecture tests for Core isolation.

Separate explicit architecture tasks are required before:

- changing `gnosis/core/*` semantics;
- automatic Core mutation from external connectors;
- identity/authentication/authorization model;
- encryption and cryptographic integrity;
- federation/trust semantics;
- autonomous self-modification.

## Gate rule

```text
explicit task
  ↓
bounded implementation
  ↓
real execution/tests
  ↓
independent verification
  ↓
correction
  ↓
re-verification
  ↓
ChatGPT integration gate
```

No connected product can bypass this sequence by virtue of having repository or cloud access.
