"""
ADK Evolution Database - Data Access Object & Repositories
Implements CRUD, Analytics, FTS search, and Developer Profile synchronization.
"""

from __future__ import annotations

import hashlib
import os
from pathlib import Path
import sqlite3
import sys
from typing import Any

from .connection import ensure_trace_exists, get_connection, get_db_path, get_schema_path

sys.dont_write_bytecode = True


def cmd_init(args: Any = None) -> dict[str, Any]:
    """Initialize evolution database and apply SQL schema."""
    db_path = get_db_path()
    schema_file = get_schema_path()
    with sqlite3.connect(str(db_path)) as conn:
        conn.executescript(schema_file.read_text(encoding="utf-8"))
    return {"status": "ok", "message": "Database initialized successfully", "db_path": str(db_path)}


def cmd_log_session(args: Any) -> dict[str, Any]:
    """Insert or update session in sessions table."""
    if not isinstance(args, dict):
        raise ValueError("log_session expects a JSON object payload.")
    session_id = args.get("id") or f"sess_{hashlib.sha256(os.urandom(16)).hexdigest()[:12]}"
    params = {
        "id": session_id,
        "project": args.get("project"),
        "user_intent": args.get("user_intent"),
        "workflow_used": args.get("workflow_used"),
        "outcome": args.get("outcome"),
        "total_turns": int(args.get("total_turns", 0)),
        "total_tokens": int(args.get("total_tokens", 0)),
        "summary": args.get("summary"),
    }
    with get_connection() as conn:
        conn.execute(
            """
            INSERT INTO sessions (id, project, user_intent, workflow_used, outcome, total_turns, total_tokens, summary)
            VALUES (:id, :project, :user_intent, :workflow_used, :outcome, :total_turns, :total_tokens, :summary)
            ON CONFLICT(id) DO UPDATE SET
                project = COALESCE(excluded.project, sessions.project),
                user_intent = COALESCE(excluded.user_intent, sessions.user_intent),
                workflow_used = COALESCE(excluded.workflow_used, sessions.workflow_used),
                outcome = COALESCE(excluded.outcome, sessions.outcome),
                total_turns = COALESCE(excluded.total_turns, sessions.total_turns),
                total_tokens = COALESCE(excluded.total_tokens, sessions.total_tokens),
                summary = COALESCE(excluded.summary, sessions.summary);
            """,
            params,
        )
    return {"status": "ok", "session_id": session_id}


def cmd_log_step(args: Any) -> dict[str, Any]:
    """Insert a new step into trace_steps table."""
    if not isinstance(args, dict):
        raise ValueError("log_step expects a JSON object payload.")
    trace_id = args.get("trace_id")
    if not trace_id:
        raise ValueError("Field 'trace_id' is required for log_step.")

    with get_connection() as conn:
        ensure_trace_exists(conn, trace_id, args.get("session_id"), args.get("task_description"))
        step_order = args.get("step_order")
        if step_order is None:
            cur = conn.execute("SELECT COALESCE(MAX(step_order), 0) + 1 FROM trace_steps WHERE trace_id = ?", (trace_id,))
            step_order = cur.fetchone()[0]

        params = {
            "trace_id": trace_id,
            "step_order": int(step_order),
            "step_type": args.get("step_type", "other"),
            "description": args.get("description"),
            "tool_used": args.get("tool_used"),
            "input_summary": args.get("input_summary"),
            "output_summary": args.get("output_summary"),
            "outcome": args.get("outcome", "pass"),
            "tokens": int(args.get("tokens", 0)),
            "duration_ms": int(args.get("duration_ms", 0)),
            "friction_note": args.get("friction_note"),
        }
        cur = conn.execute(
            """
            INSERT INTO trace_steps (
                trace_id, step_order, step_type, description, tool_used,
                input_summary, output_summary, outcome, tokens, duration_ms, friction_note
            ) VALUES (
                :trace_id, :step_order, :step_type, :description, :tool_used,
                :input_summary, :output_summary, :outcome, :tokens, :duration_ms, :friction_note
            )
            """,
            params,
        )
        return {"status": "ok", "step_id": cur.lastrowid, "trace_id": trace_id, "step_order": step_order}


