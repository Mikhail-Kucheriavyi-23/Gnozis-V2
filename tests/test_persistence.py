import sqlite3
import os
import subprocess
import sys
from pathlib import Path

import pytest

from gnosis.core import Candidate, Relation, State, TestResult, TransitionRecord
from gnosis.instances.instance import Instance
from gnosis.storage import (
    StorageCorruptionError,
    append_audit,
    connect,
    load_instance,
    persist_transition,
    recover_instance,
    save_candidate,
    save_instance,
    verify_audit_chain,
    verify_durable_graph,
)
from gnosis.storage.repositories import _audit_hash


def root():
    return Instance.create_root("user-1", State(elements={"a": 1}))


def test_root_round_trip_and_audit_chain():
    conn = connect()
    instance = root()
    save_instance(conn, instance)
    loaded = load_instance(conn, instance.instance_id)
    assert loaded.engine.state.state_id == instance.engine.state.state_id
    assert verify_audit_chain(conn)[0] == 1


def test_supported_schema_version_connects(tmp_path: Path):
    path = tmp_path / "supported.sqlite"
    conn = connect(path)
    assert conn.execute("SELECT value FROM schema_meta WHERE key='schema_version'").fetchone()[0] == "4"
    conn.close()


def test_schema_v3_migrates_to_v4(tmp_path: Path):
    path = tmp_path / "v3.sqlite"
    setup = sqlite3.connect(path)
    setup.execute("CREATE TABLE schema_meta (key TEXT PRIMARY KEY, value TEXT NOT NULL)")
    setup.execute("CREATE TABLE transitions (transition_id TEXT PRIMARY KEY, instance_id TEXT NOT NULL, candidate_id TEXT NOT NULL, from_state_id TEXT NOT NULL, to_state_id TEXT NOT NULL, accepted INTEGER NOT NULL, reasons TEXT NOT NULL, created_at TEXT NOT NULL)")
    setup.execute("INSERT INTO schema_meta(key, value) VALUES ('schema_version', '3')")
    setup.commit()
    setup.close()
    conn = connect(path)
    columns = {row[1] for row in conn.execute("PRAGMA table_info(transitions)")}
    assert "test_rule_id" in columns
    assert conn.execute("SELECT value FROM schema_meta WHERE key='schema_version'").fetchone()[0] == "4"
    conn.close()
