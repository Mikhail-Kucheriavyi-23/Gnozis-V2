# Gnozis-V2 — Connected Data Source Contract

## Status

`ARCHITECTURE CONTRACT — IMPLEMENTATION NOT YET ACCEPTED`

A connected data source is an input channel through which Gnozis may obtain information. Connection alone never means that all data in the source is available to a task.

## 1. Logical model

```text
DataSource {
    source_id
    provider
    connector_type
    location/reference
    owner_scope
    organization_scope?
    allowed_data_classes[]
    allowed_operations[]
    provenance
    observed_at
    status
}
```

The exact persistence schema is implementation-defined.

## 2. Selection gates

Every source must pass the following sequence:

```text
connected
  ↓
identified
  ↓
scope-resolved
  ↓
allowed for project
  ↓
allowed for task
  ↓
allowed data class
  ↓
selected for operation
  ↓
read/executed
```

A connector must never jump directly from `connected` to `read`.

## 3. Examples

A user's Google Drive may contain:

- project documents;
- personal documents;
- credentials or secrets;
- unrelated company information.

The existence of a Drive connector does not authorize a task to consume all of them.

Likewise, GitHub access does not mean every repository, branch, issue, or secret is task-eligible.

## 4. Evidence references

TaskContext should normally retain references to selected evidence rather than copying entire external datasets into canonical task state.

An evidence reference should eventually preserve:

```text
source_id
locator
content/data class
producer
observed_at
provenance
verification status
integrity reference when available
```

## 5. Data minimization

A task should request the smallest data scope sufficient to answer or execute the task.

A connector must not become an unrestricted project-wide memory store.

## 6. Cross-user and organization boundaries

The same physical connector may expose multiple logical scopes. These must remain distinguishable:

```text
personal user data
organization data
project data
task data
```

No implicit merge is permitted.

## 7. Output boundary

Data read from a source may only be used for destinations allowed by the task's output policy.

Input permission does not imply output permission.

## 8. Security boundary

This contract does not implement authentication, authorization, encryption, or connector credentials. Those are separate bounded phases.

## 9. Acceptance principle

A source integration is accepted only when an independent audit can demonstrate that connector presence cannot silently widen the data available to an unrelated task.
