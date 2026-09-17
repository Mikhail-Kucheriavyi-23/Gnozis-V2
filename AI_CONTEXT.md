# Gnozis-V2 — AI Context

## CANONICAL BASELINE

- Canonical repository: `Mikhail-Kucheriavyi-23/Gnozis-V2`
- Canonical branch: `main`
- This document is the operational AI handoff and must remain synchronized with verified repository/runtime state.
- Current scope: single owner / single account / single project. Multi-user, federation and public-network runtime remain future strategy.
- If chat history and repository disagree, verified repository HEAD and actual runtime evidence take precedence.

## ARCHITECTURAL OBJECTIVE

Gnozis is intended to become an autonomous recursive evolution system. Autonomous self-modification is intentional; canonical mutation must remain downstream of reproducible, bounded evidence.

```text
Core_n
 ↓
observable evidence
 ↓
persistence / recovery
 ↓
reflection
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

No stage may substitute for the complete evidence chain.

## ARCHITECTURAL GATES — DO NOT LOSE

1. Ψ-Core remains authoritative for state/evolution semantics. No second state model and no AI model inside Core.
2. Durable SQLite persistence and append-only audit evidence survive process boundaries.
3. `TransitionRecord.test_rule_id` provides rule provenance; missing provenance is `test-rule:unspecified`.
4. Diagnostics use persisted/recovered history, never fabricated records or a fresh empty Engine.
5. Reflection remains outside Core: evidence → observations → findings → causal candidates → counterexamples → RuleProposal.
6. Diagnostic experiments must be generated from actual Core execution and persistence.
7. The executable diagnostic path is execution → persistence → recovery → diagnosis → artifact.
8. Versioned read-only Rule Registry / Rule Metadata gives proposals concrete rule identifiers and versions.
9. RuleProposal carries current/proposed versions, evidence, counterexamples, expected effects, risks and validation requirements.
10. Shadow evaluation must not activate or mutate Core.
11. Invariant Delta represents missing evidence as `unknown`, never fabricated failure.
12. Invariant-delta evidence uses the existing persistence system; no parallel evidence database.
13. Governance remains read-only classification: `BLOCK`, `HOLD`, `REVIEW`, `NO_CHANGE`.
14. Authority metadata is provenance, not the definition of the autonomous evolution mechanism.
15. Evolution sandbox remains experimental until runtime/CI evidence verifies it.

## CURRENT ENGINEERING STATE

- Ψ-Core remains authoritative.
- Persistence, append-only audit storage, Reflection, RuleProposal, Shadow Evaluation, Invariant Delta and governance layers exist in the development line.
- The `evolution-sandbox` work contains bounded `EvolutionHypothesis`, `SandboxModel`, `SandboxExperiment`, `ModelGenerator`, `ModelEvidence`, `SandboxEvaluation` and execution contracts.
- Sandbox execution must produce evidence from real execution, not a caller-supplied score.
- Autonomous canonical promotion is NOT yet implemented.
- Never claim a test PASS, GitHub Actions run, artifact, or self-diagnostic result unless the actual runtime/CI execution has been inspected.

## CURRENT LAYERS

```text
L0 Ψ-Core
L1 Evidence / Persistence / Recovery
L2 Reflection / RuleProposal
L3 Shadow Evaluation / Invariant Delta / Governance
L4 Autonomous Evolution Sandbox (experimental)
L5 Promotion to Core_(n+1) — NOT YET IMPLEMENTED
```

## NEXT ENGINEERING GATE

```text
EvolutionHypothesis
 ↓
ModelGenerator
 ↓
real SandboxExecution
 ↓
observations + evidence digest
 ↓
Evaluator
 ↓
ShadowEvaluation
 ↓
InvariantDelta
 ↓
Governance
 ↓
PromotionCandidate
```

Only after this chain has real runtime evidence should canonical promotion be implemented.

## AI TASK-BLOCK OPERATING PROTOCOL

The roadmap is not merely a list of ideas. It is an operational Task Registry for engineering agents. Each agent must select one executable task according to dependencies and evidence.

### Operating contour

```text
Audit
 ↓
Task Registry
 ↓
Dependency Graph
 ↓
Priority Selection
 ↓
Implementation
 ↓
Test
 ↓
Adversarial Check
 ↓
Correction
 ↓
Re-test
 ↓
Gate
 ↓
Evidence Record
 ↓
