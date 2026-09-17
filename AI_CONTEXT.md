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

## Context integrity rule

If chat history and repository disagree, verified repository HEAD and actual runtime evidence take precedence. Never reconstruct current architecture from memory alone. Update this file whenever a major architectural gate is completed or a canonical HEAD changes materially.
