# Gnozis-V2 — AI Context

## CANONICAL BASELINE — HEAD PIN

- Canonical repository: `Mikhail-Kucheriavyi-23/Gnozis-V2`
- Canonical branch: `main`
- Last verified main HEAD before this context-sync commit: `b4482daee26a8c3ba198fc4c69fd47c237c69439`.
- Previous pinned baselines `a990a11e81c5a693ed3b2ac45f115954cad5ad5f` and older `47a7e548...` are historical.
- All architectural statements in this document refer to current `main` or explicitly marked historical commits/branches.
- Before architectural changes, reconcile current `main` HEAD if working context may be stale.

## Canonical repository and scope

- Canonical development repository: `Mikhail-Kucheriavyi-23/Gnozis-V2`
- `AI_CONTEXT.md` is the operational handoff document and must remain synchronized with verified source/runtime state.
- Current scope: SINGLE OWNER / SINGLE ACCOUNT / SINGLE PROJECT.
- Multi-user, federation, tenant and public-network runtime are future strategy only.
- Current work is repository modification, testing, persistence, reflection, autonomous evolution architecture and architecture validation.

## Core architectural objective

Gnozis is intended to become an autonomous recursive evolution system. Autonomous self-modification is intentional. The safety property is not mandatory human activation; it is evidence-backed bounded evolution.

The intended recursive contour is:

```text
Core_n
  ↓
observable evidence
  ↓
persistence / recovery
  ↓
Reflection
  ↓
versioned RuleProposal
  ↓
EvolutionHypothesis
  ↓
bounded EvolutionSandbox
  ↓
ModelGenerator
  ↓
real sandbox execution
  ↓
Shadow Evaluation
  ↓
Invariant Delta
  ↓
Governance / evidence threshold
  ↓
PromotionCandidate
  ↓
Core_(n+1)
  ↓
Reflection again
```

A proposal must never jump directly to canonical mutation. The recursive loop must generate evidence from actual execution, compare alternatives, preserve invariants, and only then make a candidate eligible for promotion.

## Historical architectural gates

1. **Ψ-Core authority** — Core remains the source of truth for state/evolution semantics. No second state model and no AI model inside Core.
2. **Persistence first** — durable SQLite storage and append-only audit evidence survive process boundaries.
3. **Provenance** — `TransitionRecord.test_rule_id` identifies the rule that produced a transition. Missing provenance remains `test-rule:unspecified`.
4. **Recovery** — diagnostic evidence comes from persisted/recovered transition history, not a fresh/empty Engine and not fabricated records.
5. **Self-Diagnostic** — Reflection remains outside Core: evidence → observations → findings → causal candidates → counterexamples → RuleProposal.
6. **Reproducible diagnostic corpus** — controlled experiments are generated from actual Core execution and persistence.
7. **Executable diagnostic path** — execution → `persist_transition()` → recovery → `diagnose(recovered_history)` → artifact.
8. **Rule Registry R1** — versioned read-only `RuleRegistry`/`RuleMetadata` gives proposals concrete `rule_id + rule_version` references.
9. **Versioned RuleProposal** — proposals contain current/proposed versions, evidence, counterexamples, expected effects, risks and validation requirements.
10. **Shadow Adapter** — proposal can be evaluated without activation or Core mutation.
11. **Invariant Delta** — shadow and active evidence are compared against the existing Core invariant surface; missing evidence becomes `unknown`, never fabricated failure.
12. **Persistent Invariant Delta** — existing reflection SQLite persistence stores invariant-delta evidence; no second storage system.
13. **Governance Decision** — read-only classification: `BLOCK`, `HOLD`, `REVIEW`, `NO_CHANGE`.
14. **Authority provenance** — AuthorityRequest records what approval/authority would be required, but it is not the intended long-term autonomous-evolution gate.
15. **Autonomous Evolution Sandbox — experimental branch** — `evolution-sandbox` contains bounded hypothesis/model generation, evaluator contracts and now an execution contract that produces evidence from an actual runner invocation.

## Current verified engineering state

- Ψ-Core remains authoritative.
- Persistence and append-only audit storage exist.
- Reflection, versioned RuleProposal and governance layers exist.
- The canonical `main` line has not yet been runtime-verified for the full autonomous evolution loop.
- `evolution-sandbox` currently contains experimental contracts for:
  - `EvolutionHypothesis`
  - `SandboxModel`
  - `SandboxExperiment`
  - bounded `ModelGenerator`
  - `ModelEvidence`
  - `SandboxEvaluation`
  - `SandboxExecution`
- `SandboxExecution` invokes a supplied runner and derives a deterministic SHA-256 evidence digest from returned observations.
- Sandbox execution has no canonical-Core mutation capability.
- Execution test exists but has **not** been run by a real runtime/CI in this session.
- **Do not claim any test PASS unless an actual runtime/CI execution is inspected.**
- **Do not claim a real GitHub Actions Self-Diagnostic run or artifact exists unless an actual run is inspected.**

## Current layers

