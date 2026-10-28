"""
ADK Session Curator - Transcript Parser & Stream Extractor
Parses Antigravity transcript.jsonl into turn-by-turn interaction trajectory.
"""

from __future__ import annotations

import json
from pathlib import Path
import re
import sys
import threading
from typing import Any

sys.dont_write_bytecode = True

SKILL_PATH_RE = re.compile(r"[/\\]+((?:adk|sk)-[a-z0-9\-]+)[/\\]+SKILL\.md$", re.IGNORECASE)
PIVOT_KEYWORDS_RE = re.compile(
    r"\b(?:không phải|sai rồi|đừng làm thế|bỏ đi|làm lại|sửa lại|ý tôi là|chuyển sang)\b",
    re.IGNORECASE,
)


def normalize_project_file(raw_path: str) -> str | None:
    """Normalize file path into clean forward-slash relative project path."""
    if not raw_path:
        return None
    cleaned = raw_path.strip().strip('"').strip("'").replace("\\\\", "/").replace("\\", "/")
    lower = cleaned.lower()
    if "/.gemini/" in lower or "/appdata/" in lower or "transcript.jsonl" in lower:
        return None
    for marker in ("/agent-dev-kit/.agents/", "/agent-dev-kit/", "/.agents/"):
        idx = lower.find(marker)
        if idx != -1:
            rel = cleaned[idx + len(marker) :].lstrip("/")
            return rel if rel else None
    parts = [p for p in cleaned.split("/") if p and not p.endswith(":")]
    if len(parts) > 3:
        return "/".join(parts[-3:])
    return "/".join(parts) if parts else None


def fingerprint_error(category: str, content: str) -> tuple[str, str]:
    """Map raw tool/step error text into a deterministic (fingerprint_id, actionable_guardrail) pair."""
    if category == "user_correction":
        return ("user_correction", "Đọc kỹ yêu cầu chỉnh sửa của Dev ở lượt trước để không lặp lại giả định cũ")
    low = (content or "").lower()
    if "target content not found" in low:
        return ("edit_target_mismatch", "Đọc lại đúng line range bằng read_file ngay trước khi edit_file; giữ nguyên CRLF/indent")
    if "unicodeencodeerror" in low or "failed to detect charset" in low or "charmap" in low:
        return ("encoding_charset", "Luôn truyền encoding='utf-8' khi đọc/ghi file và reconfigure stdout UTF-8 trên Windows")
    if "appears to be a binary file" in low:
        return ("binary_file_read", "Không gọi read_file trên file nhị phân (.db, .pyc) hoặc UTF-16LE; dùng python/sqlite3 để đọc")
    if "does not exist" in low or "cannot find path" in low or "filenotfounderror" in low or "pathnotfound" in low:
        return ("path_not_found", "Kiểm tra đường dẫn tồn tại trước khi đọc/chạy lệnh; không đoán mò vị trí file")
    if "artifactmetadata was provided" in low:
        return ("invalid_artifact_path", "Chỉ truyền ArtifactMetadata khi ghi vào brain/<conversation-id>; bỏ trống với file trong repo")
    if "no such column" in low or "operationalerror" in low or "sqlite3." in low:
        return ("sql_schema_mismatch", "Chạy ensure_schema_migrations() hoặc kiểm tra PRAGMA table_info trước khi truy vấn/tạo index cột mới")
    if "syntaxerror" in low or "parsererror" in low or "missing argument" in low or "unexpected token" in low:
        return ("shell_or_syntax_error", "Trên Windows PowerShell dùng py -3 và tránh chuỗi multiline phức tạp trong python -c")
    return ("tool_execution_error", "Kiểm tra tham số đầu vào và quyền thực thi trước khi gọi lại công cụ")


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
    last_step_file: str | None = None
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
            total_tokens += in_tok + out_tok

            if msg_type == "USER_INPUT" and source == "USER_EXPLICIT":
                total_turns += 1
                cleaned = clean_user_message(content)
                if cleaned:
                    user_messages.append(cleaned)
                is_pivot = bool(total_turns > 1 and PIVOT_KEYWORDS_RE.search(cleaned))
                prev_turn_file = last_step_file
                current_turn = {
                    "turn": total_turns,
                    "step_index": step_index,
                    "user_prompt": cleaned[:300],
                    "is_user_pivot": is_pivot,
                    "tools_called": [],
                    "skills_loaded": [],
                    "files_touched": [],
                    "commands_run": [],
                    "errors": [],
                }
                interaction_turns.append(current_turn)
                if is_pivot:
                    fp_id, fp_sum = fingerprint_error("user_correction", cleaned)
                    errors_encountered.append({
                        "step_index": step_index,
                        "category": "user_correction",
                        "source": "USER_EXPLICIT",
                        "content": f"User pivot/correction at turn {total_turns}: {cleaned[:200]}",
                        "related_file": prev_turn_file,
                        "related_skill": skills_observed[-1] if skills_observed else None,
                        "fingerprint": fp_id,
                        "fingerprint_summary": fp_sum,
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

                    # 1. Detect Observed Skill Loads & Touched Files
                    if tool_name in ("read_file", "edit_file", "write_file") and isinstance(args, dict):
                        raw_path = str(args.get("Path") or args.get("path") or "").strip().strip('"')
                        m_skill = SKILL_PATH_RE.search(raw_path)
                        if m_skill and tool_name == "read_file":
                            sk_name = m_skill.group(1).lower()
                            if sk_name not in skills_observed:
                                skills_observed.append(sk_name)
                            if current_turn is not None and sk_name not in current_turn["skills_loaded"]:
                                current_turn["skills_loaded"].append(sk_name)
                        else:
                            norm_file = normalize_project_file(raw_path)
                            if norm_file:
                                last_step_file = norm_file
                                if current_turn is not None and norm_file not in current_turn["files_touched"]:
                                    current_turn["files_touched"].append(norm_file)

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
                err_text = (raw_err or "Tool execution error")[:250]
                fp_id, fp_sum = fingerprint_error("tool_error", err_text)
                turn_skill = (
                    current_turn["skills_loaded"][-1]
                    if (current_turn and current_turn.get("skills_loaded"))
                    else (skills_observed[-1] if skills_observed else None)
                )
                err_item = {
                    "step_index": step_index,
                    "category": "tool_error",
                    "source": source,
                    "content": err_text,
                    "related_file": last_step_file,
                    "related_skill": turn_skill,
                    "fingerprint": fp_id,
                    "fingerprint_summary": fp_sum,
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
