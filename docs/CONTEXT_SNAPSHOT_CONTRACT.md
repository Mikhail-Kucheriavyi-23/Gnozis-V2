# Gnozis-V2 — Context Snapshot Contract

Status: architecture contract / implementation not yet accepted.

## Purpose

A Context Snapshot is the portable, durable representation of the information required to resume a Gnozis task from another connected product.

It is deliberately separate from chat history. A chat may contain useful observations, but the snapshot is the canonical continuation surface once accepted into project state.

## Required fields

```text
snapshot_id
project_id
task_id
user_id
created_at
updated_at
baseline_ref
implementation_state
verification_state
acceptance_state
objective
constraints
current_findings
pending_actions
blocked_actions
capabilities_required
capabilities_available
evidence_refs
source_refs
context_version
```

## State separation

The following states must never be collapsed into one `status` value:

### Implementation state

What has actually been implemented in the repository/runtime.

Examples:

```text
not_started
in_progress
implemented
```

### Verification state

What has been independently reproduced or checked.

Examples:

```text
unverified
partial
verified
failed
```

### Acceptance state

Whether the current state has passed the project integration gate.

Examples:

```text
not_submitted
pending
accepted
rejected
```

A component can therefore be:

```text
implementation = implemented
verification   = verified
acceptance     = pending
```

This distinction is mandatory because implementation reports must not become acceptance evidence automatically.

## Baseline binding

A snapshot that describes repository work must identify the source baseline:

```text
repository
branch/ref
commit SHA
```

If the snapshot references a changed artifact rather than a commit, it must contain artifact provenance sufficient to identify the exact object.

## Evidence binding

Evidence references must be immutable references to observable material, such as:

- commit;
- test result;
- audit report;
- artifact hash;
- runtime observation;
- accepted contract.

Free-form claims such as `PASS` or `implemented` are not evidence by themselves.

## Continuation rule

A new terminal resolving a task should be able to reconstruct the current state using the snapshot plus its referenced evidence without requiring the original conversation transcript.

## Conflict rule

If a connected product supplies context that conflicts with the canonical snapshot:

```text
canonical persisted state
        ↓
independent evidence
        ↓
connected-product context
```

The product context may propose an update, but it must not silently overwrite canonical state.

## Capability rule

A snapshot describes capabilities; it does not grant them.

```text
capability_required ≠ capability_granted
```

Actual execution must resolve authorization/capability state separately.

## Confidentiality

The snapshot must support future data-classification and routing controls. Sensitive payloads should preferably be referenced rather than duplicated across connectors. Connector-specific redaction must never mutate canonical source evidence.

## Versioning

`context_version` versions the snapshot contract, not the Core state model and not the repository schema version.

Changing the snapshot contract requires:

1. explicit architecture task;
2. compatibility decision;
3. tests for old/new representations where applicable;
4. independent review.

## Minimal portable handoff

A connector that cannot retrieve the entire snapshot should still be able to request a compact continuation view containing:

```text
project
 task
 objective
 current implementation state
 current verification state
 acceptance state
 baseline
 blockers
 next permitted actions
```

This is the first practical interface for cross-terminal continuity.
