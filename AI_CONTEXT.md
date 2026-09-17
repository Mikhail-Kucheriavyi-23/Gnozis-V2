# Gnozis-V2 — AI Context

## CANONICAL BASELINE

- Repository: `Mikhail-Kucheriavyi-23/Gnozis-V2`
- Branch: `main`
- This is the operational AI handoff. Reconcile repository HEAD and runtime evidence before acting.
- If chat history conflicts with repository/runtime evidence, repository/runtime evidence wins.

## ARCHITECTURAL OBJECTIVE

Gnozis is intended to become an autonomous recursive evolution system. Canonical self-modification must remain downstream of reproducible, bounded evidence.

```text
Core_n
 ↓ evidence
Persistence / Recovery
 ↓ reflection
RuleProposal / EvolutionHypothesis
 ↓ bounded Sandbox
real execution
 ↓ Shadow Evaluation
 ↓ Invariant Delta
 ↓ Governance / evidence threshold
 ↓ PromotionCandidate
 ↓ Core_(n+1)
```

No stage substitutes for the complete evidence chain.

## NON-NEGOTIABLE ARCHITECTURAL GATES

1. Ψ-Core is authoritative for state/evolution semantics. No second state model and no AI model inside Core.
2. Durable SQLite persistence and append-only audit evidence survive process boundaries.
3. `TransitionRecord.test_rule_id` provides rule provenance; missing provenance is `test-rule:unspecified`.
4. Diagnostics use persisted/recovered history, never fabricated records or a fresh empty Engine.
5. Reflection remains outside Core.
6. Diagnostic experiments derive from actual Core execution and persistence.
7. Execution → persistence → recovery → diagnosis → artifact is the diagnostic path.
8. Rule Registry/Metadata is versioned and read-only for proposals.
9. RuleProposal carries versions, evidence, counterexamples, expected effects, risks and validation requirements.
10. Shadow evaluation cannot activate or mutate Core.
11. Invariant Delta uses `unknown` for missing evidence; never fabricate failure.
12. Invariant-delta evidence uses existing persistence; no parallel evidence database.
13. Governance is read-only classification: `BLOCK`, `HOLD`, `REVIEW`, `NO_CHANGE`.
14. Authority metadata is provenance, not the autonomous evolution mechanism.
15. Evolution sandbox remains experimental until runtime/CI evidence verifies it.

## CURRENT ENGINEERING STATE

- Ψ-Core remains authoritative.
- Persistence, append-only audit storage, Reflection, RuleProposal, Shadow Evaluation, Invariant Delta and governance layers exist in the development line.
- Evolution sandbox contains bounded hypothesis/model/experiment/evidence/evaluation contracts.
- Sandbox execution must produce evidence from real execution, not caller-supplied scores.
- Autonomous canonical promotion is NOT implemented.
- Never claim PASS, CI success, artifact or self-diagnostic result unless actual execution/CI has been inspected.

## LAYERS

```text
L0 Ψ-Core
L1 Evidence / Persistence / Recovery
L2 Reflection / RuleProposal
L3 Shadow Evaluation / Invariant Delta / Governance
L4 Autonomous Evolution Sandbox (experimental)
L5 Promotion to Core_(n+1) — NOT IMPLEMENTED
```

## PERSISTENCE HARDENING — RUNTIME STATUS

The Persistence hardening gates below have now received current CI evidence and are considered **VERIFIED** on the tested development line. Do not reopen or modify them without new regression evidence.

- `GNV2-PERSIST-001` — TransitionRecord persistence integrity — VERIFIED.
- `GNV2-PERSIST-002` — Rejected transition durable semantics — VERIFIED.
- `GNV2-PERSIST-003` — Recovery/provenance verification — VERIFIED.
- `GNV2-PERSIST-003A` — Canonical `transition_id` identity verification; verifier rejects tampered transition identity — VERIFIED.
- `GNV2-PERSIST-003B` — Transition ↔ audit provenance linkage, including adversarial tampering — VERIFIED.
- `GNV2-PERSIST-004` — Transition replay/idempotency — VERIFIED.
- `GNV2-PERSIST-005` — Crash/reopen consistency across transaction checkpoints — VERIFIED.
- Audit tamper tests cover event payload, `event_hash`, and `prev_hash` corruption — VERIFIED.

