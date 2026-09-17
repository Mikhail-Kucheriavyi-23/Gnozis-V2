# Gnozis-V2 — Core Proposal Ingress Contract

Status: architecture contract; implementation not yet accepted.

## Purpose

Define how tasks originating from users, AI terminals, connectors, research tools, or organizational systems can reach Ψ-Core without allowing those external systems to mutate Core state directly.

## Boundary

```text
External product / agent
        ↓
Observation / analysis
        ↓
Proposal
        ↓
Core ingress boundary
        ↓
Candidate
        ↓
Test
        ↓
Verify
        ↓
Commit
        ↓
Ψ-State'
```

The external actor may propose. Only the Core evolution path may commit semantic Core state.

## Proposal

A proposal should be treated as an auditable envelope, not as Core state.

Minimum conceptual fields:

```text
proposal_id
task_id
actor_id
source_connector
source_context_snapshot
parent_state_id
candidate_payload
intent
scope
capability_refs
evidence_refs
created_at
sequence
```

The exact persistence model is a separate implementation task.

## Parent-state binding

A proposal intended for Core evolution must identify the Core state from which its candidate was derived:

```text
proposal.parent_state_id == current Core state
```

A stale proposal must not silently overwrite newer Core state.

The existing Engine already rejects a candidate whose `parent_state_id` does not match the current state. The ingress layer must preserve, not bypass, this invariant.

## External evidence

External evidence may support a proposal:

```text
GitHub diff
research result
calculation
user instruction
AI analysis
runtime observation
file artifact
```

Evidence supports evaluation; it does not constitute acceptance by itself.

## Capability boundary

The ingress layer must distinguish:

```text
actor identity
requested capability
authorized capability
proposal scope
Core acceptance
```

Possessing a GitHub/Drive/chat connector does not imply permission to evolve Core.

## No direct mutation

The following patterns are prohibited:

```text
connector → Core State mutation
agent → Core State mutation
chat → Core State mutation
memory → Core State mutation
notification → Core State mutation
```

Required pattern:

```text
source → proposal → Core validation → Test → Verify → Commit
```

## User intent

A user request may create a proposal, but natural-language intent must not be treated as a verified Core transition.

For example:

```text
"change the state"
```

is an input to proposal generation, not an authorization to mutate Core.

## Multi-agent behavior

Multiple agents may generate proposals for the same task and parent state:

```text
Agent A ─┐
         ├→ proposals → evaluation
Agent B ─┤
Agent C ─┘
```

The system must preserve proposal provenance and competing evidence. It must not select a proposal merely because it was produced first, by a particular vendor, or by the majority of agents.

Selection remains subject to the Core's explicit Test/Select/Verify rules and project policy.

## Stale proposal handling

If the parent state has advanced since proposal creation:

```text
proposal.parent_state_id != current_state_id
```

then the proposal must be rejected or explicitly re-derived. It must not be applied against a different parent state implicitly.

## Human gate

A proposal may require an explicit human decision depending on task policy. Human acceptance is distinct from technical verification.

```text
verified
    ≠
accepted
```

The external orchestration layer must preserve this distinction.

## Core preservation rule

This contract deliberately does not require changing `gnosis/core/*` semantics.

The existing Core contract remains:

```text
Generate → Test → Select → Evolve
```

with verification and invariant checks guarding state commitment.

Any future change to endogenous generation, population/mutation, selection semantics, invariants, budget semantics, or state representation requires a separate explicit Core architecture task.

## Initial implementation target

The first implementation should be outside `gnosis/core/*` and should provide:

1. a durable proposal envelope;
2. parent-state binding;
3. evidence references;
4. capability/scope references;
5. stale-proposal rejection;
6. an adapter that hands only validated candidates into the existing Core entry point;
7. tests proving that the adapter cannot directly mutate Core state.

## Acceptance gate

The implementation is not accepted merely because proposals can be stored.

Required evidence includes:

```text
real tests
Core isolation tests
stale-parent test
multi-agent competing-proposal test
proposal provenance test
negative test for direct mutation
```

The implementation must remain independently auditable and must not silently alter the semantics of `gnosis/core/*`.
