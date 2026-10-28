#!/usr/bin/env python3
"""
ADK Evolution Database CLI Tool & Facade
Manage evolutionary traces, steps, friction points, skills, entity graph, and metrics.
"""

from __future__ import annotations

import ast
import json
from pathlib import Path
import sys
from typing import Any

sys.dont_write_bytecode = True

# Ensure ADK root is in sys.path
ADK_ROOT = Path(__file__).resolve().parent.parent
if str(ADK_ROOT) not in sys.path:
    sys.path.insert(0, str(ADK_ROOT))

from tools.evolution import (
    ensure_trace_exists as _ensure_trace_exists,
    get_connection,
    get_db_path,
    get_schema_path,
    hash_content,
    cmd_init,
    cmd_inspect,
    cmd_log_session,
    cmd_log_step,
    cmd_log_friction,
    cmd_update_outcome,
    cmd_log_skill_use,
    cmd_query,
    cmd_search,
    cmd_health,
    cmd_log_preference,
    cmd_get_preferences,
    cmd_sync_profile,
)

COMMANDS = {
    "init": cmd_init,
    "inspect": cmd_inspect,
    "log_session": cmd_log_session,
    "log_step": cmd_log_step,
    "log_friction": cmd_log_friction,
    "update_outcome": cmd_update_outcome,
    "log_skill_use": cmd_log_skill_use,
    "query": cmd_query,
    "search": cmd_search,
    "health": cmd_health,
    "log_preference": cmd_log_preference,
    "get_preferences": cmd_get_preferences,
    "sync_profile": cmd_sync_profile,
}


def print_help() -> None:
    help_doc = {
        "name": "evolution_db.py",
        "description": "ADK Evolution Database CLI Tool & Zero-RAG Entity Graph Manager",
        "usage": "python evolution_db.py <subcommand> [json_or_str_args]",
        "commands": {
            "init": "Apply SQL schema and initialize database",
            "inspect": "Traverse Zero-RAG Entity Graph via Recursive CTE (e.g., inspect 'parser.py' or inspect)",
            "log_session": "Upsert session metadata (id, project, user_intent, workflow_used, outcome)",
            "log_step": "Append step to trace (trace_id, step_type, description, tool_used, tokens, outcome)",
            "log_friction": "Record friction point (trace_id, category, description, severity, related_skill, related_file)",
            "update_outcome": "Update trace outcome and update skill success/fail statistics",
            "log_skill_use": "Record skill execution into skills_used table",
            "query": "Execute arbitrary SQL query and return results as JSON",
            "search": "Perform FTS5 full-text search on traces or friction points",
            "health": "Display skill health matrix from v_skill_health view",
            "log_preference": "Store high-signal developer preference (preference_key, preference_value)",
            "get_preferences": "Query learned developer preferences",
            "sync_profile": "Sync high-confidence preferences into ~/.agents/developer.md",
        },
        "env": {"ADK_EVOLUTION_DB": "Override database path (default: ~/.adk/evolution.db)"},
    }
    print(json.dumps(help_doc, indent=2, ensure_ascii=False))


def parse_args_payload(raw_arg: str | None) -> Any:
    if raw_arg is None or raw_arg.strip() == "":
        return None
    raw = raw_arg.strip()
    try:
        return json.loads(raw)
    except Exception:
        pass
    try:
        val = ast.literal_eval(raw)
        if isinstance(val, (dict, list)):
            return val
    except Exception:
        pass
    return raw


def main() -> None:
    if len(sys.argv) < 2 or sys.argv[1] in ("-h", "--help", "help"):
        print_help()
        sys.exit(0)

    cmd_name = sys.argv[1].lower()
    if cmd_name not in COMMANDS:
        print(json.dumps({"status": "error", "message": f"Unknown command '{cmd_name}'. Run with --help for usage."}, ensure_ascii=False))
        sys.exit(1)

    raw_args = sys.argv[2] if len(sys.argv) > 2 else None
    parsed_payload = parse_args_payload(raw_args)

    try:
        handler = COMMANDS[cmd_name]
        result = handler(parsed_payload) if parsed_payload is not None else handler()
        print(json.dumps(result, indent=2, ensure_ascii=False))
        sys.exit(0 if result.get("status") == "ok" else 1)
    except Exception as e:
        print(json.dumps({"status": "error", "error_type": type(e).__name__, "message": str(e)}, indent=2, ensure_ascii=False))
        sys.exit(1)


if __name__ == "__main__":
    main()
