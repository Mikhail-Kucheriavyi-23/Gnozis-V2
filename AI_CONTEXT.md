# Gnozis-V2 — AI Context

## Canonical repository

- Canonical development repository: `Mikhail-Kucheriavyi-23/Gnozis-V2`
- `AI_CONTEXT.md` is the operational handoff document.
- Current scope: SINGLE OWNER / SINGLE ACCOUNT / SINGLE PROJECT.
- Multi-user, federation, tenant and public-network runtime remain future strategy only.

## Current verified engineering state

- Ψ-Core remains authoritative for state/evolution semantics.
- Persistence and append-only audit storage are implemented in `main`.
- Reflection is implemented as a read-only layer outside Ψ-Core.
- `TransitionRecord` carries `test_rule_id` provenance.
- Persistence preserves `test_rule_id` through SQLite round-trip.
- Backward-compatible persistence migration preserves older data with `test-rule:unspecified` when provenance did not exist.
- Proposal lineage and diagnostic artifact serialization exist.
- A reproducible Self-Diagnostic workflow exists.
- **A real GitHub Actions Self-Diagnostic run has NOT yet been verified.** Do not claim `SELF-DIAGNOSTIC-0001` exists or that CI passed until an actual run and artifact are inspected.

## Current critical objective

Obtain the first genuine self-reflection result from Gnozis before adding further reflection architecture.

```text
Core execution
  ↓
TransitionRecord
  ↓
persistent evidence
  ↓
load/recovery
  ↓
Self-Diagnostic
  ↓
SELF-DIAGNOSTIC-0001
  ↓
independent analysis
  ↓
architecture corrections
```

The diagnostic must use real persisted transition evidence, not an empty/new Engine and not fabricated findings.

## Self-reflection architecture

```text
L0 Ψ-Core
    ↓
L1 Observation / evidence / provenance
    ↓
L2 Findings / counterexamples / RuleProposals / proposal lineage
    ↓
L3 Shadow / invariant-delta / governance
    ↓
L4 Endogenous evolution (future only)
```

Protection rules:

- Reflection cannot mutate canonical Core.
- RuleProposal cannot activate itself.
- `NO_COUNTEREXAMPLE_FOUND` is not proof of correctness.
- No AI model belongs inside Ψ-Core.
- No second state model may be introduced.
- Autonomous self-modification remains forbidden until R1-R5 are independently verified.

## Provenance requirement

Reflection must not invent causality. If a transition contains an exact `test_rule_id`, reflection may attribute evidence to that rule. If provenance is absent, the result remains `UNSPECIFIED` rather than guessing.

```text
Finding
  ↓
evidence refs
  ↓
TransitionRecord.test_rule_id
  ↓
CausalCandidate
  ↓
RuleProposal.target
```

## Self-Diagnostic experiment

Workflow:

`.github/workflows/self-diagnostic.yml`

The workflow is intended to:

1. install the project;
2. run reflection/provenance/diagnostic tests;
3. create a real `Instance` and `Engine`;
4. produce repeated rejected transitions using a named diagnostic Test rule;
5. persist the transitions into SQLite;
6. verify the durable graph;
7. reload persisted `TransitionRecord` history;
8. call `diagnose(history)`;
9. serialize `SELF-DIAGNOSTIC-0001.json`;
10. upload the artifact.

The controlled scenario uses repeated `policy:bad-element` rejections associated with `test-rule:diagnostic-policy`, followed by an accepted transition. This validates the reflection path; it is not proof that the diagnostic rule is defective.

## Required diagnostic review

When `SELF-DIAGNOSTIC-0001.json` becomes available, inspect:

- Findings;
- evidence references;
- exact `test_rule_id` attribution;
- causal candidates;
- counterexample results;
- RuleProposals;
- proposal lineage;
- limitations / `UNSPECIFIED` cases;
- whether each proposal follows from evidence;
- whether the diagnostic itself has false positives.

Classify every finding as:

```text
CORE BUG
ARCHITECTURAL GAP
MISSING INVARIANT
MISSING TEST
FALSE POSITIVE
INSUFFICIENT EVIDENCE
FUTURE FEATURE
```

Do not implement a proposed Core change merely because the diagnostic proposes it.

## Immediate next actions

1. Obtain and inspect the actual Self-Diagnostic GitHub Actions run for the latest `main` commit.
2. Inspect the uploaded `SELF-DIAGNOSTIC-0001.json` artifact.
3. If workflow fails, fix the concrete failure and rerun; do not bypass the test.
4. If it succeeds, analyze the diagnostic output before adding new reflection architecture.
5. Define the smallest next architectural correction from evidence.
6. Keep AI_CONTEXT.md and STATUS.md synchronized with implementation and verification state.

## Persistence provenance

`TransitionRecord.test_rule_id` is part of the durable evidence chain. Transition identity includes the rule id, preventing otherwise identical transitions under different rules from collapsing into one identity.

Older persisted transitions that predate explicit rule provenance use `test-rule:unspecified`. They must not be retroactively attributed to a specific rule without evidence.

## Scope and authority

Current scope is one owner/account and one canonical repository. Other AI systems may implement or audit bounded tasks, but the project owner/ChatGPT integration gate retains architectural authority.

Evidence hierarchy:

1. current source;
2. reproducible runtime behavior and real tests/CI;
3. accepted invariants/contracts;
4. independent audit evidence;
5. AI reports/proposals.

Never claim PASS/implemented/complete from documentation alone.
