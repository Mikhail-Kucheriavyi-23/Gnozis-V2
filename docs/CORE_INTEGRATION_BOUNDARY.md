# Gnozis-V2 — Core Integration Boundary

Status: architecture contract / implementation not yet accepted.

## Purpose

Define how the emerging user/connector/task architecture interacts with Ψ-Core without turning the Core into a generic application database or connector runtime.

## Architectural separation

```text
External products / AI agents
            ↓
      Connector boundary
            ↓
     Task / Context layer
            ↓
       Workspace layer
            ↓
 Candidate generation / proposal
            ↓
 Ψ-Core: Test → Verify → Commit
            ↓
     canonical state evolution
```

The Core remains the source of truth for its own state evolution.

## Core must not become

The following must remain outside `gnosis/core/*` unless a separate architecture decision explicitly changes the boundary:

- chat history;
- connector-specific APIs;
- CRM semantics;
- mobile UI state;
- Google Drive implementation;
- arbitrary user routing rules;
- authentication implementation;
- notification transport;
- agent session state;
- application-specific workflow state.

## What may enter Core

Only a bounded candidate/proposal that satisfies the existing Core contract may be evaluated by Core.

Conceptually:

```text
external observation
      ↓
normalized proposal
      ↓
Candidate
      ↓
Test
      ↓
Verify
      ↓
Commit
```

The external agent does not directly mutate canonical Core state.

## Feedback loop

Runtime work is allowed to reveal that the architecture is missing an invariant, interface, or capability.

The feedback path is:

```text
runtime observation
      ↓
evidence
      ↓
architecture proposal
      ↓
explicit review
      ↓
contract update
      ↓
implementation
      ↓
independent verification
```

A convenient runtime behavior must not silently become a Core invariant.

## User-facing analytical architecture

A manager, engineer, researcher, or scientist may submit materially different tasks through different products.

The user-facing layer normalizes these into durable tasks and evidence while Core evaluates only the proposals relevant to its own mathematical state model.

Thus:

```text
manager question ─┐
research question ├→ Task / Context → proposal → Core
physics dataset ──┤
engineering task ─┘
```

The diversity of users does not require multiple incompatible Core state models.

## Multi-agent feedback

Different agents can contribute observations, implementations, tests, or audits to the same task.

Their outputs remain attributable evidence. Agreement between agents is not itself proof.

```text
Agent A ─┐
Agent B ─┼→ evidence / proposals → Core evaluation
Agent C ─┘
```

## Persistent context boundary

Durable context belongs to the orchestration/persistence layer, not automatically to Ψ-Core.

A Context Snapshot can identify:

- task state;
- repository baseline;
- evidence;
- pending actions;
- capability requirements;
- verification state.

It must not become a second representation of Ψ-Core state.

## Safety boundary

No connector or agent may use context restoration as an implicit authorization mechanism.

```text
context recovered
      ≠
action authorized
      ≠
Core state accepted
```

## Implementation rule

Future implementation tasks should prefer new boundary modules over modifying `gnosis/core/*`.

If a requirement cannot be implemented without changing Core semantics, it must be raised as a separate architecture task with:

1. mathematical justification;
2. invariant impact;
3. compatibility analysis;
4. migration strategy;
5. independent tests;
6. independent audit.

## Current phase

This document defines the target boundary only. It does not authorize implementation of connectors, authorization, routing, or Core modifications.
