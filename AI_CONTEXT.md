# Gnozis-V2 — AI Context

## 0. PURPOSE / OPERATING RULE

This file is the operational handoff for AI agents working on Gnozis-V2.

Repository:
- GitHub: Mikhail-Kucheriavyi-23/Gnozis-V2
- default branch: main
- current HEAD inspected historically; authoritative current main HEAD is recorded in Section 0A: 70e385702e66daa0cbb5934e30ab0e577181f959

Rules:
1. Repository code, tests and actual runtime/CI evidence outrank chat memory or this document.
2. This document is architecture/task context, not proof of PASS.
3. Never claim a test, CI run, artifact, recovery result or security property was verified unless it was actually executed/inspected.
4. Select exactly one highest-priority READY task at a time.
5. Do not broaden a task into unrelated architecture.
6. Preserve evidence: rejected, failed, quarantined and insufficient-evidence outcomes are historical data, not noise.
7. Never weaken an invariant, persistence constraint or evidence gate merely to make tests green.

## 0A. AUTHORITATIVE CONTEXT REFRESH — 2026-09-19

This section supersedes older HEAD/task-status statements in this file when they conflict.

CURRENT REPOSITORY STATE:
- Repository: Mikhail-Kucheriavyi-23/Gnozis-V2
- Current main HEAD verified from GitHub: 70e385702e66daa0cbb5934e30ab0e577181f959
- HEAD date: 2026-09-18 19:14:51 UTC
- Latest commit: `docs: record 2026-09-18 math closure and repository gaps`
- There are no repository commits dated 2026-09-19 in the inspected recent commit history; the 2026-09-19 work below is a mathematical/reverse-analysis continuation performed after the latest repository commit.
- A supplied external audit was performed against HEAD 7d40a9c91fd2e69736305141a71b62aeebb99461. GitHub comparison confirms current main is 546 commits ahead of that audit HEAD. Therefore the audit is historical architectural evidence, NOT current HEAD verification. Its observations must be revalidated before being converted into current implementation claims.

AUTHORITATIVE CURRENT TASK:
- The previously verified Reflection/Shadow gate is not to be reopened without regression evidence.
- The current research stage is formal reverse-analysis of the proof foundation and Genesis/trust-anchor model.
- Before assigning implementation work to another AI, finish the current minimal Proof/Authority dependency reverse, then update the task registry with exactly one READY implementation task.
- Do not implement speculative Genesis/meta-evolution while the dependency analysis remains unresolved.

CURRENT PROGRESS MODEL:
- Formal/architectural research maturity: approximately 96%.
- Runtime enforcement maturity: approximately 25%.
- Real runtime/CI verification must be reported separately from mathematical completion.
- These percentages are working analytical estimates, not measured software coverage.


## 1. ARCHITECTURAL PURPOSE

Gnozis-V2 is being developed as an autonomous recursive evolution system whose canonical state/evolution remains controlled by Ψ-Core.

Target evolution chain:

Core_n
  ↓
durable evidence
  ↓
Persistence / Recovery
  ↓
Reflection / RuleProposal
  ↓
bounded SandboxExecution
  ↓
real observations
  ↓
Shadow Evaluation
  ↓
Invariant Delta
  ↓
Governance / evidence threshold
  ↓
PromotionCandidate
  ↓
ONLY AFTER ALL GATES
Core_(n+1)

Canonical self-modification is NOT currently implemented.

## 2. NON-NEGOTIABLE ARCHITECTURAL PRINCIPLES

- Ψ-Core is the authoritative source of state/evolution semantics.
- No second state model may silently diverge from Core.
- No AI model belongs inside Ψ-Core.
- Reflection and diagnostics remain outside Core.
- External data is untrusted by default.
- External adapters do not receive unrestricted Core authority.
- Persistence is evidence, not a parallel state machine.
- Missing evidence must remain UNKNOWN / INSUFFICIENT_EVIDENCE.
- Rejection is valid historical evidence.
- Shadow evaluation must not activate or mutate canonical Core.
- A trigger is not authorization.
- Replication is not authority inheritance.
- Parent credentials/secrets are never inherited by child agents by default.
- Failed operations prefer REJECT, QUARANTINE or FAIL_CLOSED.
- Future autonomous mutation must never bypass invariant/evidence gates.

## 3. LAYER MODEL

L0 — Ψ-Core
- state
- candidate generation
- Test(candidate) -> bool
- selection
- protected invariants
- evolution semantics

L1 — Evidence / Persistence / Recovery
- SQLite durable history
- TransitionRecord
- canonical transition identity
- append-only audit events
- hash-chain evidence
- crash/reopen recovery

L2 — Reflection / RuleProposal
- persisted-history analysis
- diagnostic observations
- rule registry/metadata
- bounded RuleProposal generation

L3 — Shadow / Invariant Delta / Governance
- shadow execution/evaluation
- invariant comparison
- evidence classification
- governance classification

L4 — Evolution Sandbox
- hypothesis
- model generation
- bounded experiment
- observed evidence
- evaluator
- promotion candidate

L5 — Canonical promotion
- NOT IMPLEMENTED
- remains closed until all downstream gates are independently verified

## 4. VERIFIED PERSISTENCE BASELINE

The following persistence gates have received inspected runtime/CI evidence on the development line and are frozen unless new regression evidence appears:

- GNV2-PERSIST-001 — TransitionRecord persistence integrity — VERIFIED
- GNV2-PERSIST-002 — rejected transition durable semantics — VERIFIED
- GNV2-PERSIST-003 — recovery/provenance verification — VERIFIED
- GNV2-PERSIST-003A — canonical transition_id identity / tamper rejection — VERIFIED
- GNV2-PERSIST-003B — transition ↔ audit provenance linkage / tamper detection — VERIFIED
- GNV2-PERSIST-004 — transition replay/idempotency — VERIFIED
- GNV2-PERSIST-005 — crash/reopen consistency across transaction checkpoints — VERIFIED
- audit tamper coverage for event payload, event_hash and prev_hash — VERIFIED

Inspected historical CI evidence:
- run 35275548474
- commit 5591af042d31500b323e3bbf7d74cceae2268b70
- persistence-related tests passed
- overall run was NOT green because Reflection/Shadow/Diagnostic failures remained

Do not reopen these gates without a concrete regression.

Persistence chain:

Candidate
 ↓
protected invariants
 ↓
Test → TransitionRecord
 ↓
canonical transition_id
 ↓
SQLite transition
 ↓
audit transition_id
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

Rejected transitions are historical evidence and MUST NOT advance current_state_id.

## 5. CURRENT DEVELOPMENT HEAD

Current inspected HEAD:
63e1f0b57c591a06fa902fe63cd84369c30bf65c

Recent commits immediately preceding/current development include:

- 63e1f0b5 — test: persist invariant delta under a real reflection report
- ce51f0ab — test: align reflection observations with rejection evidence
- f4a9fb3c — test: verify diagnostic provenance at observation level
- 457c6d94 — core: preserve protected invariant reasons through select rejection
- 78fff04a — test: align invariant shadow predicates with strict bool contract

Earlier relevant progress:
- 090ec5bb — align rule-provenance test with strict Test(candidate)->bool contract
- 72e959f5 — align diagnostic artifact test fixture with machine-readable report contract
- 5591af04 — diagnostic corpus fixture uses valid monotonic Core versions

These commits show active correction of the Reflection/Shadow gate. They do NOT by themselves constitute runtime PASS.

## 6. CURRENT ACTIVE GATE

### GNV2-REFLECTION-GATE

STATUS: IN_PROGRESS

PRIORITY: P1

OBJECTIVE:
Complete and verify the existing Reflection / Shadow / Invariant Delta / Diagnostic evidence chain without weakening Core or Persistence.

This is currently the maximum justified integrated task because it closes the remaining evidence-processing layer before any autonomous canonical evolution work.

Required vertical path:

real Core execution
 ↓
TransitionRecord
 ↓
SQLite persistence
 ↓
recovery/history
 ↓
Reflection
 ↓
Shadow Evaluation
 ↓
Invariant Delta
 ↓
Diagnostic Artifact
 ↓
inspectable evidence

Current work must reconcile the implementation with the following semantic contracts.

### 6.1 Diagnostic Artifact

The artifact must retain complete machine-readable evidence.

Do not delete findings merely to satisfy an old test shape.

If findings are represented through causal_candidates or another canonical structure, determine whether the test contract is stale or whether serialization loses information.

Acceptance:
- no diagnostic evidence is silently dropped
- provenance is traceable to actual execution/history
- artifact structure is internally consistent

### 6.2 Invariant Delta

Target semantics:

missing candidate/state
or insufficient evidence
    → UNKNOWN / INSUFFICIENT_EVIDENCE

verified violation introduced or increased
    → VIOLATION

verified violation reduced
    → IMPROVED

verified preservation with sufficient evidence
    → PRESERVED

Critical rule:
An empty violation set is NOT proof of PRESERVED when the underlying state/invariant evidence is missing.

### 6.3 Invariant Delta Persistence

Persisted Delta records must reference a real persisted reflection report.

Do NOT:
- disable foreign keys
- fabricate report IDs
- create a parallel evidence database
- bypass normal persistence

The correct flow is:
real reflection execution → persisted report → persisted delta linked to that report.

### 6.4 Protected Invariant Rejection

Protected invariant rejection is correct behavior.

The diagnostic reason must survive:

TestResult.reasons
    →
selection/rejection
    →
TransitionRecord.reason
    →
persisted history
    →
Reflection evidence

Do not replace a real rejection with a generic success/failure label.

### 6.5 Reflection Observations

If rejected-transition evidence creates an additional observation, preserve it.

The previous expectation of 4 observations was identified as potentially stale; current commits explicitly align observations with rejection evidence.

Never delete a real observation solely to satisfy an old count.

### 6.6 Shadow Evaluation

Target semantics:

active rejected → shadow accepted
    → improvement + behavioral change

active accepted → shadow rejected
    → regression + behavioral change

same acceptance outcome
    → no improvement/regression

both rejected but rejection reason changes
    → changed diagnostic behavior only
    → NOT automatically improvement

Acceptance outcome must be based on actual execution, not caller-supplied scores.

### 6.7 Diagnostic Execution

Diagnostics must use persisted/recovered history.

Forbidden shortcuts:
- fresh empty Engine as a substitute for history
- synthetic observations
- caller-supplied evaluation scores treated as evidence
- fabricated invariant results
- fabricated transition records
- bypassing persistence

## 7. TEST / CI RULE

Relevant test areas:

- tests/test_diagnostic_artifact.py
- tests/test_diagnostic_corpus.py
- tests/test_diagnostic_execution.py
- tests/test_invariant_delta.py
- tests/test_invariant_delta_persistence.py
- tests/test_invariants.py
- tests/test_protected_invariant_gate.py
- tests/test_reflection_counterexample.py
- tests/test_reflection_foundation.py
- tests/test_reflection_history.py
- tests/test_reflection_rule_registry.py
- tests/test_reflection_shadow.py
- tests/test_shadow_adapter.py

Then execute the COMPLETE pytest suite.

A written test that was not executed is not PASS.

CI:
- inspect the workflow result for the resulting commit
- no current workflow result was found for HEAD 63e1f0b5 at the time this context was updated
- therefore current HEAD must NOT be described as CI-green

## 8. TASK-BLOCK PROTOCOL

Every AI agent must:

1. Read this complete file.
2. Reconcile current main HEAD.
3. Inspect relevant implementation and tests.
4. Determine dependency state.
5. Select exactly one highest-priority READY task.
6. Implement only that task and necessary corrections.
7. Execute relevant tests.
8. Execute/inspect CI when available.
9. Record actual evidence.
10. Mark DONE only when acceptance evidence exists.
11. Otherwise use IN_PROGRESS or BLOCKED.
12. Stop and hand off instead of jumping to unrelated capabilities.

Required fields:

TASK-ID
BLOCK
STATUS
PRIORITY
DEPENDS_ON
OBJECTIVE
SCOPE
DO_NOT_CHANGE
REQUIRED_TESTS
ACCEPTANCE
AUDIT
NEXT

Statuses:
PLANNED / READY / IN_PROGRESS / DONE / BLOCKED / REJECTED

Priority:
P0 = architectural/security blocker
P1 = foundation
P2 = subsystem
P3 = advanced
P4 = refinement

## 9. CURRENT TASK REGISTRY

### GNV2-REFLECTION-GATE
BLOCK: Reflection / Shadow / Invariant Delta / Diagnostic Evidence
STATUS: IN_PROGRESS
PRIORITY: P1
DEPENDS_ON:
- Persistence gates verified
- durable provenance verified
- recovery verified

OBJECTIVE:
Close the full evidence-processing vertical slice.

SCOPE:
- diagnostic artifact contract
- invariant delta semantics
- invariant delta persistence
- protected rejection reason propagation
- reflection observation provenance
- shadow acceptance semantics
- diagnostic execution provenance
- complete runtime/CI verification

DO_NOT_CHANGE:
- Ψ-Core authority semantics
- protected invariants
- SQLite foreign-key guarantees
- append-only audit semantics
- canonical transition identity
- recovery semantics
- evidence-gate semantics
- autonomous canonical promotion
- bridge/memory/agent architecture

REQUIRED_TESTS:
all relevant Reflection/Shadow/Invariant Delta tests + full pytest + CI inspection

ACCEPTANCE:
- relevant tests pass
- complete suite passes
- CI evidence inspected
- no persistence regression
- no invariant weakening
- unknown remains unknown when evidence is insufficient
- shadow semantics are correct
- diagnostic evidence is real and traceable

AUDIT:
Classify each failure before modifying code:
- stale test contract
- production defect
- fixture/integration defect
- missing evidence
- architectural contradiction

NEXT:
Freeze the gate after verified green evidence, then select exactly one dependency-satisfied next task.

## 10. AFTER REFLECTION GATE

The next architectural work must be selected from evidence-backed dependencies.

Priority order:

P1:
- complete sandbox execution → evaluator → shadow → invariant delta vertical slice
- verify PromotionCandidate without canonical mutation
- security/evidence gates for experimental evolution

P2:
- independent audit/state observer
- red-team/self-attack engine
- anomaly classification
- branch quarantine
- external ingestion contract
- ingress sanitization
- semantic transducer
- provenance/trust metadata

P3:
- versioned mutation contract
- digital-twin hardening
- invariant matrix
- resource/gas limits
- multi-level mutation verification
- controlled auto-merge
- agent spawning / bootstrap verification / lineage / drift / failure safety

