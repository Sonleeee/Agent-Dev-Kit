#!/usr/bin/env python3
"""
ADK Deterministic UI Anti-Slop Auditor — Impeccable 20/20 Edition (stdlib-only)
Engine: Scans Frontend/UI files, evaluates rules, calculates scores and applies auto-fixes.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import re
import sys
from typing import Any

# Ensure local directory is importable
SCRIPT_DIR = Path(__file__).resolve().parent
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

from rules_data import (
    DIMENSIONS,
    IGNORE_DIRS,
    RULES,
    SEVERITY_BADGE,
    SEVERITY_PENALTY,
    UI_EXTENSIONS,
)

sys.dont_write_bytecode = True

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")
if hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(encoding="utf-8")


def iter_ui_files(targets: list[Path]) -> list[Path]:
    files: list[Path] = []
    for target in targets:
        if not target.exists():
            continue
        if target.is_file():
            if target.suffix.lower() in UI_EXTENSIONS:
                files.append(target)
            continue
        for p in target.rglob("*"):
            if any(part in IGNORE_DIRS for part in p.parts):
                continue
            if p.is_file() and p.suffix.lower() in UI_EXTENSIONS:
                files.append(p)
    return sorted(set(files))


def apply_auto_fixes(file_path: Path) -> int:
    try:
        original = file_path.read_text(encoding="utf-8", errors="replace")
    except Exception:
        return 0

    updated = original
    fixes = 0

    # Fix 1: scale-0 -> scale-95
    updated, n = re.subn(r"\bscale-0\b", "scale-95", updated)
    fixes += n
    updated, n = re.subn(r"transform\s*:\s*scale\(\s*0\s*\)", "transform: scale(0.95)", updated)
    fixes += n

    # Fix 2: h-screen / min-h-screen / 100vh -> min-h-dvh / 100dvh
    updated, n = re.subn(r"\bmin-h-screen\b|\bh-screen\b", "min-h-dvh", updated)
    fixes += n
    updated, n = re.subn(r"\b100vh\b", "100dvh", updated)
    fixes += n

    # Fix 3: outline-none without focus ring -> outline-none focus-visible:ring-2
    lines = updated.splitlines(keepends=True)
    for idx, line in enumerate(lines):
        if re.search(
            r"\boutline-none\b(?![^\n\"'`]*(?:focus-visible:|focus:ring|focus:outline|focus-within:ring))",
            line,
        ):
            lines[idx] = re.sub(r"\boutline-none\b", "outline-none focus-visible:ring-2", line, count=1)
            fixes += 1
    updated = "".join(lines)

    if fixes > 0 and updated != original:
        file_path.write_text(updated, encoding="utf-8")
    return fixes


def scan_file(file_path: Path, base_dir: Path) -> list[dict[str, Any]]:
    findings: list[dict[str, Any]] = []
    try:
        text = file_path.read_text(encoding="utf-8", errors="replace")
    except Exception:
        return findings

    try:
        rel_path = file_path.resolve().relative_to(base_dir.resolve()).as_posix()
    except ValueError:
        rel_path = file_path.as_posix()

    seen_file_level_rules: set[str] = set()

    for line_no, line in enumerate(text.splitlines(), start=1):
        for rule in RULES:
            if rule.get("multiline"):
                continue
            if not rule["pattern"].search(line):
                continue
            line_guard = rule.get("line_guard_absent")
            if line_guard is not None and line_guard.search(line):
                continue
            file_guard = rule.get("file_guard_absent")
            if file_guard is not None:
                if file_guard.search(text):
                    continue
                if rule["id"] in seen_file_level_rules:
                    continue
                seen_file_level_rules.add(rule["id"])

            findings.append({
                "rule_id": rule["id"],
                "dimension": rule["dimension"],
                "severity": rule["severity"],
                "name": rule["name"],
                "location": f"{rel_path}:{line_no}",
                "snippet": line.strip()[:140],
                "remediation": rule["remediation"],
            })

    for rule in RULES:
        if not rule.get("multiline"):
            continue
        for m in rule["pattern"].finditer(text):
            line_no = text[:m.start()].count("\n") + 1
            snippet = m.group(0).replace("\n", " ").strip()[:140]
            findings.append({
                "rule_id": rule["id"],
                "dimension": rule["dimension"],
                "severity": rule["severity"],
                "name": rule["name"],
                "location": f"{rel_path}:{line_no}",
                "snippet": snippet,
                "remediation": rule["remediation"],
            })
    return findings


def compute_scores(findings: list[dict[str, Any]]) -> tuple[dict[str, float], float, str]:
    dim_scores: dict[str, float] = {d: 4.0 for d in DIMENSIONS}
    for f in findings:
        dim = f.get("dimension", "AESTHETICS")
        penalty = SEVERITY_PENALTY.get(f.get("severity", "LOW"), 0.5)
        if dim in dim_scores:
            dim_scores[dim] = max(0.0, round(dim_scores[dim] - penalty, 2))

    total_score = round(sum(dim_scores.values()), 2)
    if total_score >= 18.0:
        band = "STUDIO_GRADE"
    elif total_score >= 14.0:
        band = "ACCEPTABLE"
    elif total_score >= 10.0:
        band = "NEEDS_POLISH"
    else:
        band = "AI_SLOP"
    return dim_scores, total_score, band


def main() -> None:
    parser = argparse.ArgumentParser(description="ADK Deterministic UI Anti-Slop & Impeccable 20/20 Auditor")
    parser.add_argument("paths", nargs="*", default=["."], help="Files or directories to scan")
    parser.add_argument("--json", action="store_true", help="Output structured JSON report")
    parser.add_argument("--strict", action="store_true", help="Exit with code 1 if HIGH/MEDIUM findings exist")
    parser.add_argument("--fix", action="store_true", help="Auto-fix safe deterministic UI slop patterns before scanning")
    args = parser.parse_args()

    base_dir = Path.cwd()
    target_paths = [Path(p) for p in args.paths]
    ui_files = iter_ui_files(target_paths)

    fixed_count = 0
    if args.fix:
        for f in ui_files:
            fixed_count += apply_auto_fixes(f)

    all_findings: list[dict[str, Any]] = []
    for f in ui_files:
        all_findings.extend(scan_file(f, base_dir))

    dim_scores, total_score, quality_band = compute_scores(all_findings)
    high_med = [x for x in all_findings if x["severity"] in ("HIGH", "MEDIUM")]
    verdict = "PASS" if not high_med else "FAIL"

    report = {
        "scanner": "ui_slop_auditor",
        "version": "2.0.0",
        "files_scanned": len(ui_files),
        "auto_fixes_applied": fixed_count,
        "total_findings": len(all_findings),
        "high_or_medium_count": len(high_med),
        "score": total_score,
        "max_score": 20.0,
        "quality_band": quality_band,
        "dimension_scores": dim_scores,
        "verdict": verdict,
        "findings": all_findings,
    }

    if args.json:
        print(json.dumps(report, indent=2, ensure_ascii=False))
    else:
        dims_str = " | ".join(f"{k}: {v:.1f}/4.0" for k, v in dim_scores.items())
        print(
            f"=== [UI ANTI-SLOP AUDITOR] verdict: {verdict} | Score: {total_score:.1f}/20.0 ({quality_band}) "
            f"| Scanned: {len(ui_files)} UI files, Findings: {len(all_findings)}, Auto-Fixed: {fixed_count} ==="
        )
        print(f"Dimensions: [ {dims_str} ]")
        if all_findings:
            print("| Priority | Rule | Dim | Location | Issue & Remediation |")
            print("|---|---|---|---|---|")
            for item in all_findings:
                badge = SEVERITY_BADGE.get(item["severity"], item["severity"])
                print(
                    f"| {badge} | `{item['rule_id']}` | `{item['dimension']}` "
                    f"| `{item['location']}` | **{item['name']}** — {item['remediation']} |"
                )
        else:
            print("Impeccable 20/20! No AI UI Slop, Motion, A11Y, Mobile, or Data-Dense violations detected.")

    if args.strict and verdict == "FAIL":
        sys.exit(1)
    sys.exit(0)


if __name__ == "__main__":
    main()
