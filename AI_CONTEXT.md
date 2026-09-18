# Gnozis-V2 — AI Context

## 0. PURPOSE / OPERATING RULE

This file is the operational handoff for AI agents working on Gnozis-V2.

Repository:
- GitHub: Mikhail-Kucheriavyi-23/Gnozis-V2
- default branch: main
- current HEAD inspected: 63e1f0b57c591a06fa902fe63cd84369c30bf65c

Rules:
1. Repository code, tests and actual runtime/CI evidence outrank chat memory or this document.
2. This document is architecture/task context, not proof of PASS.
3. Never claim a test, CI run, artifact, recovery result or security property was verified unless it was actually executed/inspected.
4. Select exactly one highest-priority READY task at a time.
5. Do not broaden a task into unrelated architecture.
6. Preserve evidence: rejected, failed, quarantined and insufficient-evidence outcomes are historical data, not noise.
7. Never weaken an invariant, persistence constraint or evidence gate merely to make tests green.

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

Implementation status: **IMPLEMENTED — CI isolated final persistence column/placeholder mismatch; fixed.**

Trusted recovery now requires the recovered/provided `State` and independently recomputes `State.content_id`, comparing it to persisted `proposed_state_content_id`. A missing proposed state fails closed. Recovery tests were updated to exercise actual State content reconciliation and tampering remains rejected.


### GNV2-EVOLUTION-STATE-PROVENANCE-LINK-027

Implementation status: **IMPLEMENTED — awaiting CI verification**.

The existing `Candidate.binding_digest(parent_state_digest)` is now elevated into persisted provenance as `candidate_binding_digest`. Provenance identity includes the binding; persistence stores/migrates it; chain verification and recovery reconstruct it. New provenance requires a non-empty candidate binding digest, preventing a proposed state/content identity from being trusted without an explicit parent→candidate→proposed-state transition binding.
