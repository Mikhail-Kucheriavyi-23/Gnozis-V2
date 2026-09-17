# Gnozis-V2 — Capability & Connector Contract

Status: architecture contract / implementation not yet accepted.

## Purpose

Connected products are interfaces to Gnozis, not owners of Gnozis authority.

Examples include:

- AI terminals;
- mobile applications;
- work chat and bots;
- CRM systems;
- Google Drive and other storage connectors;
- research and engineering tools.

A connector can expose context, receive results, or request an operation. It does not automatically receive unrestricted access to project state.

## Capability model

A capability is an explicit permission to perform a defined class of operation against a defined scope.

Conceptually:

```text
Capability = (actor, action, resource, scope, constraints, expiry)
```

Examples:

```text
read_task
read_snapshot
read_evidence
propose_change
run_test
write_workspace
submit_for_review
```

A capability is not equivalent to authentication, ownership, or architectural authority.

## Connector boundary

```text
Connected Product
       ↓
Connector
       ↓
Capability check
       ↓
Task / Snapshot / Evidence / Workspace
       ↓
Core boundary
```

The connector must not bypass the capability boundary by writing directly to Core state.

## Read routing

A product requesting context should identify:

```text
task_id
requested_context
requested_scope
actor
```

The system returns only data authorized for that actor and scope.

The connector may transform presentation, but must not silently alter canonical state.

## Write routing

Writes should be expressed as explicit operations:

```text
actor
capability
operation
resource
payload
idempotency key
```

The operation is then validated against scope and applicable invariants before execution.

## Data routing

Users may configure which information is routed to which connected product.

The architecture must support policies such as:

```text
CRM bot → create task
Manager terminal → receive status summary
Research terminal → receive analytical dataset
Mobile app → receive notification and continuation context
Engineering agent → receive repository evidence
```

Routing policy must be explicit and revocable.

## Data classes

Future implementation should distinguish at minimum:

```text
public_project
project_internal
user_private
sensitive
secret
credential
```

A connector must not receive a data class merely because it has access to another class.

Secrets and credentials should normally be referenced or mediated rather than copied into ordinary context snapshots.

## Least privilege

Default connector access should be narrow:

```text
no capability
    ↓
explicit capability
    ↓
minimum required scope
    ↓
bounded operation
    ↓
audit event
```

Capabilities should support expiration and revocation.

## Task continuation

A connector may request:

```text
resume(task_id)
```

This reconstructs context but does not grant execution rights beyond the actor's currently resolved capabilities.

## Evidence

Connector-produced observations must retain provenance:

```text
connector
actor
source
timestamp
operation
result
baseline / task reference
```

A connector result is evidence about an observation; it is not automatically a canonical project decision.

## Failure isolation

A connector failure must not corrupt canonical task state.

Examples:

- unavailable Drive → task remains intact;
- expired AI session → task remains resumable;
- malformed connector response → rejected at boundary;
- duplicated delivery → idempotency prevents duplicate material effects;
- revoked capability → operation denied.

## Core boundary

Connectors must not redefine Ψ-Core semantics.

The intended direction is:

```text
Connector
   ↓
Task / Workspace operation
   ↓
Candidate
   ↓
Core Test / Verify / Commit
   ↓
new canonical state
```

A connector cannot directly declare a Core state accepted.

## Multi-agent operation

Multiple agents may work on the same task, but each operation remains attributable to an actor and capability.

```text
Task
 ├─ Agent A observation
 ├─ Agent B implementation
 ├─ Agent C audit
 └─ Human decision
```

The system preserves provenance rather than relying on majority agreement.

## Human control

The user/project owner can define, restrict, revoke, or re-route connector capabilities.

Connected products are execution interfaces, not autonomous sources of architectural authority.

## Implementation boundary

This contract does not itself implement authentication, authorization, encryption, connector APIs, or Core changes. Those are separate implementation phases requiring explicit scope and independent verification.