Canonical promotion remains closed until the entire evidence chain is independently verified.

## 11. EVOLUTION SANDBOX CONTRACT

Target:

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

Requirements:
- bounded execution
- real observations
- reproducible evidence
- no caller-supplied success scores as proof
- no canonical Core mutation
- no unrestricted network or authority
- no hidden side channels
- failed experiments remain inspectable

## 12. GOVERNANCE CONTRACT

Governance is classification, not an autonomous authority source.

Allowed classifications:

BLOCK
HOLD
REVIEW
NO_CHANGE

Governance metadata does not itself authorize Core mutation.

Authority metadata is provenance.

Promotion is only possible after all required evidence/security gates.

## 13. FUTURE MEMORY / RECOVERY

Memory must never become a second source of truth.

Correct model:

Durable Core history
 ↓
verified recovery
 ↓
memory reconstruction/cache
 ↓
operational context

Memory may accelerate recovery and context access, but canonical state remains grounded in durable Core history.

## 14. FUTURE BRIDGE / AGENTS / NETWORK

These capabilities are future architecture, not current proof of autonomy:

- protected user interaction bridge
- internet/world-learning ingress
- encrypted persistent memory
- isolated workspace
- multi-agent instances
- connected Gnozis network/federation
- parent/child lineage
- agent capability generation

Any external interface must be treated as untrusted and capability-limited.

No bridge may bypass Core invariants.
No child agent automatically inherits parent authority or secrets.
Network connectivity must not become a hidden authority channel.

## 15. PROVENANCE / RESEARCH INTEGRITY

Gnozis architecture and Ψ lineage must remain distinguishable from external projects and references.

External projects may be used as comparison/control points, but their architecture, provenance or claims must not be presented as originating from Gnozis.

Document:
- source
- date/version
- exact borrowed concept if any
- adaptation
- independent Gnozis contribution

## 16. SECURITY / FAILURE RULES

- external input = untrusted
- secrets = never persisted in plaintext unless explicitly required and protected
- evidence tampering = detectable
- missing evidence = fail closed / unknown
- invalid lineage = reject
- invalid provenance = reject or quarantine
- sandbox escape = fail closed
- unauthorized mutation = reject
- failed experiment = preserve evidence
- recovery mismatch = stop and investigate
- silence/non-response is not success

## 17. COMPLETION EVIDENCE FORMAT

For every completed task record:

Task ID:
Status:
Implementation:
Files changed:
Tests added/changed:
Tests actually executed:
Observed result:
CI run / commit:
Known limitations:
New dependencies discovered:
Adversarial checks:
Next task:

Never write “verified” without evidence.

## 18. FINAL SELF-EVOLUTION RULE

The canonical self-evolution gate is CLOSED.

The following chain must be proven before canonical mutation:

Candidate
 ↓ Generate
 ↓ Test
 ↓ Sandbox execution
 ↓ observed evidence
 ↓ Shadow evaluation
 ↓ Invariant delta
 ↓ Governance/evidence gate
 ↓ PromotionCandidate
 ↓ security/quarantine/recovery gates
 ↓ ONLY THEN canonical mutation

A promotion candidate is not a Core mutation.

A successful sandbox experiment is not autonomous evolution.

A passing unit test is not complete architectural verification.

CI-green is necessary evidence for the relevant gate, but does not replace adversarial architectural review.

## 19. HANDOFF

Current handoff:
- GNV2-EVOLUTION-SANDBOX-002: VERIFIED by CI (192 passed, 10 warnings).
- Persistence: VERIFIED on inspected historical CI; frozen.
- Reflection/Shadow/Invariant Delta: implementation gate completed for the currently identified failures.
- Current HEAD: f759746a2413d28bcac2942ce87eac5516b2a00d.
- CI run 35289252757: SUCCESS; Python 3.11 and 3.12 jobs passed.
- Executed suite result from CI: 185 passed, 10 warnings.
- Self-Diagnostic run 35289252756: SUCCESS.
- The last active Reflection/Shadow failure was classified as a stale test usage: `default_test` is a protected Core verifier requiring the parent/current state, while `evaluate_shadow()` is a policy-comparison API. The regression test now supplies an explicit active policy predicate rather than misusing the Core verifier as a shadow policy.
- Current maximum task GNV2-REFLECTION-GATE is now VERIFIED by CI evidence for this development line.
- Do not reopen verified persistence or reflection gates without new regression evidence.
- Do not start canonical self-evolution.
- Do not add OpenRouter, bot infrastructure, or unrelated external-agent orchestration to this gate.
- Next work must select exactly one dependency-satisfied READY task from the post-Reflection sequence.

## 19A. CURRENT EVOLUTION EVIDENCE SLICE

The first bounded evolution evidence slice is now implemented outside Core.

Implementation commits:
- c40a9d6d2c18d14d9060398bb6f14794797774bd
- bee676de71c96d954900e12e85f53f297a88993e

Added:
- gnosis/evolution/__init__.py
- gnosis/evolution/sandbox.py
- gnosis/evolution/evaluator.py
- gnosis/evolution/promotion.py
- tests/test_evolution_sandbox.py

Properties:
- sandbox input is State + Candidate only
- stale parent is rejected
- sandbox is bounded to <=20 configured operations
- observer failures become FAILED evidence and do not pass evaluation
- observations receive a deterministic evidence digest
- evaluator refuses to claim PASS for unknown policy identifiers
- PromotionCandidate is immutable evidence packaging only
- PromotionCandidate.can_activate is always False
- no Engine, persistence handle, activation API or canonical mutation path is exposed

Important limitation:
- This is the first bounded evidence slice, not a full OS/process/network sandbox.
- The current budget charges one gas/operation per worker invocation; finer-grained internal gas accounting remains a later gate.
- Evaluator semantics are intentionally minimal and do not yet constitute scientific/task-specific validation.
- PromotionCandidate is not an authorization mechanism.

CI evidence:
- CI run 35289454476: SUCCESS
- Python 3.11: SUCCESS
- Python 3.12: SUCCESS
- executed suite: 190 passed, 10 warnings
- Self-Diagnostic run 35289454521: SUCCESS

Status:
- GNV2-REFLECTION-GATE: VERIFIED
- GNV2-EVOLUTION-EVIDENCE-001: VERIFIED for this bounded slice
- Full autonomous/canonical evolution: CLOSED

Sandbox-002 implementation is now VERIFIED by CI:
- child-process execution boundary
- one-operation gas charge per invocation, hard maximum 20
- explicit positive wall-clock timeout
- timeout terminates the worker and fails closed
- worker failure/exception becomes FAILED evidence
- Core authority remains outside the worker contract

Next gate after CI verification:
GNV2-EVOLUTION-PROVENANCE-003
- persist execution evidence
- link sandbox digest to Reflection/Promotion provenance
- add tamper/mismatch detection
- keep canonical promotion closed

## 20. CONTEXT INTEGRITY

Update this file whenever:
- a major gate changes status
- canonical HEAD changes materially
- test/CI evidence changes the verified state
- a task is completed/blocked/rejected
- architecture changes

Do not maintain historical claims that are contradicted by current repository/runtime evidence.

### GNV2-EVOLUTION-PROVENANCE-003

Implementation status: **VERIFIED by CI**.

Cross-check extension:
- `ProvenanceCrossCheck` verifies candidate, parent state, evidence digest, execution identity, evaluation, shadow, invariant and governance links.
- stored provenance can be re-validated against observations.
- mismatched chain or tampered observations fail closed.
- CI run 35289996129 SUCCESS; Python 3.11 and 3.12 SUCCESS; 198 passed, 10 warnings.
- Self-Diagnostic run 35289996076 SUCCESS.

CI evidence: run 35289871794 SUCCESS; Python 3.11 and 3.12 SUCCESS; 195 passed, 10 warnings; Self-Diagnostic run 35289865670 SUCCESS.

Added:
- tamper-evident canonical evidence digest verification
- immutable `EvidenceProvenance`
- deterministic execution/provenance IDs
- rejection of mismatched observations/evidence digests
- SQLite `evolution_provenance` persistence
- load/list persistence accessors
- regression test for persistence round-trip

Security boundary:
- provenance records evidence and decisions as metadata
- persistence does not authorize activation
- `PromotionCandidate.can_activate` remains false
- canonical Core state remains untouched

Next step after CI:
- verify full pipeline evidence linkage from sandbox digest through evaluation/shadow/invariant/governance
- then add explicit cross-record consistency/tamper checks
- keep canonical promotion closed

### GNV2-EVOLUTION-PROMOTION-GATE-005

Implementation status: **VERIFIED by CI**.

CI evidence: run 35290236269 SUCCESS; Python 3.11 and 3.12 SUCCESS; 201 passed, 10 warnings.

Added a non-authoritative PromotionGate:
- validates provenance cross-check status
- requires evaluation PASS
- accepts only defined shadow statuses
- requires invariant PRESERVED/IMPROVED
- requires governance REVIEW/APPROVE
- returns REVIEW_ONLY
- `PromotionGate.can_activate` is always false
- `PromotionCandidate.can_activate` remains false
- no canonical Core mutation or activation path exists
- regression tests cover eligible, provenance-failure and unsafe-status cases

This gate is an eligibility/proof boundary, not an authorization boundary.


### GNV2-EVOLUTION-REPLAY-006

Implementation status: **VERIFIED by CI**.

CI evidence: run 35290463846 SUCCESS; Python 3.11 and 3.12 SUCCESS; 204 passed, 10 warnings.

Added:
- deterministic replay of recorded evidence without re-executing or activating a candidate
- digest recomputation against recorded observations
- replay identity check for candidate and parent state
- fail-closed mismatch reporting
- regression tests for intact, tampered and identity-mismatched evidence

Replay is verification only. It has no Core mutation or activation authority.


### GNV2-EVOLUTION-AUDIT-007

Implementation status: **VERIFIED by CI**.

CI evidence: run 35290723629 SUCCESS; Python 3.11 and 3.12 SUCCESS; 206 passed, 10 warnings. Self-Diagnostic 35290719190 SUCCESS.

Added:
- append-only evolution audit records
- monotonic sequence numbers
- chained previous/record SHA-256 digests
- SQLite persistence for the audit chain
- chain verification with fail-closed mismatch reasons
- regression tests for intact and tampered chains

Audit records are evidence/history only and have no Core mutation or activation authority.


### GNV2-EVOLUTION-RECOVERY-008

Implementation status: **VERIFIED by CI**.

CI evidence: run 35290870078 SUCCESS; Python 3.11 and 3.12 SUCCESS; 208 passed, 10 warnings. Self-Diagnostic 35290865148 SUCCESS.

Added:
- durable SQLite recovery of the evolution audit chain
- reconstruction from persisted records only
- chain verification after recovery
- explicit recovery report with record count and fail-closed reasons
- regression tests for intact persistence and persisted tampering

Recovery does not trust process memory and has no Core mutation or activation authority.


### GNV2-EVOLUTION-TRANSACTION-009

Implementation status: **VERIFIED by CI**.

CI evidence: run 35291113894 SUCCESS; Python 3.11 and 3.12 SUCCESS; 210 passed, 10 warnings. Initial CI exposed a circular import and a test-double misuse; both were corrected before verification.

Added:
- atomic SQLite transaction for evolution provenance + audit event
- BEGIN IMMEDIATE / COMMIT boundary when the caller is not already in a transaction
- rollback of both records on any persistence failure
- result object linking provenance_id to its audit record
- regression tests for atomic success and simulated audit-write failure

This is persistence atomicity only; it does not grant activation authority.


### GNV2-EVOLUTION-STATE-BINDING-010

Implementation status: **VERIFIED by CI**.

CI evidence: run 35291486930 SUCCESS; Python 3.11 and 3.12 SUCCESS; 211 passed, 10 warnings. Diagnostic runs 35291486739 and 35291483411 SUCCESS. Prior CI failures exposed and corrected sandbox constructor, SQL placeholder, and state-digest argument compatibility defects.

Added state binding to evolution provenance/execution:
- parent state content digest
- proposed state content digest
- execution identity includes both state digests
- provenance identity includes both state digests
- persisted provenance stores both digests
- sandbox execution records both digests
- replay identity verifies both digests
- regression test rejects parent-state digest tampering

This binds evolution evidence to the concrete parent/proposed state content while preserving REVIEW_ONLY / no activation authority.


### GNV2-EVOLUTION-CANDIDATE-BINDING-011

Implementation status: **VERIFIED by CI**.

CI evidence: run 35291655890 SUCCESS; Python 3.11 and 3.12 SUCCESS; 213 passed, 10 warnings.

Candidate identity is strengthened to bind:
- parent state identity
- proposed state content identity
- origin
- deterministic seed

A separate candidate binding digest additionally binds the concrete parent state content digest. This composes with the state-bound provenance contract without granting activation authority.

Regression tests cover origin, seed, proposed-content and parent-digest tampering.


### GNV2-EVOLUTION-REPLAY-COMPLETENESS-012

Implementation status: **VERIFIED by CI**.

CI evidence: run 35291797877 SUCCESS; Python 3.11 and 3.12 SUCCESS; 215 passed, 10 warnings. Initial complete-replay tests exposed contract mismatches; corrected and reverified.

Added a fail-closed complete replay contract requiring:
- execution identity
- parent/proposed state binding
- evidence digest verification
- provenance presence and cross-check
- audit record presence and candidate/execution identity binding

Missing provenance or audit evidence can never produce a reproducible/valid result.


### GNV2-EVOLUTION-AUDIT-CONTINUITY-013

Implementation status: **VERIFIED by CI**.

CI evidence: run 35292034036 SUCCESS; Python 3.11 and 3.12 SUCCESS; 216 passed, 10 warnings. Compatibility failures from prior runs were corrected before final verification.

Audit records now bind to:
- provenance_id
- parent_state_digest
- proposed_state_digest
- evidence_digest
- candidate_id
- execution identity

Complete replay verifies these links and fails closed on mismatch. Persistence schemas and atomic transaction storage were extended accordingly.


### GNV2-EVOLUTION-RECOVERY-INTEGRITY-014

Implementation status: **VERIFIED by CI**.

CI evidence: run 35292194762 SUCCESS; Python 3.11 and 3.12 SUCCESS; 218 passed, 10 warnings.

Added recovery integrity regression coverage:
- evolution provenance survives database serialization/reopen;
- audit record continuity survives persistence recovery;
- persisted audit tampering is detected by record-digest verification;
- recovered audit chain remains append-only/verifiable.


