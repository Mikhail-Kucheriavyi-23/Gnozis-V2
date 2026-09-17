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

## User-centered architecture direction

The development target is broader than a multi-agent coding workflow. Gnozis is being shaped as a **user-owned continuity architecture**.

The fundamental product property is:

> **The user owns the continuity of the work; AI terminals and connected products are replaceable interfaces to that continuity.**

A user may interact with the same project, task, evidence, data, and accumulated context through different AI products, mobile applications, work systems, or other connected terminals. A new terminal must be able to recover the canonical state without relying on the previous chat transcript.

The intended flow is:

```text
USER / ORGANIZATION
        ↓
TASK / EVENT
        ↓
CANONICAL CONTEXT
        ↓
CAPABILITIES + DATA ROUTING POLICY
        ↓
CONNECTED DATA / TOOLS / AI TERMINAL
        ↓
CORE / EXECUTION
        ↓
VERIFIED RESULT
        ↓
PROVENANCE / MEMORY
        ↓
OUTPUT ROUTING POLICY
        ↓
USER / AUTHORIZED TERMINAL / WORK SYSTEM
```

This direction is now a canonical architectural requirement for subsequent design and implementation tasks. It does **not** mean that all corresponding runtime components are already implemented.

### Any terminal must be replaceable

A user may start a task in one AI terminal, receive a notification through another product, continue analysis from a mobile application, and later resume implementation from another AI system.

The terminal is not the context. The connector is not the context. The chat transcript is not the context.

```text
canonical Gnozis context
        ≠
terminal-local context
        ≠
connector-local state
        ≠
conversation history
```

The durable project/task context must record, as applicable:

- user/organization scope;
- task identity and objective;
- current implementation state;
- verification state;
- evidence and provenance;
- relevant data/context;
- available capabilities;
- allowed data sources;
- allowed output destinations;
- unresolved findings;
- next permitted action.

### Broad user spectrum, one Core

The same architecture must support different classes of users without creating separate Core engines:

```text
Manager
Programmer
Engineer
Analyst
Physicist / Researcher
```

The specialization comes from:

```text
task + context + data + capabilities + authorized tools
```

not from a profession-specific replacement for Ψ-Core.

### Organization / CRM mode

Gnozis should also be usable by a company as a shared intelligence/continuity layer around existing work systems such as CRM and work chat.

For example:

```text
WORK CHAT / CRM / TICKET
        ↓
TASK / NOTIFICATION
        ↓
GNOZIS TASK REFERENCE
        ↓
USER DATA-ROUTING POLICY
        ├── GitHub: allowed
        ├── Work Drive: allowed
        ├── Personal Drive: denied for this task
        └── Other source: limited by data class
        ↓
ANALYSIS / CALCULATION / VERIFICATION
        ↓
RESULT + EVIDENCE + PROVENANCE
        ↓
OUTPUT-ROUTING POLICY
        ├── Mobile app: allowed
        ├── Work chat: summary only
        └── Personal channel: denied
```

Organization-level policy remains authoritative within the organization's scope. User-controlled personal sources must not become implicitly visible to an organization merely because the user connected them to Gnozis.

This is an architectural target, not a claim of existing CRM integration.

### Data routing is a first-class concept

The architecture must distinguish:

```text
available data
        ≠
data authorized for this task
        ≠
data actually used
        ≠
result authorized for a recipient
```

Connection alone does not imply permission to use every available source for every task.

Likewise, producing a result does not imply permission to deliver that result to every connected terminal or system.

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
- work chat / CRM / ticket systems — organizational task and event sources;
- user-authorized personal tools — optional data sources subject to explicit routing policy;
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

Changes to Ψ-Core, persistence contracts, trust boundaries, identity, security, context continuity, routing, and other architectural invariants require an explicit task and acceptance gate.

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

This is especially important for future Memory, Identity, Bridge, Agent, Federation, Context, Routing, and Evolution work.

The rule is:

> **Runtime interaction can influence the next design iteration, but runtime convenience must not silently redefine Ψ-Core invariants.**

Observed behavior may reveal a missing invariant, a useful interface, or a necessary contract change. Such a change must then be explicitly documented and gated before becoming part of the canonical architecture.

## Repository/Core architectural direction

The repository is now expected to evolve toward explicit layers around Ψ-Core rather than allowing each connector or AI product to invent its own context model.

The intended logical boundary is:

```text
interfaces / terminals / connectors
              ↓
       identity + capability
              ↓
       user/task/context layer
              ↓
       data + output routing
              ↓
       Memory / evidence / provenance
              ↓
       Core contract boundary
              ↓
            Ψ-Core
```

This is a logical architecture, not a requirement to create all directories immediately.

The next architectural work should define stable contracts for:

1. durable task identity and resumption;
2. canonical context reconstruction;
3. capability discovery and scoped connector access;
4. data-routing and output-routing policy;
5. provenance/evidence attached to results;
6. terminal-independent handoff;
7. organization/user scope separation;
8. explicit Core boundary adapters.

No connector should write a second state model into Ψ-Core. No AI terminal should become a hidden owner of canonical context.

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
