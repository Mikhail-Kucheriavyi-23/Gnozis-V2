# Gnozis-V2 — User Context / Core Integration Direction

## Status

`ARCHITECTURE / DIRECTION — IMPLEMENTATION NOT YET AUTHORIZED BY THIS DOCUMENT`

This document translates the user-centered architecture into repository-facing architectural boundaries. It does not claim that the runtime contracts below already exist.

## 1. Problem being solved

A user may work with Gnozis through many terminals and products:

- AI assistants;
- mobile applications;
- GitHub;
- Google Drive;
- work chat;
- CRM/ticket systems;
- research and data tools;
- future Gnozis-native agents.

The user must be able to switch terminals without losing the real state of a task.

The canonical continuity therefore belongs to the Gnozis project/user context, not to a particular AI conversation.

## 2. Target logical architecture

```text
External interfaces / terminals / connectors
                    ↓
             Identity / scope
                    ↓
        Capability + routing policy
                    ↓
        User / Organization / Task
                    ↓
          Canonical Context layer
                    ↓
       Memory / Evidence / Provenance
                    ↓
             Core adapter
                    ↓
                 Ψ-Core
                    ↓
       Verified result / state change
                    ↓
          Output routing / handoff
                    ↓
        User / terminal / work system
```

The arrows represent explicit contracts, not unrestricted access.

## 3. Canonical continuity object

The future runtime needs a durable task/context representation sufficient for another authorized terminal to resume work.

At minimum it must be able to resolve:

```text
project_id
organization_scope (optional)
user_scope
 task_id
objective
current_task_state
required_inputs
relevant_context_references
implementation_state
verification_state
evidence/provenance references
available_capabilities
allowed_data_sources
allowed_output_destinations
unresolved_findings
next_permitted_action
updated_at
```

The exact schema is a future implementation task. This document establishes the required semantics, not a premature storage schema.

## 4. Context recovery contract

A new terminal should be able to ask for a task and receive a compact, evidence-aware handoff:

```text
TASK
  ↓
canonical current state
  ↓
what exists
what was verified
what was only reported
what remains unresolved
what data may be accessed
what outputs may be produced
what action is permitted next
```

Conversation history may improve usability but must not be the sole recovery mechanism.

## 5. Data routing contract

A connector being available does not mean its data is automatically eligible.

The system must distinguish:

```text
source exists
    ↓
source connected
    ↓
source authorized for user
    ↓
source authorized for task
    ↓
data class authorized
    ↓
data actually selected/used
```

This is required for the planned organization + personal-tool model.

Example:

```text
Company task
 ├─ Work GitHub       → allowed
 ├─ Work Drive        → allowed
 ├─ Personal Drive    → denied
 └─ Personal calendar → allowed only for an explicitly permitted class
```

## 6. Output routing contract

A result must also have a destination policy.

```text
verified result
      ↓
recipient scope
      ↓
allowed result/data class
      ↓
allowed channel
      ↓
delivery
```

Example:

```text
Mobile app       → full result
Work chat        → summary
Personal channel → denied
```

This prevents a connected output channel from becoming an implicit data exfiltration path.

## 7. Organization and personal scope

The architecture must support both:

```text
organization-owned context
```

and:

```text
user-owned context
```

without merging them merely because the same user can access both.

A future authorization layer must define which scopes may intersect for a particular task. This document does not implement authentication or authorization.

## 8. Core boundary

The context layer must not become a second Ψ state machine.

The intended relationship is:

```text
Context / Task / Evidence
          ↓
     explicit adapter
          ↓
       Ψ-Core
```

The adapter may translate an authorized task into Core inputs and translate verified Core outcomes into durable evidence/result records.

It must not:

- create a parallel `State` abstraction with competing semantics;
- mutate Core state outside Core contracts;
- embed an AI model inside Ψ-Core;
- let a connector redefine Core evolution rules;
- turn conversation history into hidden Core state.

## 9. Memory boundary

Memory is a supporting persistence/evidence mechanism, not automatically the canonical Ψ state.

The current Memory implementation remains `NOT ACCEPTED` until its independent corrective audit is complete. Future context work must therefore define its contracts independently and then integrate with the accepted Memory contract through explicit adapters.

## 10. Repository direction

Future repository structure may converge toward logical areas such as:

```text
interface/ or interfaces/
identity/
capabilities/
context/
tasks/
routing/
memory/
provenance/
core/
```

These names are architectural candidates, not permission to create all modules immediately.

Before adding runtime modules, each area requires a bounded implementation task defining:

- contract;
- source of truth;
- allowed dependencies;
- forbidden dependencies;
- persistence boundary;
- security boundary;
- tests;
- independent verification criteria.

## 11. First implementation slices

When implementation resumes, the preferred order is:

1. canonical task identity and resumable task record;
2. context reconstruction/read contract;
3. evidence/provenance references;
4. capability discovery without implicit authority escalation;
5. data-routing policy;
6. output-routing policy;
7. terminal-independent handoff;
8. explicit adapter into Core;
9. integration with accepted Memory;
10. end-to-end multi-terminal runtime test.

Identity/authentication/authorization and encryption remain separate security phases and must not be faked by simple `owner_id` fields.

## 12. Acceptance boundary

No architectural direction in this document is considered implemented merely because a directory, class, or API exists.

Each slice must follow:

```text
explicit task
  ↓
bounded implementation
  ↓
real tests
  ↓
independent adversarial audit
  ↓
correction
  ↓
re-audit
  ↓
ChatGPT integration gate
```

## 13. Target outcome

A user should eventually be able to receive a task in one system and continue it in another without asking the new AI to reconstruct the project from conversation history.

The system should be able to answer, from canonical durable context:

> What is happening, what is actually known, what evidence supports it, which data may be used, where the result may go, and what can be done next?

That is the repository-facing architectural direction for the user-centered Gnozis model.