### GNV2-EVOLUTION-ATOMIC-COMMIT-015

Implementation status: **VERIFIED by CI**.

CI evidence: run 35292400779 SUCCESS; Python 3.11 and 3.12 SUCCESS; 221 passed, 10 warnings. Initial CI exposed SQLite nested-transaction and audit-failure test defects; the implementation and tests were corrected before final verification.

Evolution persistence now uses:
- one transaction when it owns the connection transaction;
- a SAVEPOINT when called inside an existing transaction;
- explicit post-write verification that provenance and audit are mutually linked;
- rollback of the complete evolution unit on failure;
- preservation of the caller's outer transaction when nested.

Regression tests cover audit-side failure, duplicate provenance failure, nested success, and nested failure isolation.


### GNV2-EVOLUTION-PROVENANCE-AUDIT-CROSSCHECK-016

Implementation status: **VERIFIED by CI**.

CI evidence: run 35292667700 SUCCESS; Python 3.11 and 3.12 SUCCESS; 222 passed, 10 warnings.

Added one fail-closed cross-check covering:
- candidate_id
- execution_id
- parent_state_digest
- proposed_state_digest
- evidence_digest
- provenance_id
- audit record digest integrity

Complete replay now invokes this unified persisted-link check when both provenance and audit are present.


### GNV2-EVOLUTION-CHAIN-VERIFIER-017

Implementation status: **VERIFIED by CI**.

CI evidence: run 35293106084 SUCCESS; Python 3.11 and 3.12 SUCCESS; 225 passed, 10 warnings.

Added an independent, read-only persisted-chain verifier. It accepts plain provenance/audit mappings plus observations and does not depend on live evolution, transaction, or runtime execution objects. It verifies provenance identity/evidence, the complete audit hash chain, and provenance↔audit linkage, failing closed on malformed or incomplete persistence.


### GNV2-EVOLUTION-RECOVERY-GATE-018

Implementation status: **VERIFIED by CI**.

CI evidence: run 35293291038 SUCCESS; Python 3.11 and 3.12 SUCCESS; 226 passed, 10 warnings.

Recovery now fails closed unless:
- a provenance identity is explicitly supplied;
- the persisted provenance record exists;
- observations are supplied for evidence verification;
- the independent persisted-chain verifier accepts provenance, audit chain, and cross-links.

The old audit-only recovery path is no longer trusted recovery.


### GNV2-EVOLUTION-RECOVERY-REPLAY-019

Implementation status: **VERIFIED by CI**.

CI evidence: run 35293773495 SUCCESS; Python 3.11 and 3.12 SUCCESS; 227 passed, 10 warnings.

Recovery now closes the persistence→verification→replay loop by recomputing the canonical evidence digest from recovered observations and requiring equality with persisted provenance evidence. The recovery report exposes expected/actual digests and a separate replay_valid gate. Changed observations fail closed.


### GNV2-EVOLUTION-RECOVERY-STATE-IDENTITY-020

Implementation status: **VERIFIED by CI**.

CI evidence: run 35293979611 SUCCESS; Python 3.11 and 3.12 SUCCESS; 228 passed, 10 warnings.

Recovery replay now revalidates persisted provenance identity fields against recovered observations and persisted evidence, not only the evidence digest. A tampered proposed-state digest is explicitly rejected during recovery replay.


### GNV2-EVOLUTION-CANONICAL-IDENTITY-021

Implementation status: **VERIFIED by CI**.

CI evidence: run 35294179445 SUCCESS; Python 3.11 and 3.12 SUCCESS; 229 passed, 10 warnings.

Added deterministic `evolution_identity` covering candidate, execution, parent/proposed state identity, evidence, evaluation/shadow/invariant/governance status, and provenance identity. Persistence stores the identity; the independent chain verifier rejects a supplied persisted identity mismatch.


### GNV2-EVOLUTION-RECOVERY-CANONICAL-IDENTITY-022

Implementation status: **VERIFIED by CI**.

CI evidence: run 35294497370 SUCCESS; Python 3.11 and 3.12 SUCCESS; 230 passed, 10 warnings.

Recovery now reconstructs the persisted EvidenceProvenance and compares its canonical `evolution_identity` with the persisted identity. Tampering the canonical identity fails recovery replay closed.


### GNV2-EVOLUTION-PERSISTENCE-IDENTITY-MIGRATION-023

Implementation status: **VERIFIED by CI**.

CI evidence: run 35294963878 SUCCESS; Python 3.11 and 3.12 SUCCESS; 231 passed, 10 warnings.

Legacy persisted provenance with empty/missing `evolution_identity` is explicitly classified as `legacy_unverified` and recovery fails closed. No silent identity generation or automatic upgrade is permitted.


### GNV2-EVOLUTION-STATE-CONTENT-BINDING-024

Implementation status: **VERIFIED by CI**.

CI evidence: run 35295419236 SUCCESS; Python 3.11 and 3.12 SUCCESS; 233 passed, 10 warnings.

Provenance now carries `proposed_state_content_id` as an explicit content-binding field. The canonical evolution identity includes it; persistence migrates/stores it; independent chain verification and recovery reconstruct and verify it; a regression test rejects tampering. Legacy records default to an empty binding and remain subject to the existing legacy fail-closed policy.


### GNV2-EVOLUTION-STATE-CONTENT-IDENTITY-025 — VERIFIED

CI evidence: runs 35295152230 / 35295152199 SUCCESS on Python 3.11 and 3.12; diagnostic suite reports 57 passed, 3 warnings. Canonical `State.content_id` remains the single content identity; no second state identity model was introduced.


### GNV2-EVOLUTION-STATE-CONTENT-RECONCILIATION-026

Implementation status: **VERIFIED by CI**.

CI evidence: run 35295966630 SUCCESS; Python 3.11 and 3.12 SUCCESS.

Trusted recovery now requires the recovered/provided `State` and independently recomputes `State.content_id`, comparing it to persisted `proposed_state_content_id`. A missing proposed state fails closed. Recovery tests were updated to exercise actual State content reconciliation and tampering remains rejected.


### GNV2-EVOLUTION-STATE-PROVENANCE-LINK-027

Implementation status: **VERIFIED by CI**.

CI evidence: run 35296130140 SUCCESS; Python 3.11 and 3.12 SUCCESS; 234 passed, 10 warnings.

The existing `Candidate.binding_digest(parent_state_digest)` is now elevated into persisted provenance as `candidate_binding_digest`. Provenance identity includes the binding; persistence stores/migrates it; chain verification and recovery reconstruct it. New provenance requires a non-empty candidate binding digest, preventing a proposed state/content identity from being trusted without an explicit parent→candidate→proposed-state transition binding.


### GNV2-EVOLUTION-ATOMIC-PERSISTENCE-028

Implementation status: **IMPLEMENTED — final nested replay test expectation corrected; awaiting CI verification.**

CI run 35296606394: 235 passed, 1 failed. The remaining failure was the nested SAVEPOINT replay test still expecting SQLite IntegrityError; production correctly raises the new semantic RuntimeError. Updated that stale expectation. Both failures were pre-030 tests expecting SQLite IntegrityError for a conflicting replay. The new semantic idempotency contract correctly raises RuntimeError and leaves the chain unchanged. Test expectations were updated; no production rollback/idempotency logic was weakened.

Audited the existing `persist_evolution_transaction()` and retained its existing BEGIN IMMEDIATE / SAVEPOINT model. Fixed the transaction writer so canonical provenance fields (`evolution_identity`, `proposed_state_content_id`, `candidate_binding_digest`) are persisted atomically with the audit record. Existing rollback and nested-savepoint tests remain the primary atomicity gates; a regression assertion verifies the canonical fields survive the atomic write.


### GNV2-EVOLUTION-IDEMPOTENCY-029

Implementation status: **VERIFIED by CI**.

CI evidence: run 35296286746 SUCCESS; Python 3.11 and 3.12 SUCCESS; 234 passed, 10 warnings.

The atomic transaction writer now re-reads the persisted provenance inside the same transaction and verifies execution_id, evolution_identity, proposed_state_content_id, and candidate_binding_digest before COMMIT/RELEASE. A mismatch raises and rolls back the transaction. This is the first half of replay/idempotency hardening; duplicate-key rejection remains the existing boundary for repeated provenance_id submissions.


### GNV2-EVOLUTION-AUDIT-IDEMPOTENCY-030

Implementation status: **VERIFIED by CI**.

CI evidence: run 35296869203 SUCCESS; Python 3.11 and 3.12 SUCCESS.

`persist_evolution_transaction()` now treats an exact replay of the same provenance + event type + payload digest as idempotent: it returns the existing audit record without appending a new sequence. A conflicting replay with the same provenance identity but different audit semantics fails closed and leaves the existing audit chain unchanged. This preserves distinct records for genuinely new provenance while preventing retry-driven duplicate history.


### GNV2-EXECUTION-AUTHORIZATION-GATE-031

Implementation status: **VERIFIED by CI**.

CI evidence: run 35297620989 SUCCESS; Python 3.11 and 3.12 SUCCESS.

CI run 35297545942: 238 passed, 1 failed. The final remaining failure was the missing-authorization assertion still expecting the pre-binding error text. Updated it to the unified fail-closed mismatch contract. Production `require_execution_authorization()` is correctly the exact-binding API. The failures were test calls still using the pre-032 signature / message. Updated tests to pass both binding arguments and assert the current fail-closed mismatch contract.

Run 35297369166: 237 passed, 2 failed. Both failures were caused by a duplicate legacy `require_execution_authorization(auth)` definition shadowing the new exact-binding signature. Production intent was correct; the stale duplicate has been removed.

The existing authority boundary is now explicit about execution: `ExecutionAuthorization` is a fail-closed marker, and `require_execution_authorization()` rejects missing authorization, non-owner-approved authorization, or authorization without provenance. This does not grant authority to promotion or Core Engine; it establishes the execution boundary that future activation code must call. No autonomous path is enabled by this change.


### GNV2-EXECUTION-AUTHORIZATION-BINDING-032

Implementation status: **VERIFIED by CI**.

CI evidence: run 35297775009 SUCCESS; Python 3.11 and 3.12 SUCCESS.

`ExecutionAuthorization` is now bound to both `request_provenance` and the exact `evolution_identity`. `require_execution_authorization()` requires an exact match and fails closed on missing, unapproved, empty, or mismatched authorization. This remains a boundary-only capability; no Core promotion or autonomous execution path is enabled by this change.


### GNV2-EXECUTION-INTENT-SNAPSHOT-033

Implementation status: **VERIFIED by CI**.

CI evidence: run 35297917002 SUCCESS.

Added `ExecutionIntentSnapshot`, a frozen identity snapshot containing provenance_id, execution_id, evolution_identity, candidate_binding_digest, and proposed_state_content_id. `require_execution_intent_snapshot()` fails closed unless the snapshot exactly matches the current provenance. This is a boundary primitive only; it is not yet wired to autonomous execution or Core mutation.


### GNV2-EXECUTION-INTENT-FRESHNESS-034

Implementation status: **IMPLEMENTED — CI exposed a missing test import; corrected. Awaiting CI verification.**

CI run 35298070747: 244 passed, 2 failed. Both failures were NameError in the new tests because `ExecutionCommitRequest` was not imported. Production gate was not implicated. Added the missing import.

`ExecutionIntentSnapshot` now includes `parent_state_id` and `parent_state_digest`, binding the authorization snapshot to the exact parent state from which the evolution was derived. A changed parent state identity or digest therefore invalidates the snapshot through the existing fail-closed match check. No global clock or second state model is introduced.


### GNV2-EXECUTION-COMMIT-GATE-035

Implementation status: **VERIFIED by CI**.

CI evidence: run 35328181440 SUCCESS.

Added `ExecutionCommitRequest` and `require_execution_commit()` as a composed pre-commit gate. It requires exact authorization binding, exact evolution identity agreement with the immutable intent snapshot, and current provenance/snapshot equality. The gate itself performs no mutation and grants no autonomous authority; it is a fail-closed precondition for a future executor.


### GNV2-EXECUTION-RECEIPT-036

Implementation status: **VERIFIED by CI**.

CI evidence: run 35330847196 SUCCESS.

Added immutable `ExecutionReceipt` as post-commit evidence. It contains execution_id, provenance_id, evolution_identity, parent_state_digest, resulting_state_digest, and candidate_binding_digest. `ExecutionReceipt.after_commit()` requires the full pre-commit gate and a non-empty resulting-state digest; `require_execution_receipt()` rejects missing or cross-bound receipts. The receipt does not itself mutate state or grant authority; it records a result only after the caller supplies the committed result digest.


### GNV2-RESULTING-STATE-DIGEST-BINDING-037

Implementation status: **IMPLEMENTED — awaiting CI verification**.

`ExecutionReceipt.after_commit()` no longer accepts a caller-asserted result digest. It receives resulting state content, computes the canonical SHA-256 digest internally, and rejects the result unless that digest equals the evolution's authorized `proposed_state_digest`. Added tests for valid content, missing result state, and tampered result content. This still does not perform persistence itself; it establishes the evidence-binding contract for the future commit/storage boundary.


### GNV2-ACTUAL-COMMIT-ADAPTER-038

Implementation status: **IMPLEMENTED — awaiting CI verification**.

Added `SQLiteExecutionCommitAdapter` as a narrow persistence boundary. It calls the complete execution commit gate before `persist_transition()`, performs no authorization of its own, reloads the persisted resulting state, verifies its actual `state_id` equals the authorized proposed-state digest, and only then creates `ExecutionReceipt`. Added integration coverage for successful durable commit/receipt creation and fail-closed rejection before mutation. Existing SQLite persistence remains the source of truth; no second persistence model was introduced.


### GNV2-AUTHORIZATION-ISSUANCE-039

Implementation status: **BOUNDARY DEFINED — trusted issuer intentionally not implemented; awaiting CI verification**.

Added `OwnerApproval` and `issue_execution_authorization()` to make the missing owner-authority source explicit. The issuer rejects absent or cross-bound approval evidence and, even with syntactically valid evidence, raises `NotImplementedError` until a trusted owner-authority mechanism exists. This prevents a boolean `owner_approved=True` from being treated as proof of legitimate ownership. Existing execution tests continue to construct authorization fixtures directly as test fixtures; they do not establish production authority.


### CI-REVIEW-FIX-038-039

