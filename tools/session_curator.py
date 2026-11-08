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
    sync_profile_enabled: bool = False,
) -> dict[str, Any]:
    """Execute full curation on a transcript: parse trajectory and store into SQLite (no auto-profile overwrite)."""
    data = parse_transcript(transcript_path)
    conv_id = data["conversation_id"]
    sess_id = f"sess_conv_{conv_id[:12]}"
    trace_id = f"trace_conv_{conv_id[:12]}"

    user_msgs = data.get("user_messages", [])
    primary_intent = user_msgs[0][:200] if user_msgs else "Autonomous session"
    summary = generate_session_summary(data)
    turns = data.get("interaction_turns", [])

    # Outcome is PARTIAL only if the final turn ended with unresolved tool/pivot errors
    final_turn_errors = turns[-1].get("errors", []) if turns else []
    outcome = "PARTIAL" if (final_turn_errors and len(data.get("errors_encountered", [])) > 0) else "SUCCESS"

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
        "interaction_turns": turns,
        "preferences_extracted": [],
        "friction_count": len(data["errors_encountered"]),
    }

    if dry_run:
        result["dry_run"] = True
        return result

    with get_connection() as conn:
        # 0. Zero-Daemon In-Query Pruning: remove deleted file nodes (cascades to graph_edges)
        conn.execute("DELETE FROM graph_nodes WHERE node_type = 'file' AND fs_exists(name) = 0;")

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

        # 2. Upsert trace with full interaction trajectory & task_outcome_observed flag
        task_outcome_observed = 1 if (outcome == "SUCCESS" and (len(data.get("verification_commands", [])) > 0 or data.get("total_turns", 0) >= 1)) else 0
        evidence_json = json.dumps(
            {
                "transcript_path": data["transcript_path"],
                "task_outcome_observed": task_outcome_observed,
                "tools_used": data["tools_used"],
                "skills_observed": data["skills_observed"],
                "verification_commands": data["verification_commands"][-10:],
                "interaction_turns": turns,
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

        # 2b. Sync interaction_turns into trace_steps (required by adk-skill-synthesizer & adk-gepa-lite)
        conn.execute("DELETE FROM trace_steps WHERE trace_id = ?;", (trace_id,))
        for idx, t in enumerate(turns, start=1):
            t_tools = t.get("tools_called") or []
            t_errs = t.get("errors") or []
            t_cmds = t.get("commands_run") or []
            t_files = t.get("files_touched") or []
            if t.get("is_user_pivot") or t_errs:
                st_type = "fix"
            elif t_cmds:
                st_type = "test"
            elif any(x in ("edit_file", "write_file") for x in t_tools):
                st_type = "impl"
            elif idx == 1:
                st_type = "clarify"
            else:
                st_type = "other"

            if t.get("is_user_pivot"):
                st_outcome = "retry"
            elif t_errs:
                st_outcome = "fail"
            else:
                st_outcome = "pass"

            conn.execute(
                """
                INSERT INTO trace_steps (
                    trace_id, step_order, step_type, description, tool_used,
                    input_summary, output_summary, outcome, friction_note
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?);
                """,
                (
                    trace_id,
                    idx,
                    st_type,
                    (t.get("user_prompt") or f"Turn {idx}")[:200],
                    ", ".join(t_tools[:4]) if t_tools else None,
                    (t.get("user_prompt") or "")[:160],
                    f"files={len(t_files)}, cmds={len(t_cmds)}",
                    st_outcome,
                    t_errs[0][:160] if t_errs else ("USER_PIVOT" if t.get("is_user_pivot") else None),
                ),
            )

        # 3. Record Observed Skills in `skills` and `skills_used` (idempotent per trace, per-skill outcome)
        prev_skills = {
            r["skill_name"]: r["outcome"]
            for r in conn.execute("SELECT skill_name, outcome FROM skills_used WHERE trace_id = ?;", (trace_id,)).fetchall()
        }
        conn.execute("DELETE FROM skills_used WHERE trace_id = ?;", (trace_id,))
        unresolved_skills = set(turns[-1].get("skills_loaded", [])) if final_turn_errors else set()
        for sk_name in data.get("skills_observed", []):
            sk_success = 0 if (sk_name in unresolved_skills and outcome != "SUCCESS") else 1
            sk_used_outcome = "success" if sk_success == 1 else "partial"
            if sk_name not in prev_skills:
                conn.execute(
                    """
                    INSERT INTO skills (name, skill_group, times_used, times_succeeded, last_used_at)
                    VALUES (?, 'core', 1, ?, strftime('%Y-%m-%dT%H:%M:%SZ', 'now'))
                    ON CONFLICT(name) DO UPDATE SET
                        times_used = skills.times_used + 1,
                        times_succeeded = skills.times_succeeded + ?,
                        last_used_at = strftime('%Y-%m-%dT%H:%M:%SZ', 'now');
                    """,
                    (sk_name, sk_success, sk_success),
                )
            else:
                prev_succ = 1 if prev_skills[sk_name] == "success" else 0
                delta_succ = sk_success - prev_succ
                if delta_succ != 0:
                    conn.execute(
                        "UPDATE skills SET times_succeeded = MAX(0, times_succeeded + ?) WHERE name = ?;",
                        (delta_succ, sk_name),
                    )
            conn.execute(
                """
                INSERT INTO skills_used (trace_id, skill_name, outcome)
                VALUES (?, ?, ?);
                """,
                (trace_id, sk_name, sk_used_outcome),
            )

        # 4. Replace friction points & populate Empirical Entity Graph (idempotent per trace)
        conn.execute("DELETE FROM friction_points WHERE trace_id = ?;", (trace_id,))
        post_hoc_skills = {"adk-code-review", "adk-git-content", "adk-regression-checklist"}
        impl_skills = [s for s in data.get("skills_observed", []) if s not in post_hoc_skills]
        fallback_skill = impl_skills[-1] if impl_skills else None
        current_trace_file_frictions: set[tuple[str, str]] = set()
        for err in data.get("errors_encountered", [])[:8]:
            cat = err.get("category") or "tool_error"
            rel_file = err.get("related_file")
            raw_skill = err.get("related_skill")
            rel_skill = raw_skill if (raw_skill and raw_skill not in post_hoc_skills) else fallback_skill
            fp_id = err.get("fingerprint") or cat
            fp_sum = err.get("fingerprint_summary") or err.get("content", "")[:140]
            if rel_file:
                current_trace_file_frictions.add((rel_file, f"friction:{fp_id}"))
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
                    fp_sum,
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

        # 5. Populate Empirical File <-> Implementation Skill Edges & auto-infer RESOLVES edges
        if upsert_graph_link is not None:
            active_skills: list[str] = []
            for turn in turns:
                for sk in turn.get("skills_loaded", []):
                    if sk not in post_hoc_skills and sk not in active_skills:
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
                        # Auto-infer (skill) --[RESOLVES]--> (friction) when session succeeds cleanly
                        if outcome == "SUCCESS":
                            past_frictions = conn.execute(
                                """
                                SELECT fn.id, fn.name, fn.summary
                                FROM graph_edges ge
                                JOIN graph_nodes fn ON fn.id = ge.target_id
                                WHERE ge.source_id = ?
                                  AND ge.edge_type = 'SUFFERED_FROM'
                                  AND fn.node_type = 'friction';
                                """,
                                (f"file:{f_path}",),
                            ).fetchall()
                            for pf in past_frictions:
                                if not final_turn_errors:
                                    upsert_graph_link(
                                        conn,
                                        f"skill:{sk}",
                                        "skill",
                                        sk,
                                        None,
                                        pf["id"],
                                        "friction",
                                        pf["name"],
                                        pf["summary"],
                                        "RESOLVES",
                                        trace_id,
                                    )

        # 6. Extract top Empirical File Guardrails (filtered by fs_exists & ranked by Time-Decay effective_score)
        guard_cur = conn.execute(
            """
            SELECT
                s.name AS file_path,
                t.name AS friction_type,
                t.summary AS how_to_operate,
                e.hit_count,
                ROUND(
                    CAST(e.hit_count AS REAL) /
                    (1.0 + 0.1 * MAX(0.0, julianday('now') - julianday(COALESCE(e.last_seen, 'now')))),
                    2
                ) AS effective_score,
                (
                    SELECT GROUP_CONCAT(sk.name, ', ')
                    FROM graph_edges es
                    JOIN graph_nodes sk ON sk.id = es.target_id
                    WHERE es.source_id = s.id
                      AND es.edge_type = 'USED_WITH_SKILL'
                      AND sk.name NOT IN ('adk-code-review', 'adk-git-content', 'adk-regression-checklist')
                ) AS impl_skills
            FROM graph_edges e
            JOIN graph_nodes s ON s.id = e.source_id
            JOIN graph_nodes t ON t.id = e.target_id
            WHERE s.node_type = 'file'
              AND e.edge_type = 'SUFFERED_FROM'
              AND fs_exists(s.name) = 1
            ORDER BY effective_score DESC, e.hit_count DESC, e.last_seen DESC
            LIMIT 10;
            """
        )
        data["file_guardrails"] = [dict(r) for r in guard_cur.fetchall()]

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
