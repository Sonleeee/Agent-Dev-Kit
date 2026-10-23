#!/usr/bin/env python3
"""
ADK Session Curator
Autonomous post-session reflection engine.
Reads conversation transcripts (transcript.jsonl), extracts:
  1. Session summary & user intent
  2. Developer style, communication habits & preferences
  3. Friction points (errors, retries, user corrections)
Persists everything directly into evolution.db without requiring user to trigger /wf.
Compatible with Antigravity Lifecycle Hooks ('Stop' event via hooks.json) and CLI execution.
"""

from __future__ import annotations

import datetime
import json
import os
from pathlib import Path
import re
import sys
import threading
import time
from typing import Any

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
        cmd_log_session,
        cmd_log_preference,
        cmd_sync_profile,
        get_db_path,
    )
except ImportError:
    # Direct fallback if imported independently
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

    cmd_log_session = None
    cmd_log_preference = None
    cmd_sync_profile = None


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
    text = re.sub(r"@\[.*?\]", "", text)  # remove mentions like @[Quote]
    return text.strip()


def parse_transcript(transcript_path: Path) -> dict[str, Any]:
    """Parse transcript.jsonl into structured conversation history."""
    if not transcript_path.exists():
        raise FileNotFoundError(f"Transcript not found: {transcript_path}")

    # Extract conversation_id from path if possible
    # e.g. ~/.gemini/antigravity/brain/<conv_id>/.system_generated/logs/transcript.jsonl
    conv_id = transcript_path.parent.parent.parent.name
    if not conv_id or len(conv_id) < 8:
        conv_id = transcript_path.stem

    user_messages: list[str] = []
    assistant_messages: list[str] = []
    tools_used: set[str] = set()
    errors_encountered: list[dict[str, Any]] = []
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

            # Count tokens if recorded
            in_tok = obj.get("input_tokens", 0) or 0
            out_tok = obj.get("output_tokens", 0) or 0
            total_tokens += (in_tok + out_tok)

            if msg_type == "USER_INPUT" and source == "USER_EXPLICIT":
                total_turns += 1
                cleaned = clean_user_message(content)
                if cleaned:
                    user_messages.append(cleaned)

            elif msg_type in ("PLANNER_RESPONSE", "GENERIC") and source == "MODEL":
                if content:
                    assistant_messages.append(content[:500])
                for call in obj.get("tool_calls", []):
                    tool_name = call.get("name") or call.get("toolName") or "tool"
                    tools_used.add(tool_name)

            # Check for error status
            if obj.get("status") == "ERROR" or (obj.get("tool_calls") and any(c.get("status") == "ERROR" for c in obj.get("tool_calls", []))):
                errors_encountered.append({
                    "step_index": obj.get("step_index"),
                    "source": source,
                    "content": (content or "")[:300],
                })

    return {
        "conversation_id": conv_id,
        "transcript_path": str(transcript_path),
        "total_turns": total_turns,
        "total_tokens": total_tokens,
        "user_messages": user_messages,
        "assistant_messages": assistant_messages,
        "tools_used": sorted(list(tools_used)),
        "errors_encountered": errors_encountered,
    }


def analyze_dev_style(user_messages: list[str]) -> list[dict[str, Any]]:
    """Analyze user prompts to extract coding style, communication tone, and preferences."""
    preferences: list[dict[str, Any]] = []
    if not user_messages:
        return preferences

    combined_text = " \n ".join(user_messages).lower()

    # 1. Communication tone & density
    avg_len = sum(len(m.split()) for m in user_messages) / len(user_messages)
    if avg_len <= 15:
        preferences.append({
            "key": "communication.tone",
            "value": "Cực kỳ ngắn gọn, súc tích (concise/terse), đi thẳng vào hành động",
            "confidence": 0.85,
        })
    elif avg_len > 60:
        preferences.append({
            "key": "communication.tone",
            "value": "Chi tiết, đầy đủ bối cảnh, mô tả cụ thể yêu cầu",
            "confidence": 0.75,
        })

    # 2. Architectural & Analysis Preferences
    if any(k in combined_text for k in ["bản chất", "cơ chế", "so sánh", "kiến trúc", "research", "tại sao"]):
        preferences.append({
            "key": "analysis.depth",
            "value": "Ưu tiên phân tích sâu cơ chế hoạt động cốt lõi, so sánh kiến trúc thực tế",
            "confidence": 0.90,
        })

    # 3. Automation & Workflow Philosophy
    if any(k in combined_text for k in ["tự động", "không cần gõ", "chịu thua", "k gọi wf"]):
        preferences.append({
            "key": "automation.philosophy",
            "value": "Tự động hóa ngầm tối đa, không phụ thuộc vào việc dev phải nhớ gõ lệnh thủ công",
            "confidence": 0.95,
        })

    # 4. Process vs Result capture
    if any(k in combined_text for k in ["style của dev", "trong 1 quá trình", "k thể bắt được style", "lưu được 1 summary"]):
        preferences.append({
            "key": "learning.capture_mode",
            "value": "Ưu tiên ghi nhận toàn bộ quá trình hội thoại và gu lập trình thay vì chỉ lấy commit snapshot",
            "confidence": 0.95,
        })

    # 5. Regex detection for explicit instructions:
    # "đừng [làm gì]"
    avoid_matches = re.findall(r"(?:đừng|không nên|tránh)\s+([a-zA-Z0-9_\-\sàáạảãâầấậẩẫăằắặẳẵèéẹẻẽêềếệểễìíịỉĩòóọỏõôồốộổỗơờớợởỡùúụủũưừứựửữỳýỵỷỹđ]{3,40})", combined_text)
    for m in avoid_matches[:2]:
        val = m.strip()
        if len(val) > 3 and not any(skip in val for val in ["lo", "sợ", "ngại"]):
            preferences.append({
                "key": f"taboo.avoid_{val[:15].replace(' ', '_')}",
                "value": f"Tránh hoặc hạn chế: {val}",
                "confidence": 0.75,
            })

    # "ưu tiên [gì đó]"
    priority_matches = re.findall(r"(?:ưu tiên|hãy dùng|nên dùng)\s+([a-zA-Z0-9_\-\sàáạảãâầấậẩẫăằắặẳẵèéẹẻẽêềếệểễìíịỉĩòóọỏõôồốộổỗơờớợởỡùúụủũưừứựửữỳýỵỷỹđ]{3,40})", combined_text)
    for m in priority_matches[:2]:
        val = m.strip()
        if len(val) > 3:
            preferences.append({
                "key": f"tech_preference.{val[:15].replace(' ', '_')}",
                "value": f"Ưu tiên sử dụng: {val}",
                "confidence": 0.80,
            })

    return preferences


