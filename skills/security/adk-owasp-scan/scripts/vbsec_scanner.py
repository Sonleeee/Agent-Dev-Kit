#!/usr/bin/env python3
"""
ADK Deterministic AI-Code Vulnerability Scanner (vbsec_scanner.py - stdlib-only)
Scans source code for high-frequency AI-generated security vulnerabilities based on
OWASP Top 10 & tanviet12/vbsec 21 AI vulnerability patterns.

Detects:
  - VBSEC-01 (HARDCODED-SECRET): Hardcoded API keys, JWT secrets, private keys, or passwords
  - VBSEC-02 (SQL-INJECTION): Raw string interpolation / concatenation inside SQL queries
  - VBSEC-03 (COMMAND-INJECTION): `shell=True`, `os.system()`, `child_process.exec()` with dynamic input
  - VBSEC-04 (XSS-BYPASS): `dangerouslySetInnerHTML`, `v-html`, `innerHTML =`, `bypassSecurityTrustHtml`
  - VBSEC-05 (JWT-UNVERIFIED): `jwt.decode(..., verify=False)` or `algorithms=["none"]`
  - VBSEC-06 (WEAK-HASHING): MD5 or SHA1 used in password/auth context
  - VBSEC-07 (INSECURE-DESERIALIZATION): `pickle.loads`, `yaml.load` (without SafeLoader), `eval()`
  - VBSEC-08 (CORS-WILDCARD): `Access-Control-Allow-Origin: *` or `origin: '*'`
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

CODE_EXTENSIONS = {".py", ".js", ".ts", ".tsx", ".jsx", ".cs", ".go", ".java", ".php", ".rb"}
IGNORE_DIRS = {".git", "node_modules", "dist", "build", ".next", "venv", ".venv", "__pycache__", ".agents", ".codegraph"}

RULES: list[dict[str, Any]] = [
    {
        "id": "VBSEC-01",
        "category": "HARDCODED-SECRET",
        "severity": "CRITICAL",
        "pattern": re.compile(
            r"(?:api[_-]?key|jwt[_-]?secret|secret[_-]?key|private[_-]?key|access[_-]?token|password)\s*[:=]\s*['\"][A-Za-z0-9_\-\.]{16,}['\"]"
            r"|-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----"
            r"|\b(?:sk-[A-Za-z0-9]{20,}|ghp_[A-Za-z0-9]{30,}|AIza[0-9A-Za-z\-_]{35})\b",
            re.IGNORECASE,
        ),
        "remediation": "Move secrets to environment variables (`os.environ` / `process.env`) or secret manager.",
    },
    {
        "id": "VBSEC-02",
        "category": "SQL-INJECTION",
        "severity": "CRITICAL",
        "pattern": re.compile(
            r"(?:execute|query|\$queryRawUnsafe)\s*\(\s*(?:f['\"]|['\"][^'\"]*\b(?:SELECT|INSERT|UPDATE|DELETE)\b[^'\"]*['\"]\s*(?:\+|%|\.format\()|`[^`]*\b(?:SELECT|INSERT|UPDATE|DELETE)\b[^`]*\$\{)",
            re.IGNORECASE,
        ),
        "remediation": "Use parameterized queries (`?`, `$1`, `@param`) instead of string interpolation or `$queryRawUnsafe`.",
    },
    {
        "id": "VBSEC-03",
        "category": "COMMAND-INJECTION",
        "severity": "HIGH",
        "pattern": re.compile(
            r"\bsubprocess\.(?:run|Popen|call|check_output)\s*\([^\n)]*\bshell\s*=\s*True\b"
            r"|\bos\.system\s*\(\s*(?:f['\"]|[a-zA-Z0-9_]+\s*\+)"
            r"|\bchild_process\.exec\s*\(\s*`[^`]*\$\{",
            re.IGNORECASE,
        ),
        "remediation": "Avoid `shell=True` and interpolated shell strings; pass command arguments as an explicit list (`['cmd', arg1]`).",
    },
    {
        "id": "VBSEC-04",
        "category": "XSS-BYPASS",
        "severity": "HIGH",
        "pattern": re.compile(
            r"\bdangerouslySetInnerHTML\b|\bv-html\s*=|\bbypassSecurityTrustHtml\b|\.innerHTML\s*=\s*(?!['\"]\s*['\"])",
            re.IGNORECASE,
        ),
        "remediation": "Sanitize untrusted HTML with DOMPurify or use safe text rendering (`textContent`).",
    },
    {
        "id": "VBSEC-05",
        "category": "JWT-NONE-ALGORITHM",
        "severity": "CRITICAL",
        "pattern": re.compile(
            r"\bjwt\.decode\s*\([^\n)]*(?:verify\s*=\s*False|verify_signature['\"]?\s*:\s*False)"
            r"|\balgorithms\s*[:=]\s*\[[^\]]*['\"]none['\"]",
            re.IGNORECASE,
        ),
        "remediation": "Always verify JWT signatures (`jwt.verify` / `verify_signature=True`) and enforce explicit algorithms (`['HS256']` / `['RS256']`).",
    },
    {
        "id": "VBSEC-06",
        "category": "WEAK-PASSWORD-HASHING",
        "severity": "HIGH",
        "pattern": re.compile(
            r"\bhashlib\.(?:md5|sha1)\s*\(|\bcrypto\.createHash\s*\(\s*['\"](?:md5|sha1)['\"]\s*\)",
            re.IGNORECASE,
        ),
        "remediation": "Use Argon2, bcrypt, or scrypt for password/credential hashing; never use MD5 or SHA-1.",
    },
    {
        "id": "VBSEC-07",
        "category": "INSECURE-DESERIALIZATION",
        "severity": "HIGH",
        "pattern": re.compile(
            r"\bpickle\.loads?\s*\(|\byaml\.load\s*\([^)\n]*(?!Loader\s*=\s*(?:yaml\.)?SafeLoader)\b",
            re.IGNORECASE,
        ),
        "remediation": "Use `yaml.safe_load()` or JSON with schema validation instead of `pickle.loads` / unsafe `yaml.load`.",
    },
    {
        "id": "VBSEC-08",
        "category": "CORS-MISCONFIG",
        "severity": "MEDIUM",
        "pattern": re.compile(
            r"Access-Control-Allow-Origin['\"]?\s*[:=]\s*['\"]\*['\"]|\borigin\s*:\s*['\"]\*['\"]|\ballow_origins\s*=\s*\[\s*['\"]\*['\"]\s*\]",
            re.IGNORECASE,
        ),
        "remediation": "Restrict CORS origins to an explicit allowlist of trusted domains on production.",
    },
]


def iter_code_files(targets: list[Path]) -> list[Path]:
    files: list[Path] = []
    self_path = Path(__file__).resolve()
    for target in targets:
        if not target.exists():
            continue
        if target.is_file():
            if target.resolve() != self_path and target.suffix.lower() in CODE_EXTENSIONS:
                files.append(target)
            continue
        for p in target.rglob("*"):
            if any(part in IGNORE_DIRS for part in p.parts):
                continue
            if p.is_file() and p.resolve() != self_path and p.suffix.lower() in CODE_EXTENSIONS:
                files.append(p)
    return sorted(set(files))


def mask_sensitive(snippet: str) -> str:
    """Mask literal tokens/secrets in output snippet per adk-owasp-scan Guardrails."""
    return re.sub(
        r"(['\"])[A-Za-z0-9_\-\.]{16,}(['\"])",
        r"\1***REDACTED***\2",
        snippet,
    )[:140]


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
        stripped = line.strip()
        if stripped.startswith(("#", "//", "/*", "*")):
            continue
        for rule in RULES:
            if rule["pattern"].search(line):
                findings.append({
                    "rule_id": rule["id"],
                    "category": rule["category"],
                    "severity": rule["severity"],
                    "location": f"{rel_path}:{line_no}",
                    "snippet": mask_sensitive(stripped),
                    "remediation": rule["remediation"],
                })
    return findings


def main() -> None:
    parser = argparse.ArgumentParser(description="ADK Deterministic OWASP & AI-Code Security Scanner (vbsec)")
    parser.add_argument("paths", nargs="*", default=["."], help="Files or directories to scan")
    parser.add_argument("--json", action="store_true", help="Output structured JSON report")
    parser.add_argument("--strict", action="store_true", help="Exit with code 1 if CRITICAL/HIGH findings exist")
    args = parser.parse_args()

    base_dir = Path.cwd()
    target_paths = [Path(p) for p in args.paths]
    code_files = iter_code_files(target_paths)

    all_findings: list[dict[str, Any]] = []
    for f in code_files:
        all_findings.extend(scan_file(f, base_dir))

    crit_high = [x for x in all_findings if x["severity"] in ("CRITICAL", "HIGH")]
    verdict = "PASS" if not all_findings else ("CONDITIONAL_PASS" if not crit_high else "FAIL")

    report = {
        "scanner": "vbsec_scanner",
        "files_scanned": len(code_files),
        "total_findings": len(all_findings),
        "critical_or_high_count": len(crit_high),
        "verdict": verdict,
        "findings": all_findings,
    }

    if args.json:
        print(json.dumps(report, indent=2, ensure_ascii=False))
    else:
        print(f"=== [VBSEC SECURITY SCANNER] verdict: {verdict} (Scanned: {len(code_files)} files, Findings: {len(all_findings)}) ===")
        if all_findings:
            print("| Rule | Category | Severity | Location | Remediation |")
            print("|---|---|---|---|---|")
            for item in all_findings:
                print(f"| `{item['rule_id']}` | `{item['category']}` | {item['severity']} | `{item['location']}` | {item['remediation']} |")
        else:
            print("No deterministic OWASP / AI-code vulnerabilities detected.")

    if args.strict and verdict == "FAIL":
        sys.exit(1)
    sys.exit(0)


if __name__ == "__main__":
    main()
