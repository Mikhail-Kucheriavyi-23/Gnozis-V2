# Gnozis-V2 — Context Snapshot Schema

## Purpose

This document defines the canonical logical model for a recoverable project-context snapshot. It is intentionally connector-neutral and implementation-neutral.

A ContextSnapshot is an **agent-facing projection of durable project evidence**. It is not a second Ψ-Core State model and it is not itself authority to modify the project.

## Design rule

A snapshot answers five separate questions:

```text
What exists?
What is verified?
What is accepted?
What may this agent do?
What evidence proves each claim?
```

These dimensions must not be collapsed into one status field.

## Canonical object

```text
ContextSnapshot
├── schema_version
├── context_id
├── generated_at
├── user_scope
├── project_scope
├── repository
│   ├── full_name
│   ├── branch
│   ├── head_sha
│   └── source_of_truth
├── active_phase
├── active_task
├── role
├── authority
│   ├── level
│   ├── allowed_scope[]
│   ├── forbidden_scope[]
│   └── final_gate
├── implementation_state
├── verification_state
├── acceptance_state
├── current_decisions[]
├── open_findings[]
├── evidence_refs[]
├── latest_tested_commit
├── recovery_point
└── next_permitted_action
```

## State vocabulary

### implementation_state

Use only:

```text
IMPLEMENTED
PARTIAL
MISSING
THEORETICAL
```

### verification_state

Use only evidence-qualified values such as:

```text
VERIFIED_BY_TESTS
VERIFIED_BY_CI
VERIFIED_BY_INDEPENDENT_AUDIT
UNVERIFIED
BLOCKED
```

Multiple evidence values may coexist when represented as a set.

### acceptance_state

Use only:

```text
ACCEPTED
NOT_ACCEPTED
PENDING_GATE
BLOCKED
```

Acceptance must never be inferred from implementation or test results alone.

## Evidence reference

Every claim presented as verified should be traceable to an evidence reference with at least:

```text
reference_id
reference_type
location
commit_sha (when applicable)
producer (when applicable)
verified_at (when applicable)
claim
```

Allowed `reference_type` values include:

```text
SOURCE
TEST
CI
AUDIT
CONTRACT
REPORT
```

`REPORT` is informational and cannot outrank source, reproducible execution, contracts, or independent audit evidence.

## Open finding

```text
finding_id
severity
summary
source_ref
status
blocking_for_acceptance
```

A finding remains open until durable evidence records its resolution and the required reviewer/gate accepts that resolution.

## Authority

Authority describes what the connected agent is permitted to do in the current phase. It does not describe what the agent is technically capable of doing.

Example:

```text
level: IMPLEMENTATION
allowed_scope:
  - docs/CONTEXT_*
forbidden_scope:
  - gnosis/core/*
  - gnosis/storage/*
  - gnosis/memory/*
final_gate: ChatGPT
```

## Freshness

`generated_at` describes when the projection was produced. `head_sha` and `latest_tested_commit` establish repository evidence independently of snapshot generation time.

A snapshot must be considered stale when its repository HEAD, active phase, acceptance state, or open findings no longer match durable project evidence.

## Minimal recovery subset

A new AI must be able to reconstruct at least:

```text
repository.full_name
repository.branch
repository.head_sha
active_phase
active_task
role
authority
implementation_state
verification_state
acceptance_state
latest_tested_commit
open_findings
next_permitted_action
```

If any of these are unavailable, the agent must report the missing evidence rather than inventing a value.

## Connector neutrality

GitHub, Google Drive, local files, AI terminals, and future connectors may transport or expose snapshot data. None of them defines the schema semantics.

A connector may provide evidence references; it must not silently rewrite project state or acceptance state.

## No runtime implementation implied

This document does not create a database table, API, identity mechanism, encryption mechanism, Memory implementation, Bridge, or Core change. Those require separate scoped implementation tasks and independent verification.
