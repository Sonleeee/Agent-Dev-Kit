"""
ADK Session Curator - Reporting & Artifact Generator
Generates Typed Handoff Packets and Session Journals in .agents/runtime/.
"""

from __future__ import annotations

from datetime import datetime, timezone
from pathlib import Path
import re
import sys
from typing import Any

sys.dont_write_bytecode = True


def analyze_dev_style(user_messages: list[str]) -> list[dict[str, Any]]:
    """Extract high-confidence communication density signals without hardcoded keyword pollution."""
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
    adk_root: Path,
) -> dict[str, str]:
    """Write human-readable interaction journal and Typed Handoff Packet to .agents/runtime/."""
    now_iso = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    runtime_dir = adk_root / ".agents" / "runtime"
    runtime_dir.mkdir(parents=True, exist_ok=True)

    handoff_path = runtime_dir / "latest-handoff.md"
    journal_path = runtime_dir / "session-journal.md"

    conv_id = data["conversation_id"]
    turns = data.get("interaction_turns", [])
    skills_obs = ", ".join(f"`{s}`" for s in data.get("skills_observed", [])) or "_(none)_"
    tools_obs = ", ".join(f"`{t}`" for t in data.get("tools_used", [])) or "_(none)_"

    # 1. Build Typed Handoff Packet
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
            fp_tag = e.get("fingerprint") or e.get("category", "error")
            file_tag = f" on `{e['related_file']}`" if e.get("related_file") else ""
            handoff_lines.append(f"- **[{fp_tag}]**{file_tag} (Step {e.get('step_index')}): {clean_err}")
    else:
        handoff_lines.append("- _(Zero tool errors or user pivot corrections in this session)_")

    guardrails = data.get("file_guardrails", [])
    if guardrails:
        handoff_lines.extend([
            "",
            "## 5. Empirical File Guardrails (from Entity Graph)",
        ])
        for fg in guardrails:
            sk_note = f" | Skills: `{fg['impl_skills']}`" if fg.get("impl_skills") else ""
            handoff_lines.append(
                f"- **`{fg['file_path']}`** (`{fg['friction_type']}` x{fg['hit_count']}): {fg['how_to_operate']}{sk_note}"
            )

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
