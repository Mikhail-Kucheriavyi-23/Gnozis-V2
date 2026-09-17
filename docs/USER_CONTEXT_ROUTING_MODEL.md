# Gnozis-V2 — User Context & Result Routing Model

Status: architecture target; implementation must be introduced through explicit bounded phases.

## Purpose

Gnozis is intended to operate as a user-controlled analytical core that can be reached through many connected products. The same user may create, continue, inspect, or delegate work from different AI terminals, mobile applications, work chats, CRM systems, or specialist tools.

The connected product is an interface, not the canonical context owner.

## User spectrum

The architecture must not assume one technical user type. A user may be:

- manager requesting operational summaries;
- developer working on a repository;
- researcher coordinating evidence;
- engineer solving a technical problem;
- scientist processing large datasets;
- organization routing work between teams and systems;
- automated or semi-automated client operating within explicitly granted capabilities.

The core contract is therefore based on **identity, task, context, capabilities, evidence and routing policy**, not on the UI product used to reach it.

## Context model

A user may have many simultaneous contexts:

```text
User
 ├── Project A
 │    ├── Task A1
 │    ├── Task A2
 │    └── Task A3
 ├── Project B
 │    └── Task B1
 └── Personal / analytical contexts
      ├── Task C1
      └── Task C2
```

Each task must be recoverable independently. A terminal should not need the full conversation that originally created the task.

## Result model

A result is not merely text. Future runtime should preserve:

```text
Result
 ├── task_id
 ├── producer / execution context
 ├── result payload or reference
 ├── evidence
 ├── verification state
 ├── timestamp / sequence
 ├── confidentiality scope
 └── routing policy
```

A product may render the same result differently for different users, but rendering must not silently change the canonical result or its verification state.

## Routing example

An organization could connect a work-chat bot to Gnozis. A user could configure in a mobile client that:

```text
incoming task/result
        ↓
classification / policy
        ├── manager → concise operational summary
        ├── engineer → technical evidence
        ├── scientist → dataset / calculations / provenance
        └── restricted recipient → no payload or redacted payload
```

The routing policy belongs to the authorized user/organization configuration. The external chat or AI product does not acquire authority merely by receiving a routed message.

## Context continuity

When a user changes product:

```text
Product 1
   ↓
Task + context + evidence persisted
   ↓
Product 2
   ↓
resolve same task
   ↓
restore canonical state
   ↓
continue
```

The continuation must distinguish:

- implementation state;
- verification state;
- acceptance state;
- pending work;
- available capabilities;
- restrictions.

## Separation of concerns

```text
Connector / Product
    = transport + presentation

Routing policy
    = who may receive which result

Task/context layer
    = durable work continuity

Capability layer
    = what an actor is allowed to request/do

Evidence layer
    = what actually happened and how it was verified

Gnozis Core
    = canonical evolution / analytical semantics
```

No connector should become a hidden second Core.

## Security boundary

Possessing access to GitHub, Google Drive, a chat application, or another connected service is not equivalent to authorization over Gnozis data or operations.

Future implementation must explicitly resolve:

```text
actor identity
→ requested capability
→ target task/context
→ data scope
→ operation scope
→ evidence requirements
→ routing policy
```

## Architectural rule

The system should be useful before full autonomy exists. A user may already connect multiple tools and use Gnozis as a common context/evidence layer while the stronger identity, authorization, federation, encryption, and autonomous-agent mechanisms are implemented and independently verified in later phases.

## Implementation consequence

Do not implement product-specific adapters directly against Core. Adapters should terminate at stable contracts around task/context, capabilities, routing and evidence. This permits new products to be added without redesigning Ψ-Core.