Latest inspected CI evidence: run `35275548474` on commit `5591af042d31500b323e3bbf7d74cceae2268b70`; persistence-related tests passed, including the audit-link tampering test. This run still had unrelated Reflection/Shadow/Diagnostic failures, so the overall CI run was not green.

### Persistence chain

```text
Candidate
 ↓
Protected invariants
 ↓
Test → TransitionRecord
 ↓
canonical transition_id
 ↓
SQLite transition
 ↓
Audit transition_id
 ↓
canonical audit event
 ↓
event_hash / prev_hash chain
 ↓
atomic transaction
 ↓
crash/reopen recovery
 ↓
verify_durable_graph()
 ↓
recovered durable State
```

Rejected transitions are historical evidence and must not advance `current_state_id`.

## CURRENT ACTIVE GATE — REFLECTION / SHADOW / INVARIANT DELTA

Persistence is frozen. The remaining active gate is Reflection/Shadow/Invariant Delta. Do not fix failures by weakening Core invariants or Persistence guarantees.

The latest inspected CI on `5591af042d31500b323e3bbf7d74cceae2268b70` reported `176 passed / 9 failed`.

Known failure clusters:

1. Diagnostic artifact contract: test expects top-level findings while the current artifact can carry findings through `causal_candidates`; determine whether this is a stale test contract or a serialization loss before changing production code.
2. Invariant Delta: insufficient evidence and shadow invariant violations are currently being classified too broadly as `PRESERVED`. Missing candidate/state must remain `unknown`/insufficient evidence; absence of a violation record is not itself proof of preservation.
3. Reflection Delta persistence fixture: saving a delta requires a valid persisted `report_id`; do not weaken storage foreign keys to satisfy an isolated fixture.
4. Protected invariant gate: invariant rejection itself is correct; diagnostic reason propagation from `TestResult.reasons` into `TransitionRecord.reason` is incomplete.
5. Reflection foundation: current analyzer produces 5 observations where an older test expects 4; the additional rejected-transition reason is real evidence and must not be deleted merely to satisfy the old count.
6. Shadow/adapter: inspect actual acceptance-outcome semantics before changing `evaluate_shadow()`. A change in rejection reason alone is not an improvement/regression; active rejected → shadow accepted is an improvement and should be represented as behavioral change.

### Invariant Delta target semantics

```text
missing candidate/state or insufficient evidence
    → UNKNOWN / INSUFFICIENT_EVIDENCE

verified violation introduced or increased
    → VIOLATION

verified violation reduced
    → IMPROVED

verified absence/preservation with sufficient evidence
    → PRESERVED
```

Do not treat an empty violation set as sufficient evidence of preservation when the underlying state/invariant evidence is absent.

### Shadow target semantics

```text
active rejected → shadow accepted
    → improvement + behavioral change

active accepted → shadow rejected
    → regression + behavioral change

active/shadow same acceptance outcome
    → no improvement/regression

rejection reason changes while both remain rejected
    → changed diagnostic behavior, not automatically improvement
```

## RECENT TEST/CORRECTION COMMITS

- `090ec5bb9082e7dc0440d005715a7151b537be57` — align rule-provenance test with strict `Test(...)->bool` contract.
- `72e959f5556d4703e6248d745d9196cb4cb46ab4` — align diagnostic artifact test fixture with machine-readable report contract.
- `5591af042d31500b323e3bbf7d74cceae2268b70` — diagnostic corpus fixture uses valid monotonic Core versions; current CI inspected at this commit.

These commits document implementation/test progress; only inspected runtime evidence determines PASS.

## NEXT GATE AFTER REFLECTION

After Reflection/Shadow/Invariant Delta reaches verified CI evidence, freeze it and continue with the next evidence-backed architecture gate. Memory/Recovery must remain derived from or anchored to durable Core history and must never become a second source of truth.

```text
Durable Core history
 ↓
verified recovery
 ↓
Memory reconstruction/cache
 ↓
operational context
```

## EVOLUTION / SANDBOX GATE

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

Canonical promotion only after real evidence.

## AI TASK-BLOCK PROTOCOL

Every agent must:

