#!/usr/bin/env python3
"""
ADK Deterministic UI Anti-Slop Auditor (stdlib-only)
Scans Frontend/UI files (.html, .css, .scss, .tsx, .jsx, .vue, .svelte) for AI UI Slop patterns
and WCAG 2.2 accessibility violations defined in `adk-ui-craft` and `rules/global.md`.

Checks:
  - BAN-01: Default AI Purple/Blue Neon Gradients (e.g. `from-purple-* to-blue-*`, `from-indigo-* via-purple-*`)
  - BAN-02: Raw Emojis inside interactive UI controls (<button>, <a>, <Badge>)
  - BAN-03: Focus Ring Removal without replacement (`outline-none` / `outline: none` without `focus-visible:` or `focus:ring`)
  - BAN-04: Elongated Pill CTA buttons (`rounded-full` combined with excessive horizontal padding `px-10`/`px-12`/`px-16`)
  - BAN-05: Overused AI Slop Display Fonts (`Space Grotesk`, `Syne`, `Outfit`) in enterprise UI
  - BAN-06: Scale-from-zero modal/popover animation (`scale-0` / `scale(0)`) instead of `scale-95`
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import re
import sys
from typing import Any

sys.dont_write_bytecode = True

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")
if hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(encoding="utf-8")

UI_EXTENSIONS = {".html", ".htm", ".css", ".scss", ".tsx", ".jsx", ".vue", ".svelte"}
IGNORE_DIRS = {".git", "node_modules", "dist", "build", ".next", ".nuxt", "coverage", "__pycache__", ".agents"}

RULES: list[dict[str, Any]] = [
    {
        "id": "BAN-01",
        "severity": "HIGH",
        "name": "AI Purple-Blue Neon Gradient",
        "pattern": re.compile(
            r"\bfrom-(?:purple|indigo|violet)-[4567]00\b[^\n\"'`]*\bto-(?:blue|pink|cyan|indigo|purple)-[4567]00\b",
            re.IGNORECASE,
        ),
        "remediation": "Use semantic brand/surface tokens from DESIGN.md instead of generic purple-to-blue AI gradients.",
    },
    {
        "id": "BAN-02",
        "severity": "MEDIUM",
        "name": "Raw Emoji Inside Interactive Control",
        "pattern": re.compile(
            r"<(?:button|a|Badge)\b[^>]*>[^<]*[\U0001F300-\U0001FAFF\u2728\u26A1\U0001F525\U0001F680][^<]*</(?:button|a|Badge)>",
            re.IGNORECASE,
        ),
        "remediation": "Replace raw emoji icons inside buttons/links/badges with 1.5px stroke SVG icons (Lucide, Heroicons, Radix).",
    },
    {
        "id": "BAN-03",
        "severity": "HIGH",
        "name": "Focus Outline Removed Without Replacement",
        "pattern": re.compile(
            r"(?:\boutline-none\b|outline\s*:\s*none\b)(?![^\n\"'`]*(?:focus-visible:|focus:ring|focus:outline|focus-within:ring))",
            re.IGNORECASE,
        ),
        "remediation": "Never strip focus outline without providing `focus-visible:ring-2 focus-visible:ring-offset-2` (WCAG 2.2 Focus Visible).",
    },
    {
        "id": "BAN-04",
        "severity": "LOW",
        "name": "Elongated Pill CTA Button",
        "pattern": re.compile(
            r"\brounded-full\b[^\n\"'`]*\bpx-(?:10|11|12|14|16|20)\b|\bpx-(?:10|11|12|14|16|20)\b[^\n\"'`]*\brounded-full\b",
            re.IGNORECASE,
        ),
        "remediation": "Use balanced button geometry (`rounded-md` or `rounded-lg` with `px-4 py-2`) instead of elongated pill CTAs.",
    },
    {
        "id": "BAN-05",
        "severity": "MEDIUM",
        "name": "Overused AI Display Typography",
        "pattern": re.compile(
            r"font-family\s*:\s*[^;\n]*\b(?:Space Grotesk|Syne|Outfit)\b|['\"](?:Space Grotesk|Syne|Outfit)['\"]",
            re.IGNORECASE,
        ),
        "remediation": "Prefer high-legibility UI fonts (`Inter`, `Geist`, `Plus Jakarta Sans`, or system-ui) with `tabular-nums` for data.",
    },
    {
        "id": "BAN-06",
        "severity": "LOW",
        "name": "Scale-From-Zero Animation (`scale-0` / `scale(0)`)",
        "pattern": re.compile(
            r"\bscale-0\b|transform\s*:\s*scale\(\s*0\s*\)",
            re.IGNORECASE,
        ),
        "remediation": "Start modals/popovers from `scale-95 opacity-0` (`scale(0.95)`) instead of `scale(0)` per Emil Kowalski motion principles.",
    },
]


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

    for line_no, line in enumerate(text.splitlines(), start=1):
        for rule in RULES:
            if rule["pattern"].search(line):
                findings.append({
                    "rule_id": rule["id"],
                    "severity": rule["severity"],
                    "name": rule["name"],
                    "location": f"{rel_path}:{line_no}",
                    "snippet": line.strip()[:140],
                    "remediation": rule["remediation"],
                })
    return findings


def main() -> None:
    parser = argparse.ArgumentParser(description="ADK Deterministic UI Anti-Slop & Accessibility Auditor")
    parser.add_argument("paths", nargs="*", default=["."], help="Files or directories to scan")
    parser.add_argument("--json", action="store_true", help="Output structured JSON report")
    parser.add_argument("--strict", action="store_true", help="Exit with code 1 if HIGH/MEDIUM findings exist")
    args = parser.parse_args()

    base_dir = Path.cwd()
    target_paths = [Path(p) for p in args.paths]
    ui_files = iter_ui_files(target_paths)

    all_findings: list[dict[str, Any]] = []
    for f in ui_files:
        all_findings.extend(scan_file(f, base_dir))

    high_med = [x for x in all_findings if x["severity"] in ("HIGH", "MEDIUM")]
    verdict = "PASS" if not high_med else "FAIL"

    report = {
        "scanner": "ui_slop_auditor",
        "files_scanned": len(ui_files),
        "total_findings": len(all_findings),
        "high_or_medium_count": len(high_med),
        "verdict": verdict,
        "findings": all_findings,
    }

    if args.json:
        print(json.dumps(report, indent=2, ensure_ascii=False))
    else:
        print(f"=== [UI ANTI-SLOP AUDITOR] verdict: {verdict} (Scanned: {len(ui_files)} UI files, Findings: {len(all_findings)}) ===")
        if all_findings:
            print("| Rule | Severity | Location | Issue & Remediation |")
            print("|---|---|---|---|")
            for item in all_findings:
                print(f"| `{item['rule_id']}` | {item['severity']} | `{item['location']}` | **{item['name']}** — {item['remediation']} |")
        else:
            print("No AI UI Slop or Focus-Visible violations detected.")

    if args.strict and verdict == "FAIL":
        sys.exit(1)
    sys.exit(0)


if __name__ == "__main__":
    main()
