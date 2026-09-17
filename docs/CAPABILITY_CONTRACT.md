# Gnozis-V2 — Capability Contract

## Status

`ARCHITECTURE CONTRACT — IMPLEMENTATION NOT YET ACCEPTED`

A capability describes what a connected product, agent, or subsystem can technically do. It is not authority and never becomes permission merely because it is connected.

## 1. Capability model

A capability is logically:

```text
Capability {
    capability_id
    provider
    operation
    target_class
    constraints[]
    availability
    scope
    provenance
    observed_at
}
```

The exact storage schema is implementation-defined.

## 2. Mandatory distinction

```text
capability exists
    ≠ capability enabled
    ≠ capability authorized
    ≠ action authorized
    ≠ action executed
    ≠ result verified
```

Examples:

- GitHub access may provide a repository-read capability but does not authorize architectural changes.
- Google Drive access may provide a document-read capability but does not authorize disclosure of every document.
- An AI terminal may be able to call a tool without being authorized to perform every operation exposed by that tool.

## 3. Capability use

Before execution, a future action layer must resolve:

```text
requested action
    ↓
required capability
    ↓
scope
    ↓
explicit authorization
    ↓
data policy
    ↓
execution
    ↓
verification
```

A missing capability must block the action. A present capability must not bypass authorization.

## 4. User-centered continuity

Capabilities belong to the connected environment, not to a conversation. A new terminal may discover the capabilities available to it and compare them with the canonical TaskContext.

The TaskContext may declare:

```text
available_capabilities[]
```

but that declaration is descriptive only.

## 5. Scope

Capabilities must be evaluated against:

```text
user_scope
organization_scope
project_scope
task_scope
data_class
operation
```

No capability may silently widen any of these scopes.

## 6. Auditability

Executed capability use must eventually be attributable to:

```text
capability_id
actor/context
requested operation
target
scope
result
verification state
time
```

This contract does not implement identity or authorization.

## 7. Core boundary

Capabilities must not directly mutate Ψ-Core semantics. Core-changing actions remain subject to the established Candidate → Test → Verify → Commit boundary.

## 8. Non-goals

This contract does not implement:

- authentication;
- authorization;
- credentials;
- connector adapters;
- autonomous agents;
- routing;
- encryption;
- Core evolution.

## 9. Acceptance principle

A capability layer is not accepted because an external tool can technically execute an operation. Acceptance requires proof that capability discovery cannot silently become authority and that execution remains within explicit task and data scope.