CI run 35332087037 exposed one test defect in the new fail-closed adapter test: `Engine.step()` updates the in-memory engine state, so the test incorrectly compared durable state against the mutated in-memory state instead of the captured pre-execution state. Fixed by capturing `initial_state_id` before stepping. Also removed the dead `if False` expression in `verify_durable_graph` and clarified the replay provenance guard. These are test/code-quality corrections; no production authorization or persistence semantics were weakened.


### CI-FIX-038-039-FINAL

Run 35333218308 still failed because the previous correction inserted `initial_state_id` into the neighboring success test rather than the rejection test. The rejection test now captures `initial_state_id` immediately after instance creation. This is a test-only correction; no production code changed.


### CI-VERIFIED-038-039

CI run 35333354866 SUCCESS. The corrected fail-closed SQLite execution adapter test passes. Python 3.11/3.12 workflow checks are green. 038 is now CI-VERIFIED. 039 boundary tests are also CI-VERIFIED; trusted owner-authority issuance remains intentionally NOT IMPLEMENTED.


### GNV2-REFLECTION-GATE-040

Implementation status: **IMPLEMENTED — awaiting CI verification**.

Added a read-only `run_reflection_gate()` orchestration boundary. It verifies canonical Core history exists, validates the durable SQLite graph, recovers the instance and compares the recovered state with the canonical engine head, runs reflection against canonical history plus prior persisted reflection evidence, and produces a machine-readable SELF-DIAGNOSTIC artifact explicitly marked `READ_ONLY`. It does not issue authority, activate proposals, mutate Core, or change invariants. Added positive and fail-closed integration tests.


### CI-FIX-040

CI run 35333646417 found a defect in the new Reflection Gate test path: `verify_durable_graph()` returns the audit-chain tuple, not an instance-id collection. The gate incorrectly tested `instance_id in durable`, causing a false negative despite successful durable verification. Fixed the gate to treat successful completion of `verify_durable_graph()` as the durable-graph proof; exceptions remain fail-closed. No persistence semantics changed.


### CI-VERIFIED-040

CI run 35333760106 SUCCESS after the Reflection Gate correction. The end-to-end read-only Reflection Gate is now CI-verified. The gate proves canonical Core history, durable SQLite graph verification, recovery/state-head consistency, reflection evidence generation, and READ_ONLY diagnostic artifact production; failure remains fail-closed.


### GNV2-REFLECTION-EVIDENCE-GATE-041

Implementation status: **IMPLEMENTED — awaiting CI verification**.

Added `run_reflection_evidence_gate()` as a read-only orchestration boundary over existing ShadowEvaluation, InvariantDelta, and GovernanceDecision. It requires blocking decisions to have actual regression/invariant evidence, requires REVIEW to have behavioral change or improvement evidence, treats insufficient input as HOLD, and asserts governance never grants activation or rollback authority. Exceptions fail closed to HOLD/INSUFFICIENT_EVIDENCE. Added integration tests for regression/BLOCK and empty-input/HOLD paths.


### CI-VERIFIED-041

CI run 35336802374 SUCCESS. Reflection Evidence Gate is CI-verified. Shadow → Invariant Delta → Governance is now connected through a read-only, fail-closed evidence boundary; governance remains non-authoritative (`can_activate=False`, `can_rollback=False`).


### GNV2-ENDOGENOUS-GENERATE-042

Implementation status: **IMPLEMENTED — awaiting CI verification**.

Added `generate_endogenous_candidates()` in `gnosis/reflection/endogenous.py`. It converts evidence-backed `RuleProposal` objects into ordinary Core `Candidate` objects by encoding each hypothesis as a bounded `Relation` in the proposed state. The generator is deterministic, limited to 20 candidates, does not mutate Engine/Core state, does not activate proposals, and does not bypass Test/Select. This is the first endogenous candidate-generation boundary; it is intentionally proposal/evidence-driven rather than direct rule self-modification.


### GNV2-ENDOGENOUS-BUDGET-BINDING

042 refinement: endogenous candidate generation now accepts the existing Core `Budget` and caps generation by `budget.remaining`; an exhausted budget produces zero candidates. The legacy `20` remains the default upper bound, not a mathematical constant. Added tests for partial and exhausted budgets. Awaiting CI verification.


### CI-VERIFIED-ENDOGENOUS-BUDGET-042

CI run 35337420893 SUCCESS after budget binding. Endogenous generation now has CI verification for partial/exhausted budgets. Added a Core-path integration test to prove generated candidates are passed to the existing `Test/Select` path (`Engine.step_select`) rather than a parallel evolution mechanism. Awaiting CI for this new integration test.


### CI-FIX-ENDOGENOUS-042

CI run 35337563386 exposed a real Core invariant failure in the new endogenous integration test: proposal relations referenced `__gnozis_reflection__` and `proposal:<id>` as relation endpoints without placing them in State.X. This correctly triggered `transition_validity`. Fixed by making both nodes explicit elements in the proposed State before adding the relation. This preserves Ψ=(X,R): endogenous proposal evidence is now represented as valid X nodes plus an R edge, rather than dangling metadata. New test asserts the reflection node is part of X. Awaiting CI verification.


### CI-FIX-ENDOGENOUS-042-TEST-FORMAT

CI run 35337753436 failed during test collection, before executing tests. Cause: the added assertion in `tests/test_endogenous_generation.py` contained a literal escaped `\\n` sequence in source, producing a SyntaxError. Fixed only the test formatting; no production code changed. Awaiting CI verification.


### CI-FIX-042-TEST-SYNTAX

CI run 35337753436 failed during test collection due to an accidentally literal `\\n` sequence inserted into `tests/test_endogenous_generation.py`, not due to product code. Fixed the test source in commit `de7a2e026ca98d0411427d565eb59accee89c5b5`. Awaiting CI verification.


### CI-FIX-042-PRODUCT-SYNTAX

CI run 35337956893 showed the previous test-source fix was insufficient: `gnosis/reflection/endogenous.py` itself contained literal `\\n` escape sequences in the multiline `with_elements()` block. Corrected the production source in commit `14c1cc03e20f7e1ff434c7cf43ef354ca8d1d6b8`. This is a source-generation/formatting defect, not a semantic change. Awaiting CI verification.


### CI-VERIFIED-042

CI run 35338134710 SUCCESS on commit `587d3ef7358a484d959bed07d1234e1f6d921301`. Endogenous candidate generation is now CI-verified after fixing source-formatting defects and the earlier Ψ=(X,R) dangling-relation invariant failure. 042 is complete: bounded endogenous Generate, Core Budget binding, valid X/R proposal representation, and normal Core Test/Select path are verified.


### GNV2-EVOLUTION-MEMORY-043

Implementation status: **IMPLEMENTED — awaiting CI verification**.

Added schema v4 `evolution_memory` as an append-only durable record of endogenous evolution attempts. Each record binds `instance_id`, `candidate_id`, `transition_id`, `state_id`, optional `proposal_id`, outcome (`accepted|rejected|inconclusive`), evidence references, timestamp, and a deterministic digest. SQLite UPDATE/DELETE triggers make the memory append-only. Added load/verify APIs and tests for round-trip integrity, digest consistency, append-only enforcement, and invalid outcomes. This memory is evidence/history, not authority and not an activation mechanism.


### CI-VERIFIED-043

CI run `35338572905` SUCCESS on `dc9a0eb34b14289cc37f25680215ad731e0026c3`. Evolution Memory schema v4, append-only storage, digest verification, and associated tests are CI-verified.

### GNV2-MEMORY-TO-REFLECTION-044

Implementation status: **IMPLEMENTED — awaiting CI verification**. Added `gnosis/reflection/memory_evidence.py` as a read-only projection from verified `EvolutionMemoryRecord` to Reflection evidence. It does not create candidates, mutate Core, or grant authority. Projection is bounded by an explicit limit. Added tests for projection and bounding.


### GNV2-MEMORY-TO-REFLECTION-044-BINDING

044 refined: cumulative Reflection now exposes instance-scoped `EvolutionEvidence` from durable evolution memory. The binding accepts an explicit `instance_id` rather than guessing from Engine, preserving instance isolation. Memory remains read-only evidence and does not create candidates, mutate Core, or grant authority. Added a regression test for empty instance-scoped memory. Awaiting CI verification.


### CI-VERIFIED-044

CI run `35339136889` SUCCESS on `9bea14f72e244c39b8b3d689f63da88af1813a9e`. Instance-scoped Evolution Memory → Reflection evidence binding is CI-verified. Reflection remains read-only with respect to memory/Core; no authority or mutation path was introduced.


### CI-VERIFIED-044A

CI run `35339905264` SUCCESS on `a23d1a404cbbcc7bf7a48cc9d2884d8b84ac1fe0`. Evolution evidence is now carried directly on `ReflectionReport.evolution_evidence` when using `reflect_with_history`. The evidence is still read-only and verified before projection; this makes the memory visible to the endogenous generation input contract without yet changing proposal-selection semantics. CI pending.


## GNOZIS CONTEXT AUTOPOIESIS — FUTURE PRINCIPLE

The AI_CONTEXT.md file is part of the project's developmental continuity. It must preserve both the philosophical identity of Gnozis and the operational state needed for future AI agents to continue the work without losing the Ψ/Gnozis development line.

### Earned Context Authorship

A future Gnozis instance may progressively earn the ability to propose and eventually author new versions of AI_CONTEXT.md. This authority must be earned through externally verifiable evidence of sustained effectiveness, not self-declared by the system.

The intended progression is:

READ → PROPOSE → EVIDENCE → REVIEW → EARNED CONTEXT AUTHORSHIP → VERIFIED CONTEXT → PROMOTION

Context authorship is not absolute authority. Even an earned context-authoring capability must not silently erase historical evidence, alter protected Core invariants, or redefine its own authority boundary.

A new context version must preserve historical continuity. Previous context versions and their provenance remain recoverable; a new version is a candidate until independently verified and promoted.

### Context Efficiency

"High effectiveness" must eventually be defined by measurable, externally verifiable criteria. Candidate criteria include invariant preservation, reproducibility, provenance integrity, self-error detection, evolutionary stability, and context continuity. The system must not determine its own promotion threshold solely from its internal assessment.

### Context Autopoiesis Boundary

The long-term objective is a controlled form of context autopoiesis: Gnozis can eventually maintain and improve the context through which future instances understand and continue its development. This is an evolutionary capability, not unrestricted self-modification.

The distinction must remain explicit:

Observation ≠ authority
Memory ≠ truth
Proposal ≠ change
Context authorship ≠ absolute authority
New context ≠ deletion of history

This principle is recorded as a FUTURE architectural direction. It is not an implementation grant and must not be interpreted by an agent as permission to modify AI_CONTEXT autonomously at the current stage.


### GNV2-MEMORY-AWARE-GENERATE-045

Implementation status: **IMPLEMENTED — awaiting CI verification**. Endogenous Generate now accepts verified `EvolutionEvidence` as an explicit input and carries its immutable memory identifiers into the proposed-state evidence record. This is evidence binding only: historical memory does not automatically reject, accept, rank, or activate a proposal. Selection semantics remain unchanged. Added regression coverage for the binding. This preserves the distinction Memory → Evidence → Hypothesis while preparing the next phase for genuine memory-informed hypothesis formation.


### CI-VERIFIED-045

CI run `35340047648` SUCCESS on `335a77cab1ea81ee571797b6131628048d011df7`. Memory-aware endogenous generation is CI-verified. Evolution memory is now carried from verified storage through Reflection into Generate as explicit evidence references without changing selection or granting authority.


### CI-VERIFIED-046

CI run `35340210780` SUCCESS on `aba33cf8455f88afe50a45b337ede8b176d2af95`. Memory-informed hypothesis formation is CI-verified.

### GNV2-MEMORY-FORMATION-046

Implementation status: **IMPLEMENTED — awaiting CI verification**. Endogenous Generate now incorporates verified historical memory outcomes into each generated hypothesis state's evidence payload (`historical_memory_outcomes`) alongside immutable memory references. This is contextual formation, not selection: outcomes are recorded as historical evidence and do not automatically veto, approve, rank, or activate a candidate. Candidate testing and selection remain governed by Core.


### CI-VERIFIED-047

CI run `35340364864` SUCCESS on `66e9fa873576034845792c5597ec8c4ae85cb70f`. Differential memory influence is CI-verified.

### GNV2-MEMORY-DIFFERENTIAL-047

Implementation status: **IMPLEMENTED — awaiting CI verification**. Added regression coverage showing that identical reflection proposals produce identical proposal selection while historical memory changes only the evidence attached to the generated hypothesis. Historical memory therefore influences hypothesis context without becoming a hidden selector or automatic veto/approval mechanism.


### GNV2-MEMORY-SIGNATURE-048

Implementation status: **IMPLEMENTED — awaiting CI verification**. Endogenous Generate now derives a deterministic `memory_signature` from verified memory identifiers and carries it into hypothesis context. Regression tests demonstrate that different memory histories can produce different hypothesis context while preserving deterministic generation and identical proposal selection. This is contextual memory influence, not a hidden selector.


## FUTURE PHILOSOPHICAL PRINCIPLE — CONFLICT AS EVOLUTIONARY PRESSURE

Gnozis may represent multiple world-models whose differences create measurable or structurally describable tension. Conflict is not merely an error condition or a source of information. It may function as an evolutionary pressure that motivates the creation of new capabilities and new organization.

The intended developmental pattern is:

CONFLICT → TENSION → LIMITATION → HYPOTHESIS → NEW CAPABILITY → TEST → INTEGRATION → REDUCED TENSION

The objective is not to force one world-model to defeat another, nor to compute a simplistic midpoint between them. A successful evolution may instead create a third organization in which previously incompatible requirements can coexist under new conditions:

W_A ⊕ W_B → W_C

Safety/preservation and development/exploration are therefore treated as potentially complementary evolutionary pressures. Safety preserves viable structure; development expands the space of viable possibilities. Neither pole is itself the complete objective of Gnozis.

A future conflict model may track tension T between world-models and evaluate whether a tested transition produces a viable reduction in tension while preserving protected invariants and increasing useful capability. This is a future research direction, not a current Core rule.

The philosophical use of panpsychism, if retained, is a design hypothesis and vocabulary for this line of inquiry, not a scientific fact and not a protected implementation invariant.


### GNV2-FUTURE-049 — CONFLICT MODEL FORMALIZATION

