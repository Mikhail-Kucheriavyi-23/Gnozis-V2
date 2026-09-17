# Gnozis-V2 — Evidence Reference Contract

Status: architecture contract; implementation not yet accepted.

## Purpose

Gnozis must distinguish canonical, reproducible evidence from AI reports, interface state, and reconstructed context.

Evidence is the bridge that allows a user to move between terminals and still receive the real current state of a task.

## Evidence identity

Every durable evidence item should have a stable reference:

```text
evidence_id
```

The reference must survive connector replacement and must not depend on a chat message ID.

## Evidence record

A future implementation should represent at least:

```text
evidence_id
type
producer
created_at
source_ref
content_digest
scope
status
related_task_id
related_checkpoint_id
```

The exact persistence schema is deferred to an explicit implementation task.

## Evidence types

Examples include:

```text
source_commit
diff
test_result
runtime_observation
artifact
artifact_hash
independent_audit
human_decision
external_document
core_transition
```

The system may add types later, but a type must describe what the evidence actually is rather than how trustworthy an agent claims it is.

## Trust distinction

The following are different things:

```text
Evidence exists
Evidence is reproducible
Evidence is independently verified
Evidence is accepted for a project decision
```

An AI report can point to evidence, but the report itself does not automatically become equivalent to the evidence.

## Provenance

Evidence must preserve provenance sufficient to answer:

```text
Who/what produced it?
From which baseline?
When?
Through which connector or runtime?
With which command or operation?
What exact artifact/content does the reference identify?
```

For exchanged archives, the minimum provenance should include:

```text
filename
SHA-256
baseline commit
producer
scope
test command
verification status
```

## Content digest

When the evidence is a file or artifact, a cryptographic digest should identify the exact bytes that were reviewed.

A digest proves identity of the referenced bytes; it does not by itself prove that the contents are correct.

## Evidence status

Evidence status must remain separate from task status.

Possible states include:

```text
observed
reproducible
independently_verified
superseded
rejected
```

`independently_verified` must only be assigned when the verification actually occurred.

## Task integration

A Task checkpoint references evidence by stable `evidence_id` values:

```text
Task
  ↓
Checkpoint
  ↓
Evidence references
  ↓
Source / runtime / artifact
```

The checkpoint should not duplicate large evidence payloads unnecessarily.

## Cross-terminal continuation

When a user asks another connected AI terminal for the current state, the terminal should resolve:

```text
current task
→ latest checkpoint
→ evidence references
→ evidence status
→ current capabilities
```

This prevents the terminal from treating an old conversation or stale local file as the current truth.

## Conflicting evidence

Conflicting evidence must not be silently collapsed.

Example:

```text
Claude: 103/103 offline tests
Manus: 159 pytest tests
```

These are distinct evidence items with distinct execution environments and semantics. A higher-level integration decision may compare them, but one must not be silently rewritten as the other.

## Human decisions

A human decision is evidence of a decision, not proof of the technical fact that motivated it.

For example:

```text
human accepted phase X
```

records acceptance; it does not transform an unverified test result into a verified one.

## Connector boundary

Connectors may create or retrieve evidence references, but they must not rewrite the canonical meaning of existing evidence.

```text
GitHub connector
Drive connector
AI terminal connector
Chat connector
Mobile connector
        ↓
 evidence references
```

## Core boundary

An accepted Core transition may be referenced as evidence for a task.

Evidence must not directly mutate Core state.

```text
Evidence → reference
Evidence ↛ Ψ-Core mutation
```

## Required invariants for implementation

1. Every durable evidence item has a stable ID.
2. Evidence references identify their source/provenance.
3. Artifact evidence can be integrity-checked by digest.
4. Evidence status cannot be upgraded merely by copying an agent claim.
5. Conflicting evidence remains separately addressable.
6. Connector replacement does not invalidate canonical evidence identity.
7. Task checkpoints reference evidence rather than embedding unverified claims as facts.
8. Evidence cannot directly mutate Ψ-Core.
9. Verification status records what was actually verified, not what was requested.
10. Historical evidence remains inspectable after later evidence supersedes it.

## Implementation boundary

This document does not authorize implementation of authentication, authorization, encryption, federation, autonomous self-modification, or changes to Ψ-Core semantics.

Any implementation derived from this contract requires an explicit bounded task and independent verification.
