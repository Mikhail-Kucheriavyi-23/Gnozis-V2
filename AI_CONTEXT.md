# GNOSIS-V2 — Shared AI Working Context

> Canonical handoff document for AI tools working on this repository.
> This file records project context and collaboration rules; it is not a substitute for the source code, tests, CI, or formal specifications.

## 1. Project identity

- Repository: `Mikhail-Kucheriavyi-23/Gnozis-V2`
- Project: GNOSIS 2.0
- This repository is the canonical development line for V2.
- The older `Mikhail-Kucheriavyi-23/Gnozis` repository is an archived/research line and must not be treated as the automatic source of code for V2.

## 2. Current architectural direction

Core mathematical state:

`Ψ = (X, R)`

The Core must remain the authoritative source of truth for state transitions.

Current conceptual transition pipeline:

`Candidate → Test → Verify → Commit → State′`

The following boundaries are intentional:

- Core must not depend directly on SQLite, GitHub, terminal tools, workers, or external AI services.
- Persistence is a representation of Core state, not a second mutable state machine.
- External interfaces must not receive unrestricted authority to mutate Core.
- `Generate` is currently caller-supplied; endogenous Generate is a future research stage, not an assumption of current implementation.

## 3. Current status — verify before relying on it

Known direction/status at the time this file was created:

### Implemented / substantially implemented

- Immutable `State` / `Relation` model.
- Deep-freeze protection for nested state data.
- Candidate / TestResult / Verify / Commit flow.
- Meaningful-change / no-op protection.
- Deterministic Select.
- Budget constraints.
- Clone/fork/lineage mechanisms.
- Runtime history.
- GitHub Actions CI for the current main revision.

### Not yet established as complete

- Persistent SQLite storage.
- Append-only, hash-chained audit log.
- Recovery of state and lineage after process restart.
- Cryptographic Instance/Agent identity and signatures.
- Persistent Memory layer.
- Agent layer.
- Secure external Bridge.
- Federation.
- Endogenous Generate inside the verified Core.
- Formal theorem-prover integration.

**Rule:** these statuses are a handoff snapshot, not proof. Every AI tool must verify the current repository before changing or reporting implementation status.

## 4. Current next development stage

The immediate planned implementation stage is:

**Persistence + Append-Only Audit Log**

Target architecture:

`Core → Storage Adapter → SQLite`

and:

`Commit → Audit Event → Hash Chain`

Required outcomes:

1. Persist State, Candidate, Transition and Instance/lineage.
2. Use deterministic canonical serialization.
3. Maintain an append-only audit API.
4. Hash-chain audit events with SHA-256.
5. Verify the complete audit chain.
6. Make logical commit persistence transactional.
7. Recover current state and lineage after restart.
8. Preserve all existing Core invariants and tests.

Do not automatically proceed to Agent, Memory, Federation, Bridge, endogenous Generate, or theorem-prover work after completing this stage. Stop and report remaining gaps first.

## 5. AI collaboration protocol

Multiple AI tools may work on this repository. They must behave as independent collaborators, not as competing sources of truth.

### Before work

1. Read this file.
2. Read `STATUS.md` if present.
3. Inspect the relevant source code and tests.
4. Check current `main` and recent commits/CI when the task depends on repository state.
5. Never assume another AI's description is correct without checking the code.

### During work

- Make the smallest change that satisfies the agreed task.
- Preserve existing architectural boundaries.
- Do not silently broaden scope.
- Do not rewrite working Core code merely for style.
- Add or update tests for behavior changes.
- Do not weaken, delete, skip, or falsify tests to obtain green CI.
- Do not claim a feature is implemented because a placeholder, interface, or documentation exists.

### After work

Every AI that changes the repository should report:

- exact files changed;
- exact behavior added/changed;
- tests added/changed;
- tests actually run and their results;
- CI result if available;
- remaining limitations;
- whether the change affects the mathematical Core or only an adapter/infrastructure layer;
- one recommended next task, without starting it automatically.

## 6. Conflict resolution between AI tools

If two AI tools disagree:

1. Source code is stronger evidence than prose.
2. Passing behavioral tests are stronger evidence than comments.
3. Actual CI results are stronger evidence than claimed local results.
4. The mathematical/architectural specification is the reference for intended behavior.
5. If implementation and specification disagree, do not silently choose one; document the discrepancy and request/record the decision.

Never merge two incompatible architectural interpretations merely to remove a conflict.

## 7. Status vocabulary

Use only these implementation labels:

- `IMPLEMENTED` — behavior exists and is supported by code plus appropriate tests/evidence.
- `PARTIAL` — some implementation exists but the acceptance criteria are incomplete.
- `MISSING` — no working implementation exists.
- `THEORETICAL` — described as an idea/specification but not implemented.

Do not use documentation, filenames, TODOs, or class declarations alone to justify `IMPLEMENTED`.

## 8. Provenance and external research

External projects, papers, biological analogies, AI-agent systems, and third-party architectures may be used as comparison or research material.

They must not silently become part of GNOSIS architecture or be presented as the origin of the Ψ/Gnozis line.

Record significant external architectural influences explicitly when they are adopted.

## 9. Sensitive boundaries

Do not add OpenRouter or a bot to V2 unless the project owner explicitly changes this decision.

Do not expose internal Core implementation merely for convenience of external tools.

Security features must not be claimed until their threat model, implementation and tests exist.

## 10. Context recovery procedure

If an AI tool enters this repository with no prior conversation context, it should reconstruct working context in this order:

1. Read `AI_CONTEXT.md`.
2. Read `STATUS.md`.
3. Read the relevant `docs/` specification.
4. Inspect the Core source.
5. Inspect the relevant tests.
6. Inspect recent Git history and CI.
7. Determine the actual status using `IMPLEMENTED/PARTIAL/MISSING/THEORETICAL`.
8. Continue only with the currently authorized task.

The AI must not infer unfinished work from old conversation history when the repository contains newer evidence.

## 11. Context update rule

When a major architectural decision changes, update this file in the same change set or immediately after the decision.

Do not turn this file into a chronological chat transcript. Keep it as a compact operational handoff document.

## 12. Current handoff

At creation of this document:

- Canonical repository: `Gnozis-V2`.
- Older repository: archival/research reference.
- Immediate engineering focus: Persistence + Append-Only Audit Log.
- Next stages remain gated by verification of the current stage.
- Any AI tool joining the project should begin by validating this document against the repository.