Next primary research task: formalize a conflict/tension model before implementing conflict-driven evolution. Define world-model identity, evidence provenance, conflict representation, a bounded tension measure or partial order, and criteria for a transition to count as tension-reducing while preserving Core invariants. Do not encode a simplistic scalar "truth" score and do not allow conflict/tension to become an implicit selector. The first implementation should remain observational/evaluative and generate evidence for later hypothesis formation.


### GNV2-FORMAL-049A — CONFLICT REPRESENTATION

First formalization step: represent a conflict as a structured relation between two or more world-model claims, not as a scalar score. A conflict record should preserve: model identities, claim identities, evidence/provenance references, the exact incompatibility relation, affected constraints/invariants, and the conditions under which the incompatibility was observed.

A conflict is observational when the evidence establishes incompatibility under specified conditions. It must not imply that either model is globally false.

Preferred conceptual form:

C = (W_a, W_b, Claims, Evidence, Conditions, Incompatibility)

Tension is initially treated as a structured/partially ordered object rather than a universal numeric truth value. Any later scalarization must be justified as an observational convenience and must never become an implicit selector.

Acceptance for 049A: conflict records are provenance-preserving, condition-scoped, deterministic, immutable after creation, and incapable by themselves of authorizing mutation or selecting a world-model.


### GNV2-FORMAL-049B — INCOMPATIBILITY AND CONDITIONS

A conflict must identify the precise incompatibility and the conditions under which it holds. Represent incompatibility as a typed relation between claims rather than a free-form assertion. Initial relation types may include CONTRADICTORY, INCOMPATIBLE_UNDER_CONDITION, RESOURCE_TENSION, OBJECTIVE_TENSION, and UNRESOLVED. Conditions must be explicit, canonicalizable, and provenance-bound so that the same conflict can be independently reconstructed.

Conceptual form:

Incompatibility = (claim_a, claim_b, relation_type, conditions, evidence_refs)

Conditions are part of the identity of an observed conflict. Removing or changing conditions must produce a distinct conflict observation rather than silently generalizing the original one.

Acceptance for 049B: the representation is deterministic, immutable, provenance-preserving, condition-scoped, and does not itself imply truth, priority, selection, or authority.


### GNV2-FORMAL-049C — STRUCTURED TENSION, NOT TRUTH SCORE

Tension is defined initially as a structured relation over observed incompatibilities, affected constraints, conditions, evidence strength, and unresolved capability gaps. It is not a universal scalar truth score.

Conceptual form:

T(C) = (Incompatibilities, Conditions, ConstraintImpact, EvidenceStatus, CapabilityGap)

A tension state may be partially ordered when one state has strictly fewer or weaker unresolved incompatibilities under comparable conditions while preserving the same required evidence basis and protected invariants. This relation is observational and does not select a world-model.

A transition may be described as tension-reducing only when it is independently testable and demonstrates at least one of: removal of an incompatibility under its stated conditions; relaxation of a verified constraint conflict; or creation of a verified capability that makes previously incompatible requirements jointly satisfiable. The transition must not achieve this by deleting evidence, weakening protected invariants, or silently changing the conflict conditions.

Conceptual relation:

T_after ≺ T_before  iff  verified_reduction(T_after, T_before) ∧ invariants_preserved

No implementation of a scalar tension score is authorized by this task. The first runtime layer should preserve the structured evidence needed for later comparison.


### GNV2-FORMAL-049D — EVOLUTIONARY TENSION LOOP + PREDICTION

The conflict model is extended into a long-horizon evolutionary loop. Persistent or significant tension should create pressure to develop and record tools/capabilities targeted at the boundary of the contradiction. The historical record must preserve the conflict, tension structure, proposed capability, intervention, test evidence, observed change, and forecast context.

Conceptual loop:

T_t → CapabilityGap_t → CapabilityHypothesis_t → Test → Integration → T_{t+1}

The system should also support a predictive branch:

History_t → Forecast(T_{t+k}) → PreventiveCapabilityHypothesis → Test → Integration

The desired long-term behavior is not zero tension everywhere. The objective is reduction of destructive or unresolved tension while preserving diversity, exploration, protected invariants, and the ability to generate new possibilities. Some tension may remain useful as evolutionary pressure.

A historical trajectory may therefore contain:

T_0, Tool_0, ΔT_0, T_1, Tool_1, ΔT_1, ...

A repeated failure to reduce a tension should be evidence that the capability class or hypothesis class may be inadequate, not a reason to repeatedly apply the same intervention. A forecast of rising tension may justify generating preventive capability hypotheses before the predicted conflict manifests.

This is a future research/architecture principle. No automatic authority, mutation, or scalar tension objective is introduced by this entry.


### GNV2-FORMAL-049E — CAPABILITY GAP TAXONOMY

A CapabilityGap is a verified or explicitly unresolved limitation in what the current system organization can perform that prevents a stated hypothesis, test, integration, or conflict-reduction operation from being carried out or evaluated adequately.

Conceptual form:

G = (target_operation, current_capability, missing_capability, evidence_refs, conditions)

The first taxonomy distinguishes:

- CAPABILITY_GAP — the system lacks an operation or instrument required to act/evaluate;
- KNOWLEDGE_GAP — the required operation exists, but relevant knowledge/model information is insufficient;
- EVIDENCE_GAP — a claim or transition cannot yet be adequately tested because evidence is insufficient;
- RESOURCE_GAP — the capability exists conceptually but available bounded resources prevent execution;
- MODEL_CONFLICT — existing models impose incompatible requirements and a new capability may be required to reconcile them.

These categories must not be silently conflated. In particular, missing knowledge must not be misreported as missing capability, and missing evidence must not be treated as proof that a capability failed.

Capability gaps are descriptive evidence for hypothesis generation. A gap must not itself create authority, mutate Core, select a candidate, or prove that a proposed tool is necessary. A future CapabilityHypothesis must specify the target gap, expected effect, test conditions, resource bound, and acceptance evidence.

Long-term history should permit:

CapabilityGap → CapabilityHypothesis → Tool/Capability → Test → ObservedEffect → ΔT

This entry is a formal research contract; no runtime authority is introduced.


### GNV2-FORMAL-049F — CAPABILITY HYPOTHESIS

A CapabilityHypothesis is a testable proposal for a new operation, tool, procedure, model, or organizational change intended to address a specific CapabilityGap or related limitation.

Conceptual form:

H = (gap_id, proposed_capability, rationale, expected_effect, test_conditions, resource_bound, acceptance_evidence)

The hypothesis must remain separate from implementation and authority. Proposing a capability does not create the capability, execute it, activate it, or grant permission to modify protected Core.

A valid hypothesis must identify:

1. the exact gap it targets;
2. the proposed capability or change;
3. the causal/functional rationale linking the capability to the gap;
4. the expected observable effect;
5. bounded test conditions and resources;
6. evidence required to accept, reject, or leave the hypothesis unresolved.

The result vocabulary should remain at least:

ACCEPTED — evidence supports the stated capability under its conditions;
REJECTED — evidence contradicts the stated capability under its conditions;
INCONCLUSIVE — evidence is insufficient to distinguish the hypothesis;
SUPERSEDED — a later verified hypothesis addresses the same gap under better-supported conditions.

A CapabilityHypothesis must never be treated as a truth claim merely because it reduces a modeled tension. Reduction must be independently observed and provenance-bound.

Long-term evolutionary history should connect:

Conflict → Tension → Gap → CapabilityHypothesis → Test → Result → ΔT → Memory

This entry defines the research contract only; it does not authorize autonomous activation or self-modification.


### GNV2-FORMAL-049G — CAPABILITY EVALUATION AND LONG-HORIZON EFFECT

A capability evaluation must distinguish immediate local effect from durable evolutionary effect. A capability is not considered successful merely because a single observation shows lower tension.

Conceptual evaluation record:

E_cap = (hypothesis_id, test_execution, conditions, observed_effect, ΔT_local, ΔT_longitudinal, invariant_status, provenance)

Evaluation should inspect at least three levels:

1. LOCAL — did the capability resolve or reduce the targeted incompatibility under the stated test conditions?
2. STABILITY — does the effect persist across subsequent observations/transitions rather than immediately regress?
3. GENERALIZATION — does the capability remain useful across relevant variations of conditions without violating protected invariants?

A capability may therefore be:

LOCALLY_EFFECTIVE — immediate evidence supports the target effect;
STABLE_EFFECTIVE — repeated evidence supports persistence;
GENERALIZED_EFFECTIVE — evidence supports usefulness across specified condition classes;
REGRESSED — the observed benefit later disappears or reverses;
INCONCLUSIVE — evidence is insufficient.

Long-horizon evaluation must preserve the full trajectory rather than overwrite earlier observations. A later regression does not erase a previous success; it becomes new evidence about the boundary conditions of the capability.

The evolution loop should prefer evidence of durable tension reduction, but must not convert this into an unconditional scalar objective. Diversity, exploration, safety invariants, and capability creation remain part of the evaluation context.

This is a research contract only. Evaluation produces evidence and does not itself grant authority to activate or deploy a capability.


### GNV2-FORMAL-049H — LONG-HORIZON TENSION TRAJECTORY AND FORECAST

Forecasting must predict possible future tension patterns, not declare future truth. A forecast is an evidence-bound hypothesis derived from historical tension trajectories, capability effects, conditions, and unresolved gaps.

Conceptual forecast record:

F = (history_window, target_conditions, observed_trend, uncertainty, predicted_gap_or_tension, supporting_evidence)

A forecast may identify:

- persistent tension — repeated unresolved incompatibility under comparable conditions;
- emerging tension — a trend suggesting that an existing capability or condition is approaching a known boundary;
- recurrent tension — a conflict that repeatedly returns after temporary reduction;
- displaced tension — reduction in one conflict accompanied by appearance of a related conflict elsewhere;
- insufficient evidence — history does not support a defensible directional inference.

Forecasts must preserve uncertainty and their conditioning assumptions. They must never be treated as guaranteed future states or as authority for autonomous mutation.

A future preventive hypothesis may be generated when:

Forecast(T_{t+k} | H_t, Conditions) indicates a supported unresolved or emerging capability gap

but the forecast itself remains a hypothesis until subsequent evidence validates or falsifies it.

Long-horizon learning should compare predicted and observed trajectories:

Forecast_t → Observed_{t+k} → ForecastError → Memory

This creates a second-order learning loop in which Gnozis can improve not only its capabilities but also its ability to anticipate where capabilities will be needed.

No single scalar forecasting score is required. Forecast quality should initially be represented through provenance, calibration evidence, uncertainty, conditions, and later observed outcomes.


### GNV2-FORMAL-049I — TENSION FIELD AND COUPLED CONFLICTS

Conflicts must not be assumed independent. Multiple conflict observations may share claims, constraints, conditions, capabilities, resources, or world-model boundaries. A tension field represents these dependencies without collapsing them into a single truth score.

Conceptual form:

F_T = (Conflicts, SharedConstraints, Dependencies, Couplings, Conditions, Evidence)

A coupling exists when a verified or explicitly unresolved relation indicates that changing one conflict may alter another conflict, capability gap, or resource requirement. Couplings should be typed and provenance-bound rather than inferred solely from temporal coincidence.

Important patterns include:

- COUPLED_REDUCTION — one capability reduces multiple related tensions;
- TRADEOFF — reducing one tension increases another under stated conditions;
- DISPLACEMENT — a conflict is reduced locally while a related conflict emerges elsewhere;
- SHARED_GAP — multiple conflicts depend on the same missing capability;
- CASCADE — a verified transition changes a chain of dependent conflicts;
- INDEPENDENT — available evidence supports treating conflicts as unrelated under the observed conditions.

The field should support identifying shared capability gaps. This permits Gnozis to search for a capability that addresses several tensions simultaneously without assuming that such a capability is automatically preferable.

A coupled-conflict record must preserve the individual conflict identities and their provenance. Aggregation must never erase the underlying observations.

No global scalar tension field or automatic optimization rule is introduced. This is a representation and analysis contract for future evolution research.


### GNV2-FORMAL-049J — SHARED GAP DISCOVERY

A Shared Gap is a candidate common limitation associated with multiple conflict observations. It must be distinguished from coincidence. Gnozis should require explicit evidence of a common dependency, shared constraint, shared missing operation, or reproducible cross-conflict effect before treating multiple conflicts as one Shared Gap.

Conceptual form:

SG = (conflict_refs, common_dependency, supporting_evidence, conditions, counterevidence, confidence_status)

Discovery evidence may include:

- SHARED_CONSTRAINT — the conflicts depend on the same protected or externally verified constraint;
- SHARED_OPERATION — the same missing operation is required to test or resolve each conflict;
- SHARED_RESOURCE — the conflicts compete for the same bounded resource;
- CROSS_EFFECT — an independently observed intervention changes multiple conflicts through a reproducible mechanism;
- STRUCTURAL_DEPENDENCY — the conflict representations share a verified dependency in their claims/models.

Temporal correlation alone is insufficient. A capability that happened to affect two conflicts once must not be declared a shared cause without mechanism or repeatable evidence.

Shared-gap discovery produces a hypothesis and evidence record, not a selector. It may prioritize future investigation only through an explicitly defined research policy; it cannot itself authorize mutation or capability activation.

Acceptance for 049J: preserve individual conflict provenance, expose supporting and counterevidence, record conditions, distinguish observed dependency from inferred dependency, and fail closed when evidence is insufficient.


### GNV2-FORMAL-049K — CAPABILITY SYNTHESIS ACROSS COUPLED TENSIONS

When a Shared Gap is sufficiently evidenced, Gnozis may form a CapabilitySynthesis hypothesis: a proposed capability intended to address multiple coupled tensions through one explicit mechanism. Synthesis is a hypothesis-generation operation, not an assumption that one tool is globally preferable.

Conceptual form:

CS = (shared_gap_id, target_conflicts, mechanism, expected_effects, possible_side_effects, test_plan, resource_bound)

The synthesis must specify which conflicts it targets, the hypothesized mechanism connecting the capability to each target, expected local effects, expected cross-effects, plausible new tensions or regressions, and bounded tests/resource limits.

Evaluation must use an effect vector rather than a single aggregate score:

DeltaT = (DeltaT_1, DeltaT_2, ..., DeltaT_n, DeltaT_new)

DeltaT_new records newly observed or displaced tensions. A capability is not considered successful merely because selected effects are favorable if it creates a destructive new conflict or violates protected invariants.

The synthesis loop is:

multiple tensions → shared gap → capability hypothesis → bounded test → effect vector → memory

