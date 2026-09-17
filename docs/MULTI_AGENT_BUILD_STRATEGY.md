# Gnozis-V2 — Multi-Agent Core-Building Strategy

## Purpose

Gnozis is developed as a real, continuously tested system rather than as a design that is completed in isolation before runtime work begins.

The project uses the user's available AI systems and connected data surfaces as part of the engineering environment. Their observations, implementations, tests, failures, and independent audits become evidence for the next iteration of the system.

This document records the operating strategy as of 2026-09-17.

## Core principle

> **Build the core, test the core through real use, audit every meaningful change, and let verified interaction between independent AI agents inform the next engineering iteration.**

The strategy is deliberately empirical:

```text
architecture / invariant
        ↓
bounded task
        ↓
AI implementation
        ↓
real execution and tests
        ↓
independent adversarial review
        ↓
correction
        ↓
ChatGPT integration / final gate
        ↓
verified project context
        ↓
next task
```

The system is therefore not treated as a static specification followed by a one-time implementation. The implementation process itself is a controlled source of engineering evidence.

## Multi-agent operating model

### ChatGPT

Architecture, integration and final gate:

- maintains Ψ-Core invariants and architectural boundaries;
- defines bounded phases and acceptance criteria;
- decides which findings require correction;
- reconciles evidence from multiple AI systems;
- accepts, rejects, or returns a phase for correction;
- keeps the project context synchronized.

### Claude

Primary implementation engineer for large bounded tasks unless explicitly reassigned:

- implements the assigned phase;
- writes tests and technical documentation;
- performs local/runtime validation available in its environment;
- reports implementation and limitations without overstating verification;
- does not silently expand the architecture beyond the task.

### Manus

Independent engineer and adversarial reviewer:

- reviews the actual artifact rather than accepting implementation reports as proof;
- executes independent tests where possible;
- searches for boundary violations, hidden coupling, incomplete invariants, and unsupported claims;
- may perform explicitly assigned corrective work;
- does not grant final acceptance.

### Gemini and other connected AI systems

Any additional AI system with authorized access to project resources may participate as:

- implementation contributor when explicitly assigned;
- independent auditor;
- source of alternative designs or counterexamples;
- runtime observer;
- research input for the next iteration.

Its findings are evidence, not authority. The same source-of-truth rules apply to every agent.

## Connected resources

AI systems may be connected to project resources such as:

- GitHub — canonical source, branches, tests, CI, review history;
- Google Drive — exchange of archives, audit reports, snapshots, and other artifacts;
- other explicitly authorized project interfaces.

Access is intentionally broader than write authority.

> **Repository or Drive access does not by itself grant permission to modify the canonical core.**

Write authority remains task-scoped and must be explicit.

## Source-of-truth and evidence hierarchy

When agents disagree, use this order:

1. actual repository source at a pinned commit;
2. reproducible runtime behavior and real tests/CI;
3. explicit project invariants and accepted contracts;
4. independent audit evidence;
5. implementation reports, design proposals, and AI opinions.

A claim such as `PASS`, `implemented`, or `complete` is not evidence by itself.

Archives are valid engineering artifacts when their exact contents can be inspected and reproduced. A textual summary of an archive is not a substitute for the archive.

## Human authority boundary

The user remains the human authority for the project direction and authorization of meaningful changes.

AI agents can propose, implement, test, challenge, and report. They do not acquire architectural authority merely because they have repository or cloud-storage access.

This distinction is essential as Gnozis moves toward multi-agent operation and eventual self-improvement.

## Safe write model

The project should prefer:

```text
broad observation / read access
            ↓
bounded implementation authority
            ↓
independent verification
            ↓
final integration gate
```

rather than:

```text
broad access = unrestricted write authority
```

Changes to Ψ-Core, persistence contracts, trust boundaries, identity, security, and other architectural invariants require an explicit task and acceptance gate.

## Phase lifecycle

Every substantive phase follows:

```text
1. Task definition
2. Baseline pinning
3. Primary implementation
4. Real tests / runtime execution
5. Independent adversarial review
6. Corrective pass
7. Independent re-review
8. ChatGPT final gate
9. Documentation/status synchronization
10. Next phase
```

A phase may be returned to implementation repeatedly. A green implementation report is never a substitute for the independent review or final gate.

## Building and testing the core simultaneously

The project intentionally does not require every future subsystem to be designed and implemented before the core is exercised.

Instead, each new layer is introduced as a bounded vertical slice where practical. The running system exposes real integration problems that pure design review can miss, while independent agents provide different failure modes and perspectives.

This is especially important for future Memory, Identity, Bridge, Agent, Federation, and Evolution work.

The rule is:

> **Runtime interaction can influence the next design iteration, but runtime convenience must not silently redefine Ψ-Core invariants.**

Observed behavior may reveal a missing invariant, a useful interface, or a necessary contract change. Such a change must then be explicitly documented and gated before becoming part of the canonical architecture.

## Multi-agent formation direction

The long-term objective is not merely to use several AI assistants around Gnozis. Gnozis itself is intended to become capable of operating with multiple agents and user-owned copies in a connected network.

The development workflow therefore serves as an early engineering experiment for that future architecture:

```text
Human
  ↕
AI agents
  ↕
Gnozis instances / copies
  ↕
shared protocols, evidence and trust boundaries
```

This diagram describes a development direction, not an assertion that federation, autonomous agents, identity, or secure delegation are already implemented.

## No implicit autonomy

Connected AI agents must not be treated as autonomous project owners merely because they can access GitHub or Google Drive.

Until capability, identity, authorization, auditability, rollback, and proof/invariant mechanisms are implemented and independently verified, autonomous modification of the canonical architecture remains outside the default authority model.

## Current practical workflow

For the current Gnozis-V2 work:

- Claude performs the main implementation task;
- Manus independently attacks and verifies the resulting artifact;
- Claude performs corrective passes when Manus identifies defects;
- Manus re-audits corrective work;
- ChatGPT performs the final integration gate;
- verified findings are written into project documentation;
- the next task is then defined from the verified state.

Additional connected AI systems can participate without changing this evidence hierarchy.

## Status rule

The project must distinguish:

- **implementation state** — `IMPLEMENTED / PARTIAL / MISSING / THEORETICAL`;
- **verification state** — `VERIFIED / UNVERIFIED / BLOCKED / NOT_APPLICABLE`.

Neither documentation nor an AI report may convert an unverified implementation into `IMPLEMENTED` merely by assertion.

## Relationship to future autonomous evolution

This strategy is also a controlled precursor to Gnozis self-improvement. Before Gnozis is allowed to modify itself, the project must establish explicit mechanisms for:

- identity and capabilities;
- authorization;
- proof/invariant checks;
- bounded operations;
- rollback;
- durable audit evidence;
- conflict resolution;
- human override;
- reproducible recovery.

Until those mechanisms are implemented and independently verified, multi-agent development remains human-authorized and externally governed.
