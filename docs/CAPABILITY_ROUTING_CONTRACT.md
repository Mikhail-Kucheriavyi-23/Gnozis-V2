# Gnozis-V2 — Capability and Result Routing Contract

Status: architecture specification / no runtime implementation yet.

## 1. Principle

A connected product is a surface through which a user or authorized agent interacts with Gnozis. Connection alone grants no architectural authority.

```text
connection
  ≠ identity
  ≠ capability
  ≠ authority
```

## 2. Capability classes

Initial conceptual capabilities:

```text
READ_PROJECT
READ_CONTEXT
READ_TASK
READ_EXTERNAL_ARTIFACT
RUN_TESTS
SUBMIT_REQUEST
SUBMIT_ANALYSIS
WRITE_DOCUMENTATION
WRITE_CODE
CREATE_TASK
UPDATE_TASK
READ_RESULT
RECEIVE_RESULT
```

These names are architectural vocabulary only until a bounded implementation task defines their storage and enforcement semantics.

## 3. Scope

Every future capability grant should identify, where applicable:

```text
subject
project
resource
operation
scope
expiry/revocation state
issuer
```

A broad connector permission must not silently become unrestricted access to all projects or all user data.

## 4. Result routing

A result may be delivered to one or more explicitly authorized channels:

```text
mobile application
AI terminal
coding terminal
work chat
email/document system
another authorized product
```

Routing must be policy-driven.

```text
result exists
    ↓
routing policy
    ↓
capability check
    ↓
authorized channel
```

Connector availability alone is insufficient.

## 5. Data minimization

A result channel should receive the minimum result representation necessary for the requested purpose.

Possible representations:

```text
status-only
summary
verified findings
full task result
artifact reference
artifact content
```

The channel must not receive unrelated project context merely because it is connected.

## 6. Verification distinction

A routed result must preserve its verification state.

Conceptual fields:

```text
result_id
task_id
status
verification_state
evidence_refs
created_at
```

For example:

```text
IMPLEMENTED
UNVERIFIED
```

must remain distinguishable from:

```text
IMPLEMENTED
INDEPENDENTLY_VERIFIED
```

## 7. Cross-product continuity

The receiving product must be able to request current task state rather than trusting a copied message as canonical state.

Preferred flow:

```text
notification
  ↓
task_id
  ↓
resolve canonical task/context
  ↓
resolve evidence
  ↓
return current state
```

This prevents stale notifications from becoming authoritative project state.

## 8. Organization / CRM routing

An organization may use Gnozis as an analytical core while individual users retain separate personal tool connections.

Example:

```text
work chat → creates organizational task
                 ↓
              Gnozis
                 ↓
       role-specific analysis
          ↙             ↘
     manager          specialist
       ↓                  ↓
   summary             dataset/result
```

Routing policies must explicitly define what each role may receive.

## 9. Future implementation boundary

This contract does not implement authentication, authorization, encryption, provider adapters, notifications, or CRM integration.

Those are separate security-sensitive implementation phases requiring explicit scope and independent verification.
