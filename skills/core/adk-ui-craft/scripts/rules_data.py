"""
ADK Deterministic UI Anti-Slop Rules Data Definition (Impeccable 20/20 Edition)
Contains 20 rules grouped into 5 dimensions (AESTHETICS, MOTION, A11Y, MOBILE, DATA_DENSE).
"""

from __future__ import annotations

import re
from typing import Any

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
