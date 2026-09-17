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

## Current promotion boundary

The next implementation stage is the **Promotion Engine**. It must be the first component allowed to materialize `Core_n → Core_(n+1)`, but only after:

- a valid `PromotionCandidate`;
- stable bounded recursive re-evaluation;
- valid parent Core state;
- deterministic proposed next state;
- complete provenance/rollback record.

Failure must leave `Core_n` unchanged.

Promotion must therefore be atomic and evidence-gated:

```text
PromotionCandidate
        +
Stable ReEvaluationResult
        +
CoreVersionDescriptor
        ↓
PromotionEngine
        ↓
validate
        ↓
construct Core_(n+1)
        ↓
write immutable promotion/provenance record
        ↓
commit canonical next state
```

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
 ↓ atomic Core_n → Core_(n+1)
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