def cmd_log_friction(args: Any) -> dict[str, Any]:
    """Insert friction point record into friction_points table."""
    if not isinstance(args, dict):
        raise ValueError("log_friction expects a JSON object payload.")
    trace_id, description = args.get("trace_id"), args.get("description")
    if not trace_id or not description:
        raise ValueError("Fields 'trace_id' and 'description' are required for log_friction.")

    with get_connection() as conn:
        ensure_trace_exists(conn, trace_id)
        params = {
            "trace_id": trace_id,
            "step_id": args.get("step_id"),
            "category": args.get("category", "tool_error"),
            "description": description,
            "severity": args.get("severity", "medium"),
            "related_skill": args.get("related_skill"),
            "related_rule": args.get("related_rule"),
            "suggested_fix": args.get("suggested_fix"),
        }
        cur = conn.execute(
            """
            INSERT INTO friction_points (
                trace_id, step_id, category, description, severity,
                related_skill, related_rule, suggested_fix
            ) VALUES (
                :trace_id, :step_id, :category, :description, :severity,
                :related_skill, :related_rule, :suggested_fix
            )
            """,
            params,
        )
        return {"status": "ok", "friction_id": cur.lastrowid, "trace_id": trace_id}


def cmd_update_outcome(args: Any) -> dict[str, Any]:
    """Update trace outcome and increment skill success/fail statistics."""
    if not isinstance(args, dict):
        raise ValueError("update_outcome expects a JSON object payload.")
    trace_id, outcome = args.get("trace_id"), args.get("outcome")
    if not trace_id or not outcome:
        raise ValueError("Fields 'trace_id' and 'outcome' are required for update_outcome.")
    outcome_upper = outcome.upper()
    if outcome_upper not in ("SUCCESS", "PARTIAL", "FAILED"):
        raise ValueError("outcome must be one of 'SUCCESS', 'PARTIAL', 'FAILED'")

    with get_connection() as conn:
        ensure_trace_exists(conn, trace_id)
        old_row = conn.execute("SELECT outcome FROM traces WHERE id = ?", (trace_id,)).fetchone()
        old_outcome = old_row[0] if old_row else None

        conn.execute(
            """
            UPDATE traces
            SET outcome = :outcome,
                duration_turns = COALESCE(:duration_turns, duration_turns),
                tokens_used = COALESCE(:tokens_used, tokens_used),
                acceptance_evidence = COALESCE(:acceptance_evidence, acceptance_evidence)
            WHERE id = :trace_id
            """,
            {
                "trace_id": trace_id,
                "outcome": outcome_upper,
                "duration_turns": args.get("duration_turns"),
                "tokens_used": args.get("tokens_used"),
                "acceptance_evidence": args.get("acceptance_evidence"),
            },
        )

        session_id = args.get("session_id")
        conn.execute(
            "UPDATE sessions SET outcome = ? WHERE id = COALESCE(?, (SELECT session_id FROM traces WHERE id = ?))",
            (outcome_upper, session_id, trace_id),
        )

        cur = conn.execute("SELECT DISTINCT skill_name FROM skills_used WHERE trace_id = ?", (trace_id,))
        skills = [r[0] for r in cur.fetchall()]

        if old_outcome != outcome_upper:
            succ_delta = (1 if outcome_upper == "SUCCESS" else 0) - (1 if old_outcome == "SUCCESS" else 0)
            fail_delta = (1 if outcome_upper == "FAILED" else 0) - (1 if old_outcome == "FAILED" else 0)
            for skill_name in skills:
                conn.execute(
                    """
                    UPDATE skills
                    SET times_succeeded = MAX(0, times_succeeded + ?),
                        times_failed = MAX(0, times_failed + ?),
                        last_used_at = strftime('%Y-%m-%dT%H:%M:%SZ', 'now')
                    WHERE name = ?
                    """,
                    (succ_delta, fail_delta, skill_name),
                )
            used_outcome = "success" if outcome_upper == "SUCCESS" else ("failed" if outcome_upper == "FAILED" else "partial")
            conn.execute("UPDATE skills_used SET outcome = ? WHERE trace_id = ?", (used_outcome, trace_id))

        return {"status": "ok", "trace_id": trace_id, "outcome": outcome_upper, "updated_skills": skills}