and:

capability → new tension → new conflict record → updated field

No scalar global utility function or autonomous authority is introduced by this task. Trade-offs remain explicit and provenance-preserving.


### GNV2-FORMAL-049L — EVOLUTIONARY MEMORY GRAPH

Evolutionary history should be represented as a provenance-preserving graph rather than a flat event log. The graph connects conflicts, tensions, capability gaps, hypotheses, capabilities, tests, observed effects, forecasts, regressions, and subsequent conflicts.

Conceptual node types:

WORLD_MODEL, CLAIM, EVIDENCE, CONFLICT, TENSION, CAPABILITY_GAP, HYPOTHESIS, CAPABILITY, TEST, RESULT, EFFECT, FORECAST, REGRESSION, STATE_TRANSITION.

Conceptual edge types include:

SUPPORTED_BY, CONFLICTS_WITH, CONDITIONS_ON, EXPOSES_GAP, PROPOSES, TESTS, PRODUCES, REDUCES, INCREASES, DISPLACES, CAUSES_NEW_CONFLICT, FORECASTS, CONFIRMS, REFUTES, SUPERSEDES.

A historical chain may therefore be reconstructed as:

Conflict → Gap → Hypothesis → Capability → Test → Effect → StateTransition → NewConflict

The graph must preserve original observations when later interpretations change. New evidence may create new edges or revise the status of a hypothesis, but must not rewrite historical evidence into conformity with the latest model.

The graph should support long-horizon questions such as: which capabilities repeatedly reduced a class of tension; which capabilities created recurring side effects; which gaps recur across different conflicts; where forecasts repeatedly failed; and which evolutionary transitions produced durable structural change.

This graph is an analytical memory model, not an autonomous decision-maker. It must not itself authorize mutation, select a world-model as truth, or erase contradictory evidence.


### GNV2-FORMAL-049M — EVOLUTIONARY IDENTITY AND LINEAGE

Evolutionary identity must distinguish the continuity of an evolution process from the identity of any individual state, instance, clone, or capability. A state transition may preserve an evolutionary lineage while changing state identity; a clone may preserve provenance to a parent while receiving a distinct instance identity.

Conceptual relations:

StateIdentity_t != EvolutionIdentity
InstanceIdentity_clone != InstanceIdentity_parent
InstanceIdentity_clone derived_from InstanceIdentity_parent

An EvolutionIdentity should bind a sequence of accepted, provenance-preserving transitions into a reconstructable lineage. The lineage must not depend solely on mutable labels, filenames, process IDs, or external runtime location.

The identity model must distinguish at least:

- EVOLUTION_ID — continuity of a particular evolutionary lineage;
- STATE_ID — identity/digest of a concrete state;
- INSTANCE_ID — identity of a running or persisted instance;
- CAPABILITY_ID — identity of a proposed or verified capability;
- PROVENANCE_ID — identity of the evidence chain supporting an event or transition.

Forks and clones create new instance identities while retaining explicit ancestry. A derived lineage may diverge from its parent without rewriting the parent's historical graph. Shared ancestry is provenance, not shared mutable state.

Evolutionary identity must be cryptographically or deterministically bound to the relevant provenance where required by the existing persistence/evolution contracts. It must not grant authority: identity proves continuity/lineage, not permission to mutate or activate.

This identity layer is required before later federation/autopoietic-network work so that multiple Gnozis instances can cooperate without collapsing their histories or authority boundaries.


### GNV2-FORMAL-049N — EVOLUTIONARY LINEAGE AND BRANCHING

An evolutionary lineage may branch when an instance, state, or capability-development path is forked for independent exploration. Branching creates distinct descendant lineages while preserving explicit ancestry and provenance.

Conceptual structure:

L_parent → {L_1, L_2, ..., L_n}

Each branch must retain:

- parent EvolutionIdentity;
- branch-specific EvolutionIdentity;
- fork/base StateIdentity;
- provenance of the branching event;
- independent subsequent transitions and evidence.

Branch comparison is evidence comparison, not winner selection. A branch may provide evidence that a capability, hypothesis, or transition works under its tested conditions, but that evidence must remain scoped to those conditions and provenance.

A useful result from one branch may be imported or referenced by another branch through an explicit provenance-preserving relation such as DERIVED_FROM, REPLICATED_BY, VALIDATED_BY, or REJECTED_BY. Importing evidence must not merge identities or silently copy mutable state.

Lineage convergence is therefore distinct from identity convergence:

L_1 + evidence(L_2) → improved hypothesis in L_1

without requiring:

Identity(L_1) = Identity(L_2)

Branch failure is retained as evidence and is not treated as deletion of the branch's history. Successful branches also remain subject to later regression evidence.

This branching model is a prerequisite for future multi-agent and networked autopoietic evolution. It permits parallel exploration while preserving independent provenance, state, and authority boundaries.


### GNV2-FORMAL-049O — CROSS-LINEAGE EVIDENCE EXCHANGE

Independent evolutionary lineages may exchange evidence, hypotheses, capability descriptions, and replication results through explicit provenance-preserving records. Exchange does not merge lineage identities, mutable state, authority, or protected Core.

Conceptual exchange record:

X = (source_lineage, source_identity, artifact_id, artifact_type, provenance, conditions, integrity, receiving_lineage, receipt)

Artifact types may include EVIDENCE, HYPOTHESIS, CAPABILITY_DESCRIPTION, TEST_RESULT, FORECAST, or REPLICATION_RESULT. Each received artifact must retain its source provenance and conditions. The receiving lineage may classify it as ACCEPTED_FOR_REPLICATION, REQUIRES_REVIEW, REJECTED, or INCONCLUSIVE without rewriting the source record.

Cross-lineage evidence should be distinguished from locally reproduced evidence. A claim imported from another lineage is not equivalent to an independently reproduced observation until the receiving lineage performs a bounded replication or otherwise obtains qualifying evidence.

Exchange must be fail-closed with respect to identity and integrity: malformed, unverifiable, condition-mismatched, or provenance-incomplete artifacts must not enter the trusted evidence set.

A capability description may be shared without granting execution authority. An evidence exchange may influence future hypothesis generation, but cannot itself mutate Core, activate a capability, merge identities, or bypass protected invariants.

This establishes the conceptual bridge for future networked Gnozis: independent agents can learn from one another while preserving independent histories and authority boundaries.


### GNV2-FORMAL-049P — REPLICATION AND INDEPENDENT CONFIRMATION

A result originating in one evolutionary lineage becomes independently confirmed only when another lineage reproduces the relevant claim, capability effect, or transition under explicitly recorded conditions and obtains qualifying evidence through an independent execution path.

Conceptual replication record:

R = (source_result, source_provenance, receiving_lineage, replication_conditions, execution_identity, observed_result, comparison, independence_status)

Replication must preserve the distinction between SOURCE_RESULT, REPLICATION_RESULT, and CONFIRMATION. Independence is contextual, not absolute: shared data, artifacts, implementations, or conditions that weaken independence must be disclosed.

Possible outcomes: CONFIRMED, PARTIAL, FAILED, INCONCLUSIVE, DEPENDENCY_CONSTRAINED.

A replication result never rewrites the source result. Agreement strengthens the provenance graph; disagreement becomes new evidence and may expose boundary conditions, model conflict, or hidden dependencies.

Independent confirmation is epistemic only. It does not grant authority, merge identities, activate capabilities, or bypass protected invariants.

This establishes distributed learning in which multiple Gnozis lineages can validate one another while retaining separate identities and histories.


### GNV2-FORMAL-049Q — DISTRIBUTED EVOLUTION WITHOUT CENTRAL AUTHORITY

Multiple Gnozis lineages may participate in a shared evolutionary evidence network without requiring a central arbiter that declares one world-model true. Each lineage retains independent identity, state, provenance, authority boundary, and local protected invariants.

Conceptual network:

N = (L, E, ReplicationRelations, EvidenceRelations, CapabilityRelations, TrustContext)

where L is the set of independent lineages and E contains explicit, provenance-preserving exchange relations.

The network may establish relations such as AGREES_WITH, REPLICATES, DISAGREES_WITH, EXTENDS, REQUIRES, or SHARES_GAP. These relations describe evidence and dependencies; they do not constitute a global vote on truth.

When lineages disagree, disagreement remains a first-class observation. The network should preserve the competing claims, conditions, evidence, and replication status. Resolution may occur through additional experiments, narrower conditions, capability development, or model revision; no node is entitled to resolve the disagreement merely by network position or accumulated authority unless an explicit external governance contract says so.

Collective learning therefore means:

independent observations → exchange → replication/critique → richer evidence graph → new hypotheses/capabilities

not:

independent observations → central score → imposed truth.

A capability discovered by one lineage may become a candidate for replication by others. Repeated cross-lineage evidence can increase evidentiary support, but support remains scoped to declared conditions and provenance.

Network participation must not bypass local Core invariants, execution authorization, persistence integrity, or identity boundaries. Federation is an evidence and learning layer unless a separately specified governance layer explicitly grants additional authority.

This principle is foundational for future Gnozis federation and multi-agent autopoiesis: collective development emerges from interaction among autonomous lineages rather than from a single central decision-maker.


### GNV2-FORMAL-049R — CONFLICT AS EVOLUTIONARY PRESSURE AND AUTOPOIETIC LOOP

Conflict is modeled as a source of evolutionary pressure when incompatible constraints, models, objectives, or observed effects create persistent tension that cannot be adequately resolved by the current capability set. Conflict is not itself a command to mutate; it is an observation that may expose a capability gap.

Conceptual loop:

Conflict → Tension → Gap → CapabilityHypothesis → Bounded Test → Evidence → Transformation → New State → New Conflict/Tension

For the loop to qualify as an autopoietic process, the system must satisfy all of the following conditions:

1. SELF-REFERENCE — outcomes of its own prior transformations become part of the evidence available to subsequent evolution;
2. CAPABILITY GENERATION — unresolved gaps can produce explicit hypotheses for new capabilities rather than only selecting among fixed actions;
3. STRUCTURAL CLOSURE — accepted transformations operate through defined internal state/provenance contracts and cannot bypass protected invariants;
4. CONTINUITY — the evolutionary identity and memory graph preserve the relation between successive transformations;
5. BOUNDED REPRODUCTION — a capability or organizational pattern may be reproduced in a new bounded lineage/instance through explicit provenance;
6. ENVIRONMENTAL COUPLING — external observations may expose new tensions or evidence, while external input does not directly dictate Core state;
7. FAIL-CLOSED EVOLUTION — insufficient evidence, failed tests, broken provenance, or authorization failures halt or downgrade the evolutionary transition rather than silently mutating state.

Autopoiesis therefore does not mean unrestricted self-modification. It means that the system can participate in a closed evolutionary loop in which its own history, limitations, generated capabilities, and observed consequences become material for subsequent organization.

A candidate transition can be represented as:

Ψ_t + Evidence_t + Gap_t + Capability_t → Ψ_{t+1}

with the requirement that the transition is accepted only when its declared invariants, provenance, test result, and authorization conditions are satisfied.

The current implementation should not claim full autonomous autopoiesis while Generate remains caller-supplied and capability activation remains disabled. This section defines the target research property and its acceptance conditions; it does not claim that the property is already implemented.


### GNV2-FORMAL-049S — AUTOPOIETIC CORE ACCEPTANCE CONDITIONS

The project must not claim an implemented autopoietic core until the following conditions are demonstrably satisfied by runtime evidence, tests, and provenance records. These are acceptance conditions, not implementation claims.

A — SELF-REFERENTIAL MEMORY: the system can consume its own prior accepted evolution records as input to subsequent bounded evolution without rewriting immutable history.

B — ENDOGENOUS GAP DETECTION: at least one runtime path can derive a capability gap from observed state/evidence rather than requiring the gap to be manually supplied by the caller.

C — CAPABILITY HYPOTHESIS GENERATION: the system can construct a bounded capability hypothesis from an evidenced gap, including mechanism, expected effects, side effects, test plan, and resource bound.

D — BOUNDED CAPABILITY TESTING: a generated capability can be tested in an isolated, resource-bounded execution path with protected invariants enforced independently of the candidate's own test function.

E — EVIDENCE-PRESERVING SELECTION: the system can evaluate candidate outcomes without rewriting source evidence, suppressing contradictory observations, or using an undocumented global selector.

F — STATE TRANSFORMATION: an accepted, authorized transition can produce a new durable state whose provenance links the previous state, candidate/capability, test evidence, and resulting state.

G — RECURSIVE FEEDBACK: the resulting state and its observed consequences become available to the next evolution cycle, closing the loop.

H — FAILURE/REGRESSION LEARNING: failed, inconclusive, and regressed capabilities remain in evolutionary memory and can alter subsequent hypotheses without being treated as successful evidence.

I — FORECAST FEEDBACK: the system can compare a prior forecast with later observations and retain forecast error as evidence for future forecasting.

J — BRANCHING CONTINUITY: bounded forks/clones can evolve independently while retaining explicit ancestry and separate identities.

K — CROSS-LINEAGE VALIDATION: independent lineages can replicate or critique evidence without merging identity or authority.

L — FAIL-CLOSED AUTHORITY: no evolutionary discovery, forecast, replication, or capability hypothesis can itself grant permission to mutate protected Core; activation requires the separately defined authorization contract.

M — OBSERVABLE PROOF: each accepted transition exposes sufficient provenance, audit evidence, and deterministic identifiers for an independent reviewer to reconstruct why the transition occurred.

The minimum autopoietic claim is therefore:

AutopoieticCore = A ∧ B ∧ C ∧ D ∧ E ∧ F ∧ G ∧ H ∧ L ∧ M

J and K become required for the stronger claim of distributed/networked autopoiesis. I becomes required for the stronger claim of predictive autopoietic adaptation.

Until the corresponding runtime evidence exists, these conditions remain a roadmap and acceptance gate, not a statement that the current implementation satisfies them.


### GNV2-FORMAL-049T — ENDOGENOUS CAPABILITY-GAP DETECTION

Endogenous gap detection is the first transition from externally supplied evolution toward an autopoietic research loop. The system must be able to derive a candidate capability gap from its own accumulated state, evidence, history, regressions, unresolved conflicts, or forecast errors without the caller explicitly naming the gap.

Conceptual operator:

Gap_t = DetectGap(State_t, Evidence_t, EvolutionMemory_t, TensionField_t, ForecastError_t)

Detection must produce a structured hypothesis rather than an authority-bearing command:

