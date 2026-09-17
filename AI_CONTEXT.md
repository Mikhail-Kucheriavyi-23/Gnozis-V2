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

## Experimental evolution branch

Branch: `evolution-sandbox`

Implemented experimental stages:

1. `EvolutionHypothesis` — bounded hypothesis with target, rationale, expected effects and constraints.
2. bounded model generation — deterministic candidate models, maximum three per hypothesis.
3. `SandboxExperiment` — isolated experiment description; canonical Core mutation remains forbidden during sandbox work.
4. `SandboxEvaluator` — compares actual model evidence and selects the best passing model.
5. `SandboxExecution` / executable pipeline — runs each sandbox model through an injected runner and converts observations into `ModelEvidence`.
6. `PromotionCandidate` — descriptive candidate requiring passed evidence and invariant status `PRESERVED` or `IMPROVED`.

The next required bridge is:

```text
ModelEvidence
   ↓
existing Core invariant checks
   ↓
InvariantDelta
   ↓
PromotionCandidate
```

Do not invent a second invariant model.

## Recursive evolution target

```text
Core_n
 ↓ Reflection
EvolutionHypothesis
 ↓ bounded generation
Sandbox models A/B/C
 ↓ execution
Evidence
 ↓ evaluation
InvariantDelta
 ↓ Governance
PromotionCandidate
 ↓ full recursive re-evaluation
Core_(n+1)
 ↓ Reflection
 ↺
```

Promotion must be a distinct evidence-gated stage. It must not be an uncontrolled direct `patch → activate` operation.

## Verification discipline

- Runtime/CI tests are NOT considered passing until an actual runtime/CI result is inspected.
- Do not fabricate commits, files, test results, telemetry, or artifacts.
- Keep `main` and `evolution-sandbox` explicitly separated.
- Every major architectural checkpoint must update this file with the verified commit SHA.