def cmd_log_skill_use(args: Any) -> dict[str, Any]:
    """Insert into skills_used and upsert into skills table."""
    if not isinstance(args, dict):
        raise ValueError("log_skill_use expects a JSON object payload.")
    trace_id, skill_name = args.get("trace_id"), args.get("skill_name")
    if not trace_id or not skill_name:
        raise ValueError("Fields 'trace_id' and 'skill_name' are required for log_skill_use.")

    outcome = (args.get("outcome") or "success").lower()
    skill_group = args.get("skill_group") or "core"

    with get_connection() as conn:
        ensure_trace_exists(conn, trace_id)
        conn.execute(
            """
            INSERT INTO skills (name, skill_group, current_version, times_used, times_succeeded, times_failed, last_used_at)
            VALUES (?, ?, '1.0', 1, 0, 0, strftime('%Y-%m-%dT%H:%M:%SZ', 'now'))
            ON CONFLICT(name) DO UPDATE SET
                times_used = times_used + 1,
                last_used_at = strftime('%Y-%m-%dT%H:%M:%SZ', 'now');
            """,
            (skill_name, skill_group),
        )
        cur = conn.execute(
            "INSERT INTO skills_used (trace_id, skill_name, outcome) VALUES (?, ?, ?)",
            (trace_id, skill_name, outcome),
        )
        return {"status": "ok", "skill_used_id": cur.lastrowid, "skill_name": skill_name}


def cmd_query(args: Any) -> dict[str, Any]:
    """Run arbitrary SQL and return results as JSON."""
    if isinstance(args, str):
        sql, params = args, []
    elif isinstance(args, dict):
        sql, params = args.get("sql") or args.get("query", ""), args.get("params", [])
    else:
        raise ValueError("query expects SQL string or object with 'sql' and optional 'params'.")
    if not sql or not sql.strip():
        raise ValueError("Query string cannot be empty.")

    with get_connection() as conn:
        cur = conn.execute(sql, params)
        if cur.description is not None:
            rows = [dict(row) for row in cur.fetchall()]
            return {"status": "ok", "count": len(rows), "rows": rows}
        return {"status": "ok", "rows_affected": cur.rowcount}


def cmd_search(args: Any) -> dict[str, Any]:
    """Perform FTS5 full-text search on traces_fts or friction_fts."""
    if isinstance(args, str):
        search_query, target = args, "traces"
    elif isinstance(args, dict):
        search_query = args.get("query") or args.get("q", "")
        target = args.get("target", "traces").lower()
    else:
        raise ValueError("search expects query string or object with 'query'.")
    if not search_query or not search_query.strip():
        raise ValueError("Search query cannot be empty.")

    with get_connection() as conn:
        if target in ("traces", "trace", "traces_fts"):
            cur = conn.execute(
                """
                SELECT t.id, t.session_id, t.task_description, t.workflow, t.complexity, t.outcome, t.created_at, f.rank
                FROM traces_fts f
                JOIN traces t ON t.rowid = f.rowid
                WHERE traces_fts MATCH ? ORDER BY rank LIMIT 50;
                """,
                (search_query,),
            )
        elif target in ("friction", "friction_points", "friction_fts"):
            cur = conn.execute(
                """
                SELECT fp.id, fp.trace_id, fp.step_id, fp.category, fp.description, fp.severity, fp.related_skill, fp.suggested_fix, f.rank
                FROM friction_fts f
                JOIN friction_points fp ON fp.id = f.rowid
                WHERE friction_fts MATCH ? ORDER BY rank LIMIT 50;
                """,
                (search_query,),
            )
        else:
            raise ValueError(f"Unknown target '{target}'. Allowed: 'traces', 'friction'.")
        results = [dict(row) for row in cur.fetchall()]
        return {"status": "ok", "target": target, "count": len(results), "results": results}


def cmd_health(args: Any = None) -> dict[str, Any]:
    """Return health metrics from v_skill_health view."""
    name = (
        args.strip()
        if isinstance(args, str) and args.strip()
        else (args.get("skill_name") or args.get("name") if isinstance(args, dict) else None)
    )
    with get_connection() as conn:
        if name:
            cur = conn.execute("SELECT * FROM v_skill_health WHERE name = ?", (name,))
        else:
            cur = conn.execute("SELECT * FROM v_skill_health ORDER BY times_used DESC, success_rate ASC")
        rows = [dict(row) for row in cur.fetchall()]
        return {"status": "ok", "count": len(rows), "skills": rows}


