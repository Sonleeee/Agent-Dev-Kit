#!/usr/bin/env python3
"""
ADK Deterministic UI Anti-Slop Auditor — Impeccable 20/20 Edition (stdlib-only)
Scans Frontend/UI files (.html, .htm, .css, .scss, .tsx, .jsx, .vue, .svelte) across 20 rules
grouped into 5 dimensions (AESTHETICS, MOTION, A11Y, MOBILE, DATA_DENSE), each worth 4.0 points
for a total score out of 20.0. Supports auto-remediation via `--fix`.
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

DIMENSIONS = ("AESTHETICS", "MOTION", "A11Y", "MOBILE", "DATA_DENSE")
SEVERITY_PENALTY = {"HIGH": 2.0, "MEDIUM": 1.0, "LOW": 0.5}

RULES: list[dict[str, Any]] = [
    # --- Dimension 1: AESTHETICS (4.0 pts) ---
    {
        "id": "BAN-01",
        "dimension": "AESTHETICS",
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
        "dimension": "AESTHETICS",
        "severity": "MEDIUM",
        "name": "Raw Emoji Inside Interactive Control or Heading",
        "pattern": re.compile(
            r"<(?:button|a|Badge|h[1-3])\b[^>]*>[^<]*[\U0001F300-\U0001FAFF\u2728\u26A1\U0001F525\U0001F680\u2705\U0001F4A1][^<]*</(?:button|a|Badge|h[1-3])>",
            re.IGNORECASE,
        ),
        "remediation": "Replace raw emoji icons inside buttons/links/badges/headings with 1.5px stroke SVG icons (Lucide, Heroicons, Radix).",
    },
    {
        "id": "BAN-04",
        "dimension": "AESTHETICS",
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
        "dimension": "AESTHETICS",
        "severity": "MEDIUM",
        "name": "Overused AI Display Typography",
        "pattern": re.compile(
            r"font-family\s*:\s*[^;\n]*\b(?:Space Grotesk|Syne|Outfit|Sora)\b|['\"](?:Space Grotesk|Syne|Outfit|Sora)['\"]",
            re.IGNORECASE,
        ),
        "remediation": "Prefer high-legibility UI fonts (`Inter`, `Geist`, `Plus Jakarta Sans`, or system-ui) with `tabular-nums` for data.",
    },
    {
        "id": "BAN-07",
        "dimension": "AESTHETICS",
        "severity": "LOW",
        "name": "Dark Mode Harsh Solid Border",
        "pattern": re.compile(
            r"\bdark:border-(?:gray|slate|zinc)-[678]00(?!/)\b",
            re.IGNORECASE,
        ),
        "remediation": "Use subtle semi-transparent borders in dark mode (`dark:border-white/10` or `dark:border-slate-700/50`) instead of harsh solid borders.",
    },
    {
        "id": "BAN-08",
        "dimension": "AESTHETICS",
        "severity": "HIGH",
        "name": "Lazy AI Placeholder Comment or Marketing Cliché",
        "pattern": re.compile(
            r"(?://\s*\.\.\.\s*rest of|/\*\s*\.\.\.\s*existing|\b(?:Unleash the power|Supercharge your workflow|Elevate your experience|Revolutionize the way)\b)",
            re.IGNORECASE,
        ),
        "remediation": "Write complete implementation code and specific, factual product microcopy instead of lazy AI placeholders or clichés.",
    },
    # --- Dimension 2: MOTION (4.0 pts) ---
    {
        "id": "BAN-06",
        "dimension": "MOTION",
        "severity": "LOW",
        "name": "Scale-From-Zero Animation (`scale-0` / `scale(0)`)",
        "pattern": re.compile(
            r"\bscale-0\b|transform\s*:\s*scale\(\s*0\s*\)",
            re.IGNORECASE,
        ),
        "remediation": "Start modals/popovers from `scale-95 opacity-0` (`scale(0.95)`) instead of `scale(0)` per Emil Kowalski motion principles.",
    },
    {
        "id": "MOT-01",
        "dimension": "MOTION",
        "severity": "MEDIUM",
        "name": "Wrong Easing Curve on Enter/Modal (`ease-in`)",
        "pattern": re.compile(
            r"(?:\b(?:animate-in|enter|modal|dialog|popover)\b[^\n\"'`]*\bease-in\b(?![-a-z])|\bease-in\b(?![-a-z])[^\n\"'`]*\b(?:animate-in|enter|modal|dialog|popover)\b)",
            re.IGNORECASE,
        ),
        "remediation": "Use `ease-out` (`cubic-bezier(0.16, 1, 0.3, 1)`) for entering elements/modals and reserve `ease-in` for exits.",
    },
    {
        "id": "MOT-02",
        "dimension": "MOTION",
        "severity": "MEDIUM",
        "name": "Layout-Thrashing Transition (`transition-all` / geometry)",
        "pattern": re.compile(
            r"\btransition-(?:all|width|height|top|left)\b|transition\s*:\s*(?:all|width|height|top|left)\b",
            re.IGNORECASE,
        ),
        "remediation": "Avoid `transition-all` or animating layout geometry; use `transition-colors`, `transition-transform`, or `transition-opacity`.",
    },
    {
        "id": "MOT-03",
        "dimension": "MOTION",
        "severity": "LOW",
        "name": "Sluggish Micro-Interaction Duration (`>=500ms`)",
        "pattern": re.compile(
            r"<(?:button|input|a|Badge)\b[^>]*\bduration-(?:500|700|1000)\b",
            re.IGNORECASE,
        ),
        "remediation": "Keep interactive control transitions crisp (`duration-150` or `duration-200`, 150ms-200ms budget).",
    },
    {
        "id": "MOT-04",
        "dimension": "MOTION",
        "severity": "MEDIUM",
        "name": "Infinite Animation Without Reduced-Motion Guard",
        "pattern": re.compile(
            r"\banimate-(?:spin|ping|bounce)\b|@keyframes\b",
            re.IGNORECASE,
        ),
        "file_guard_absent": re.compile(r"motion-reduce:|prefers-reduced-motion", re.IGNORECASE),
        "remediation": "Add `motion-reduce:animate-none` or `@media (prefers-reduced-motion: reduce)` when using continuous animations.",
    },
    # --- Dimension 3: A11Y (4.0 pts) ---
    {
        "id": "BAN-03",
        "dimension": "A11Y",
        "severity": "HIGH",
        "name": "Focus Outline Removed Without Replacement",
        "pattern": re.compile(
            r"(?:\boutline-none\b|outline\s*:\s*none\b)(?![^\n\"'`]*(?:focus-visible:|focus:ring|focus:outline|focus-within:ring))",
            re.IGNORECASE,
        ),
        "remediation": "Never strip focus outline without providing `focus-visible:ring-2 focus-visible:ring-offset-2` (WCAG 2.2 Focus Visible).",
    },
    {
        "id": "A11Y-01",
        "dimension": "A11Y",
        "severity": "HIGH",
        "name": "Non-Interactive Element With `onClick` Missing Semantics",
        "pattern": re.compile(
            r"<(?:div|span)\b(?![^>]*\b(?:role=|tabIndex=))[^>]*\bonClick=",
            re.IGNORECASE,
        ),
        "remediation": "Use a native `<button>` or add `role=\"button\" tabIndex={0}` and keyboard handler (`onKeyDown`) for clickable elements.",
    },
    {
        "id": "A11Y-02",
        "dimension": "A11Y",
        "severity": "HIGH",
        "name": "Icon-Only Button Missing Accessible Label",
        "pattern": re.compile(
            r"<button\b(?![^>]*\b(?:aria-label=|aria-labelledby=|title=))[^>]*>\s*<(?:svg|Icon|[A-Z][A-Za-z0-9]*Icon)\b[^>]*>(?:(?!</button>).)*</button>",
            re.IGNORECASE,
        ),
        "line_guard_absent": re.compile(r"\bsr-only\b", re.IGNORECASE),
        "remediation": "Add `aria-label=\"...\"` or a `<span className=\"sr-only\">` label inside icon-only buttons.",
    },
    {
        "id": "A11Y-03",
        "dimension": "A11Y",
        "severity": "HIGH",
        "name": "Image Element Missing `alt` Attribute",
        "pattern": re.compile(
            r"<img\b(?![^>]*\balt=)[^>]*>",
            re.IGNORECASE,
        ),
        "remediation": "Provide a descriptive `alt=\"...\"` attribute (or `alt=\"\"` for decorative images) on every `<img>` element.",
    },
    # --- Dimension 4: MOBILE (4.0 pts) ---
    {
        "id": "MOB-01",
        "dimension": "MOBILE",
        "severity": "MEDIUM",
        "name": "iOS Safari Auto-Zoom Input (`font-size < 16px`)",
        "pattern": re.compile(
            r"<(?:input|textarea|select)\b[^>]*\bclass(?:Name)?=['\"][^'\"]*\btext-(?:xs|sm)\b(?![^'\"]*\btext-base\b)",
            re.IGNORECASE,
        ),
        "remediation": "Use `text-base sm:text-sm` on `<input>`, `<textarea>`, and `<select>` so mobile font-size is >=16px, preventing iOS Safari auto-zoom.",
    },
    {
        "id": "MOB-02",
        "dimension": "MOBILE",
        "severity": "LOW",
        "name": "Legacy Static Viewport Height (`h-screen` / `100vh`)",
        "pattern": re.compile(
            r"\bh-screen\b|\bmin-h-screen\b|\b100vh\b",
            re.IGNORECASE,
        ),
        "remediation": "Use dynamic viewport units (`min-h-dvh`, `h-dvh`, `100dvh`) to prevent mobile browser address bars from clipping content.",
    },
    {
        "id": "MOB-03",
        "dimension": "MOBILE",
        "severity": "MEDIUM",
        "name": "Hardcoded Wide Pixel Width (`>=400px`) Breaking 320px Viewport",
        "pattern": re.compile(
            r"(?<![a-z0-9]:)\b(?:w|min-w)-\[[4-9]\d{2}px\]",
            re.IGNORECASE,
        ),
        "line_guard_absent": re.compile(r"\bmax-w-full\b|\bw-full\b", re.IGNORECASE),
        "remediation": "Use responsive width utilities (`w-full max-w-[500px]` or `sm:w-[500px]`) to guarantee zero horizontal overflow at 320px.",
    },
    # --- Dimension 5: DATA_DENSE (4.0 pts) ---
    {
        "id": "DAT-01",
        "dimension": "DATA_DENSE",
        "severity": "MEDIUM",
        "name": "Numeric/Currency Table Cell Missing `tabular-nums`",
        "pattern": re.compile(
            r"<td\b[^>]*>[^<]*(?:\$\s*\d|\d\s*(?:₫|VND|%))[^<]*</td>",
            re.IGNORECASE,
        ),
        "file_guard_absent": re.compile(r"\btabular-nums\b|\bfont-mono\b", re.IGNORECASE),
        "remediation": "Add `tabular-nums` or `font-mono` (and `text-right`) on numeric/currency table cells for vertical decimal alignment.",
    },
    {
        "id": "DAT-02",
        "dimension": "DATA_DENSE",
        "severity": "LOW",
        "name": "Data Table Missing Horizontal Scroll Wrapper (`overflow-x-auto`)",
        "pattern": re.compile(
            r"<table\b",
            re.IGNORECASE,
        ),
        "file_guard_absent": re.compile(r"\boverflow-x-auto\b|\boverflow-auto\b", re.IGNORECASE),
        "remediation": "Wrap `<table>` inside `<div className=\"overflow-x-auto\">` to prevent table overflow on narrow screens.",
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
            print("| Rule | Dim | Severity | Location | Issue & Remediation |")
            print("|---|---|---|---|---|")
            for item in all_findings:
                print(
                    f"| `{item['rule_id']}` | `{item['dimension']}` | {item['severity']} "
                    f"| `{item['location']}` | **{item['name']}** — {item['remediation']} |"
                )
        else:
            print("Impeccable 20/20! No AI UI Slop, Motion, A11Y, Mobile, or Data-Dense violations detected.")

    if args.strict and verdict == "FAIL":
        sys.exit(1)
    sys.exit(0)


if __name__ == "__main__":
    main()
