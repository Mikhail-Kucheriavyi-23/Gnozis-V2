# DATABASE SCHEMA — GNOSIS 2.0 (spec section 37)

Status: DRAFT SCHEMA, NOT YET IMPLEMENTED AS CODE. No ORM/SQL migration
exists yet — `gnosis/storage/` is currently empty. This document fixes the
shape so Phase 3+ implementations don't invent divergent schemas.

Engine: SQLite for local/dev, designed to be Postgres-portable (no
SQLite-only types). Recommendation: SQLAlchemy Core (not ORM) — keeps
`gnosis/storage/repositories.py` as the only place that knows SQL, so
`gnosis/core/*` stays dependency-free per spec section 44.

## Tables

### states
| column | type | notes |
|---|---|---|
| state_id | TEXT PK | = `State.state_id` (sha256 hex) |
| version | INTEGER | |
| payload | TEXT (JSON) | serialized `elements` |
| created_at | TEXT (ISO8601) | |

### relations
| column | type | notes |
|---|---|---|
| relation_id | TEXT PK | = `Relation.relation_id` |
| state_id | TEXT FK -> states.state_id | which state this relation belongs to |
| source_id | TEXT | |
| target_id | TEXT | |
| relation_type | TEXT | |
| value | TEXT (JSON, nullable) | |
| created_at | TEXT | |

### candidates
| column | type | notes |
|---|---|---|
| candidate_id | TEXT PK | |
| parent_state_id | TEXT FK -> states.state_id | |
| candidate_state_id | TEXT FK -> states.state_id | the proposed state, stored regardless of accept/reject, for audit |
| origin | TEXT | e.g. `agent:<id>`, `user:<id>`, `generator:default` |
| seed | INTEGER (nullable) | |
| created_at | TEXT | |

### transitions  (not in original spec list, but required by section 39 auditability — records Test/Verify outcome per candidate)
| column | type | notes |
|---|---|---|
| transition_id | TEXT PK | |
| candidate_id | TEXT FK -> candidates.candidate_id | |
| accepted | INTEGER (bool) | |
| reasons | TEXT (JSON list) | |
| created_at | TEXT | |

### agents  — Phase 5, schema fixed now so Phase 3 identities/instances line up
| column | type | notes |
|---|---|---|
| agent_id | TEXT PK | |
| agent_type | TEXT | human / psi / gnozis / external |
| owner_id | TEXT | Human User id, nullable for `external` |
| instance_id | TEXT FK -> instances.instance_id | |
| status | TEXT | active / suspended / revoked |
| created_at | TEXT | |

### instances  — Phase 3
| column | type | notes |
|---|---|---|
| instance_id | TEXT PK | |
| parent_instance_id | TEXT FK -> instances.instance_id, nullable | null for root |
| owner_id | TEXT | |
| generation | INTEGER | root = 0 |
| status | TEXT | active / stopped / archived |
| created_at | TEXT | |

### identities — Phase 5
| column | type | notes |
|---|---|---|
| identity_id | TEXT PK | |
| subject_id | TEXT | agent_id or instance_id this identity belongs to |
| public_key | TEXT | |
| status | TEXT | active / revoked / rotated |
| created_at | TEXT | |

### capabilities — Phase 5/8
| column | type | notes |
|---|---|---|
| capability_id | TEXT PK | |
| subject_id | TEXT | who holds it |
| operation | TEXT | |
| resource | TEXT | |
| scope | TEXT (JSON) | |
| expiration | TEXT (ISO8601, nullable) | |
| status | TEXT | active / revoked / expired |

### memory — Phase 4
| column | type | notes |
|---|---|---|
| memory_id | TEXT PK | |
| owner_id | TEXT | agent_id or instance_id |
| type | TEXT | |
| payload_ref | TEXT | pointer to encrypted blob or inline JSON |
| version | INTEGER | |
| created_at | TEXT | |

### trust — Phase 7
| column | type | notes |
|---|---|---|
| source_id | TEXT | |
| target_id | TEXT | |
| value | REAL | |
| evidence | TEXT (JSON) | |
| updated_at | TEXT | |
| | | PK (source_id, target_id) |

### relations_agents — Phase 5 (agent-to-agent graph, distinct from Core `relations`)
| column | type | notes |
|---|---|---|
| source_agent | TEXT | |
| target_agent | TEXT | |
| relation_type | TEXT | |
| weight | REAL | |

### messages — Phase 5/7
| column | type | notes |
|---|---|---|
| message_id | TEXT PK | |
| sender | TEXT | |
| receiver | TEXT | |
| timestamp | TEXT | |
| payload_ref | TEXT | |
| signature | TEXT | |
| status | TEXT | sent / delivered / rejected |

### delegations — Phase 5/7
| column | type | notes |
|---|---|---|
| delegation_id | TEXT PK | |
| issuer | TEXT | |
| subject | TEXT | |
| scope | TEXT (JSON) | |
| budget | INTEGER | |
| expiration | TEXT (ISO8601, nullable) | |
| status | TEXT | active / revoked / expired |

### audit_events — Phase 1 (should exist now; not yet persisted — see STATUS.md)
| column | type | notes |
|---|---|---|
| event_id | TEXT PK | |
| actor | TEXT | |
| action | TEXT | |
| resource | TEXT | |
| result | TEXT | |
| timestamp | TEXT | |
| hash_ref | TEXT | hash of previous event, for hash-chained tamper evidence |

## Explicit rule (spec section 37)
No table stores raw private keys, raw passwords, or unencrypted secret
material. `identities.public_key` is public by definition; any private
key material belongs to the caller's own secure storage, never this DB.

## Not yet implemented
Nothing in this document is wired to code yet. `gnosis/storage/database.py`
and `repositories.py` are the next concrete artifacts once Phase 3
(Instance) needs to persist something beyond a Python process's memory.
