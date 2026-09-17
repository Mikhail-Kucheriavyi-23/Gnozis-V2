# Gnozis-V2 — Architecture Implementation Sequencing

## Status

`ARCHITECTURE CONTRACT — CURRENT SINGLE-OWNER PHASE`

This document defines how the two current architectural tracks relate. It prevents future AI agents from treating the long-term architecture as one undifferentiated implementation task.

## 1. Current operating boundary

The project is currently a single-owner, single-account, single-canonical-repository experiment.

```text
ONE OWNER
   ↓
Gnozis-V2
   ├── durable project/task continuity
   ├── Ψ-Core
   ├── persistence
   ├── audit/provenance
   └── controlled self-reflection foundation
```

Multi-user, multi-tenant and federation runtime are future strategy only.

## 2. Two architectural tracks

### Track A — User Continuity

Purpose: make work recoverable from durable project/task context by another authorized terminal without relying on conversation history.

Canonical contracts:

- `docs/USER_ARCHITECTURE.md`
- `docs/CONTEXT_CONTRACT.md`
- `docs/CONTEXT_IMPLEMENTATION_TASK.md`

First runtime slice:

```text
Context types
    ↓
Context repository
    ↓
Revision-safe create/update/read
    ↓
Context reconstruction / handoff
    ↓
Real tests
    ↓
Independent audit
```

Track A must not implement authentication, authorization, encryption, external connectors, routing execution, Memory acceptance, or Ψ-Core changes.

### Track B — Core Self-Reflection

Purpose: make Core execution observable and eventually enable evidence-based proposals for rule changes without giving reflection direct authority over canonical Core.

Canonical contracts:

- `docs/CORE_REFLECTION_ROADMAP.md`
- `docs/CORE_REFLECTION_R1_TASK.md`

Runtime sequence:

```text
R1 Foundation
    ↓
R2 Observation / Finding
    ↓
R3 Counterexample
    ↓
R4 Shadow Evaluation
    ↓
R5 Governance / Rollback
    ↓
R6 Endogenous Rule Generation
```

Track B must not implement unrestricted self-modification, autonomous rule activation, a second State model, Memory, Identity, Bridge, or federation.

## 3. Relationship between tracks

The tracks are complementary but independently bounded.

```text
                 Gnozis-V2
                     │
          ┌──────────┴──────────┐
          ↓                     ↓
     Track A                  Track B
 User/Task Continuity     Core Reflection
          │                     │
          ↓                     ↓
 durable context          evidence/proposals
          │                     │
          └──────────┬──────────┘
                     ↓
              future integration
```

Track A does not become a second Core state model.
Track B does not become a user/session management system.

## 4. Recommended implementation order

For the current product goal, **Track A is the first practical runtime proof of the user-centered architecture**, because it directly tests the fundamental property:

> another authorized terminal can continue a task from durable context rather than conversation history.

Track B may then proceed as an independent bounded Core modernization track.

The two tracks may be developed by different AI agents, but neither may silently expand into the other.

## 5. Shared invariants

Both tracks must preserve:

```text
canonical source is durable
conversation is non-canonical
implementation ≠ verification ≠ acceptance
capability ≠ authority
connector ≠ source of truth
provenance is explicit
historical evidence is not silently rewritten
Core semantics remain authoritative
```

## 6. Future integration boundary

Only after both tracks are independently verified may the project define a higher-level orchestration layer connecting:

```text
TaskContext
    ↓
allowed capabilities / evidence
    ↓
Core execution
    ↓
reflection evidence
    ↓
verified result
    ↓
TaskContext update
```

This future orchestration layer must use explicit contracts. It must not bypass Core invariants or treat an AI terminal as the owner of canonical state.

## 7. Future multi-user boundary

Multi-user cooperation is intentionally deferred.

When eventually introduced, it must be an additional authorization/identity/trust layer around the existing contracts rather than a rewrite of Ψ-Core or the single-owner continuity model.

The future target is:

```text
multiple users
    ↓
explicit identities / scopes
    ↓
shared or private task contexts
    ↓
capability + data routing policies
    ↓
Core / analysis
    ↓
provenance-aware results
```

No implementation of this future layer is authorized by this document.

## 8. Handoff rule

A new AI agent must first inspect the current source, tests and CI, then read this sequencing document and the contract for the specific track it is assigned.

It must not infer that another track is complete merely because its documentation exists.

The active task is always the narrowest explicitly assigned bounded phase.
