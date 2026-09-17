# Gnozis-V2 — Output Routing Contract

## Status

`ARCHITECTURE CONTRACT — IMPLEMENTATION NOT YET ACCEPTED`

Gnozis may eventually deliver verified task results through multiple connected products: AI terminals, work chats, mobile applications, CRM systems, or other user-selected destinations. Delivery must remain an explicit policy decision rather than an accidental property of connector availability.

## 1. Logical model

```text
OutputPolicy {
    destination_id
    recipient_scope
    allowed_data_classes[]
    allowed_result_states[]
    purpose
    task_scope
    constraints[]
}
```

The exact storage schema is implementation-defined.

## 2. Delivery gates

```text
result produced
  ↓
result verification state
  ↓
recipient scope
  ↓
data-class policy
  ↓
destination authorization
  ↓
delivery
  ↓
delivery evidence
```

A connected channel is not automatically an output destination.

## 3. Verification boundary

A result reported by one AI is not automatically a verified result.

At minimum, the routing layer must distinguish:

```text
reported
implemented
runtime_verified
independently_verified
accepted
rejected
```

A policy may restrict delivery to a minimum verification state.

## 4. User-controlled routing

The intended user experience includes user-configurable routing such as:

```text
Task class A → mobile notification
Task class B → work chat
Task class C → personal AI terminal
Task class D → CRM record
```

The routing layer must preserve the distinction between:

```text
user preference
organization policy
task policy
security authorization
```

A mobile setting must not override a stronger organization or task restriction.

## 5. Data minimization

A destination receives only the data class and content permitted for that destination.

The system should prefer a concise evidence-aware result over unrestricted context replication.

## 6. Multi-terminal continuity

A notification is an entry point, not the canonical task state.

Example:

```text
work chat
  ↓
"Task #123 requires verification"
  ↓
any connected AI terminal
  ↓
canonical TaskContext
  ↓
evidence-aware current state
  ↓
permitted next action
```

The terminal that delivered the notification does not own the task context.

## 7. Organization and personal use

The same routing architecture must eventually support:

```text
individual user
team
company / CRM
```

without merging their scopes.

## 8. Auditability

A future delivery record should identify:

```text
task/context
result revision
recipient scope
destination
policy used
verification state
time
success/failure
```

## 9. Non-goals

This contract does not implement:

- messaging adapters;
- CRM adapters;
- mobile applications;
- authentication;
- authorization;
- encryption;
- autonomous agent execution.

## 10. Acceptance principle

Output routing is accepted only when an independent audit proves that no connected destination can become an implicit data-exfiltration path and that stale or unverified task results cannot be silently delivered as authoritative results.
