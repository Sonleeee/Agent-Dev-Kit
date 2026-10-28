#!/usr/bin/env python3
"""
ADK Session Curator
Autonomous post-session reflection & interaction trajectory engine.
Reads conversation transcripts (transcript.jsonl), extracts trajectory, friction points,
entity graph edges, and developer preferences, persisting everything into evolution.db.
Compatible with Antigravity Lifecycle Hooks ('Stop' event via hooks.json) and CLI execution.
"""

from __future__ import annotations

import json
import os
from pathlib import Path
import sys
from typing import Any

# Configure UTF-8 stdout for Windows consoles
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")
if hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(encoding="utf-8")

sys.dont_write_bytecode = True

# Ensure ADK root is in sys.path
ADK_ROOT = Path(__file__).resolve().parent.parent
if str(ADK_ROOT) not in sys.path:
    sys.path.insert(0, str(ADK_ROOT))

from tools.curator import (
    analyze_dev_style,
    clean_user_message,
    find_latest_transcript,
    generate_session_summary,
    parse_transcript,
    read_stdin_with_timeout,
    write_runtime_artifacts,
)

try:
    from tools.evolution import (
        cmd_sync_profile,
        get_connection,
        get_db_path,
        upsert_graph_link,
    )
except ImportError:
    def get_db_path() -> Path:
        env = os.environ.get("ADK_EVOLUTION_DB")
        return Path(env).expanduser().resolve() if env else Path.home() / ".adk" / "evolution.db"

    def get_connection():
        import sqlite3
        p = get_db_path()
        p.parent.mkdir(parents=True, exist_ok=True)
        conn = sqlite3.connect(str(p))
        conn.row_factory = sqlite3.Row
        conn.execute("PRAGMA foreign_keys = ON;")
        return conn

    cmd_sync_profile = None
    upsert_graph_link = None


