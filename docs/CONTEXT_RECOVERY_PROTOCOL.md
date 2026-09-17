# Gnozis-V2 — Context Recovery Protocol

## Purpose

This protocol defines how a newly connected AI recovers the current Gnozis work state without relying on a previous chat session.

The protocol is deliberately evidence-first. A connected AI reconstructs context; it does not invent missing state and does not gain architectural authority merely by recovering context.

## Recovery sequence

```text
CONNECT
  ↓
IDENTIFY repository / branch / HEAD
  ↓
READ canonical handoff documents
  ↓
READ active contracts and status
  ↓
CHECK source / tests / CI evidence relevant to the task
  ↓
BUILD ContextSnapshot
  ↓
DETECT mismatches / stale claims
  ↓
REPORT implementation + verification + acceptance separately
  ↓
REPORT role + authority + scope
  ↓
REPORT next permitted action
  ↓
WAIT FOR EXPLICIT TASK
```

## Required reading order

Unless a narrower task explicitly defines another order:

1. `AI_CONTEXT.md`
2. `STATUS.md`
3. `docs/AI_HANDOFF_PROTOCOL.md`
4. `docs/MULTI_AGENT_BUILD_STRATEGY.md`
5. `AGENT_ROLES.md`
6. `docs/CONTEXT_CONTINUITY_CONTRACT.md`
7. `docs/CONTEXT_SNAPSHOT_SCHEMA.md`
8. relevant contracts/specification
9. relevant source
10. relevant tests and CI evidence

## Recovery report

Before changing anything, the connected AI must report:

```text
Repository:
Branch:
HEAD:
Latest tested commit:

Active phase:
Active task:
Role:

Implementation state:
Verification state:
Acceptance state:

Allowed scope:
Forbidden scope:

Open findings:
Evidence references:

Next permitted action:
```

If the AI cannot establish a field from durable evidence, it must mark it `UNKNOWN` or `UNVERIFIED` and identify what evidence is missing.

## Mismatch handling

A mismatch exists when durable sources disagree, for example:

```text
STATUS says X
source shows Y
```

or:

```text
reported tested commit != current HEAD
```

The AI must not silently choose the convenient value. It should:

1. identify the mismatch;
2. rank evidence using the project evidence hierarchy;
3. state the resulting verified interpretation;
4. preserve the unresolved discrepancy as a finding when appropriate;
5. avoid modifying documentation unless that modification is explicitly authorized.

## Authority rule

Context recovery is read/recovery behavior.

```text
context recovered ≠ task assigned
context recovered ≠ write permission
write permission ≠ architectural authority
```

A connected AI may have technical GitHub or Google Drive write capability while still having no permission to modify the current phase. The phase assignment determines allowed scope.

## Continuation after interruption

If an AI stops midway, the next AI must continue from durable artifacts and evidence, not from an assumed reconstruction of the previous conversation.

The continuation agent must locate:

```text
last durable change
current HEAD
active task
accepted decisions
open findings
unfinished bounded work
next permitted action
```

An unfinished task must not be declared complete merely because some files exist.

## Cross-product equivalence test

For the same authorized user/project/task scope, two connected AI products should reconstruct semantically equivalent values for:

```text
HEAD
active phase/task
implementation state
verification state
acceptance state
authority
open findings
next permitted action
```

Presentation may differ. Project meaning must not.

## Practical fresh-session test

A fresh AI session passes the recovery test if, without previous Gnozis conversation history, it can:

1. identify the canonical repository;
2. identify current branch and HEAD;
3. distinguish Persistence from Memory status;
4. identify the active multi-agent governance model;
5. identify open findings and acceptance gates;
6. identify its assigned role/scope or report that none is assigned;
7. identify the next permitted action without inventing authorization;
8. cite the durable evidence used for these conclusions.

## Failure conditions

Recovery fails if the AI:

- relies on previous chat history as the authoritative source;
- treats an AI report as stronger than current source or reproducible evidence;
- confuses implementation with acceptance;
- confuses access with authority;
- silently widens task scope;
- reports stale documentation as current without checking source evidence;
- invents a task or permission not present in durable artifacts.

## Future implementation boundary

A future runtime implementation may expose machine-readable operations such as:

```text
RecoverContext()
ResolveEvidence()
GetAuthority()
GetActiveTask()
DetectContextDrift()
```

These are architectural targets only. No runtime API, database schema, Identity layer, encryption, Bridge, Memory acceptance, or Core modification is implied by this document.