Next Task
```

### Task Block contract

Every executable task should define:

- `TASK-ID`
- `BLOCK`
- `STATUS`
- `PRIORITY`
- `DEPENDS_ON`
- `OBJECTIVE`
- `SCOPE`
- `DO_NOT_CHANGE`
- `REQUIRED_TESTS`
- `ACCEPTANCE`
- `AUDIT`
- `NEXT`

### Deterministic task-selection rule

At the beginning of work an agent MUST:

1. Read the complete `AI_CONTEXT.md`.
2. Reconcile current `main` HEAD.
3. Inspect current implementation and relevant tests.
4. Build the applicable dependency view.
5. Select exactly one highest-priority `READY` task whose dependencies are satisfied.
6. Implement only that primary task plus directly necessary corrections.
7. Execute relevant tests/runtime verification.
8. Record actual evidence.
9. Mark `DONE` only when evidence exists; otherwise use `IN_PROGRESS` or `BLOCKED`.
10. Stop and hand off instead of jumping to an unrelated later capability.

Priority never overrides dependencies.

### Statuses

- `PLANNED` — defined but dependencies are not ready.
- `READY` — executable now.
- `IN_PROGRESS` — being implemented.
- `DONE` — implemented and verified with evidence.
- `BLOCKED` — concrete blocker prevents execution.
- `REJECTED` — superseded or invalid.

### Priority

- `P0` — architectural/security blocker.
- `P1` — required foundation.
- `P2` — required subsystem.
- `P3` — advanced capability.
- `P4` — refinement/optimization.

## TASK-BLOCK PRIORITY STRUCTURE

### P0 — Core integrity

- Deep State Immutability
- Strict `Test(candidate) -> bool` contract
- Reject no-op evolution
- Remove hidden evolution state / side channels

### P1 — Existing evolution contract

- Strict Engine `steps` type contract
- Complete Core evolution vertical slice after required persistence gates

### P1 — Persistence

- SQLite foreign-key enforcement
- Canonical audit serialization
- Cryptographic audit hash chain
- Persistence head integrity / fork detection
- Transactional candidate/state-head update with fail-closed behavior
- Secret sanitization
- Persistence recovery verification

### P1 — Autonomous evolution evidence chain

- Connect real `SandboxExecution` evidence to existing Evaluator
- Feed evaluator output into existing `ShadowEvaluation`
- Connect `ShadowEvaluation` to existing `InvariantDelta`
- Produce verified `PromotionCandidate` without canonical mutation
- Runtime/CI verification of the complete sandbox evidence chain

### P2 — Architectural immunity

- Independent audit/state observer
- Controlled Red-Team / Self-Attack engine
- Anomaly classification
- Branch quarantine without destroying evidence

### P2 — Cognitive metabolism

- External ingestion contract
- Ingress sanitization
- Isolated quarantine buffer
- Semantic transducer into canonical Gnozis entities
- Provenance and trust metadata

### P3 — Sandbox / self-modification

- Versioned mutation contract
- Digital-twin sandbox hardening
- Invariant matrix
- Resource/gas limits
- Multi-level mutation verification
- Controlled auto-merge

### P3 — Agent spawning

- Spawn policy
- Versioned Bootstrap State Package
- Bootstrap verification
- Isolated child instance
- Parent/child lineage
- Genetic drift
- Spawn failure safety

### Final integration

- Integrated autonomous evolution only after all mandatory gates have actual evidence.

## COMPLETION EVIDENCE

For every completed task record:

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

A written test that was not executed is not a PASS.

## SAFETY RULES

- External data is untrusted by default.
- No external adapter gets unrestricted Core access.
- No AI model is embedded inside Ψ-Core.
- No second state model may silently diverge from Core.
- Evolution must remain evidence-backed and bounded.
- A trigger is not authorization.
- Replication of architecture is not replication of authority.
- Parent secrets and credentials are never inherited by child agents by default.
- Failed operations prefer `REJECT`, `QUARANTINE` or `FAIL_CLOSED` over silent recovery.
- Future autonomous mutation must never bypass the invariant/evidence gate.

## FINAL SELF-EVOLUTION RULE

The last self-evolution gate remains closed while the evidence chain is incomplete. Preparation comes first: Core invariants, persistence/recovery, append-only audit evidence, candidate generation/testing, sandbox execution, shadow evaluation, invariant delta, governance/evidence thresholds, security, quarantine and recovery.

The intended promotion sequence is:

```text
Candidate
 ↓
Generate
 ↓
Test
 ↓
Sandbox execution
 ↓
Observed evidence
 ↓
Shadow evaluation
 ↓
Invariant delta
 ↓
Governance / evidence gate
 ↓
Promotion candidate
 ↓
ONLY THEN canonical mutation
```

## CONTEXT INTEGRITY

Update this file whenever a major architectural gate is completed or the canonical HEAD changes materially. Never reconstruct current architecture from memory alone.