# Task Context Continuity Contract

## Purpose

Gnozis is a user-owned working context, not an application context tied to one AI product. A user may enter the same task through different connected terminals, agents, or products and continue from the durable project state without reconstructing the conversation manually.

## Core principle

```text
AI terminal is an interface/actor.
Task context belongs to the Gnozis workspace/task.
```

Connection to GitHub, Google Drive, an AI product, CRM, chat, or mobile application does not create a new authoritative context. It provides a bounded interface to an existing context.

## Continuity model

Every resumable task MUST have a durable context sufficient to reconstruct its current operational state:

```text
TaskContext = {
    task_id,
    owner_scope,
    objective,
    current_state,
    completed_work,
    pending_work,
    decisions,
    constraints,
    evidence_refs,
    capability_requirements,
    source_refs,
    output_routes,
    verification_state,
    provenance,
    updated_at
}
```

The exact storage representation is an implementation concern; the semantic fields above are architectural requirements.

## Resume operation

A connected actor MUST be able to request a bounded task resume operation:

```text
connect
  -> authenticate/identify actor
  -> resolve authorized task
  -> load durable TaskContext
  -> load relevant evidence/provenance
  -> resolve currently available capabilities
  -> resolve permitted data sources and output routes
  -> return resumable context
```

The resume result MUST distinguish:

- facts/evidence;
- decisions;
- unresolved questions;
- completed operations;
- pending operations;
- permissions/capabilities;
- verification status.

A conversation transcript alone is not sufficient evidence of task state.

## Context portability

A task MUST NOT depend on a specific AI vendor, terminal, model, chat thread, browser session, or local working directory for continuity.

Changing the interface:

```text
Claude -> ChatGPT
ChatGPT -> Gemini
mobile -> desktop
AI terminal -> CRM/chat
```

MUST NOT require rebuilding the authoritative task context from memory of the previous conversation.

## Context freshness

Every resumed context MUST expose its freshness/provenance boundary. Consumers must be able to distinguish:

```text
current durable state
stale observation
unverified claim
verified evidence
external source requiring refresh
```

No actor may silently present stale context as current fact.

## Multi-terminal operation

Multiple connected actors may work on different tasks or on the same task. Concurrent work MUST be represented explicitly rather than inferred from chat history.

The architecture must eventually support:

- task leases or equivalent conflict control;
- operation identity;
- idempotency keys;
- append-only audit events;
- conflict detection;
- deterministic reconciliation rules.

These are requirements for the future execution layer; this document does not claim they are already implemented.

## Data routing

Task context is not automatically broadcast to every connected product.

Routing MUST remain subject to:

```text
owner scope
+ actor identity
+ capability
+ data-source permission
+ output policy
+ task scope
```

A connected product may receive only the subset of context and evidence permitted for that actor and route.

## Practical user scenario

A user receives a task notification in one product, opens another AI terminal, asks for the real current status, and expects a response based on the durable Gnozis context and permitted connected sources.

The expected flow is:

```text
notification
   -> task_id
   -> authorized context resolution
   -> current evidence retrieval
   -> verification/status evaluation
   -> bounded analysis
   -> routed response
```

The response must state when required evidence is unavailable, stale, or unverified instead of inventing continuity.

## User spectrum

The contract is intentionally domain-neutral. The same continuity model must support users ranging from:

- managers and operators;
- developers and researchers;
- engineers;
- analysts;
- scientists processing large datasets;
- organizational users using Gnozis as a shared analytical/CRM-like core.

The domain-specific product remains an interface. The durable task/context model remains shared.

## Organizational model

A company may use Gnozis as a shared analytical core while individual users retain their own connected tools and routing preferences.

Conceptually:

```text
Company / workspace
        |
        +-- shared tasks / permitted data
        |
        +-- user A -> personal tools / routes
        +-- user B -> personal tools / routes
        +-- bot/chat -> bounded company interface
```

Shared organizational context MUST NOT imply unrestricted access to every user's private context.

## Architectural boundary

This contract does not authorize autonomous modification of Core, Identity, Memory, Bridge, or Federation semantics. It defines the continuity requirement that those components must eventually satisfy.

Implementation changes require a separate explicit bounded task and independent verification.

## Acceptance criteria for future implementation

A future implementation phase must demonstrate at minimum:

1. durable task identification;
2. context persistence independent of AI terminal;
3. resume from a second connected actor;
4. provenance/evidence reconstruction;
5. capability and routing resolution;
6. stale/unverified context distinction;
7. scope isolation;
8. auditability;
9. no dependency on conversation transcript as the source of truth.

This document is a contract and design direction, not a claim that all criteria are currently implemented.