```text
L0 Ψ-Core
L1 Evidence / Persistence / Recovery
L2 Reflection / RuleProposal
L3 Shadow Evaluation / Invariant Delta / Governance
L4 Autonomous Evolution Sandbox (experimental)
L5 Promotion to Core_(n+1) (NOT YET IMPLEMENTED)
```

## Current next engineering gate

The next gate is to connect real sandbox execution evidence to the existing evaluator and then to existing ShadowEvaluation + InvariantDelta, without creating a parallel evidence model.

Required direction:

```text
EvolutionHypothesis
 ↓
ModelGenerator
 ↓
SandboxExecution
 ↓
real observations + digest
 ↓
Evaluator
 ↓
ShadowEvaluation
 ↓
InvariantDelta
 ↓
PromotionCandidate
```

Only after this entire chain has real runtime evidence should canonical promotion be implemented.

## Independent External Audit Roadmap

The following roadmap was supplied by independent external audits on 2026-09-17. It is a **future architectural requirements baseline**, not implementation evidence. Requirements must be independently classified as `SPECIFIED | IMPLEMENTED | TESTED | VERIFIED`.

### Stage 1 — Persistence Stabilization

- SQLite `PRAGMA foreign_keys = ON` for every connection.
- Canonical JSON serialization for `audit_events`.
- Cryptographic `prev_hash` / `event_hash` chain verification.
- Fork-after-restart detection.
- Atomic candidate/state-head updates with `FAIL_CLOSED` behavior on broken transaction boundaries.
- Secret sanitization for persistent logs.
- Persistence/recovery verification.

### Stage 2 — Architectural Immunity

- Independent audit/state observer.
- Controlled Red Team / Self-Attack engine.
- Detection of malformed candidates, invalid transitions, race conditions and persistence corruption.
- Explicit anomaly classification.
- Branch quarantine without destruction of evidence.

### Stage 3 — Cognitive Metabolism

- External ingestion boundary.
- Ingress secret/malicious-pattern sanitization.
- Isolated quarantine buffer.
- Semantic transducer into canonical Gnozis entities.
- Provenance and trust metadata.
- No direct executable access from external input to Core.

### Stage 4 — Sandbox / Controlled Self-Evolution

- Isolated digital twin / execution environment.
- Mutation as a first-class versioned object.
- Invariant matrix.
- Resource/gas limits.
- Multi-level verification.
- Controlled merge only after evidence-backed verification.

### Stage 5 — Agent Spawning / Lineage

- Explicit spawn policy and validated triggers.
- Versioned Bootstrap State Package.
- Bootstrap integrity/compatibility verification.
- Isolated child runtime and separate database.
- Parent/child lineage and generation provenance.
- Separation of inherited baseline, child experience and child mutations.
- Failed initialization must never leave a partially trusted active child.

**Important:** trigger ≠ authorization; replication of architecture ≠ replication of authority; child agents must not automatically inherit parent secrets or unrestricted capabilities.

## Autonomous Task Queue

This queue converts the roadmap into deterministic executable work blocks for Claude, ChatGPT, Manus, Gemini or another engineering agent.

### Task-selection protocol

When starting work, an agent MUST:

1. Read this `AI_CONTEXT.md`.
2. Reconcile current repository HEAD.
3. Inspect the current implementation and tests.
4. Find the highest-priority task with status `READY` whose dependencies are satisfied.
5. Implement only that primary task unless a directly necessary correction is discovered.
6. Run the relevant tests/runtime verification.
7. Record implementation and evidence.
8. Mark the task `DONE` only with evidence, otherwise `BLOCKED` or leave it `IN_PROGRESS`.
9. Stop and hand off.

The agent must not choose tasks based on preference or jump to a later capability merely because it is interesting.

### Statuses

- `PLANNED` — defined but dependencies are not ready.
- `READY` — executable now.
- `IN_PROGRESS` — actively being implemented.
- `DONE` — implemented and verified with evidence.
- `BLOCKED` — concrete blocker prevents execution.
- `REJECTED` — superseded or invalid specification.

### Priority

- `P0` — architectural/security blocker.
- `P1` — required foundation.
- `P2` — required subsystem.
- `P3` — advanced capability.
- `P4` — refinement/optimization.

Priority never overrides dependencies.

## Current Task Queue

### P0 — Evolution/Core Integrity

| ID | Task | Status | Dependencies |
|---|---|---|---|
| GNV2-001 | Deep State Immutability | READY | none |
| GNV2-002 | Strict `Test(candidate) -> bool` contract | READY | none |
| GNV2-003 | Reject no-op evolution | PLANNED | GNV2-001 |
| GNV2-004 | Remove hidden evolution state / side channels | PLANNED | GNV2-001 |

### P1 — Existing Evolution Contract

| ID | Task | Status | Dependencies |
|---|---|---|---|
| GNV2-005 | Strict Engine `steps` type contract | READY | none |
| GNV2-020 | Complete Core evolution vertical slice | PLANNED | GNV2-001..005, persistence gates |

### P1 — Persistence