def curate_session(
    transcript_path: Path,
    dry_run: bool = False,
    sync_profile_enabled: bool = True,
) -> dict[str, Any]:
    """Execute full curation on a transcript: parse trajectory, store into SQLite and sync."""
    data = parse_transcript(transcript_path)
    conv_id = data["conversation_id"]
    sess_id = f"sess_conv_{conv_id[:12]}"
    trace_id = f"trace_conv_{conv_id[:12]}"

    user_msgs = data.get("user_messages", [])
    primary_intent = user_msgs[0][:200] if user_msgs else "Autonomous session"
    summary = generate_session_summary(data)
    preferences = analyze_dev_style(user_msgs)

    outcome = "SUCCESS"
    if len(data.get("errors_encountered", [])) > 5:
        outcome = "PARTIAL"

    result: dict[str, Any] = {
        "status": "ok",
        "session_id": sess_id,
        "trace_id": trace_id,
        "conversation_id": conv_id,
        "total_turns": data["total_turns"],
        "total_tokens": data["total_tokens"],
        "primary_intent": primary_intent,
        "summary": summary,
        "skills_observed": data["skills_observed"],
        "verification_commands_count": len(data["verification_commands"]),
        "interaction_turns": data["interaction_turns"],
        "preferences_extracted": preferences,
        "friction_count": len(data["errors_encountered"]),
    }

    if dry_run:
        result["dry_run"] = True
        return result

    with get_connection() as conn:
        # 1. Upsert session
        conn.execute(
            """
            INSERT INTO sessions (id, project, user_intent, workflow_used, outcome, total_turns, total_tokens, summary)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            ON CONFLICT(id) DO UPDATE SET
                project = COALESCE(excluded.project, sessions.project),
                user_intent = COALESCE(excluded.user_intent, sessions.user_intent),
                workflow_used = COALESCE(excluded.workflow_used, sessions.workflow_used),
                outcome = COALESCE(excluded.outcome, sessions.outcome),
                total_turns = excluded.total_turns,
                total_tokens = excluded.total_tokens,
                summary = excluded.summary;
            """,
            (
                sess_id,
                ADK_ROOT.name,
                primary_intent,
                "skill-first-session",
                outcome,
                data["total_turns"],
                data["total_tokens"],
                summary,
            ),
        )

        # 2. Upsert trace with full interaction trajectory & observed verification commands
        evidence_json = json.dumps(
            {
                "transcript_path": data["transcript_path"],
                "tools_used": data["tools_used"],
                "skills_observed": data["skills_observed"],
                "verification_commands": data["verification_commands"][-10:],
                "interaction_turns": data["interaction_turns"],
                "errors_count": len(data["errors_encountered"]),
            },
            ensure_ascii=False,
        )

        conn.execute(
            """
            INSERT INTO traces (id, session_id, task_description, workflow, complexity, outcome, duration_turns, tokens_used, acceptance_evidence)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            ON CONFLICT(id) DO UPDATE SET
                outcome = excluded.outcome,
                duration_turns = excluded.duration_turns,
                tokens_used = excluded.tokens_used,
                acceptance_evidence = excluded.acceptance_evidence;
            """,
            (
                trace_id,
                sess_id,
                primary_intent,
                "skill-first-session",
                "High" if data["total_turns"] > 6 else ("Medium" if data["total_turns"] > 2 else "Low"),
                outcome,
                data["total_turns"],
                data["total_tokens"],
                evidence_json,
            ),
        )

        # 3. Record Observed Skills in `skills` and `skills_used` (idempotent per trace)
        conn.execute("DELETE FROM skills_used WHERE trace_id = ?;", (trace_id,))
        for sk_name in data.get("skills_observed", []):
            conn.execute(
                """
                INSERT INTO skills (name, skill_group, times_used, times_succeeded, last_used_at)
                VALUES (?, 'core', 1, ?, strftime('%Y-%m-%dT%H:%M:%SZ', 'now'))
                ON CONFLICT(name) DO UPDATE SET
                    times_used = skills.times_used + 1,
                    times_succeeded = skills.times_succeeded + ?,
                    last_used_at = strftime('%Y-%m-%dT%H:%M:%SZ', 'now');
                """,
                (sk_name, 1 if outcome == "SUCCESS" else 0, 1 if outcome == "SUCCESS" else 0),
            )
            conn.execute(
                """
                INSERT INTO skills_used (trace_id, skill_name, outcome)
                VALUES (?, ?, ?);
                """,
                (trace_id, sk_name, "success" if outcome == "SUCCESS" else "partial"),
            )

        # 4. Replace friction points & populate Empirical Entity Graph (idempotent per trace)
        conn.execute("DELETE FROM friction_points WHERE trace_id = ?;", (trace_id,))
        fallback_skill = data["skills_observed"][-1] if data.get("skills_observed") else None
        for err in data.get("errors_encountered", [])[:8]:
            cat = err.get("category") or "tool_error"
            rel_file = err.get("related_file")
            rel_skill = err.get("related_skill") or fallback_skill
            fp_id = err.get("fingerprint") or cat
            fp_sum = err.get("fingerprint_summary") or err.get("content", "")[:140]
            conn.execute(
                """
                INSERT INTO friction_points (
                    trace_id, category, description, severity,
                    related_skill, related_file, error_fingerprint, suggested_fix
                )
                VALUES (?, ?, ?, ?, ?, ?, ?, ?);
                """,
                (
                    trace_id,
                    cat,
                    f"Step {err.get('step_index')}: {err.get('content', '')[:180]}",
                    "medium",
                    rel_skill,
                    rel_file,
                    fp_id,
                    "Review turn trajectory and add deterministic guard/script if recurring",
                ),
            )
            if upsert_graph_link is not None:
                frict_node_id = f"friction:{fp_id}"
                if rel_file:
                    upsert_graph_link(
                        conn,
                        f"file:{rel_file}",
                        "file",
                        rel_file,
                        None,
                        frict_node_id,
                        "friction",
                        fp_id,
                        fp_sum,
                        "SUFFERED_FROM",
                        trace_id,
                    )
                if rel_skill:
                    upsert_graph_link(
                        conn,
                        f"skill:{rel_skill}",
                        "skill",
                        rel_skill,
                        None,
                        frict_node_id,
                        "friction",
                        fp_id,
                        fp_sum,
                        "SUFFERED_FROM",
                        trace_id,
                    )

        # 5. Populate Empirical File <-> Skill Edges from Turn Co-occurrence
        if upsert_graph_link is not None:
            active_skills: list[str] = []
            for turn in data.get("interaction_turns", []):
                for sk in turn.get("skills_loaded", []):
                    if sk not in active_skills:
                        active_skills.append(sk)
                for f_path in turn.get("files_touched", []):
                    for sk in active_skills:
                        upsert_graph_link(
                            conn,
                            f"file:{f_path}",
                            "file",
                            f_path,
                            None,
                            f"skill:{sk}",
                            "skill",
                            sk,
                            None,
                            "USED_WITH_SKILL",
                            trace_id,
                        )

        # 6. Upsert user preferences
        for pref in preferences:
            conn.execute(
                """
                INSERT INTO user_preferences (preference_key, preference_value, confidence, source_session, learned_at, last_confirmed)
                VALUES (?, ?, ?, ?, strftime('%Y-%m-%dT%H:%M:%SZ', 'now'), strftime('%Y-%m-%dT%H:%M:%SZ', 'now'))
                ON CONFLICT(preference_key) DO UPDATE SET
                    preference_value = excluded.preference_value,
                    confidence = MIN(1.0, user_preferences.confidence + 0.1),
                    source_session = excluded.source_session,
                    last_confirmed = excluded.last_confirmed;
                """,
                (pref["key"], pref["value"], pref["confidence"], sess_id),
            )

    if sync_profile_enabled and cmd_sync_profile is not None:
        try:
            sync_res = cmd_sync_profile({"min_confidence": 0.7})
            result["profile_sync"] = sync_res
        except Exception as e:
            result["profile_sync_error"] = str(e)

    try:
        result["runtime_artifacts"] = write_runtime_artifacts(data, sess_id, outcome, summary, ADK_ROOT)
    except Exception as e:
        result["runtime_artifacts_error"] = str(e)

    return result


