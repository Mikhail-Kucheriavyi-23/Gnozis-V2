# Gnozis-V2 — Durable User Context Contract

## Status

`ARCHITECTURE / CONTRACT — DOCUMENTED / NOT IMPLEMENTED`

This document defines the minimum durable context contract required for Gnozis to let a user continue a task from any authorized connected terminal. It does not authorize runtime implementation by itself.

## 1. Problem

A user may interact with Gnozis through different AI terminals, mobile applications, work chats, repositories, drives, research tools, or other products. The terminal is replaceable; the durable task context is not.

The system therefore needs a canonical, machine-readable context boundary that can be reconstructed without relying on conversational history.

## 2. Canonical context packet

The target durable context object is conceptually:

```text
ContextPacket = {
    project,
    organization_scope?,
    user_scope,
    task,
    task_state,
    relevant_context,
    evidence_refs,
    implementation_state?,
    verification_state?,
    capabilities,
    data_routes,
    output_routes,
    authority_scope,
    unresolved_findings,
    next_permitted_action,
    provenance,
    version,
    updated_at
}
```

The exact runtime representation may change, but the semantic fields above must remain distinguishable.

## 3. Non-negotiable distinctions

The context layer must never collapse these concepts:

```text
identity       != capability
capability     != authority
resource       != evidence
observation    != verified fact
proposal       != accepted decision
notification   != task state
chat history   != canonical context
connector copy != canonical state
available data != authorized data
used data      != merely available data
result         != permission to deliver result
```

## 4. Task identity and resumption

Every durable task must have a stable task identifier and enough state to resume independently of the originating terminal.

Minimum semantic task fields:

```text
task_id
project_id
owner_scope
objective
scope
state
required_inputs
expected_result
constraints
unresolved_findings
next_permitted_action
created_at
updated_at
provenance
```

A notification should carry or resolve to `task_id`; it must not be the authoritative task record.

## 5. Context versioning

Context is mutable over time, but each durable update must be attributable to a version or event sequence.

Target invariant:

```text
Context(t+1) = accepted update(Context(t), event, evidence, policy)
```

A terminal must be able to determine whether the context it recovered is current and whether it is operating from a stale snapshot.

Concurrent updates must not silently overwrite one another. The future implementation must define optimistic version checks, event ordering, or another explicit conflict rule.

## 6. Capability envelope

A terminal/session receives a bounded capability envelope, conceptually:

```text
Capability = {
    capability_id,
    provider,
    operation,
    resource_scope,
    data_classes,
    task_scope,
    expiry?,
    provenance
}
```

Examples:

```text
GitHub → read repository X
Drive  → read folder Y
Calendar → read events for task Z
Calculator → execute bounded calculation
WorkChat → receive task notification
```

A capability is an ability, not a policy decision to use the ability for every task.

## 7. Data routing

For every connected source, the target system must be able to distinguish:

```text
connected
  ↓
available
  ↓
authorized for task
  ↓
selected for this operation
  ↓
actually read/used
```

The runtime must preserve provenance for data that materially affects a result.

Personal, organizational, project, and public data must retain separate scope labels. A connector must not be able to widen its own scope by returning additional resources.

## 8. Output routing

Results require an explicit output policy. Conceptually:

```text
OutputRoute = {
    recipient_scope,
    channel,
    allowed_result_classes,
    allowed_fields?,
    redaction_policy?,
    task_scope,
    expiry?
}
```

Example:

```text
Mobile app → full result + evidence
Work chat  → summary only
Personal channel → prohibited
```

A successful analysis does not automatically authorize delivery to every connected terminal.

## 9. Result and evidence classes

Results should be typed at the architecture boundary:

```text
VERIFIED_FACT
OBSERVATION
CALCULATION
DERIVED_ANALYSIS
PROPOSAL
UNRESOLVED_CLAIM
ERROR
```

Where applicable, each result should reference:

```text
source/evidence
producer
operation/task
verification status
creation/update event
```

The system must not represent an unverified AI statement as a verified fact merely because a connector produced it.

## 10. Context recovery contract

A replacement terminal must be able to request:

```text
recover(task_id, caller_capabilities)
```

and receive only the context permitted by the caller's capabilities and routing policy.

The recovered packet should answer:

```text
What task is this?
What is its current state?
What evidence is current?
What has been verified?
What data was used?
What data may still be used?
What outputs may be sent?
What capabilities are available?
What findings remain open?
What action is currently permitted?
```

Failure to answer one of these questions must produce an explicit `UNKNOWN`, `UNVERIFIED`, or `NOT_AUTHORIZED` state rather than an inferred value.

## 11. Connector contract

A connector should expose capabilities and data through an adapter boundary. It must not write arbitrary canonical state.

Target direction:

```text
Connector
   ↓
Adapter / capability boundary
   ↓
policy + scope resolution
   ↓
context/task layer
   ↓
explicit Core contract
```

The connector layer may observe or provide inputs; it does not become Ψ-Core and does not receive implicit authority over Core evolution.

## 12. Boundary with Ψ-Core

The context layer must not introduce a second Core state model.

It may maintain durable task/context metadata needed to orchestrate work, but the semantics of Ψ-Core remain authoritative for Core state/evolution.

The target boundary is:

```text
User / Task / Context / Capability / Routing
                    ↓
             explicit adapter
                    ↓
                 Ψ-Core
                    ↓
        candidate / verification / result
                    ↓
          provenance + task update
```

## 13. Recovery after terminal loss

If a terminal disappears, reaches a usage limit, or is replaced:

```text
new terminal
    ↓
read canonical handoff
    ↓
resolve task_id
    ↓
recover current context
    ↓
resolve capabilities + routing
    ↓
continue only the permitted action
```

The new terminal must not infer unfinished work from an old chat transcript.

## 14. Organization and personal scope

The architecture supports both individual and organizational use.

Organizational scope may define work resources and policy. User-controlled personal resources remain separately scoped. A user's connection of a personal source does not grant an organization access to it by default.

Likewise, a work-chat notification does not authorize a terminal to inspect unrelated personal data.

## 15. Implementation gates

This contract does not authorize immediate runtime implementation.

Any implementation must be assigned as a bounded phase with:

```text
Primary implementer
Independent reviewer
Allowed files
Forbidden files
Acceptance tests
Security tests
Recovery tests
Conflict tests
Evidence requirements
```

The first runtime slice should be deliberately small: durable task identity + context snapshot/version + capability envelope + recovery read path. Data routing and output routing should then be added under independent security review.
