#!/usr/bin/env python3
"""
ADK Session Curator
Autonomous post-session reflection & interaction trajectory engine.
Reads conversation transcripts (transcript.jsonl), extracts:
  1. Turn-by-turn User <-> Agent Interaction Trajectory & Pivot Points
  2. Observed Skills actually read during the session (read_file on SKILL.md)
  3. Observed Verification Commands executed (run_command)
  4. Friction points (tool errors, retries, explicit user corrections)
  5. Explicit Developer Preferences (only high-signal directives, zero toy regex)
Persists everything into evolution.db without requiring manual commands.
Compatible with Antigravity Lifecycle Hooks ('Stop' event via hooks.json) and CLI execution.
"""

from __future__ import annotations

import json
import os
from pathlib import Path
import re
import sys
import threading
from typing import Any

sys.dont_write_bytecode = True

# Configure UTF-8 stdout for Windows consoles
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")
if hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(encoding="utf-8")


def read_stdin_with_timeout(timeout_sec: float = 0.5) -> str:
    """Read stdin with a non-blocking timeout to prevent hanging on open pipes."""
    res = [""]

    def worker():
        try:
            res[0] = sys.stdin.read()
        except Exception:
            pass

    t = threading.Thread(target=worker, daemon=True)
    t.start()
    t.join(timeout=timeout_sec)
    return res[0]


# Ensure ADK root is in sys.path
ADK_ROOT = Path(__file__).resolve().parent.parent
if str(ADK_ROOT) not in sys.path:
    sys.path.insert(0, str(ADK_ROOT))

