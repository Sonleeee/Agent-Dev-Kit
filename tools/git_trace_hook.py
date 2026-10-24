#!/usr/bin/env python3
"""
ADK Git Trace Hook
Automatically captures Git commits as evolutionary traces in SQLite (evolution.db).
Zero-dependency: standard library only (subprocess, json, sqlite3, pathlib, re).
Silent fail-safe: never interrupts developer flow or GUI tools like GitHub Desktop.
"""

from __future__ import annotations

import json
import os
from pathlib import Path
import re
import subprocess
import sys
from typing import Any

sys.dont_write_bytecode = True

# Ensure ADK root is in sys.path to import evolution_db if available
ADK_ROOT = Path(__file__).resolve().parent.parent
if str(ADK_ROOT) not in sys.path:
    sys.path.insert(0, str(ADK_ROOT))

try:
    from tools.evolution_db import get_connection, cmd_init, get_db_path
except ImportError:
    # Fallback if run in isolated environment
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

    cmd_init = None


def run_git(args: list[str], cwd: Path | None = None) -> str:
    """Run a git command and return standard output as string."""
    try:
        res = subprocess.run(
            ["git"] + args,
            cwd=str(cwd or Path.cwd()),
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            check=True,
        )
        return res.stdout.strip()
    except Exception:
        return ""


def get_commit_metadata(repo_dir: Path | None = None) -> dict[str, Any] | None:
    """Extract metadata of HEAD commit using pure git plumbing commands."""
    raw = run_git(["log", "-1", "--pretty=format:%H%x00%s%x00%an%x00%aI%x00%b"], repo_dir)
    if not raw or "\x00" not in raw:
        return None

    parts = raw.split("\x00")
    commit_hash = parts[0].strip()
    subject = parts[1].strip() if len(parts) > 1 else ""
    author = parts[2].strip() if len(parts) > 2 else ""
    date_iso = parts[3].strip() if len(parts) > 3 else ""
    body = parts[4].strip() if len(parts) > 4 else ""

    # Get changed files
    diff_tree = run_git(["diff-tree", "--no-commit-id", "--name-status", "-r", "HEAD"], repo_dir)
    changed_files: list[dict[str, str]] = []
    if diff_tree:
        for line in diff_tree.splitlines():
            line = line.strip()
            if not line:
                continue
            cols = line.split(None, 1)
            if len(cols) == 2:
                changed_files.append({"status": cols[0], "path": cols[1]})

    # Get diff stat
    # Try against HEAD~1; if single commit repo, compare with empty tree
    stat_raw = run_git(["diff", "HEAD~1", "HEAD", "--shortstat"], repo_dir)
    if not stat_raw:
        stat_raw = run_git(["diff", "4b825dc642cb6eb9a060e54bf8d69288fbee4904", "HEAD", "--shortstat"], repo_dir)

    insertions = 0
    deletions = 0
    m_ins = re.search(r"(\d+)\s+insertion", stat_raw)
    if m_ins:
        insertions = int(m_ins.group(1))
    m_del = re.search(r"(\d+)\s+deletion", stat_raw)
    if m_del:
        deletions = int(m_del.group(1))

    return {
        "hash": commit_hash,
        "subject": subject,
        "author": author,
        "date": date_iso,
        "body": body,
        "changed_files": changed_files,
        "insertions": insertions,
        "deletions": deletions,
        "stat_raw": stat_raw,
    }


