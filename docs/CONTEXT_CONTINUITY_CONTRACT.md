# Gnozis-V2 — Context Continuity Contract

## Purpose

This contract defines the product-independent interface for restoring project context when a user connects to Gnozis-V2 from a different AI product, terminal, connector, or session.

The contract is intentionally independent of Google Drive, GitHub, Claude, Manus, ChatGPT, Gemini, or any other provider.

The objective is not to reproduce a conversation. The objective is to reconstruct the **current project state and the next permitted action** from durable evidence.

## 1. Core principle

```text
Conversation = transient interface state
Repository / accepted artifacts = durable engineering state
Context snapshot = portable projection of durable state
Task envelope = bounded request against that state
```

A connected product may consume the context snapshot through any permitted connector. It must not manufacture missing state from conversational memory.

## 2. Portable Context Snapshot

Every continuation-capable product should be able to obtain a snapshot containing at least:

```text
snapshot_schema
snapshot_id
created_at
repository
canonical_branch
canonical_head
latest_tested_commit
implementation_state
verification_state
acceptance_state
active_phase
active_task
primary_implementer
independent_reviewer
integration_gate
allowed_scope
forbidden_scope
open_findings
next_permitted_action
source_references
evidence_references
staleness_rule
```

`canonical_head` is the authoritative source revision. A consumer must compare it with the live repository before acting.

## 3. Task Envelope

A product requesting work must be able to express a bounded task as:

```text
task_id
issued_at
requester
objective
baseline_commit
allowed_scope
forbidden_scope
acceptance_criteria
evidence_required
requested_outputs
review_required
```

The task envelope does not grant architectural authority. It only defines the work explicitly delegated by the project owner/workflow.

## 4. Continuation algorithm

A newly connected product follows:

```text
1. Read canonical context sources.
2. Read live repository HEAD.
3. Compare snapshot canonical_head with live HEAD.
4. If different, refresh the snapshot before acting.
5. Determine implementation / verification / acceptance separately.
6. Determine active phase and task.
7. Check allowed and forbidden scope.
8. Read only relevant source, tests and contracts.
9. Produce a baseline report.
10. Execute only the bounded task that is authorized.
11. Record reproducible evidence.
12. Leave durable state sufficient for the next product to continue.
```

If any required field is unavailable, the product must mark it `UNKNOWN` or `UNVERIFIED`.

## 5. Resource model

Connected products may expose different resources:

```text
GitHub      → source, tests, commits, CI, issues
Google Drive → external artifacts, reports, user-provided documents
AI product  → interaction and task interface
Terminal    → local execution environment
Future plug-in → another permitted project resource
```

Resources are interchangeable **interfaces**, not automatically interchangeable authorities.

The repository remains the canonical source for merged source state. External artifacts become engineering evidence only when their provenance is recorded and their contents are reproducible.

## 6. Real-current-state response

When a user asks another connected product for the real state of a task, the response should be reconstructed from evidence in this order:

```text
live repository state
→ reproducible tests / CI
→ accepted contracts
→ independent audit evidence
→ external artifact provenance
→ conversation context (only as non-canonical context)
```

The response should explicitly distinguish:

```text
IMPLEMENTED
VERIFIED
ACCEPTED
UNVERIFIED
NOT_ACCEPTED
UNKNOWN
```

No provider-specific conversation memory is required for correctness.

## 7. Handoff completion requirement

A task is not considered continuation-safe merely because code was changed.

Before handing work to another product, the durable state should identify:

```text
what changed
what was tested
what was independently verified
what remains unverified
what is accepted
what remains open
what the next permitted action is
```

## 8. Cross-product invariant

The same repository state must produce materially consistent answers from different connected products when they have equivalent read access.

Differences caused by provider-specific presentation are acceptable. Differences in factual project state caused only by hidden conversation history are not.

## 9. Security boundary

This contract does not implement identity, authorization, encryption, or the Internet Bridge.

Those are separate architectural layers.

Therefore:

```text
context visibility ≠ authorization
resource access ≠ architectural authority
project state ≠ user identity
```

Those boundaries must remain explicit when implementation begins.

## 10. Current implementation status

The current repository contains the documentation and machine-readable state layer for this contract.

The following remain future/runtime work:

- provider-neutral context API;
- authenticated caller identity;
- encrypted context transport/storage where required;
- automated cross-product consistency test;
- user-facing notification/task routing;
- capability-scoped resource access.

These are not implied to be implemented by this document.