1. Read complete `AI_CONTEXT.md`.
2. Reconcile current `main` HEAD.
3. Inspect implementation and relevant tests.
4. Build dependency view.
5. Select exactly one highest-priority READY task with dependencies satisfied.
6. Implement only that task plus necessary corrections.
7. Execute relevant tests/runtime verification.
8. Record actual evidence.
9. Mark DONE only with evidence; otherwise IN_PROGRESS/BLOCKED.
10. Stop and hand off rather than jumping to unrelated capabilities.

Task Block fields:
`TASK-ID`, `BLOCK`, `STATUS`, `PRIORITY`, `DEPENDS_ON`, `OBJECTIVE`, `SCOPE`, `DO_NOT_CHANGE`, `REQUIRED_TESTS`, `ACCEPTANCE`, `AUDIT`, `NEXT`.

Statuses: `PLANNED`, `READY`, `IN_PROGRESS`, `DONE`, `BLOCKED`, `REJECTED`.

Priority: `P0` architectural/security blocker; `P1` foundation; `P2` subsystem; `P3` advanced; `P4` refinement.

## PRIORITY STRUCTURE

### P0 Core integrity
- Deep State Immutability
- Strict `Test(candidate) -> bool`
- Reject no-op evolution
- Remove hidden evolution state/side channels

### P1 Existing evolution
- Strict Engine `steps` type contract
- Complete Core evolution vertical slice after persistence gates

### P1 Persistence
- SQLite foreign-key enforcement
- Canonical audit serialization
- Cryptographic audit hash chain
- Head integrity/fork detection
- Transactional candidate/state-head update with fail-closed behavior
- Secret sanitization
- Recovery verification

### P1 Autonomous evolution evidence
- Real SandboxExecution → Evaluator
- Evaluator → ShadowEvaluation
- ShadowEvaluation → InvariantDelta
- Verified PromotionCandidate without canonical mutation
- Runtime/CI verification of the complete sandbox evidence chain

### P2 Architectural immunity
- Independent audit/state observer
- Controlled Red-Team/Self-Attack engine
- Anomaly classification
- Branch quarantine without destroying evidence

### P2 Cognitive metabolism
- External ingestion contract
- Ingress sanitization
- Isolated quarantine buffer
- Semantic transducer
- Provenance/trust metadata

### P3 Sandbox/self-modification
- Versioned mutation contract
- Digital-twin hardening
- Invariant matrix
- Resource/gas limits
- Multi-level mutation verification
- Controlled auto-merge

### P3 Agent spawning
- Spawn policy
- Versioned Bootstrap State Package
- Bootstrap verification
- Isolated child instance
- Parent/child lineage
- Genetic drift
- Spawn failure safety

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

A written test that was not executed is not PASS.

## SAFETY RULES

- External data is untrusted by default.
- No external adapter gets unrestricted Core access.
- No AI model inside Ψ-Core.
- No second state model may silently diverge from Core.
- Evolution remains evidence-backed and bounded.
- A trigger is not authorization.
- Replication of architecture is not replication of authority.
- Parent secrets/credentials are never inherited by child agents by default.
- Failed operations prefer `REJECT`, `QUARANTINE` or `FAIL_CLOSED`.
- Future autonomous mutation must never bypass invariant/evidence gates.

## FINAL SELF-EVOLUTION RULE

The last self-evolution gate remains closed while the evidence chain is incomplete. Preparation first: Core invariants, persistence/recovery, append-only audit evidence, candidate generation/testing, sandbox execution, shadow evaluation, invariant delta, governance/evidence thresholds, security, quarantine and recovery.

```text
Candidate
 ↓ Generate
 ↓ Test
 ↓ Sandbox execution
 ↓ Observed evidence
 ↓ Shadow evaluation
 ↓ Invariant delta
 ↓ Governance/evidence gate
 ↓ Promotion candidate
 ↓ ONLY THEN canonical mutation
```

## CONTEXT INTEGRITY

Update this file whenever a major architectural gate is completed or canonical HEAD changes materially. Never reconstruct current architecture from memory alone.

## HANDOFF NOTE — NEXT CLAUDE REVIEW

The repository is ready for an external Claude review after the current Reflection/Shadow/Invariant Delta fixes are staged. Claude must read this file first, inspect current `main` HEAD, and independently verify claims against code/tests/runtime evidence. It must not assume that this context file alone constitutes PASS evidence. In particular, Persistence is runtime-verified by the inspected CI above, while Reflection/Shadow/Invariant Delta remains IN_PROGRESS.