GapHypothesis = (gap_id, source_records, affected_conflicts, missing_capability_description, conditions, counterevidence, confidence_status)

A gap may be triggered by patterns such as:

- repeated unresolved conflict;
- recurring regression after apparently successful capabilities;
- repeated forecast error indicating a missing predictive capability;
- repeated failure of candidate tests for the same structural reason;
- a shared gap supported across multiple conflicts or lineages;
- an observed transition that exposes a missing operation or representation.

The detector must preserve provenance to the records from which the hypothesis was derived. Temporal correlation alone must not be represented as causal proof.

Gap detection must be conservative: when evidence is insufficient, it returns INCONCLUSIVE rather than inventing a missing capability. Counterevidence remains attached to the hypothesis.

Most importantly, endogenous gap detection does not authorize mutation. Its output enters the same bounded hypothesis/test/governance pipeline as externally proposed gaps.

Acceptance target for this phase:

External caller supplies State/history only → detector identifies a reproducible unresolved pattern → emits GapHypothesis with provenance → no Core mutation and no execution authority are granted.

This is the first required runtime capability for demonstrating that future evolution can originate from the system's own history rather than solely from an external operator.


### GNV2-FORMAL-049U2 — ARCHITECTURAL CORRECTION: EVOLUTIONARY RULES VS PROTECTED CORE

The autopoietic roadmap must distinguish evolutionary rules from protected Core invariants. Full autopoiesis does not require the system to rewrite its own protected validation boundaries. Evolution may propose changes to models, capabilities, strategies, agents, and other mutable organizational structures, but protected Core invariants remain an external constraint on that evolution.

Therefore:

ProtectedCore ≠ EvolutionRules ≠ MutableWorkspace

Self-modification must not become circular authority in which the system changes the rules that authorize its own change. Discovery, hypothesis generation, testing, and evidence may be endogenous; authorization remains separately constrained.

### GNV2-FORMAL-049V — AUTOPOIETIC CANDIDATE GENERATION LOOP

Target loop:

History → Gap → CapabilityHypothesis → BoundedTest → Evidence → ProposedStateTransition → History'

The loop is considered endogenous when Gap detection and CapabilityHypothesis generation can originate from the system's own accumulated evidence/history without a caller naming the target capability. Until activation authority is explicitly implemented and accepted, the loop remains proposal-producing and cannot mutate protected Core.

### GNV2-FORMAL-049W — SELF-IMMUNITY AS A CONTROLLED EVOLUTION LAYER

Threat handling is modeled as a specialized application of the same evidence-driven evolutionary loop, not as an independent authority center:

Threat → Observation → ImmunityHypothesis → Isolation/Sandbox → Test → Evidence → DefensiveCapability → AuthorizationBoundary

A Sentinel/Observer may monitor events, memory access patterns, task flows, and integrity signals through an isolated event channel, but it must not acquire unrestricted authority over Core. Generated defensive agents or patches must be treated as untrusted artifacts until static inspection, bounded sandbox execution, and declared tests produce evidence.

### GNV2-FORMAL-049X — EXTERNAL PERCEPTION BOUNDARY

External world data must enter through a perception boundary:

ExternalData → Bridge → Perception/Filtering → Pattern/Evidence → EvolutionPipeline

External content must not be treated as executable instructions merely because it arrived through a trusted bridge. Pattern extraction may produce observations or hypotheses; it cannot directly mutate Core or grant authority.

### GNV2-FORMAL-049Y — IMMUTABLE CORE / MUTABLE EVOLUTION BOUNDARY

The architecture must explicitly classify what may evolve and what may not. Mutable candidates may include models, capabilities, strategies, agent definitions, declarative graphs, and workspace structures. Protected invariants, provenance integrity, authorization boundaries, identity separation, and fail-closed safety constraints remain protected unless an explicitly external governance contract changes them.

This boundary prevents circular self-authorization:

SelfModification ≠ SelfAuthorization.

These sections incorporate the additional architectural audit while preserving the existing Ψ/Core, provenance, evidence, lineage, and authority model. They are roadmap/acceptance contracts unless corresponding runtime evidence exists.


### GNV2-FORMAL-049V2 — MINIMUM RUNTIME AUTOPOIETIC LOOP CONTRACT

Before autonomous activation is considered, implement and test the smallest runtime loop capable of demonstrating endogenous evolutionary proposal generation while preserving the existing authority boundary.

Required runtime stages:

1. READ_HISTORY — consume immutable accepted evolution records, current state, evidence, tensions, regressions, and forecast errors;
2. DETECT_GAP — produce zero or more provenance-bound GapHypotheses;
3. SYNTHESIZE_CAPABILITY — derive zero or more bounded CapabilityHypotheses from eligible gaps;
4. PLAN_TEST — produce an explicit bounded test plan for each candidate;
5. SANDBOX_TEST — execute only inside the existing bounded sandbox/test contract;
6. RECORD_EVIDENCE — persist observed results without rewriting source history;
7. PROPOSE_TRANSITION — construct a proposed state transition, but do not commit it autonomously;
8. EMIT_AUDIT — record the complete provenance chain needed for independent reconstruction.

The first implementation may use deliberately simple deterministic detectors and capability templates. Complexity is not an acceptance criterion. The critical property is endogenous causation: the caller supplies the state/history/environmental observations, but does not name the missing capability or final proposal.

Hard constraints:

- no direct Core mutation from detection or synthesis;
- no generated code executed outside sandbox;
- no generated capability receives authority automatically;
- protected invariants remain enforced;
- insufficient evidence yields no proposal or an explicitly INCONCLUSIVE proposal;
- every generated artifact has deterministic identity and provenance;
- failed candidates remain in memory as evidence;
- the loop must be bounded by operation/gas limits and terminate deterministically;
- existing Test/Select/authorization semantics must not be bypassed.

Acceptance evidence should demonstrate at minimum:

A. identical input history produces identical GapHypothesis identity;
B. changing relevant evidence can change the detected gap;
C. the detector can discover a gap not explicitly named by the caller;
D. a generated capability remains a proposal after testing;
E. failed tests do not mutate protected Core;
F. complete provenance reconstructs History → Gap → Capability → Test → Evidence → Proposal.

This is the first concrete runtime milestone toward autopoiesis. It intentionally stops one step before autonomous state activation.

## 20. REVERSE-ANALYSIS LOG — 2026-09-18 / 2026-09-19

This section records the mathematical reverse work performed after the repository implementation gates were substantially stabilized. It is a research/architecture record, not a claim that all concepts below are implemented.

### 20.1 2026-09-18 — Reverse direction and semantic preservation

The analysis moved from implementation-first thinking toward a bottom-up mathematical reverse:

Psi = (X,R)
→ transition semantics
→ evidence/provenance
→ proof obligations
→ reflection
→ meaning preservation
→ authority boundaries
→ trust anchor / Genesis.

Key conclusions:

1. Structural preservation is not semantic preservation.