def cmd_log_preference(args: Any) -> dict[str, Any]:
    """Insert or update user preference in user_preferences table."""
    if not isinstance(args, dict):
        raise ValueError("log_preference expects a JSON object payload.")
    key = args.get("preference_key") or args.get("key")
    val = args.get("preference_value") or args.get("value")
    if not key or val is None:
        raise ValueError("Fields 'preference_key' and 'preference_value' are required for log_preference.")
    confidence = float(args.get("confidence", 0.7))
    source_session = args.get("source_session")

    with get_connection() as conn:
        conn.execute(
            """
            INSERT INTO user_preferences (preference_key, preference_value, confidence, source_session, learned_at, last_confirmed)
            VALUES (?, ?, ?, ?, strftime('%Y-%m-%dT%H:%M:%SZ', 'now'), strftime('%Y-%m-%dT%H:%M:%SZ', 'now'))
            ON CONFLICT(preference_key) DO UPDATE SET
                preference_value = excluded.preference_value,
                confidence = MIN(1.0, user_preferences.confidence + 0.1),
                source_session = COALESCE(excluded.source_session, user_preferences.source_session),
                last_confirmed = excluded.last_confirmed;
            """,
            (key, str(val), confidence, source_session),
        )
        return {"status": "ok", "preference_key": key, "preference_value": val, "confidence": confidence}


def cmd_get_preferences(args: Any = None) -> dict[str, Any]:
    """Query user preferences, optionally filtered by prefix or min_confidence."""
    prefix = ""
    min_confidence = 0.0
    if isinstance(args, dict):
        prefix = args.get("prefix", "")
        min_confidence = float(args.get("min_confidence", 0.0))
    elif isinstance(args, str) and args.strip():
        prefix = args.strip()

    with get_connection() as conn:
        if prefix:
            cur = conn.execute(
                "SELECT * FROM user_preferences WHERE preference_key LIKE ? AND confidence >= ? ORDER BY confidence DESC, last_confirmed DESC",
                (f"{prefix}%", min_confidence),
            )
        else:
            cur = conn.execute(
                "SELECT * FROM user_preferences WHERE confidence >= ? ORDER BY confidence DESC, last_confirmed DESC",
                (min_confidence,),
            )
        rows = [dict(row) for row in cur.fetchall()]
        return {"status": "ok", "count": len(rows), "preferences": rows}


def cmd_sync_profile(args: Any = None) -> dict[str, Any]:
    """Synchronize high-confidence preferences into ~/.agents/developer.md."""
    min_conf = 0.6
    if isinstance(args, dict):
        min_conf = float(args.get("min_confidence", 0.6))
    profile_path = Path.home() / ".agents" / "developer.md"
    profile_path.parent.mkdir(parents=True, exist_ok=True)

    with get_connection() as conn:
        cur = conn.execute(
            "SELECT preference_key, preference_value, confidence, last_confirmed FROM user_preferences WHERE confidence >= ? ORDER BY preference_key ASC",
            (min_conf,),
        )
        prefs = [dict(r) for r in cur.fetchall()]

    if not prefs:
        return {"status": "ok", "message": "No high-confidence preferences to sync", "synced": 0}

    section_header = "## Auto-Learned Preferences (from Evolution DB)"
    lines = [
        f"\n{section_header}",
        "> Tự động đồng bộ từ ~/.adk/evolution.db qua session_curator.",
        "",
    ]
    for p in prefs:
        lines.append(f"- **{p['preference_key']}**: {p['preference_value']} *(confidence: {p['confidence']:.2f}, confirmed: {str(p['last_confirmed'])[:10]})*")
    lines.append("")
    new_section = "\n".join(lines)

    existing_content = profile_path.read_text(encoding="utf-8") if profile_path.exists() else ""
    if section_header in existing_content:
        parts = existing_content.split(section_header)
        prefix = parts[0].rstrip()
        remainder = parts[1]
        next_sec_idx = remainder.find("\n## ")
        suffix = remainder[next_sec_idx:] if next_sec_idx != -1 else ""
        updated_content = f"{prefix}\n{new_section}{suffix}".strip() + "\n"
    else:
        updated_content = (existing_content.rstrip() + "\n" + new_section).strip() + "\n"

    profile_path.write_text(updated_content, encoding="utf-8")
    return {"status": "ok", "profile_path": str(profile_path), "synced_count": len(prefs)}