| ID | Task | Status | Dependencies |
|---|---|---|---|
| GNV2-010 | SQLite foreign-key enforcement | READY | storage layer |
| GNV2-011 | Canonical audit serialization | PLANNED | GNV2-010 |
| GNV2-012 | Audit hash chain | PLANNED | GNV2-011 |
| GNV2-013 | Persistence head integrity / fork detection | PLANNED | GNV2-012 |
| GNV2-014 | Transactional candidate/head update | PLANNED | GNV2-013 |
| GNV2-015 | Secret sanitization | PLANNED | audit persistence |
| GNV2-016 | Persistence recovery verification | PLANNED | GNV2-014 |

### P1 — Current Autonomous Evolution Gate

| ID | Task | Status | Dependencies |
|---|---|---|---|
| GNV2-021 | Connect real `SandboxExecution` evidence to existing Evaluator | READY | current sandbox contracts |
| GNV2-022 | Feed evaluator output into existing `ShadowEvaluation` | PLANNED | GNV2-021 |
| GNV2-023 | Connect `ShadowEvaluation` to existing `InvariantDelta` | PLANNED | GNV2-022 |
| GNV2-024 | Produce verified `PromotionCandidate` without canonical mutation | PLANNED | GNV2-023 |
| GNV2-025 | Runtime/CI verification of the complete sandbox evidence chain | PLANNED | GNV2-024 |

### P2 — Architectural Immunity

| ID | Task | Status | Dependencies |
|---|---|---|---|
| GNV2-030 | Immunologist contract and authority boundary | PLANNED | GNV2-025 |
| GNV2-031 | Audit/state observer | PLANNED | GNV2-030 |
| GNV2-032 | Self-Red-Team engine | PLANNED | GNV2-031 |
| GNV2-033 | Anomaly classification | PLANNED | GNV2-032 |
| GNV2-034 | Branch quarantine | PLANNED | GNV2-033 |

### P2 — Cognitive Metabolism

| ID | Task | Status | Dependencies |
|---|---|---|---|
| GNV2-040 | External ingestion contract | PLANNED | GNV2-025 |
| GNV2-041 | Ingress sanitizer | PLANNED | GNV2-040 |
| GNV2-042 | Quarantine buffer | PLANNED | GNV2-041 |
| GNV2-043 | Semantic transducer | PLANNED | GNV2-042 |
| GNV2-044 | Provenance tracking | PLANNED | GNV2-043 |

### P3 — Sandbox / Self-Modification

| ID | Task | Status | Dependencies |
|---|---|---|---|
| GNV2-050 | Versioned mutation contract | PLANNED | GNV2-025 |
| GNV2-051 | Digital-twin sandbox hardening | PLANNED | GNV2-050 |
| GNV2-052 | Invariant matrix | PLANNED | GNV2-051 |
| GNV2-053 | Resource/gas limits | PLANNED | GNV2-051 |
| GNV2-054 | Multi-level mutation verification | PLANNED | GNV2-052, GNV2-053 |
| GNV2-055 | Controlled auto-merge | PLANNED | GNV2-054 |

### P3 — Agent Spawning

| ID | Task | Status | Dependencies |
|---|---|---|---|
| GNV2-060 | Spawn policy | PLANNED | GNV2-055 |
| GNV2-061 | Bootstrap State Package | PLANNED | GNV2-060 |
| GNV2-062 | Bootstrap verification | PLANNED | GNV2-061 |
| GNV2-063 | Isolated child instance | PLANNED | GNV2-062 |
| GNV2-064 | Parent/child lineage | PLANNED | GNV2-063 |
| GNV2-065 | Genetic drift | PLANNED | GNV2-064 |
| GNV2-066 | Spawn failure safety | PLANNED | GNV2-063 |

### Final integration

| ID | Task | Status | Dependencies |
|---|---|---|---|
| GNV2-100 | Integrated autonomous evolution | PLANNED | all mandatory gates |

## Task completion evidence

For every completed task, record:

```text
Task ID:
Status:
Implementation:
Files changed:
Tests added/changed:
Tests actually executed:
Observed result:
Known limitations:
New dependencies discovered:
```

`DONE` means actual evidence exists. A written test that was not executed is not a PASS.

## Architecture safety rules for future autonomous work

- External data is untrusted by default.
- No external adapter receives direct unrestricted Core access.
- No AI model is embedded inside Ψ-Core.
- No second state model may silently diverge from Core.
- Evolution must remain evidence-backed and bounded.
- A trigger is not authorization.
- Replication of architecture is not replication of authority.
- Parent secrets and credentials are never inherited by child agents by default.
- Failed operations prefer `REJECT`, `QUARANTINE` or `FAIL_CLOSED` over silent recovery.
- Future autonomous mutation must never bypass the invariant/evidence gate.

## Context integrity rule

If chat history and repository disagree, verified repository HEAD and actual runtime evidence take precedence. Never reconstruct current architecture from memory alone. Update this file whenever a major architectural gate is completed or a canonical HEAD changes materially.