Structural validity:
  Valid_struct(Psi') = 1

does not imply:

  Meaning(Psi') = Meaning(Psi).

A separate derived semantic representation M(Psi) is therefore useful for reasoning, but it MUST NOT become a second source of truth. Meaning must remain derivable from canonical state plus protected criteria/context.

2. Meaning should be divided conceptually:

  M = M_K ∪ M_E

where M_K is the protected minimum semantic foundation and M_E is evolvable semantic organization.

Ordinary evolution must preserve M_K. Changes to M_K are meta-evolution and require a separate external/meta proof contract.

3. Semantic loss is not automatically forbidden, but unexplained semantic loss is.

  MeaningLoss(tau) = M_required(Psi) - M(Psi')

A loss may be allowed only if its removal is explicitly justified/proven. This is preferable to an absolute monotonicity rule because genuine evolution may remove obsolete structure.

4. Claim, observation, change and authority are distinct concepts.

  Observation(Psi) != Transition(Psi)
  Claim(C) != Proof(C)
  Information != Authority
  Information does not imply Authority without a qualifying proof/admission path.

5. Information flow and authority flow are different graphs.

Information graph:
  Psi → Evidence → Reflection → Candidate → Proof

Authority graph:
  K → Rules → Semantic constraints → State

They may interact only through explicit proof/admission boundaries.

6. Endogenous generation is not automatically authoritative.

A generated candidate may be recorded as state/evidence if explicitly allowed, but candidate generation must not silently become rule activation or trust-anchor mutation.

### 20.2 2026-09-18 — Authority and trust-anchor reverse

The analysis identified the following boundary:

  Descendant ↛ Ancestor

for authority mutation.

A descendant transition may produce information about an ancestor-level rule, but cannot redefine the trust ancestor using the same authority path that it is trying to justify.

Therefore:

  SelfModification != SelfAuthorization.

Ordinary evolution:
  K fixed
  Rules/semantic organization/state may evolve under K.

Meta-evolution:
  K or M_K changes
  requires a separate meta-level contract and must not be justified solely by the descendant system.

Cryptographic integrity and epistemic validity are distinct:

  Integrity(Hash(K)) != Truth(K).

A hash can identify the exact Genesis artifact used by a proof chain; it does not independently establish the philosophical or epistemic truth of the Genesis assumptions.

The project should therefore use a minimal trust base rather than attempting to make Gnozis prove the foundations of logic/world-modeling from inside itself.

### 20.3 2026-09-18 — Minimal Genesis candidate

An initial Genesis candidate contained:

- State ontology
- Identity
- Transition
- Admissibility
- Observation/change separation
- Information/authority separation
- Claim/proof separation
- Conflict/tension
- Unknown/insufficient evidence
- No implicit selector/incomparability
- Trust boundary

Deletion analysis then showed that several of these may be derived rather than primitive.

Current reduced candidate:

  K0_candidate =
  {
    K_S = State ontology,
    K_C = Change/transition ontology,
    K_P = Claim/Proof boundary,
    K_A = Information/Authority boundary,
    K_T = Trust/authority ancestor boundary
  }

This is a candidate only. Minimality is not yet formally proven.

Potentially derived rather than independent Genesis axioms:

- Unknown != False
- NotProven(C) != Proven(not C)
- unresolved contradiction/tension
- incomparability
- identity/lineage if identity can be derived from state/lineage semantics
- transition as a relation if it is fully defined by the change ontology.

Important negative result:
No global clock, global selector, winner function, external AI model, human preference function, or utility function is required as a Genesis primitive. Lineage/generation can be represented causally without a global clock.

### 20.4 2026-09-19 — Deletion test result

The following candidate primitives survived first-pass deletion testing:

1. State ontology is necessary to define the evolving object.
2. Change/transition ontology is necessary to distinguish evolution from arbitrary state replacement.
3. Admissibility is necessary if not every mathematically possible transition is acceptable; however, the concrete admissibility rules need not all be Genesis primitives.
4. Claim/Proof distinction is necessary unless it can be derived from a more primitive justified-authority relation.
5. Information/Authority distinction is necessary to prevent observation/reflection from becoming implicit mutation.
6. Trust boundary is necessary to prevent self-authorization.

Current status:
- These are semantic necessities.
- Their status as independent axioms is still unresolved.
- The next reverse must test whether Claim/Proof and Information/Authority can be reduced to a smaller primitive such as JustifiedAuthority.

### 20.5 2026-09-19 — Current deepest unresolved question

Test:

  K_P = Claim != Proof

against:

  K_A = Information does not imply Authority.

Question:

  Can both be derived from a single primitive:

  JustifiedAuthority(C, context, proof)

such that:
- a claim has no authority merely by being generated;
- evidence can contribute to proof;
- proof can satisfy an admission contract;
- authority is scoped to an effect;
- no authority can modify its own trust ancestor;
- absence of proof remains UNKNOWN rather than FALSE.

If the reduction is valid, Genesis can become smaller and the architecture can treat proof/admission/activation as instances of justified, scoped authority rather than unrelated mechanisms.

If the reduction is invalid, retain Proof and Authority as independent boundaries and document the exact dependency.

DO NOT implement this reduction before the reverse analysis is complete.

### 20.6 2026-09-19 — Current formal hierarchy

Current working model:

  K
  ↓
  F (evolution/rule constraints)
  ↓
  M = M_K ∪ M_E
  ↓
  Psi = (X,R)

with proof/evidence context:

  Proof_K → Proof_F → Proof_M → Proof_Psi

Ordinary evolution keeps K and M_K fixed.

Meta-evolution is a separate class and is not currently autonomous.

Full transition evidence chain:

  State_t
  → Observation
  → Evidence
  → Reflection
  → Candidate
  → Proof
  → Authority/Admission gate
  → State_(t+1)

The candidate is not the proof.
The proof is not automatically authority.
Authority is scoped to the declared effect.
No descendant may redefine its own trust ancestor.

### 20.7 2026-09-19 — Meaning preservation contract

Meaning must not be implemented as a second mutable state model.

Preferred abstraction:

  M(Psi) = Derived(Psi, K, context)

with a protected semantic core M_K and evolvable M_E.

For a transition tau:

  M_required(Psi_t) ⊆ M(Psi_(t+1))

is the preservation condition for the declared required meaning.

If:

  MeaningLoss(tau) != empty

then the transition requires explicit removal justification.

Do not equate existing Core `check_meaningful_change` with semantic preservation. A structural change detector and a semantic-preservation verifier answer different questions.

### 20.8 External audit integration — 2026-09-19

A supplied independent audit inspected the repository at historical HEAD 7d40a9c... and reported:

- evolution layer has bounded child-process sandboxing, wall-clock timeout and operation budget;
- promotion/capability activation is hard-disabled;
- audit/transaction layer uses append-only records and hash-chain provenance;
- recovery is fail-closed when provenance/audit diverges;
- reflection governance/authority activation remains disabled;
- `reflection/endogenous.py` can generate Candidate records which, if passed into Core Engine.step(), may enter canonical X/R as proposal metadata; the audit identified this as requiring an explicit architecture decision;
- reflection persistence creates its own SQLite tables and migration handling should be reviewed;
- storage has SQLite-level append-only triggers, audit hash chain, secret rejection and integrity checks;
- instances documentation contains stale statements claiming persistence is not implemented;
- root documentation may lag actual storage implementation;
- the audit could not itself verify pytest/CI execution at that historical HEAD.

Important qualification:
GitHub confirms current main 70e3857... is 546 commits ahead of the audited 7d40a9c... HEAD. Therefore these findings are treated as:
  historical findings requiring revalidation,
not:
  current verified defects.

The `endogenous.py` finding is especially important and should be rechecked against current code before assigning any implementation task involving endogenous candidates.

### 20.9 2026-09-18 repository progress relevant to the research stage

Recent main commits inspected include:

- 70e3857 — docs: record 2026-09-18 math closure and repository gaps
- 29014d1 — test: derive gaps from persisted transition records
- 89b7f29 — feat: adapt persisted transition history to gap detection
- 27f06ec — feat: export endogenous evolution primitives
- e0782c9 — test: cover endogenous gap and capability hypotheses
- 43ec8b5 — feat: add authority-free capability synthesis
- 4e199f1 — feat: add endogenous capability gap detector
- e8942b2 — docs: define minimum runtime autopoietic loop
- f47a216 — docs: extend autopoietic, immunity, perception and protected-core architecture
- 9a5939c — docs: define endogenous capability-gap detection
- be7e16c — docs: define autopoietic core acceptance conditions
- f6be3c6 — docs: formalize conflict pressure and autopoietic loop
- 257749d — docs: formalize distributed evolution without central authority
- 7df2e83 — docs: formalize replication and independent confirmation
- 62c150a — docs: formalize cross-lineage evidence exchange
- b0a99de — docs: formalize evolutionary lineage branching
- 3382c4b — docs: formalize evolutionary identity and lineage
- 634c13c — docs: formalize evolutionary memory graph

These commits establish that the repository has already moved from purely static reflection toward persisted-history gap detection and authority-free capability synthesis. They do NOT mean full autonomous autopoiesis is implemented.

### 20.10 Current research percentages — 2026-09-19

Working analytical estimates:

| Layer | Completion |
|---|---:|
| Psi=(X,R) | 99% |
| Transition / lineage | 96% |
| Structural invariants | 96% |
| Evidence / provenance | 96% |
| Proof obligations | 92% |
| Proof DAG | 86% |
| Tension / contradiction | 87% |
| Incomparability | 83% |
| Composition | 82% |
| Meaning preservation | 79% |
| Meaning-loss accounting | 68% |
| F/rule evolution | 72% |
| Evolvable meaning M_E | 64% |
| Protected M_K boundary | 95% |
| Information ↔ authority separation | 93% |
| Trust boundary | 96% |
| Genesis candidate | 78% |
| Genesis minimality | 57% |
| External proof verification | 40% |
| Meta-evolution | 44% |
| Runtime enforcement | 25% |
| Real pytest/CI verification of current research layer | 20% |

Overall formal/architectural research maturity: approximately 96%.

This is NOT software test coverage and MUST NOT be reported as implementation completion.

### 20.11 Next AI handoff decision

Claude or another implementation AI should be engaged only after the current reverse has resolved:

  Proof/Claim
  ↔
  Information/Authority
  ↔
  JustifiedAuthority?

The first implementation task after that analysis should be one self-contained Task Block, not a broad "continue development" instruction.

Proposed next task envelope:

TASK-ID: GNV2-GENESIS-PROOF-001
BLOCK: Minimal proof/authority foundation
STATUS: ANALYSIS
PRIORITY: P1
DEPENDS_ON:
- current Reflection/Shadow gate evidence
- persisted provenance baseline
- current endogenous gap/capability implementation
- completion of Proof/Authority deletion reverse

OBJECTIVE:
Determine and, only if justified, implement the smallest non-self-authorizing contract connecting claim, evidence, proof, scoped authority and admission.

SCOPE:
- inspect current core/reflection/evolution authority boundaries;
- map mathematical primitives to existing code;
- determine whether Proof and Authority are independent or reducible;
- identify hidden self-authorization paths;
- implement only the justified minimum;
- add boundary tests;
- execute tests and inspect CI.

DO_NOT_CHANGE:
- Psi=(X,R)
- Core as source of truth
- protected invariants
- can_activate=False until separately authorized
- can_rollback=False
- no autonomous Genesis mutation
- no global selector
- no global clock
- no second state model
- no AI model inside Core
- persistence append-only/hash-chain semantics
- existing evidence gates.

ACCEPTANCE:
- primitive vs derived concepts explicitly separated;
- no authority path bypasses proof/admission;
- no descendant can rewrite its trust ancestor;
- insufficient evidence remains UNKNOWN/INCONCLUSIVE;
- tests cover the actual boundary;
- real execution evidence is recorded;
- CI status is inspected before marking DONE.

AUDIT:
Compare code, tests and current HEAD; do not trust stale README/STATUS statements; revalidate the historical endogenous.py concern before changing it.

NEXT:
If JustifiedAuthority reduction is proven, implement the reduced contract. Otherwise preserve independent Proof and Authority layers and document the dependency.

### 20.12 Handoff rule

The mathematical reverse work is not a license to start canonical self-evolution.

Current state remains:

  Canonical self-evolution = CLOSED.

The next agent must read this entire AI_CONTEXT, reconcile current HEAD, inspect the actual code, and select exactly one READY task. It must not assume that a mathematical completion percentage is runtime verification.


### 20.13 — 2026-09-19 RUNTIME BOUNDARY PROGRESS UPDATE

This section records the verified work completed after the earlier mathematical reverse-analysis and must be treated as the latest operational handoff for this workstream.

IMPORTANT:
- This work was performed on development branch `runtime-slice-001`, not main.
- Do not treat branch commits as current main HEAD.
- Main remains the authoritative production/reference branch until the development work is intentionally merged.
- CI evidence below is real GitHub CI evidence for the stated commits.

#### Verified progress

1. Endogenous reflection candidate boundary
- A multi-cycle regression test was added for three successive Reflection → endogenous Candidate → Core Test/Select cycles.
- The test verifies that proposals may enter Ψ as proposal metadata while no `activated_rule`, `authority`, or `authorization` record is produced.
- CI run 644 completed successfully with 302 passed.
- This confirms the distinction:
  Candidate/proposal state ≠ rule activation ≠ authority.

2. Shared bounded candidate execution boundary
A common Evolution boundary was added:

Reflection Candidate
  OR
Gap/Capability Candidate
  ↓
run_bounded_candidate()
  ↓
Sandbox
  ↓
Evaluation
  ↓
Provenance
  ↓
Audit transaction
  ↓
Review

The new boundary is intentionally non-authoritative:
- it accepts a supplied Candidate;
- executes it through the existing bounded sandbox/evidence path;
- records provenance and a `BOUNDED_RUNTIME_EVIDENCE` transaction;
- returns governance classification as REVIEW;
- does not mutate canonical Core state;
- does not activate the Candidate.

The public Evolution export now exposes `run_bounded_candidate`.

3. Real CI correction cycle
The new integration test initially exposed two schema mismatches in the newly written test/adapter code:
- GapHypothesis constructor mismatch;
- CapabilityHypothesis required fields mismatch.

These were corrected against the actual repository dataclass definitions. This is useful evidence: the CI loop caught concrete integration errors rather than allowing an unexecuted test to be called complete.

Final CI:
- commit: `836a69fface0170f638fb07014d0de20e0636909`
- CI run: 652
- result: SUCCESS
- suite result: 305 passed
- Python 3.11/3.12 workflow completed successfully.

#### Current verified architectural position

The current tested boundary is:

Reflection
  ↓
RuleProposal
  ↓
endogenous Candidate
  ↓
shared bounded candidate boundary
  ↓
Sandbox / Evaluation / Provenance / Audit
  ↓
REVIEW
  ↓
NO AUTONOMOUS ACTIVATION

The canonical Core state remains unchanged by `run_bounded_candidate`.

This is stronger than the historical external-audit wording that merely said endogenous candidates "may enter canonical X/R if passed to Engine.step()". The current code now has an explicitly tested non-authoritative evidence path for those candidates. The historical audit finding remains relevant only to the separate question of whether proposal metadata is permitted to become canonical state through normal Core Test/Select.

#### Current progress estimate — 2026-09-19

These are analytical completion estimates, NOT test coverage:

| Layer | Completion |
|---|---:|
| Ψ=(X,R) | 99% |
| Transition / lineage | 96% |
| Structural invariants | 96% |
| Evidence / provenance | 97% |
| Proof obligations | 92% |
| Proof DAG | 86% |
| Tension / contradiction | 87% |
| Incomparability | 83% |
| Composition | 82% |
| Meaning preservation | 79% |
| Meaning-loss accounting | 68% |
| F/rule evolution | 72% |
| Evolvable meaning M_E | 64% |
| Protected M_K boundary | 95% |
| Information ↔ authority separation | 96% |
| Trust boundary | 96% |
| Genesis candidate | 78% |
| Genesis minimality | 57% |
| External proof verification | 40% |
| Meta-evolution | 44% |
| Runtime enforcement | 35% |
| Real pytest/CI verification of current research/runtime slice | 35% |

Working overall engineering/architecture progress: approximately **94%** for the currently defined foundation/evidence workstream.

This percentage must NOT be interpreted as:
- repository completion;
- autonomous evolution completion;
- test coverage;
- percentage of all planned Gnozis capabilities.

Canonical self-evolution remains CLOSED.

#### Current next task

TASK-ID: GNV2-RUNTIME-FAILCLOSED-001
BLOCK: Shared bounded candidate execution — failure path
STATUS: READY
PRIORITY: P1
DEPENDS_ON:
- shared bounded candidate boundary implemented;
- Reflection → endogenous Candidate boundary verified;
- CI run 652 SUCCESS.

OBJECTIVE:
Verify that a Reflection-generated Candidate which fails inside the bounded execution boundary becomes explicit rejected/insufficient evidence, remains auditable, and cannot become authority or canonical mutation.

SCOPE:
- use a real endogenous Reflection Candidate;
- force a deterministic sandbox/test failure without bypassing the sandbox;
- verify evaluation status is REJECTED/INCONCLUSIVE as appropriate;
- verify provenance remains reconstructable;
- verify audit transaction records the failure;
- verify governance remains non-authoritative;
- verify canonical Core state remains unchanged.

DO_NOT_CHANGE:
- Ψ-Core authority semantics;
- protected invariants;
- persistence append-only/hash-chain semantics;
- `can_activate=False`;
- `can_rollback=False`;
- no autonomous promotion;
- no Genesis implementation;
- no JustifiedAuthority implementation yet.

REQUIRED_TESTS:
- new focused failure-path regression test;
- relevant runtime/evolution suite;
- complete pytest/CI verification.

ACCEPTANCE:
- deterministic failure is observed by the real sandbox;
- failure is not converted into success;
- evidence/provenance/audit survives;
- no canonical Core mutation occurs;
- no authority/authorization is granted;
- CI is green before DONE.

AUDIT:
Classify every failure as production defect, test/fixture defect, or architectural contradiction. Do not weaken the boundary to make the test pass.

NEXT:
After this failure-path gate is green, perform the complete Reflection → Candidate → Sandbox → Evidence → Review vertical integration test. Only then reconsider the Proof/Authority mathematical implementation boundary.

#### Handoff note

The mathematical stopping-rule discussion remains active, but implementation is no longer blocked on solving Genesis minimality. The repository already contains a concrete bounded runtime contract compatible with the current research model. Therefore future work should alternate:
1. one concrete evidence-backed runtime task;
2. real CI verification;
3. reverse-analysis only where a concrete architectural dependency remains unresolved.

Do not return to an open-ended "reduce primitives further" loop without a measurable deletion/reduction criterion.


## 2026-09-19 — Runtime reverse-analysis progress checkpoint

### Current verified state
- Working branch: `runtime-slice-001`.
- Gap Detection contract is verified by CI through the current sequence ending at **CI 671: 314 passed**.
- Verified Gap properties:
  1. identical history produces identical Gap identity;
  2. irrelevant evidence/noise does not change the Gap;
  3. breaking a repeated material pattern removes the Gap;
  4. replacing one repeated material pattern with another produces a different Gap.
- Important semantic correction from CI 667–671: Gap identity represents a repeated pattern, not arbitrary whole-history identity. Changing one record while preserving the same repeated pattern need not change the Gap.
- Capability Synthesis positive-path contract verified at **CI 672: 317 passed**:
  - deterministic for the same Gap;
  - operation ordering does not alter capability identity;
  - `source_gap_id` is bound to the source Gap;
  - provenance/source records and target conflicts remain Gap-bound;
  - missing dependencies are explicit;
  - `can_activate=False`.
- A deliberate fabricated-`GapHypothesis` test produced **CI 674: 318 passed, 1 failed**. This established a real architectural fact: `CapabilitySynthesizer` accepts a `GapHypothesis` object without proving that it was produced by `GapDetector`. Do NOT treat this as a production defect automatically.
- Reverse-analysis found existing provenance infrastructure (`gnosis/evolution/provenance.py`, `ProvenanceCrossCheck`, evidence/provenance contracts), but that infrastructure primarily protects execution/evidence/candidate provenance downstream; it does not independently attest that a GapHypothesis was detector-produced.
- Therefore do NOT introduce a new `VerifiedGap` primitive yet. Current reasoning is that Capability is explicitly a non-authoritative hypothesis, and downstream promotion remains review-only/non-activating.
- Current Core `Candidate` is independently identity-bound by `parent_state_id`, proposed-state content identity, origin, seed, and a `binding_digest` tied to parent-state digest. PromotionCandidate/PromotionGate both expose `can_activate=False`.
- The remaining open executable boundary is:
  `CapabilityHypothesis -> Candidate -> Evaluation -> Provenance -> PromotionGate`.
  Specifically verify whether the Capability/Gap provenance is preserved or independently revalidated before Candidate/evolution can proceed.
- Current overall progress estimate: **~98.2%**. Keep percentage updates explicit in every continuation.
- Do not return to already closed Gap Detection unless new evidence contradicts the verified contract.
- Do not resolve the Genesis/JustifiedAuthority philosophical question as a prerequisite for this runtime work. Continue with executable contracts and CI evidence.

### CI lessons from this session
- CI failures were used to correct test assumptions rather than to alter production semantics blindly.
- The actual `GapDetector.detect()` API returns a tuple of GapHypotheses.
- Material Gap change must alter the repeated pattern itself, not merely mutate one record that leaves the same repeated pattern intact.
- Existing provenance should be reused before proposing new primitives.

### Next task
Reverse-audit the actual producer/consumer path from `CapabilityHypothesis` to `Candidate`. Establish:
1. where Candidate is constructed;
2. whether Capability provenance/source_gap_id is preserved;
3. whether Candidate creation requires an independent verification/evidence step;
4. whether any fabricated Capability can reach a state-changing path;
5. add only the minimum executable test/implementation required by the discovered contract.
