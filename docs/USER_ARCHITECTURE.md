# Gnozis-V2 — User Architecture

## Status

`ARCHITECTURE / DOCUMENTED — NOT YET IMPLEMENTED`

This document records the intended user-facing architecture. It is a design contract, not a claim that the runtime layers described here already exist.

## 1. Purpose

Gnozis is being built as a **user-centered architecture** in which a user can interact with the same project, task, data, and accumulated evidence through different connected products or AI terminals without losing the canonical context.

The same architecture may also be used as an **organizational/CRM intelligence layer**: an organization can feed work events, requests, notifications, and records into Gnozis, while individual users retain control over which of their authorized personal or professional data sources may participate in analysis and which results may be returned to them.

A connected product is an interface, connector, tool source, or execution environment around Gnozis. It is not automatically the source of truth and does not receive architectural authority merely because it has access to GitHub, Google Drive, a work chat, CRM, email, calendar, or another resource.

The target property is:

```text
Any authorized connected terminal
        ↓
recover canonical project/task context
        ↓
understand current verified state
        ↓
resolve the capabilities and data sources allowed for this request
        ↓
continue the task
        ↓
produce a result with provenance/evidence
        ↓
persist the result back into the shared project/user context
```

## 2. Context continuity is a first-class requirement

A new AI session must not need the previous conversation transcript to continue work.

The canonical context must be recoverable from durable project artifacts and verified state, including as applicable:

- project identity;
- organization/workspace identity;
- user identity and scope;
- task identity and scope;
- current task state;
- relevant context;
- current implementation state;
- verification state;
- evidence and provenance;
- available capabilities/connectors;
- data-routing permissions;
- output-routing permissions;
- permissions/delegation boundaries;
- unresolved findings and next permitted action.

Recovery must distinguish **what exists**, **what was verified**, and **what was merely reported**.

This extends the existing `AI_CONTEXT.md` / `STATUS.md` handoff model from project continuity to user/task continuity and, where applicable, organization/workspace continuity.

## 3. User / Task / Context / Capability model

The intended common abstraction is:

```text
USER / ORGANIZATION
        ↓
TASK
        ↓
CONTEXT
        ↓
CAPABILITIES + DATA ROUTING POLICY
        ↓
DATA / TOOLS / CONNECTORS
        ↓
CORE / EXECUTION
        ↓
VERIFIED RESULT
        ↓
PROVENANCE / MEMORY
        ↓
AUTHORIZED OUTPUT ROUTING
```

### User

Represents the human principal and the scope in which work is requested. A user is not equivalent to an AI terminal.

### Organization / workspace

Represents an optional shared work context such as a company, team, project group, or CRM workspace. Organizational data and user-controlled personal data must remain distinguishable by ownership, scope, and routing policy.

### Task

A bounded unit of requested work. A task records enough durable information to resume it independently of the terminal that originally received it.

A task should expose, at minimum:

- objective;
- scope;
- current state;
- required inputs;
- expected result/evidence;
- constraints;
- unresolved findings;
- next permitted action.

### Context

The information relevant to a task at a particular point in time. Context must be recoverable and provenance-aware rather than being treated as ephemeral chat history.

### Capability

A bounded ability available to the current terminal/session, such as reading a repository, reading a Drive document, executing a permitted calculation, or interacting with a connected service.

```text
Capability ≠ Authority
Resource access ≠ Architectural authority
```

A capability must be scoped and must not silently expand the task or redefine Core semantics.

### Data routing policy

Defines which authorized data sources may be supplied to a particular task or analysis. Connection alone does not imply that all available data is eligible for every task.

### Output routing policy

Defines which results, fields, evidence, notifications, or responses may be returned to which user, organization, terminal, or connected product.

The routing layer must preserve the distinction between:

```text
available data
        ≠
data authorized for this task
        ≠
data actually used
        ≠
result authorized for a recipient
```

## 4. Different users, one architecture

Gnozis must support a broad spectrum of users without creating a separate Core engine for every profession.

Examples include:

```text
Manager
  → project status, blockers, decisions, reports

Programmer
  → repository state, implementation, tests, debugging

Engineer
  → specifications, calculations, CAD/data, production constraints

Physicist / researcher
  → datasets, models, calculations, experiments, evidence

Analyst
  → structured data, comparisons, trends, reports
```

These are **usage contexts**, not separate Core architectures.

The specialization of a session should arise from:

```text
task + context + data + available capabilities + authorized tools
```

not from multiplying the Core into profession-specific engines.

## 5. Connected products are terminals/connectors

Google Drive, GitHub, AI terminals, work chats, CRM systems, research systems, calendars, data tools, and other products are intended to become connected interfaces/capability providers around the same user/project/organization context.

A connector may provide:

- data;
- documents;
- execution;
- observation;
- communication;
- task notifications;
- external-world access.

A connector does not become the canonical project state merely because it contains a copy of some information.

The architecture must preserve a distinction between:

```text
canonical Gnozis state
        ≠
connector-local state
        ≠
chat/session transcript
```

## 6. Organization / CRM use case

Gnozis may serve as an intelligence and continuity layer around an organization's existing CRM/work systems without requiring the organization to replace those systems.

Example:

```text
Work chat / CRM / ticket system
        ↓
organization task / notification
        ↓
Gnozis task reference
        ↓
authorized analysis context
        ↑
user-selected personal/professional connectors
        ↓
verified analysis / answer
        ↓
user-selected output channel
```

A company could, for example, send a bot notification or work-chat task into the Gnozis environment. The employee could then use their own authorized AI terminal or mobile application to request the current situation, analysis, calculation, or next action.

The employee's personal configuration would determine which connected sources may participate in that request and which classes of results may be returned. The organization may control organizational resources and policies within its scope; it must not silently acquire access to unrelated user-controlled data merely because the user connected that source to Gnozis.

This is an architectural target, not an implemented CRM integration.

## 7. Real-world interaction example

A task notification may arrive through one connected product. The user may then open any other authorized AI terminal and ask:

> What is the real current status of this task, and what evidence supports the answer?

The terminal should reconstruct the answer from the canonical task/project context and current evidence, rather than relying on its own previous conversation history.

A more advanced organization flow is:

```text
Company work chat
      ↓
Task / event notification
      ↓
Gnozis canonical task reference
      ↓
User's routing policy
      ├── GitHub: allowed
      ├── Work Drive: allowed
      ├── Personal Drive: not allowed for this task
      ├── Calendar: allowed
      └── Other source: allowed only for specified data class
      ↓
Analysis / calculation / verification
      ↓
Result + evidence + provenance
      ↓
User routing policy
      ├── Mobile app: allowed
      ├── Work chat: summary only
      └── Personal channel: prohibited for this result
```

The important property is that **the user can configure data and output routing explicitly**, while organization-level policy and security boundaries remain authoritative within the organization's scope.

## 8. Result model

A user request should not terminate at an unqualified generated answer.

The target result model is:

```text
Request
  ↓
Context reconstruction
  ↓
Capability + routing resolution
  ↓
Candidate / analysis / operation
  ↓
Test / verification where applicable
  ↓
Result
  ↓
Evidence + provenance
  ↓
Policy-checked output routing
  ↓
Durable task/project update
```

The strength of the result depends on the evidence available. The system must distinguish verified facts, observations, calculations, proposals, and unresolved claims.

## 9. Multi-terminal continuity

Multiple AI systems may work on the same project through different terminals:

```text
Terminal A ─┐
Terminal B ─┼──→ shared canonical context/state ←── connectors
Terminal C ─┤                                  ↑
Mobile app ─┘                                  │
                                             policies
```

The terminals are replaceable. The durable project/task context is not.

A terminal can disappear, reach a usage limit, or be replaced. The next terminal must be able to recover from durable artifacts and continue without reconstructing the project from conversational memory.

## 10. Notifications and task resumption

Notifications are entry points, not the canonical context.

A notification should identify or resolve to a durable task reference. From that reference an authorized terminal can recover the current task state, relevant context, evidence, allowed data sources, allowed outputs, and capabilities.

Target flow:

```text
Notification
  ↓
Task reference
  ↓
Canonical task state
  ↓
Context + evidence + routing policy
  ↓
User request
  ↓
Verified response / next action
```

## 11. Boundary with Ψ-Core

This architecture does not introduce a second state model into Ψ-Core.

The user/task/context/capability/routing layers are external architectural layers that must interact with Core through explicit contracts. They may organize work, permissions, evidence, and interfaces, but they must not silently redefine the mathematical or state semantics of Ψ-Core.

In particular:

- no AI model is inserted into Ψ-Core;
- connector access does not grant Core authority;
- task context is not a second `State` model;
- routing policy is not Core evolution logic;
- Memory is not accepted merely because a context layer needs it;
- Identity/capability security remains a separate explicit phase;
- autonomous modification remains blocked until its required safeguards are independently verified.

## 12. Development rule

This document records architecture only. It does not authorize implementation by itself.

Any runtime implementation must be introduced through the established project chain:

```text
explicit task
  ↓
bounded implementation
  ↓
independent verification
  ↓
correction
  ↓
re-verification
  ↓
ChatGPT integration gate
  ↓
context/status update
```

Runtime observations may refine this architecture, but a refinement becomes canonical only after explicit review and documentation.

## 13. Target architectural property

The long-term property being built is:

> **The user owns the continuity of the work; terminals and connected products are replaceable interfaces to that continuity.**

For organizations, the corresponding property is:

> **The organization can provide shared work context and tasks, while each authorized user can explicitly control which of their connected data sources participate in analysis and where resulting information may be delivered, subject to applicable organizational policy and security boundaries.**

Gnozis should therefore make project/task context portable across authorized terminals while preserving provenance, scope, evidence, data-routing policy, output-routing policy, and authority boundaries.
