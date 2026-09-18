from __future__ import annotations

import sqlite3
from contextlib import contextmanager
from pathlib import Path
from typing import Iterator

SCHEMA_VERSION = 4
GENESIS_HASH = "0" * 64
SCHEMA = """
PRAGMA foreign_keys = ON;
CREATE TABLE IF NOT EXISTS schema_meta (key TEXT PRIMARY KEY, value TEXT NOT NULL);
CREATE TABLE IF NOT EXISTS states (state_id TEXT PRIMARY KEY, version INTEGER NOT NULL CHECK(version >= 0), payload TEXT NOT NULL, created_at TEXT NOT NULL);
CREATE TABLE IF NOT EXISTS relations (state_id TEXT NOT NULL, relation_order INTEGER NOT NULL CHECK(relation_order >= 0), relation_id TEXT NOT NULL, source_id TEXT NOT NULL, target_id TEXT NOT NULL, relation_type TEXT NOT NULL, value TEXT, created_at TEXT NOT NULL, PRIMARY KEY(state_id, relation_id), UNIQUE(state_id, relation_order), FOREIGN KEY(state_id) REFERENCES states(state_id) ON DELETE CASCADE);
CREATE TABLE IF NOT EXISTS candidates (candidate_id TEXT PRIMARY KEY, parent_state_id TEXT NOT NULL, candidate_state_id TEXT NOT NULL, origin TEXT NOT NULL, seed INTEGER, created_at TEXT NOT NULL, FOREIGN KEY(parent_state_id) REFERENCES states(state_id), FOREIGN KEY(candidate_state_id) REFERENCES states(state_id));
CREATE TABLE IF NOT EXISTS instances (instance_id TEXT PRIMARY KEY, parent_instance_id TEXT, owner_id TEXT NOT NULL, root_state_id TEXT NOT NULL, current_state_id TEXT NOT NULL, generation INTEGER NOT NULL CHECK(generation >= 0), status TEXT NOT NULL CHECK(status IN ('active','stopped','archived')), budget_total INTEGER NOT NULL CHECK(budget_total >= 0), budget_spent INTEGER NOT NULL CHECK(budget_spent >= 0), created_at TEXT NOT NULL, FOREIGN KEY(parent_instance_id) REFERENCES instances(instance_id), FOREIGN KEY(root_state_id) REFERENCES states(state_id), FOREIGN KEY(current_state_id) REFERENCES states(state_id));
CREATE TABLE IF NOT EXISTS transitions (transition_id TEXT PRIMARY KEY, instance_id TEXT NOT NULL, candidate_id TEXT NOT NULL, from_state_id TEXT NOT NULL, to_state_id TEXT NOT NULL, accepted INTEGER NOT NULL CHECK(accepted IN(0,1)), reasons TEXT NOT NULL, test_rule_id TEXT NOT NULL DEFAULT 'test-rule:unspecified', created_at TEXT NOT NULL, FOREIGN KEY(instance_id) REFERENCES instances(instance_id), FOREIGN KEY(candidate_id) REFERENCES candidates(candidate_id), FOREIGN KEY(from_state_id) REFERENCES states(state_id), FOREIGN KEY(to_state_id) REFERENCES states(state_id));
CREATE INDEX IF NOT EXISTS idx_transitions_instance ON transitions(instance_id);
CREATE TABLE IF NOT EXISTS evolution_memory (memory_id TEXT PRIMARY KEY, instance_id TEXT NOT NULL, candidate_id TEXT NOT NULL, transition_id TEXT NOT NULL, state_id TEXT NOT NULL, proposal_id TEXT, outcome TEXT NOT NULL CHECK(outcome IN ('accepted','rejected','inconclusive')), evidence TEXT NOT NULL, created_at TEXT NOT NULL, FOREIGN KEY(instance_id) REFERENCES instances(instance_id), FOREIGN KEY(candidate_id) REFERENCES candidates(candidate_id), FOREIGN KEY(transition_id) REFERENCES transitions(transition_id), FOREIGN KEY(state_id) REFERENCES states(state_id));
CREATE INDEX IF NOT EXISTS idx_evolution_memory_instance ON evolution_memory(instance_id);
CREATE TRIGGER IF NOT EXISTS evolution_memory_no_update BEFORE UPDATE ON evolution_memory BEGIN SELECT RAISE(ABORT,'evolution_memory is append-only'); END;
CREATE TRIGGER IF NOT EXISTS evolution_memory_no_delete BEFORE DELETE ON evolution_memory BEGIN SELECT RAISE(ABORT,'evolution_memory is append-only'); END;
CREATE TABLE IF NOT EXISTS audit_events (event_id TEXT PRIMARY KEY, sequence INTEGER NOT NULL UNIQUE CHECK(sequence > 0), transition_id TEXT, actor TEXT NOT NULL, action TEXT NOT NULL, resource TEXT NOT NULL, result TEXT NOT NULL, timestamp TEXT NOT NULL, prev_hash TEXT NOT NULL, event_hash TEXT NOT NULL UNIQUE, FOREIGN KEY(transition_id) REFERENCES transitions(transition_id));
CREATE TRIGGER IF NOT EXISTS audit_events_no_update BEFORE UPDATE ON audit_events BEGIN SELECT RAISE(ABORT,'audit_events are append-only'); END;
CREATE TRIGGER IF NOT EXISTS audit_events_no_delete BEFORE DELETE ON audit_events BEGIN SELECT RAISE(ABORT,'audit_events are append-only'); END;
"""

def connect(path: str | Path = ":memory:") -> sqlite3.Connection:
    conn = sqlite3.connect(str(path), isolation_level=None, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys=ON")
    conn.execute("PRAGMA busy_timeout=5000")
    schema_meta_exists = conn.execute(
        "SELECT 1 FROM sqlite_master WHERE type='table' AND name='schema_meta'"
    ).fetchone()
    if schema_meta_exists:
        stored = conn.execute(
            "SELECT value FROM schema_meta WHERE key='schema_version'"
        ).fetchone()
        if stored is not None:
            version = int(stored[0])
            if version == 3:
                conn.execute("UPDATE schema_meta SET value=? WHERE key='schema_version'", (str(SCHEMA_VERSION),))
                # Existing v3 databases are structurally compatible; v4 adds evolution_memory.
                columns = {
                    row[1]
                    for row in conn.execute("PRAGMA table_info(transitions)")
                }
                if "test_rule_id" not in columns:
                    conn.execute(
                        "ALTER TABLE transitions ADD COLUMN test_rule_id TEXT NOT NULL DEFAULT 'test-rule:unspecified'"
                    )
            elif version != SCHEMA_VERSION:
                conn.close()
                raise RuntimeError(
                    f"incompatible schema version: {version} (expected {SCHEMA_VERSION})"
                )
    conn.executescript(SCHEMA)
    conn.execute(
        "INSERT OR IGNORE INTO schema_meta(key,value) VALUES('schema_version',?)",
        (str(SCHEMA_VERSION),),
    )
    if int(conn.execute("PRAGMA foreign_keys").fetchone()[0]) != 1:
        conn.close()
        raise RuntimeError("SQLite foreign_keys pragma is not active")
    return conn


@contextmanager
def transaction(conn: sqlite3.Connection) -> Iterator[sqlite3.Connection]:
    conn.execute("BEGIN IMMEDIATE")
    try:
        yield conn
    except BaseException:
        conn.rollback()
        raise
    else:
        conn.commit()


def close(conn: sqlite3.Connection) -> None:
    conn.close()
