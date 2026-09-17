# GNOSIS-V2 — Shared AI Working Context

> Canonical handoff document for AI tools working on this repository.
> This file records project context and collaboration rules; it is not a substitute for source code, tests, CI, or formal specifications.

## 1. Project identity

- Repository: `Mikhail-Kucheriavyi-23/Gnozis-V2`
- Project: GNOSIS 2.0
- This repository is the canonical development line for V2.
- The older `Mikhail-Kucheriavyi-23/Gnozis` repository is an archived/research line and must not be treated as the automatic source of code for V2.

## 2. Current architectural direction

Core mathematical state:

`Ψ = (X, R)`

The Core is the authoritative source of truth for state transitions.

Current verified Core transition pattern:

`Candidate → Test → Verify → Commit → State′`

The multi-candidate path additionally supports:

`Generate(caller-supplied) → Test → Select → Evolve → State′`

Important boundaries:

- Core must not depend directly on SQLite, GitHub, terminal tools, workers, or external AI services.
- Persistence is a representation/storage layer for Core state, not a second mutable state machine.
- External interfaces must not receive unrestricted authority to mutate Core.
- Current `GenerateFn` is caller-supplied. Endogenous/population-level Generate is future research work and is NOT implemented.
- Do not introduce OpenRouter, Telegram/bot infrastructure, a global controller, direct Internet-to-Core paths, or global mutable memory unless the project owner explicitly changes the architecture.

## 3. Verified repository status

This section is a handoff snapshot based on repository evidence. It must still be re-verified before making new claims.

### IMPLEMENTED

- Ψ=(X,R) Core state model with `State` and `Relation`.
- Deep-freeze protection for nested `State`/`Relation` data.
- Candidate / TestResult / Verify / Commit flow.
- Content-based meaningful-change/no-op protection.
- Multi-candidate `Select` via `Engine.step_select`.
- Resource budget constraints (default budget 20).
- Clone/fork/lineage mechanisms with instance isolation tests.
- Phase 0/1 Core contracts and tests.
- Threat model and database schema documents.
- Dependency separation: zero core dependencies; analytics dependencies isolated as an optional extra.
- Current `logs/` directory structure exists as an explicit audit/logging placeholder.

### PARTIAL

- Generate→Test→Select→Evolve: multi-candidate Select exists, but Generate remains caller-supplied and there is no population-level endogenous generation.
- Protected invariants: Core/state/transition/monotonic-version/meaningful-change invariants exist; identity, capability, cryptographic, memory and persistent-audit invariants are not implemented.
- Proof-preserving evolution: verification interface exists, but no Lean/Coq/F* theorem-prover binding.
- Stop conditions: implemented conditions include budget exhaustion and invalid state; additional stop reasons remain reserved/future.
- Instance/clone/fork/lineage: implemented in memory, but no persistent DB recovery and no cryptographic per-instance identity.
- Logs/auditability: `Engine.history` is in-memory only; `logs/` contains placeholders/documentation and has no persistent audit writer yet.
- Test strategy/security: Core and adversarial tests exist, but Agent/Federation/Memory/cryptographic security tiers cannot be complete before those layers exist.
- Reproducibility: candidate seed exists, but no complete experiment harness recording seed/config/event log.
- Architecture layout: Core/instances are implemented; Agent, Memory, Bridge, Federation and Analytics implementation layers are not yet established; `storage/` is currently a placeholder.

### MISSING

- Persistent SQLite storage implementation.
- Append-only, hash-chained audit-log writer and complete chain verification.
- Restart recovery of state and lineage.
- Cryptographic Instance/Agent identity and signatures.
- Persistent Memory layer and encryption layer.
- Agent and multi-agent layers.
- User-owned copies, Federation, Trust and Delegation implementation.
- Secure external Bridge/world-exploration layer.
- Analytics implementation.

### THEORETICAL / FUTURE

- Endogenous/population-level Generate inside the verified evolution system.
- Mathematical population/mutation implementation described by the specification.
- Formal theorem-prover integration.

### CI / test evidence

- The repository contains GitHub Actions CI configuration.
- Current sandbox/connector evidence does **not** establish that CI has actually executed successfully; do not report CI as green merely because the workflow file exists.
- `STATUS.md` records 61 tests executed through an offline runner, with a caveat that real dependency installation/network-backed CI was not executed in that environment.
- Never convert static workflow correctness into a claim of successful CI execution.

## 4. Current next development stage

The immediate engineering focus is:

**Persistence + Append-Only Audit Log**

Target architecture:

`Core → Storage Adapter → SQLite`

and:

`Commit → Audit Event → Hash Chain`

The database schema is already drafted in `docs/DATABASE_SCHEMA.md`; implementation is not complete.

Required outcomes:

1. Persist State, Candidate, Transition and Instance/lineage.
2. Use deterministic canonical serialization.
3. Implement a real append-only audit API/writer.
4. Hash-chain audit events with SHA-256.
5. Verify the complete audit chain.
6. Make logical commit persistence transactional.
7. Recover current state and lineage after restart.
8. Preserve all existing Core invariants and tests.

After this stage, stop and report remaining gaps. Do not automatically start Agent, Memory, Federation, Bridge, endogenous Generate, or theorem-prover work without an explicitly authorized next task.

## 5. AI collaboration protocol

Multiple AI tools may work on this repository. They are independent collaborators, not competing sources of truth.

### Before work

1. Read `AI_CONTEXT.md`.
2. Read `STATUS.md` if present.
3. Inspect the relevant source code and tests.
4. Check current `main`, recent commits, and CI when the task depends on repository state.
5. Never assume another AI's description is correct without checking repository evidence.

### During work

- Make the smallest change that satisfies the agreed task.
- Preserve existing architectural boundaries.
- Do not silently broaden scope.
- Do not rewrite working Core code merely for style.
- Add or update tests for behavior changes.
- Do not weaken, delete, skip, or falsify tests to obtain green CI.
- Do not claim a feature is implemented because a placeholder, interface, enum, filename, or documentation exists.

### After work

Every AI that changes the repository should report:

- exact files changed;
- exact behavior added/changed;
- tests added/changed;
- tests actually run and their results;
- CI result if actually available;
- remaining limitations;
- whether the change affects the mathematical Core or only an adapter/infrastructure layer;
- one recommended next task, without starting it automatically.

## 6. Conflict resolution between AI tools

If two AI tools disagree:

1. Source code is stronger evidence than prose.
2. Passing behavioral tests are stronger evidence than comments.
3. Actual CI results are stronger evidence than claimed local results.
4. The mathematical/architectural specification is the reference for intended behavior.
5. If implementation and specification disagree, do not silently choose one; document the discrepancy and record the required decision.

Never merge incompatible architectural interpretations merely to remove a conflict.

## 7. Status vocabulary

Use only these implementation labels when reporting implementation state:

- `IMPLEMENTED` — behavior exists and is supported by code plus appropriate tests/evidence.
- `PARTIAL` — some implementation exists but acceptance criteria are incomplete.
- `MISSING` — no working implementation exists.
- `THEORETICAL` — described as an idea/specification but not implemented.

Do not use documentation, filenames, TODOs, enum members, class declarations, or placeholders alone to justify `IMPLEMENTED`.

## 8. Provenance and external research

External projects, papers, biological analogies, AI-agent systems, and third-party architectures may be used as comparison or research material.

They must not silently become part of GNOSIS architecture or be presented as the origin of the Ψ/Gnozis line.

Record significant external architectural influences explicitly when they are adopted.

## 9. Sensitive boundaries

- Do not add OpenRouter or a bot to V2 unless the project owner explicitly changes this decision.
- Do not expose internal Core implementation merely for convenience of external tools.
- Security features must not be claimed until their threat model, implementation, and tests exist.
- `logs/` is for inspectable evolution/audit evidence; do not represent its current placeholders as a working persistent audit system.

## 10. Context recovery procedure

If an AI tool enters this repository with no prior conversation context, reconstruct working context in this order:

1. Read `AI_CONTEXT.md`.
2. Read `STATUS.md`.
3. Read the relevant `docs/` specifications, especially `docs/DATABASE_SCHEMA.md` and `docs/THREAT_MODEL.md`.
4. Inspect the Core source.
5. Inspect the relevant tests.
6. Inspect recent Git history and CI.
7. Determine actual status using `IMPLEMENTED/PARTIAL/MISSING/THEORETICAL`.
8. Continue only with the currently authorized task.

The AI must not infer unfinished work from old conversation history when the repository contains newer evidence.

## 11. Context update rule

When a major architectural decision or implementation status changes, update this file in the same change set or immediately after the decision.

Do not turn this file into a chronological chat transcript. Keep it as a compact operational handoff document.

## 12. Current handoff

- Canonical repository: `Gnozis-V2`.
- Older `Gnozis`: archival/research reference only.
- Current Core: Phase 0/1 substantially implemented and tested; Instance layer partially implemented in memory.
- Immediate engineering focus: persistent SQLite storage + append-only hash-chained audit log.
- `docs/DATABASE_SCHEMA.md` already defines the intended database structure; implementation remains incomplete.
- `logs/` currently provides the inspection/documentation boundary, not a completed persistent audit backend.
- CI must be reported as `UNVERIFIED` unless an actual CI run/result is available.
- Next stages remain gated by verification of the current persistence/audit stage.
- Any AI tool joining the project should begin by validating this document against the repository.