try:
    from tools.evolution_db import (
        get_connection,
        cmd_sync_profile,
        get_db_path,
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


SKILL_PATH_RE = re.compile(r"[/\\]+(sk-[a-z0-9\-]+)[/\\]+SKILL\.md$", re.IGNORECASE)
PIVOT_KEYWORDS_RE = re.compile(
    r"\b(?:không phải|sai rồi|đừng làm thế|bỏ đi|làm lại|sửa lại|ý tôi là|chuyển sang)\b",
    re.IGNORECASE,
)


def find_latest_transcript() -> Path | None:
    """Find the most recently modified transcript.jsonl under ~/.gemini/antigravity/brain."""
    brain_dir = Path.home() / ".gemini" / "antigravity" / "brain"
    if not brain_dir.exists():
        return None

    candidates: list[Path] = []
    for log_file in brain_dir.glob("*/.system_generated/logs/transcript.jsonl"):
        if log_file.is_file():
            candidates.append(log_file)

    if not candidates:
        return None

    candidates.sort(key=lambda p: p.stat().st_mtime, reverse=True)
    return candidates[0]


def clean_user_message(content: str) -> str:
    """Remove Antigravity XML tags (<USER_REQUEST>, <ADDITIONAL_METADATA>) from user text."""
    if not content:
        return ""
    text = re.sub(r"<ADDITIONAL_METADATA>[\s\S]*?</ADDITIONAL_METADATA>", "", content)
    text = re.sub(r"<USER_SETTINGS_CHANGE>[\s\S]*?</USER_SETTINGS_CHANGE>", "", text)
    match = re.search(r"<USER_REQUEST>([\s\S]*?)</USER_REQUEST>", text)
    if match:
        text = match.group(1)
    text = re.sub(r"@\[.*?\]", "", text)
    return text.strip()


def parse_transcript(transcript_path: Path) -> dict[str, Any]:
    """Parse transcript.jsonl into structured User <-> Agent interaction trajectory."""
    if not transcript_path.exists():
        raise FileNotFoundError(f"Transcript not found: {transcript_path}")

    conv_id = transcript_path.parent.parent.parent.name
    if not conv_id or len(conv_id) < 8:
        conv_id = transcript_path.stem

    user_messages: list[str] = []
    assistant_messages: list[str] = []
    tools_used: set[str] = set()
    skills_observed: list[str] = []
    verification_commands: list[dict[str, str]] = []
    errors_encountered: list[dict[str, Any]] = []
    interaction_turns: list[dict[str, Any]] = []
    current_turn: dict[str, Any] | None = None
    total_tokens = 0
    total_turns = 0

    with transcript_path.open("r", encoding="utf-8", errors="replace") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                obj = json.loads(line)
            except Exception:
                continue

            msg_type = obj.get("type")
            source = obj.get("source")
            content = obj.get("content", "")
            step_index = obj.get("step_index")

            in_tok = obj.get("input_tokens", 0) or 0
            out_tok = obj.get("output_tokens", 0) or 0
            total_tokens += (in_tok + out_tok)

            if msg_type == "USER_INPUT" and source == "USER_EXPLICIT":
                total_turns += 1
                cleaned = clean_user_message(content)
                if cleaned:
                    user_messages.append(cleaned)
                is_pivot = bool(total_turns > 1 and PIVOT_KEYWORDS_RE.search(cleaned))
                current_turn = {
                    "turn": total_turns,
                    "step_index": step_index,
                    "user_prompt": cleaned[:300],
                    "is_user_pivot": is_pivot,
                    "tools_called": [],
                    "skills_loaded": [],
                    "commands_run": [],
                    "errors": [],
                }
                interaction_turns.append(current_turn)
                if is_pivot:
                    errors_encountered.append({
                        "step_index": step_index,
                        "category": "user_correction",
                        "source": "USER_EXPLICIT",
                        "content": f"User pivot/correction at turn {total_turns}: {cleaned[:200]}",
                    })

            elif msg_type in ("PLANNER_RESPONSE", "GENERIC") and source == "MODEL":
                if content:
                    assistant_messages.append(content[:500])
                for call in obj.get("tool_calls", []):
                    tool_name = call.get("name") or call.get("toolName") or "tool"
                    tools_used.add(tool_name)
                    if current_turn is not None and tool_name not in current_turn["tools_called"]:
                        current_turn["tools_called"].append(tool_name)

                    args = call.get("args") or call.get("arguments") or {}
                    if isinstance(args, str):
                        try:
                            args = json.loads(args)
                        except Exception:
                            args = {}

                    # 1. Detect Observed Skill Loads (read_file on .../sk-*/SKILL.md)
                    if tool_name == "read_file" and isinstance(args, dict):
                        file_path = str(args.get("Path") or args.get("path") or "").strip().strip('"')
                        m_skill = SKILL_PATH_RE.search(file_path)
                        if m_skill:
                            sk_name = m_skill.group(1).lower()
                            if sk_name not in skills_observed:
                                skills_observed.append(sk_name)
                            if current_turn is not None and sk_name not in current_turn["skills_loaded"]:
                                current_turn["skills_loaded"].append(sk_name)

                    # 2. Detect Observed Commands (run_command)
                    if tool_name == "run_command" and isinstance(args, dict):
                        cmd_line = str(args.get("CommandLine") or args.get("command") or "").strip().strip('"')
                        summary_label = str(args.get("toolSummary") or "").strip().strip('"')
                        if cmd_line:
                            cmd_entry = {
                                "step_index": str(step_index),
                                "summary": summary_label[:80],
                                "command": cmd_line[:200],
                            }
                            verification_commands.append(cmd_entry)
                            if current_turn is not None:
                                current_turn["commands_run"].append(cmd_line[:120])

            # 3. Check for Tool or Step Error Status
            has_step_err = obj.get("status") == "ERROR"
            has_call_err = bool(
                obj.get("tool_calls")
                and any(c.get("status") == "ERROR" for c in obj.get("tool_calls", []))
            )
            if has_step_err or has_call_err:
                raw_err = re.sub(r"^(?:Created|Completed) At:[^\n]*\n?", "", content or "", flags=re.MULTILINE).strip()
                err_item = {
                    "step_index": step_index,
                    "category": "tool_error",
                    "source": source,
                    "content": (raw_err or "Tool execution error")[:250],
                }
                errors_encountered.append(err_item)
                if current_turn is not None:
                    current_turn["errors"].append(err_item["content"][:120])

    return {
        "conversation_id": conv_id,
        "transcript_path": str(transcript_path),
        "total_turns": total_turns,
        "total_tokens": total_tokens,
        "user_messages": user_messages,
        "assistant_messages": assistant_messages,
        "tools_used": sorted(list(tools_used)),
        "skills_observed": skills_observed,
        "verification_commands": verification_commands,
        "interaction_turns": interaction_turns,
        "errors_encountered": errors_encountered,
    }


def analyze_dev_style(user_messages: list[str]) -> list[dict[str, Any]]:
    """Extract only high-confidence communication density signals without hardcoded keyword pollution."""
    preferences: list[dict[str, Any]] = []
    if not user_messages:
        return preferences

    avg_words = sum(len(m.split()) for m in user_messages) / len(user_messages)
    if avg_words <= 18:
        preferences.append({
            "key": "communication.prompt_density",
            "value": "Ngắn gọn, trực diện (avg <= 18 từ/lượt); ưu tiên trả lời thẳng vào kết quả",
            "confidence": 0.75,
        })
    elif avg_words >= 65:
        preferences.append({
            "key": "communication.prompt_density",
            "value": "Đầy đủ bối cảnh và ràng buộc chi tiết trong mỗi lượt prompt",
            "confidence": 0.75,
        })

    return preferences


def generate_session_summary(data: dict[str, Any]) -> str:
    """Generate concise, factual summary of the session including observed skills & commands."""
    user_msgs = data.get("user_messages", [])
    if not user_msgs:
        return "Session with no explicit user messages."

    first_req = user_msgs[0][:140].replace("\n", " ")
    last_req = user_msgs[-1][:140].replace("\n", " ") if len(user_msgs) > 1 else ""
    tools_str = ", ".join(data.get("tools_used", [])[:6]) or "none"
    skills_str = ", ".join(data.get("skills_observed", [])) or "none"

    if len(user_msgs) == 1:
        return f"Yêu cầu: '{first_req}'. Skills đã nạp: [{skills_str}]. Tools: [{tools_str}]."

    return (
        f"Khởi đầu: '{first_req}' -> Lượt cuối ({data.get('total_turns', 0)} turns): '{last_req}'. "
        f"Skills đã nạp: [{skills_str}]. Tools: [{tools_str}]."
    )


def write_runtime_artifacts(
    data: dict[str, Any],
    sess_id: str,
    outcome: str,
    summary: str,
) -> dict[str, str]:
    """Write human-readable interaction journal and Typed Handoff Packet to .agents/runtime/."""
    from datetime import datetime, timezone

    now_iso = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    runtime_dir = ADK_ROOT / ".agents" / "runtime"
    runtime_dir.mkdir(parents=True, exist_ok=True)

    handoff_path = runtime_dir / "latest-handoff.md"
    journal_path = runtime_dir / "session-journal.md"

    conv_id = data["conversation_id"]
    turns = data.get("interaction_turns", [])
    skills_obs = ", ".join(f"`{s}`" for s in data.get("skills_observed", [])) or "_(none)_"
    tools_obs = ", ".join(f"`{t}`" for t in data.get("tools_used", [])) or "_(none)_"

    # 1. Build Typed Handoff Packet (akitaonrails/ai-memory pattern: zero-LLM cross-agent continuity)
    handoff_lines = [
        f"# Typed Handoff Packet — `{sess_id}`",
        "",
        f"- **Conversation ID:** `{conv_id}`",
        f"- **Updated At (UTC):** `{now_iso}`",
        f"- **Outcome:** `{outcome}` | **Turns:** `{data.get('total_turns', 0)}` | **Tokens:** `{data.get('total_tokens', 0)}`",
        f"- **Observed Skills Loaded:** {skills_obs}",
        f"- **Tools Used:** {tools_obs}",
        "",
        "## 1. Executive Summary",
        f"> {summary}",
        "",
        "## 2. Turn-by-Turn Interaction Trajectory",
        "| Turn | User Intent / Prompt | Skills Loaded | Verification / Commands | Pivot / Friction |",
        "|:---:|---|---|---|---|",
    ]
    for t in turns:
        prompt_snip = t["user_prompt"].replace("\n", " ").replace("|", "\\|")[:110]
        sk_list = ", ".join(f"`{s}`" for s in t.get("skills_loaded", [])) or "-"
        cmd_list = ", ".join(f"`{c[:45]}`" for c in t.get("commands_run", [])[:2]) or "-"
        pivot_flag = "⚠️ **USER_PIVOT**" if t.get("is_user_pivot") else ("❌ Error" if t.get("errors") else "✅ OK")
        handoff_lines.append(f"| {t['turn']} | {prompt_snip} | {sk_list} | {cmd_list} | {pivot_flag} |")

    handoff_lines.extend([
        "",
        "## 3. Verified Commands Executed (Last 8)",
    ])
    ver_cmds = data.get("verification_commands", [])[-8:]
    if ver_cmds:
        for vc in ver_cmds:
            handoff_lines.append(f"- `[Step {vc['step_index']}]` **{vc['summary'] or 'cmd'}**: `{vc['command']}`")
    else:
        handoff_lines.append("- _(No verification commands recorded)_")

    handoff_lines.extend([
        "",
        "## 4. Friction & Failed Approaches to Avoid",
    ])
    errs = data.get("errors_encountered", [])[-6:]
    if errs:
        for e in errs:
            clean_err = str(e.get("content", "")).replace("\n", " ")[:160]
            handoff_lines.append(f"- **[{e.get('category', 'error')}]** (Step {e.get('step_index')}): {clean_err}")
    else:
        handoff_lines.append("- _(Zero tool errors or user pivot corrections in this session)_")

    handoff_path.write_text("\n".join(handoff_lines) + "\n", encoding="utf-8")

    # 2. Upsert Session Block inside session-journal.md
    session_header = f"## Session `{sess_id}` ({now_iso[:10]})"
    journal_entry_lines = [
        session_header,
        f"- **Conversation:** `{conv_id}` | **Turns:** `{data.get('total_turns', 0)}` | **Outcome:** `{outcome}`",
        f"- **Observed Skills:** {skills_obs}",
        f"- **Summary:** {summary}",
        "",
        "| Turn | User Prompt | Skills | Commands Count | Status |",
        "|:---:|---|---|:---:|---|",
    ]
    for t in turns:
        p_short = t["user_prompt"].replace("\n", " ").replace("|", "\\|")[:90]
        sk_short = ", ".join(t.get("skills_loaded", [])) or "-"
        c_cnt = len(t.get("commands_run", []))
        st = "PIVOT" if t.get("is_user_pivot") else ("ERR" if t.get("errors") else "OK")
        journal_entry_lines.append(f"| {t['turn']} | {p_short} | {sk_short} | {c_cnt} | {st} |")
    journal_entry_lines.append("")
    entry_block = "\n".join(journal_entry_lines)

    if journal_path.exists():
        existing = journal_path.read_text(encoding="utf-8", errors="replace")
        pattern = re.compile(
            rf"^## Session `{re.escape(sess_id)}`.*?(?=^## Session `|\Z)",
            re.MULTILINE | re.DOTALL,
        )
        if pattern.search(existing):
            updated = pattern.sub(entry_block + "\n", existing)
        else:
            updated = existing.rstrip() + "\n\n" + entry_block + "\n"
        journal_path.write_text(updated, encoding="utf-8")
    else:
        header = "# ADK User ↔ Agent Interaction Journal\n\n> Tự động trích xuất từ `transcript.jsonl` qua `tools/session_curator.py`.\n\n"
        journal_path.write_text(header + entry_block + "\n", encoding="utf-8")

    return {
        "latest_handoff": str(handoff_path),
        "session_journal": str(journal_path),
    }


def curate_session(transcript_path: Path, dry_run: bool = False, sync_profile_enabled: bool = True) -> dict[str, Any]:
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
        evidence_json = json.dumps({
            "transcript_path": data["transcript_path"],
            "tools_used": data["tools_used"],
            "skills_observed": data["skills_observed"],
            "verification_commands": data["verification_commands"][-10:],
            "interaction_turns": data["interaction_turns"],
            "errors_count": len(data["errors_encountered"]),
        }, ensure_ascii=False)

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

        # 4. Replace friction points for this trace (idempotent re-runs)
        conn.execute("DELETE FROM friction_points WHERE trace_id = ?;", (trace_id,))
        last_skill = data["skills_observed"][-1] if data.get("skills_observed") else None
        for err in data.get("errors_encountered", [])[:8]:
            cat = err.get("category") or "tool_error"
            conn.execute(
                """
                INSERT INTO friction_points (trace_id, category, description, severity, related_skill, suggested_fix)
                VALUES (?, ?, ?, ?, ?, ?);
                """,
                (
                    trace_id,
                    cat,
                    f"Step {err.get('step_index')}: {err.get('content', '')[:180]}",
                    "medium",
                    last_skill,
                    "Review turn trajectory and add deterministic guard/script if recurring",
                ),
            )

        # 5. Upsert user preferences
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
        result["runtime_artifacts"] = write_runtime_artifacts(data, sess_id, outcome, summary)
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
