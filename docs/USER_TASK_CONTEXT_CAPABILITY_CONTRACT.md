# Gnozis-V2 — User / Task / Context / Capability Contract

## Purpose

This document extends the Context Continuity Contract into the intended user-facing architecture.

Gnozis is designed to be usable through multiple products and terminals without requiring the user to rebuild project context manually.

A user may be:

- an individual developer;
- a manager coordinating work;
- a researcher or scientist processing large datasets;
- an analyst;
- a technical specialist;
- an organization using Gnozis as a shared analytical/project core.

The connected product is an interface. The durable project state and Gnozis contracts remain independent of the interface.

## 1. Architectural model

```text
                         USER
                           │
                  intent / request / policy
                           │
                           ▼
                ┌─────────────────────┐
                │   CONTEXT LAYER     │
                │ project/task state  │
                │ history/evidence    │
                └──────────┬──────────┘
                           │
                           ▼
                ┌─────────────────────┐
                │    TASK LAYER       │
                │ objective/scope     │
                │ acceptance criteria │
                └──────────┬──────────┘
                           │
                           ▼
                ┌─────────────────────┐
                │ CAPABILITY LAYER    │
                │ allowed resources   │
                │ operations/tools    │
                └──────────┬──────────┘
                           │
                           ▼
                ┌─────────────────────┐
                │      GNOZIS         │
                │ analysis / Core /   │
                │ persistence /       │
                │ future agents       │
                └──────────┬──────────┘
                           │
                           ▼
                    evidence + result
                           │
                           ▼
                  selected user tools
```

The layers must remain separable. A capability is not an authority grant; a task is not identity; context is not authentication.

## 2. User model

The system must eventually represent a durable user context independently of any single AI product.

Conceptual identity:

```text
User
 ├── user_id
 ├── owned projects
 ├── connected products/resources
 ├── task preferences
 ├── routing preferences
 └── capability grants
```

The identity implementation is intentionally outside this documentation-only phase.

## 3. Connected products

A connected product may be:

```text
AI assistant
AI coding terminal
mobile application
work chat / bot
Google Drive
GitHub
local terminal
future plugin / connector
```

These are resource or interaction surfaces.

A connection must expose only the capabilities explicitly granted to it.

Example:

```text
Mobile app
  → may read task status
  → may submit a user request
  → may receive selected results

Coding terminal
  → may read repository
  → may execute tests
  → may modify only explicitly assigned scope

Drive connector
  → may provide external documents/artifacts
  → does not itself authorize repository modification
```

## 4. Task as the unit of work

Every actionable request should eventually become a durable Task Envelope.

Minimum conceptual fields:

```text
task_id
user_id
project_id
created_at
objective
context_snapshot_id
baseline_commit
allowed_scope
forbidden_scope
required_capabilities
acceptance_criteria
evidence_required
requested_result_channel
status
```

The task must remain understandable after the originating conversation disappears.

## 5. Capability model

Capabilities describe what a connected product or agent is permitted to do.

Examples:

```text
READ_PROJECT
READ_EXTERNAL_ARTIFACT
RUN_TESTS
WRITE_DOCUMENTATION
WRITE_CODE
CREATE_TASK
SUBMIT_ANALYSIS
READ_TASK_STATUS
RECEIVE_RESULT
```

Future implementation must distinguish at least:

```text
resource access
operation capability
architectural authority
```

They are not equivalent.

## 6. Context as a durable projection

A context snapshot answers:

```text
Where is the project now?
What is implemented?
What is verified?
What is accepted?
What is unresolved?
What task is active?
What may happen next?
```

It must not depend on hidden conversation history.

The existing `PROJECT_CONTEXT.json` is the first machine-readable implementation of this principle.

## 7. Task lifecycle

```text
REQUEST
  ↓
CONTEXT RESOLUTION
  ↓
CAPABILITY CHECK
  ↓
BOUNDED EXECUTION
  ↓
RESULT / EVIDENCE
  ↓
PERSISTED TASK STATE
  ↓
AVAILABLE TO OTHER CONNECTED PRODUCTS
```

A task can therefore be created in one interface and continued in another.

Example:

```text
Work chat
  → notification: analysis task requires attention

Mobile AI
  → user asks: "What is the actual state?"

Gnozis
  → reconstructs context from durable evidence
  → checks task status
  → returns current verified state

Coding terminal
  → user continues implementation

Mobile AI
  → receives the resulting status/report if routing permits
```

## 8. Result routing

Results should eventually be routable independently of the product that created the task.

Conceptual routing policy:

```text
Task result
   ├── user mobile app
   ├── work chat
   ├── coding terminal
   ├── email/document channel
   └── another authorized AI product
```

The user should be able to configure which classes of results may be delivered to which connected products.

No result should be routed merely because a connector exists.

## 9. Organization / CRM use case

Gnozis may eventually operate as an analytical/project core for an organization.

Example:

```text
CRM / work chat / operational systems
                ↓
          authorized tasks
                ↓
             Gnozis
                ↓
       analysis / synthesis
                ↓
       role-specific results
                ↓
 managers / engineers / researchers / users
```

Different users may receive different result views according to explicit capability and routing policies.

This does not imply that Gnozis automatically receives unrestricted organizational data.

## 10. Multi-agent model

There are two distinct meanings of multi-agent operation:

### A. Multi-agent development

Different external AI systems help build and verify Gnozis.

### B. Multi-agent Gnozis

Gnozis itself eventually coordinates multiple bounded agents on behalf of users or projects.

The second is future runtime architecture and must not be inferred from the first.

A future agent should have:

```text
agent_id
owner/user scope
capabilities
assigned tasks
resource boundaries
proof/evidence requirements
rollback boundary
audit trail
```

## 11. Cross-terminal continuity invariant

For equivalent permissions and the same canonical repository/project state:

```text
Product A asks for project state
Product B asks for project state
Product C asks for project state
```

must produce materially consistent factual state.

Presentation may differ.

Hidden conversation history must not change the canonical project facts.

## 12. Safety and authority invariant

The architecture must preserve:

```text
connection ≠ identity
identity ≠ capability
capability ≠ authority
context ≠ authorization
task ≠ unrestricted permission
AI recommendation ≠ acceptance
```

Human project ownership remains the governing authority for architectural decisions unless the user explicitly delegates a bounded workflow.

## 13. Runtime implementation boundary

This document does not implement:

- identity/authentication;
- authorization;
- encrypted transport/storage;
- Internet Bridge;
- provider adapters;
- notification routing;
- multi-agent runtime;
- organizational CRM integration.

Those require separate bounded implementation tasks and independent verification.

## 14. Immediate architectural objective

Before implementing the full runtime, the repository must remain understandable to a replacement AI product with only permitted project access.

The minimum durable chain is:

```text
User
 → Context Snapshot
 → Task Envelope
 → Capability Check
 → bounded operation
 → evidence
 → persisted result
 → routable continuation
```

This is the architectural bridge between today's multi-terminal development workflow and the intended user-facing Gnozis system.
