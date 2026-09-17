# Gnozis-V2 — AI Context

## CANONICAL BASELINE — HEAD PIN

- Canonical repository: `Mikhail-Kucheriavyi-23/Gnozis-V2`
- Canonical branch: `main`
- Verified baseline at this checkpoint: `a990a11e81c5a693ed3b2ac45f115954cad5ad5f`.
- Experimental endogenous-evolution work is on `evolution-sandbox`; it is not canonical main until explicitly reconciled and promoted.

## Current objective

Gnozis is intended to become capable of autonomous self-improvement through a **recursive evidence-backed evolution loop**. Autonomous modification is an intended capability; mandatory human approval of every mutation is not the architectural goal.

The safety boundary is not "never self-modify". It is:

```text
hypothesis
 → bounded model generation
 → sandbox execution
 → evidence
 → invariant analysis
 → governance
 → recursive re-evaluation
 → promotion
 → Core_(n+1)
 → reflection again
```

A candidate must earn promotion through evidence. A score alone is never sufficient evidence.

## Existing verified architecture

```text
Ψ-Core
  ↓
Evidence / Persistence / Recovery
  ↓
Reflection
  ↓
RuleProposal
  ↓
ShadowEvaluation
  ↓
InvariantDelta
  ↓
GovernanceDecision
  ↓
AuthorityRequest / provenance
```

Existing Core invariants remain canonical. Do not create a second invariant system inside `evolution/`.

## AI_CONTEXT as a self-descriptive reflection surface

`AI_CONTEXT.md` is not an authority source and must not be treated as ground truth merely because it says something about Gnozis. It is a serialized self-description surface whose claims are themselves eligible for observation, verification, rejection, contradiction analysis, and evolution.

The internal representation is introduced in `gnosis/reflection/context.py`:

```text
ContextClaim
   ↓
status: HYPOTHESIS / OBSERVED / VERIFIED / REJECTED
   ↓
provenance + evidence_refs
   ↓
ContextVersion
   ↓
ContextDelta
```

Therefore Gnozis must eventually be able to analyze questions such as:

- what it currently claims about itself;
- which claims are hypotheses versus verified facts;
- what evidence supports a claim;
- which claims changed between context versions;
- whether current runtime state contradicts the self-description;
- whether the self-description itself should evolve.

The context layer must remain descriptive and provenance-backed. It must never bypass Core invariants or governance.

## Experimental evolution branch

Branch: `evolution-sandbox`

Implemented experimental stages:

1. `EvolutionHypothesis` — bounded hypothesis with target, rationale, expected effects and constraints.
2. bounded model generation — deterministic candidate models, maximum three per hypothesis.
3. `SandboxExperiment` — isolated experiment description; canonical Core mutation remains forbidden during sandbox work.
4. `SandboxEvaluator` — compares actual model evidence and selects the best passing model.
5. `SandboxExecution` / executable pipeline — runs each sandbox model through an injected runner and converts observations into `ModelEvidence`.
6. `PromotionCandidate` — descriptive candidate requiring passed evidence and invariant status `PRESERVED` or `IMPROVED`.
7. bounded recursive re-evaluation — candidate evidence is independently re-run for up to three rounds; failed rounds stop evaluation and prevent stability.
8. `CoreVersionDescriptor` — immutable description of a proposed next Core version; it does not itself mutate canonical Core.
9. `gnosis/reflection/context.py` — self-descriptive context claims, versions, and deltas.
10. `PromotionEngine` — evidence-gated domain materialization of a distinct proposed Core state.
11. atomic promotion persistence — dedicated promotion provenance record, proposed state persistence, audit event and authoritative head update in one transaction.

## Current promotion boundary

The promotion boundary is split into two explicit layers:

1. `PromotionEngine` — validates evidence and materializes an immutable proposed `Core_(n+1)` at the domain boundary.
2. `persist_promotion` — atomically persists the promotion and advances the authoritative instance head.

Required gates remain:

- valid `PromotionCandidate`;
- stable bounded recursive re-evaluation;
- valid parent Core state;
- deterministic proposed next state;
- complete provenance/evidence digest;
- atomic persistence and rollback.

Failure must leave `Core_n` and the authoritative head unchanged.

Do not implement uncontrolled `patch → activate` behavior.

## Recursive evolution target

```text
Core_n
 ↓ Reflection
 ├─ Self-description / AI_CONTEXT claims
 └─ Runtime observations
 ↓
EvolutionHypothesis
 ↓ bounded generation
Sandbox models A/B/C
 ↓ execution
Evidence
 ↓ evaluation
InvariantDelta
 ↓ Governance
PromotionCandidate
 ↓ bounded recursive re-evaluation
 ↓ stable evidence
PromotionEngine
 ↓
atomic promotion persistence
 ↓
Core_(n+1)
 ↓ new ContextVersion / ContextDelta
 ↓ Reflection of the new self-description
 ↺
```

This creates the required second-order loop: Gnozis does not only evolve its Core; it can eventually analyze and evolve the principles by which it describes and justifies its own evolution.

## Verification discipline

- Runtime/CI tests are NOT considered passing until an actual runtime/CI result is inspected.
- Do not fabricate commits, files, test results, telemetry, or artifacts.
- Keep `main` and `evolution-sandbox` explicitly separated.
- `AI_CONTEXT` claims are evidence-bearing claims, not automatic truth.
- Every major architectural checkpoint must update this file with the verified commit SHA.

## Current implementation checkpoint — 2026-09-17

### Promotion Engine

Implemented on `evolution-sandbox`:

- `gnosis/evolution/promotion_engine.py`
- `tests/test_evolution_promotion_engine.py`

The engine validates, before materialization:

- `PromotionCandidate.can_promote`;
- stable bounded re-evaluation;
- descriptor readiness;
- parent-state identity;
- proposed-state identity;
- model identity;
- evidence-round count;
- non-no-op Core transition;
- candidate/evidence model consistency.

The engine has no persistence, subprocess, Git, or external authority side effect. It returns the already-constructed immutable proposed `State` only after all gates pass. A failed promotion leaves the supplied parent `State` untouched.

Commits:

- implementation: `598bb445637a2004cdc17857c421438e9ae2a40c`
- tests: `03dae8d507531f32d8ba472acfc31f6d1d863505`

### Promotion persistence

Implemented on `evolution-sandbox`:

- SQLite schema version `4` with dedicated `promotions` provenance table;
- `gnosis/evolution/promotion_persistence.py`;
- `tests/test_evolution_promotion_persistence.py`.

The persistence boundary:

```text
validate
 ↓
lock canonical head
 ↓
persist proposed state
 ↓
persist immutable promotion provenance
 ↓
append audit event
 ↓
advance authoritative head
 ↓
COMMIT
```

Any injected failure before commit rolls back the proposed state, promotion record, audit event and head update together.

Commits:

- schema: `8a23f99017a01a1ae77eb9bb6e4cf5ad3b113e7d`
- persistence: `4ff522634e0ddf736713221a3b7e9658e9f8cca0`
- tests: `0776078640f947d7c3eb8e76a9d908371ceaa159`

**Verification status:** `IMPLEMENTED / TESTS WRITTEN / RUNTIME NOT VERIFIED`.

No GitHub Actions workflow run is available for these commits, and the local environment cannot clone the repository because network/DNS access is unavailable. Therefore these tests MUST NOT be reported as PASS yet.

### Next task

`GNV2-PROMOTION-003 — Promotion recovery verification`

Required:

1. Extend durable-graph recovery to recognize promotion provenance as a valid authoritative-head transition.
2. Verify restart/recovery reconstructs `Core_(n+1)` after a committed promotion.
3. Verify an interrupted promotion leaves recoverable `Core_n` with no partially trusted `Core_(n+1)`.
4. Verify promotion audit/hash-chain evidence remains valid after recovery.
5. Add real runtime/CI verification before marking DONE.

Only after this gate is closed should promotion be considered a persistence-safe evolution capability.