def main() -> None:
    """Entry point for Antigravity Hook ('Stop' event) or CLI execution."""
    transcript_path: Path | None = None
    dry_run = "--dry-run" in sys.argv

    stdin_payload: dict[str, Any] | None = None
    raw_stdin = read_stdin_with_timeout(timeout_sec=0.5).strip()
    if raw_stdin.startswith("{") and raw_stdin.endswith("}"):
        try:
            stdin_payload = json.loads(raw_stdin)
        except Exception:
            stdin_payload = None

    if stdin_payload and "transcriptPath" in stdin_payload:
        transcript_path = Path(stdin_payload["transcriptPath"])

    if not transcript_path:
        for i, arg in enumerate(sys.argv):
            if arg in ("--transcript", "-t") and i + 1 < len(sys.argv):
                transcript_path = Path(sys.argv[i + 1])
                break

    if not transcript_path or not transcript_path.exists():
        transcript_path = find_latest_transcript()

    if not transcript_path or not transcript_path.exists():
        out = {"decision": "allow", "status": "skipped", "reason": "No valid transcript found"}
        print(json.dumps(out, ensure_ascii=False))
        sys.exit(0)

    try:
        res = curate_session(transcript_path, dry_run=dry_run)
        res["decision"] = "allow"
        print(json.dumps(res, indent=2, ensure_ascii=False))
        sys.exit(0)
    except Exception as exc:
        err_out = {"decision": "allow", "status": "error", "error": str(exc)}
        print(json.dumps(err_out, ensure_ascii=False))
        sys.exit(0)


if __name__ == "__main__":
    main()
