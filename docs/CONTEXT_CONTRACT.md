# Gnozis-V2 — Canonical Context Continuity Contract

## Status

`ARCHITECTURE CONTRACT — IMPLEMENTATION NOT YET ACCEPTED`

This contract defines the first implementation slice of the user-centered architecture: a durable, terminal-independent representation of a task that allows an authorized product or AI system to resume work without relying on conversation history.

It does **not** implement authentication, authorization, Memory, routing, or Ψ-Core changes.

## 1. Purpose

Gnozis must preserve the canonical state of work independently of the AI terminal used to access it.

A connected product is an interface to the project context, not the owner of that context.

Therefore:

```text
terminal A
   ↓
canonical context
   ↓
terminal B
```

must preserve semantic continuity.

## 2. Canonical Task Context

The minimum logical object is:

```text
TaskContext {
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
}
```

The names above are semantic fields, not a final storage schema.

## 3. Source-of-truth rules

The following distinction is mandatory:

```text
conversation history     = convenience/contextual input
canonical TaskContext    = durable task continuity
Memory                   = supporting durable evidence/context
Ψ-Core State              = canonical evolutionary state of Core
```

No connector conversation may silently become canonical project state.

No TaskContext implementation may create a competing Ψ-Core `State` model.

## 4. Task state

`current_task_state` must describe the workflow state, not reproduce the entire Core state.

Minimum semantic states:

```text
proposed
active
blocked
awaiting_review
corrective
verified
accepted
closed
```

The exact transition matrix belongs to the implementation task and must be explicit before code is accepted.

## 5. Verification state

Implementation and verification are separate dimensions.

A context record must be able to distinguish at least:

```text
reported
implemented
runtime_verified
independently_verified
accepted
rejected
```

An AI message saying `PASS` is never equivalent to independent verification.

## 6. Evidence references

Context should reference evidence rather than silently copying unbounded external data.

An evidence reference should eventually identify:

```text
source
locator
content/type
producer
observed_at
provenance
verification_status
integrity/reference hash when available
```

This enables a new terminal to reconstruct why the current task state exists.

## 7. Capabilities

A capability listed in context means only that the capability is available for consideration.

It does **not** grant authority.

Required distinction:

```text
capability exists
        ≠
capability enabled
        ≠
capability authorized for task
        ≠
action authorized
```

This prevents GitHub/Drive/AI access from becoming implicit architectural authority.

## 8. Data-source policy

A context may reference connected sources, but every source must eventually pass these gates:

```text
connected
  ↓
identified
  ↓
allowed for scope
  ↓
allowed for task
  ↓
allowed data class
  ↓
actually selected
```

The context contract must never interpret mere connector presence as permission to consume all available data.

## 9. Output policy

A result is not complete until its permitted destination is known.

```text
verified result
  ↓
recipient scope
  ↓
allowed data class
  ↓
allowed destination
  ↓
delivery
```

The implementation must prevent a connected channel from becoming an implicit exfiltration path.

## 10. Recovery / handoff contract

An authorized terminal requesting a task context must receive enough information to continue without the previous conversation.

Minimum recovery response:

```text
WHAT IS THE TASK?
WHAT IS THE CURRENT STATE?
WHAT IS ACTUALLY IMPLEMENTED?
WHAT IS VERIFIED?
WHAT IS ONLY REPORTED?
WHAT EVIDENCE SUPPORTS THE STATE?
WHAT REMAINS UNRESOLVED?
WHAT DATA MAY BE USED?
WHAT CAPABILITIES ARE AVAILABLE?
WHAT OUTPUTS ARE ALLOWED?
WHAT ACTION IS PERMITTED NEXT?
```

The response should be compact and reference durable evidence rather than duplicating entire files or conversations.

## 11. Revision and concurrency

Task context is versioned logically by `revision`.

A future write API must reject or explicitly reconcile stale revisions rather than silently overwriting newer context.

Required invariant:

```text
write(expected_revision = R)
    succeeds only if
current_revision == R
```

The exact concurrency mechanism is an implementation concern and must be tested independently.

## 12. Core boundary

TaskContext may prepare inputs for Core through an explicit adapter.

It may not:

- mutate `gnosis/core/*` directly;
- define a second `State` machine;
- store hidden Core state in conversation history;
- bypass Candidate → Test → Verify → Commit;
- allow a connector to redefine Ψ-Core evolution semantics.

## 13. Security boundary

This contract deliberately does not implement:

- authentication;
- authorization;
- encryption;
- cryptographic integrity;
- secret storage;
- connector credentials.

These must be separate bounded phases.

`user_scope` and `organization_scope` are context identifiers, not proof of identity or permission.

## 14. Implementation slice

The first runtime implementation task derived from this contract should contain only:

```text
context types
context repository
create/update/read task context
revision conflict protection
context reconstruction
contract tests
```

It must not modify:

```text
gnosis/core/*
gnosis/instances/*
gnosis/storage/repositories.py
gnosis/storage/__init__.py
Memory implementation
Identity/authentication/authorization
Internet Bridge
```

unless a separate explicit task authorizes it.

## 15. Acceptance evidence

The first implementation is not accepted from a code review alone.

Minimum evidence:

1. real test execution;
2. stale-revision rejection;
3. close/reopen recovery;
4. terminal-independent reconstruction from durable context;
5. proof that Core tables/state are untouched;
6. proof that unscoped data cannot be silently attached to a task;
7. independent adversarial audit;
8. corrective pass if findings remain;
9. re-audit;
10. ChatGPT integration gate.

## 16. Target user experience

A user may receive:

```text
Task #123 requires verification.
```

in a work chat.

The user can then open any connected AI terminal and ask:

```text
What is the real state of Task #123 and what can I do next?
```

The terminal should resolve the canonical context and return an evidence-aware answer without requiring the previous AI conversation.

The same mechanism must eventually support both:

```text
individual user workflows
```

and:

```text
organization / CRM / team workflows
```

without collapsing their data scopes.

## 17. Required development loop

```text
contract
  ↓
bounded implementation
  ↓
real execution
  ↓
adversarial audit
  ↓
correction
  ↓
re-audit
  ↓
integration gate
```

The contract itself is now canonical architectural input for the first Context implementation phase. It does not claim that the runtime exists.