def record_commit_trace(repo_dir: Path | None = None) -> dict[str, Any]:
    """Capture current HEAD commit into SQLite evolution database."""
    meta = get_commit_metadata(repo_dir)
    if not meta or not meta["hash"]:
        return {"status": "skipped", "reason": "No commit metadata found"}

    commit_hash = meta["hash"]
    subject = meta["subject"] or f"Commit {commit_hash[:8]}"
    files_count = len(meta["changed_files"])
    # A commit only proves that Git recorded a commit. Its prefix and changed
    # paths do not prove which workflow/skill ran, whether the task is complete,
    # or whether the author experienced friction.
    workflow = None
    complexity = None
    skills: list[str] = []
    friction = None

    trace_id = f"trace_git_{commit_hash[:8]}"
    session_id = f"sess_git_{commit_hash[:8]}"

    # Project name from repo folder
    project_name = repo_dir.name if repo_dir else Path.cwd().name

    # Evidence summary
    evidence = {
        "commit": commit_hash,
        "commit_subject": subject,
        "author": meta["author"],
        "date": meta["date"],
        "files_changed_count": files_count,
        "stat": meta["stat_raw"],
        "files": [f["path"] for f in meta["changed_files"][:30]],
        "capture_type": "git_commit_metadata",
        "task_outcome_observed": False,
        "workflow_observed": False,
        "skill_usage_observed": False,
        "friction_observed": False,
    }

    # Ensure database exists
    db_path = get_db_path()
    if not db_path.exists() and cmd_init:
        cmd_init({})

    with get_connection() as conn:
        # 1. Insert session
        conn.execute(
            """
            INSERT INTO sessions (id, project, user_intent, workflow_used, outcome, total_turns, summary)
            VALUES (?, ?, ?, ?, 'PARTIAL', 0, ?)
            ON CONFLICT(id) DO UPDATE SET
                summary = excluded.summary,
                outcome = 'PARTIAL';
            """,
            (session_id, project_name, None, workflow, f"Commit metadata only; task outcome unknown. {meta['stat_raw']}"),
        )

        # 2. Insert trace
        conn.execute(
            """
            INSERT INTO traces (id, session_id, task_description, workflow, complexity, outcome, duration_turns, tokens_used, acceptance_evidence)
            VALUES (?, ?, ?, ?, ?, 'PARTIAL', 0, 0, ?)
            ON CONFLICT(id) DO NOTHING;
            """,
            (trace_id, session_id, f"Git commit metadata capture ({commit_hash[:8]})", workflow, complexity, json.dumps(evidence)),
        )

        # 3. Associate skills used
        for sk in skills:
            conn.execute(
                """
                INSERT INTO skills (name, skill_group, current_version, times_used, times_succeeded)
                VALUES (?, 'core', '1.0', 1, 1)
                ON CONFLICT(name) DO UPDATE SET
                    times_used = times_used + 1,
                    times_succeeded = times_succeeded + 1,
                    last_used_at = strftime('%Y-%m-%dT%H:%M:%SZ', 'now');
                """,
                (sk,),
            )
            conn.execute(
                """
                INSERT INTO skills_used (trace_id, skill_name, outcome)
                VALUES (?, ?, 'success');
                """,
                (trace_id, sk),
            )

        # 4. Insert friction if detected
        if friction:
            conn.execute(
                """
                INSERT INTO friction_points (trace_id, category, description, severity, suggested_fix)
                VALUES (?, ?, ?, ?, ?);
                """,
                (trace_id, friction["category"], friction["description"], friction["severity"], friction["suggested_fix"]),
            )

    return {
        "status": "ok",
        "trace_id": trace_id,
        "workflow": workflow,
        "complexity": complexity,
        "skills": skills,
        "has_friction": friction is not None,
    }


def install_hook(repo_dir: Path | None = None) -> bool:
    """Install post-commit hook into current git repository."""
    target_dir = repo_dir or Path.cwd()
    git_dir = target_dir / ".git"
    if not git_dir.exists() or not git_dir.is_dir():
        print(f"[!] Error: {target_dir} is not a git repository.")
        return False

    hooks_dir = git_dir / "hooks"
    hooks_dir.mkdir(parents=True, exist_ok=True)
    hook_file = hooks_dir / "post-commit"

    # Relative path using forward slashes for Git Bash compatibility
    script_rel = "tools/git_trace_hook.py"

    hook_content = (
        "#!/bin/sh\n"
        "# ADK Post-Commit Trace Hook (Asynchronous & Non-blocking)\n"
        "# Automatically records git commits into evolution.db in background\n"
        "# Silent fail-safe: never interrupts git commit or GUI tools\n"
        "if command -v cmd.exe >/dev/null 2>&1; then\n"
        f"    cmd.exe /c start /b \"\" py -3 {script_rel} >/dev/null 2>&1 || true\n"
        "else\n"
        f"    (nohup python3 {script_rel} </dev/null >/dev/null 2>&1 &) || true\n"
        "fi\n"
        "exit 0\n"
    )

    hook_file.write_text(hook_content, encoding="utf-8")
    try:
        # On POSIX / WSL, ensure executable permission
        hook_file.chmod(0o755)
    except Exception:
        pass

    print(f"[+] Post-commit hook installed successfully at: {hook_file}")
    return True


def main() -> None:
    """Main CLI entrypoint with fail-safe error suppression."""
    try:
        if "--install" in sys.argv:
            install_hook()
            return

        if "--test" in sys.argv:
            res = record_commit_trace()
            print(json.dumps(res, indent=2))
            return

        # Default execution from git post-commit hook
        record_commit_trace()
    except Exception:
        # Silent fail-safe: never bubble errors up to Git or GitHub Desktop
        sys.exit(0)


if __name__ == "__main__":
    main()
