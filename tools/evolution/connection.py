"""
ADK Evolution Database - Connection & Schema Infrastructure
"""

from __future__ import annotations

import hashlib
import os
from pathlib import Path
import sqlite3
import sys

sys.dont_write_bytecode = True


def get_db_path() -> Path:
    """Return database path from ADK_EVOLUTION_DB or default ~/.adk/evolution.db."""
    env_path = os.environ.get("ADK_EVOLUTION_DB")
    path = Path(env_path).expanduser().resolve() if env_path else Path.home() / ".adk" / "evolution.db"
    path.parent.mkdir(parents=True, exist_ok=True)
    return path


def get_schema_path() -> Path:
    """Return path to evolution-schema.sql."""
    schema_path = Path(__file__).resolve().parent.parent.parent / "schemas" / "evolution-schema.sql"
    if not schema_path.exists():
        raise FileNotFoundError(f"Schema file not found at: {schema_path}")
    return schema_path


def hash_content(content: str) -> str:
    """Compute SHA-256 hash for content versioning and tracking."""
    return hashlib.sha256(content.encode("utf-8")).hexdigest()


def ensure_schema_migrations(conn: sqlite3.Connection) -> None:
    """Apply idempotent schema migrations for existing evolution.db files."""
    has_fp = conn.execute("SELECT 1 FROM sqlite_master WHERE type='table' AND name='friction_points';").fetchone()
    if has_fp:
        cols = {r[1] for r in conn.execute("PRAGMA table_info(friction_points);").fetchall()}
        if "related_file" not in cols:
            conn.execute("ALTER TABLE friction_points ADD COLUMN related_file TEXT;")
        if "error_fingerprint" not in cols:
            conn.execute("ALTER TABLE friction_points ADD COLUMN error_fingerprint TEXT;")

    conn.executescript(
        """
        CREATE TABLE IF NOT EXISTS graph_nodes (
            id TEXT PRIMARY KEY,
            node_type TEXT NOT NULL CHECK(node_type IN ('file','skill','rule','friction')),
            name TEXT NOT NULL,
            summary TEXT
        );

        CREATE TABLE IF NOT EXISTS graph_edges (
            source_id TEXT NOT NULL REFERENCES graph_nodes(id) ON DELETE CASCADE,
            target_id TEXT NOT NULL REFERENCES graph_nodes(id) ON DELETE CASCADE,
            edge_type TEXT NOT NULL CHECK(edge_type IN ('SUFFERED_FROM','USED_WITH_SKILL','GOVERNED_BY','RESOLVES')),
            hit_count INTEGER DEFAULT 1,
            last_trace_id TEXT,
            last_seen TEXT NOT NULL DEFAULT (strftime('%Y-%m-%dT%H:%M:%SZ', 'now')),
            PRIMARY KEY (source_id, target_id, edge_type)
        );

        CREATE INDEX IF NOT EXISTS idx_graph_edges_source ON graph_edges(source_id);
        CREATE INDEX IF NOT EXISTS idx_graph_edges_target ON graph_edges(target_id);
        """
    )


def get_connection(db_path: Path | None = None) -> sqlite3.Connection:
    """Open SQLite connection with Row factory, foreign keys, and schema migrations enabled."""
    conn = sqlite3.connect(str(db_path or get_db_path()))
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON;")
    ensure_schema_migrations(conn)
    return conn


def ensure_trace_exists(
    conn: sqlite3.Connection,
    trace_id: str,
    session_id: str | None = None,
    task_desc: str | None = None,
) -> None:
    """Ensure parent session and trace exist to satisfy foreign key constraints."""
    if not conn.execute("SELECT 1 FROM traces WHERE id = ?", (trace_id,)).fetchone():
        sess_id = session_id or "sess_default"
        conn.execute(
            "INSERT OR IGNORE INTO sessions (id, project, user_intent, summary) VALUES (?, ?, ?, ?)",
            (sess_id, "default", "Auto-created session for trace", "Default session"),
        )
        conn.execute(
            "INSERT OR IGNORE INTO traces (id, session_id, task_description, outcome) VALUES (?, ?, ?, ?)",
            (trace_id, sess_id, task_desc or f"Trace {trace_id}", "PARTIAL"),
        )


def upsert_graph_link(
    conn: sqlite3.Connection,
    source_id: str,
    source_type: str,
    source_name: str,
    source_summary: str | None,
    target_id: str,
    target_type: str,
    target_name: str,
    target_summary: str | None,
    edge_type: str,
    trace_id: str | None = None,
) -> None:
    """Upsert source/target nodes and increment edge hit_count idempotently per trace_id."""
    conn.execute(
        """
        INSERT INTO graph_nodes (id, node_type, name, summary)
        VALUES (?, ?, ?, ?)
        ON CONFLICT(id) DO UPDATE SET
            summary = COALESCE(excluded.summary, graph_nodes.summary);
        """,
        (source_id, source_type, source_name, source_summary),
    )
    conn.execute(
        """
        INSERT INTO graph_nodes (id, node_type, name, summary)
        VALUES (?, ?, ?, ?)
        ON CONFLICT(id) DO UPDATE SET
            summary = COALESCE(excluded.summary, graph_nodes.summary);
        """,
        (target_id, target_type, target_name, target_summary),
    )
    conn.execute(
        """
        INSERT INTO graph_edges (source_id, target_id, edge_type, hit_count, last_trace_id, last_seen)
        VALUES (?, ?, ?, 1, ?, strftime('%Y-%m-%dT%H:%M:%SZ', 'now'))
        ON CONFLICT(source_id, target_id, edge_type) DO UPDATE SET
            hit_count = CASE
                WHEN ? IS NULL OR graph_edges.last_trace_id IS NOT ?
                THEN graph_edges.hit_count + 1
                ELSE graph_edges.hit_count
            END,
            last_trace_id = COALESCE(?, graph_edges.last_trace_id),
            last_seen = excluded.last_seen;
        """,
        (source_id, target_id, edge_type, trace_id, trace_id, trace_id, trace_id),
    )
