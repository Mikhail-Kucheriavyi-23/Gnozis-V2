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

## PERSISTENCE HARDENING — IMPLEMENTATION REVIEW STATUS

The following gates have been implemented as contracts/tests or enforcement on `main`. They are **NOT DONE until actual runtime/CI evidence is inspected**:

- `GNV2-PERSIST-001` — TransitionRecord persistence integrity.
- `GNV2-PERSIST-002` — Rejected transition durable semantics.
- `GNV2-PERSIST-003` — Recovery/provenance verification.
- `GNV2-PERSIST-003A` — Canonical `transition_id` identity verification; verifier rejects tampered transition identity.
- `GNV2-PERSIST-003B` — Transition ↔ audit provenance linkage tests.
- `GNV2-PERSIST-004` — Transition replay/idempotency tests.
- `GNV2-PERSIST-005` — Crash/reopen consistency tests across transaction checkpoints.
- Audit tamper tests cover event payload, `event_hash`, and `prev_hash` corruption.

Test files created/modified by an agent are specifications until executed. Source inspection is not a PASS.

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

## CURRENT ACTIVE GATE — PERSISTENCE RUNTIME VERIFICATION

Before adding more Persistence mechanisms, execute and inspect the current suite and resolve actual failures. Required evidence:

1. valid transition identity accepted;
2. tampered transition identity rejected;
3. transition/audit linkage tampering rejected;
4. audit payload/hash/prev-hash tampering rejected;
5. identical transition replay idempotent;
6. conflicting replay rejected;
7. each transaction failure checkpoint survives close/reopen without partial commit;
8. post-commit failure preserves the fully committed transition;
9. `verify_durable_graph()` passes valid graphs and fails closed on corruption.

Relevant recent implementation/test commits include:

- `3dd8e28af2dad5f8ddd1a853ed6523366632e1ee` — canonical transition identity enforcement.
- `4fc368d523344f315c673ddca4705827c32e956b` — valid identity regression.
- `f1d154cc7778beaa5080b7abb46801341ab24300` — transition/audit linkage tests.
- `c7169e9c710784aec586e2470e13e6277c7c1749` — audit hash tamper tests.
- `95fb3594ba1112a62f3c664664c4e31ef8db7dc8` — replay/idempotency tests.
- `a16055671a427bcbb9766bd4d4f89e688fd04b66` — crash/reopen persistence tests.

These commit references document implementation progress only; they do not constitute runtime PASS evidence.

## NEXT GATE AFTER PERSISTENCE

If the Persistence gate obtains actual passing evidence, freeze Persistence and move to **Memory/Recovery architecture** without creating a second source of truth.

Memory must be derived from or anchored to durable Core history:

```text
Durable Core history
 ↓
verified recovery
 ↓
Memory reconstruction/cache
 ↓
operational context
```

Memory corruption must never silently override canonical persisted state.

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