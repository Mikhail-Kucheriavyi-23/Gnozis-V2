# Gnozis-V2 — AI Context

## Canonical repository
- Canonical development repository: `Mikhail-Kucheriavyi-23/Gnozis-V2`
- Legacy `Gnozis` remains an archival research source and historical provenance.
- `AI_CONTEXT.md` is the operational handoff document for participating AI systems.

## Current verified baseline
- Ψ-Core is the source of truth for state/evolution semantics.
- `docs/DATABASE_SCHEMA.md` defines the intended persistence shape but is not itself implementation.
- `gnosis/storage/` is not yet implemented.
- `logs/` currently contains only a placeholder; it is not a functioning persistent audit system.
- `Engine.history` is in-process history and is lost on process exit.
- The latest synchronization commit passed GitHub Actions CI successfully.
- Current implementation status must always be verified from source, tests and CI rather than inferred from documentation.

## Status vocabulary
Use only these implementation states:
- `IMPLEMENTED` — verified in source and tests where applicable.
- `PARTIAL` — some implementation exists but required behavior is incomplete.
- `MISSING` — specified but not implemented.
- `THEORETICAL` — design/research only; no implementation claim.

Documentation, schemas, enums, placeholders, interfaces, or planned directories must never be presented as implemented functionality.

## Trust boundary
Do not weaken the separation between:
- Ψ-Core and external interfaces;
- analysis and decision layers;
- immutable/core semantics and mutable workspace;
- identity/capability/policy and privileged operations.

No AI model belongs inside Ψ-Core. No external selector/operator/global clock may silently become part of Core semantics.

## Current development direction
The immediate engineering sequence begins with:
1. Persistence;
2. Append-only audit log with hash chaining;
3. Instance/lifecycle persistence;
4. Memory;
5. Identity/capability/trust boundary;
6. User/world bridge;
7. Multi-agent network;
8. Evolution/autopoiesis and system integration.

This sequence is a working roadmap, not an immutable architecture. Each phase must be validated before the next phase expands its scope.

## Multi-AI project governance — FIXED WORKING MODEL

The project is developed collaboratively by multiple AI systems. The following governance model is now the default operating model.

### ChatGPT — architecture, integration and final gate
ChatGPT is responsible for:
- maintaining the architectural direction and Ψ/Core invariants;
- decomposing work into bounded phases/tasks;
- defining acceptance criteria and forbidden changes;
- reconciling Claude/Manus/auditor findings;
- reviewing completed implementations against source, tests and project theory;
- deciding whether a phase is accepted, rejected, or returned for correction;
- maintaining the canonical project context and preventing architectural drift.

ChatGPT should not duplicate large implementation tasks unnecessarily when another assigned AI is already implementing them.

### Claude — primary implementation engineer
Claude is the default primary implementer for large, well-bounded engineering tasks unless a phase is explicitly assigned elsewhere.

Claude should:
- implement the requested phase;
- add/maintain tests;
- update relevant technical documentation;
- report exactly what is IMPLEMENTED/PARTIAL/MISSING/THEORETICAL;
- avoid unrelated refactors and architecture changes;
- provide a concise handoff for independent review.

### Manus — independent engineer and adversarial reviewer
Manus is used for:
- independent implementation of phases explicitly assigned to Manus;
- independent review of Claude implementations;
- architectural consistency checks;
- security/trust-boundary review;
- finding hidden coupling, incomplete implementations, and unsupported claims;
- proposing corrective changes after review.

Manus should not silently replace or fork the architecture. Changes must remain within the assigned task and current project invariants.

### Gemini and other AI systems without repository access — external audit
Systems without repository access are treated as external/read-only auditors.

They may receive:
- repository snapshots;
- relevant source files;
- `AI_CONTEXT.md`;
- `STATUS.md`;
- schemas and audit reports.

They should focus on independent criticism, counterexamples, security issues, mathematical consistency, architectural contradictions, and claims that are not supported by implementation. They do not directly modify the canonical repository.

## Handoff protocol
For every substantial phase:

`Task definition → primary implementation → independent review → ChatGPT integration/final gate → context/status update → next phase`

A phase handoff must contain:
- files changed;
- behavior implemented;
- tests added/changed;
- test/CI result;
- known limitations;
- security/trust-boundary implications;
- remaining `PARTIAL/MISSING/THEORETICAL` items;
- recommended next step.

Parallel edits to the same architectural area should be avoided unless explicitly coordinated.

## Conflict resolution between AI systems
When AI conclusions differ, use this precedence:

1. actual source code;
2. reproducible tests and CI;
3. explicit project invariants/specification;
4. verified audit evidence;
5. design proposals and AI opinions.

No AI assertion overrides executable evidence merely because it appears in a report.

If two implementations are plausible, do not merge both by default. Stop, compare their architectural consequences, and resolve the conflict before proceeding.

## Phase ownership is provisional per phase
The global governance model is fixed, but the implementation owner may change from phase to phase.

Before each major phase, explicitly record:
- primary implementer;
- reviewer;
- ChatGPT acceptance role;
- external audit requirement, if any.

The same AI should not automatically implement and independently certify its own work.

## Mandatory quality gates
No phase is considered complete solely because code exists.

A phase must be evaluated for:
- functional correctness;
- tests;
- CI where applicable;
- persistence/recovery behavior where applicable;
- security and trust-boundary preservation;
- compatibility with Ψ-Core;
- absence of undocumented architectural coupling;
- accurate status classification.

## Open evolution question
As Gnozis approaches autonomous/self-directed evolution, this governance model must be revisited. In particular, future work must determine how human authority, AI-agent authority, proof/invariant checks, rollback, capability limits, and auditability interact when the system can propose or perform its own modifications.

No claim of autonomous self-development should be made until the corresponding mechanisms are implemented and independently verified.

## Immediate next task
The next engineering phase is **Persistence + Append-Only Audit Log**.

Required direction:
- SQLite local persistence;
- repository/storage boundary outside Ψ-Core;
- state save/load and restart recovery;
- append-only audit events;
- SHA-256 hash chaining and integrity verification;
- transaction/crash behavior tests;
- no raw private keys/passwords/secrets in the database;
- tests proving that audit history cannot be silently rewritten through the normal API.

The implementation must follow `docs/DATABASE_SCHEMA.md` rather than inventing a divergent schema.

## Context recovery procedure
A new AI session must read, in order:
1. `AI_CONTEXT.md`;
2. `STATUS.md`;
3. `docs/DATABASE_SCHEMA.md`;
4. relevant source files;
5. relevant tests;
6. latest CI status.

Then report the current state using `IMPLEMENTED / PARTIAL / MISSING / THEORETICAL` before proposing changes.

Never assume that an earlier AI's report is proof of implementation.