def generate_session_summary(data: dict[str, Any]) -> str:
    """Generate concise, factual summary of the session."""
    user_msgs = data.get("user_messages", [])
    if not user_msgs:
        return "Session with no explicit user messages."

    first_req = user_msgs[0][:150]
    last_req = user_msgs[-1][:150] if len(user_msgs) > 1 else ""
    tools_str = ", ".join(data.get("tools_used", [])[:5]) or "none"

    if len(user_msgs) == 1:
        return f"Yêu cầu: {first_req}. Đã xử lý bằng tools: [{tools_str}]."

    return (
        f"Mục tiêu ban đầu: '{first_req}'. "
        f"Qua {data.get('total_turns', 0)} lượt trao đổi, người dùng đã làm rõ/yêu cầu thêm: '{last_req}'. "
        f"Công cụ đã sử dụng: [{tools_str}]."
    )


def curate_session(transcript_path: Path, dry_run: bool = False, sync_profile_enabled: bool = True) -> dict[str, Any]:
    """Execute full curation on a transcript: parse, extract, store into SQLite and sync."""
    data = parse_transcript(transcript_path)
    conv_id = data["conversation_id"]
    sess_id = f"sess_conv_{conv_id[:12]}"
    trace_id = f"trace_conv_{conv_id[:12]}"

    user_msgs = data.get("user_messages", [])
    primary_intent = user_msgs[0][:200] if user_msgs else "Autonomous session"
    summary = generate_session_summary(data)
    preferences = analyze_dev_style(user_msgs)

    # Determine outcome
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
        "preferences_extracted": preferences,
        "friction_count": len(data["errors_encountered"]),
    }

    if dry_run:
        result["dry_run"] = True
        return result

    # Persist to evolution.db
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
                total_turns = COALESCE(excluded.total_turns, sessions.total_turns),
                total_tokens = COALESCE(excluded.total_tokens, sessions.total_tokens),
                summary = COALESCE(excluded.summary, sessions.summary);
            """,
            (
                sess_id,
                "Agent-Dev-Kit",
                primary_intent,
                "autonomous-curator",
                outcome,
                data["total_turns"],
                data["total_tokens"],
                summary,
            ),
        )

        # 2. Upsert trace
        evidence_json = json.dumps({
            "transcript_path": data["transcript_path"],
            "tools_used": data["tools_used"],
            "user_messages_count": len(user_msgs),
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
                "autonomous-curator",
                "Medium" if data["total_turns"] > 3 else "Low",
                outcome,
                data["total_turns"],
                data["total_tokens"],
                evidence_json,
            ),
        )

        # 3. Log friction points if errors occurred
        for err in data.get("errors_encountered", [])[:5]:
            conn.execute(
                """
                INSERT INTO friction_points (trace_id, category, description, severity, suggested_fix)
                VALUES (?, ?, ?, ?, ?);
                """,
                (
                    trace_id,
                    "tool_error",
                    f"Error at step {err.get('step_index')}: {err.get('content', '')[:150]}",
                    "medium",
                    "Verify syntax and platform-specific commands before execution",
                ),
            )

        # 4. Upsert user preferences
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

    # 5. Sync to ~/.agents/developer.md
    if sync_profile_enabled:
        try:
            from tools.evolution_db import cmd_sync_profile
            sync_res = cmd_sync_profile({"min_confidence": 0.7})
            result["profile_sync"] = sync_res
        except Exception as e:
            result["profile_sync_error"] = str(e)

    return result


def main() -> None:
    """Entry point for Antigravity Hook ('Stop' event) or CLI execution."""
    transcript_path: Path | None = None
    dry_run = "--dry-run" in sys.argv
    is_hook = "--hook" in sys.argv

    # 1. Read stdin if invoked as hook or if stdin data is piped
    stdin_payload: dict[str, Any] | None = None
    raw_stdin = read_stdin_with_timeout(timeout_sec=0.5).strip()
    if raw_stdin.startswith("{") and raw_stdin.endswith("}"):
        try:
            stdin_payload = json.loads(raw_stdin)
        except Exception:
            stdin_payload = None

    if stdin_payload and "transcriptPath" in stdin_payload:
        transcript_path = Path(stdin_payload["transcriptPath"])

    # 2. Check CLI flags for explicit transcript
    if not transcript_path:
        for i, arg in enumerate(sys.argv):
            if arg in ("--transcript", "-t") and i + 1 < len(sys.argv):
                transcript_path = Path(sys.argv[i + 1])
                break

    # 3. Fallback to latest transcript in brain directory
    if not transcript_path or not transcript_path.exists():
        transcript_path = find_latest_transcript()

    if not transcript_path or not transcript_path.exists():
        # Clean exit for hook compatibility
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
