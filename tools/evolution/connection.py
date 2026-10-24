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


def get_connection(db_path: Path | None = None) -> sqlite3.Connection:
    """Open SQLite connection with Row factory and foreign keys enabled."""
    conn = sqlite3.connect(str(db_path or get_db_path()))
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON;")
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
