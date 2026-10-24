/**
 * UI Slop Auditor Service
 * Provides AST / Regex inspection of frontend source files (.html, .css, .tsx, .jsx, .vue, .svelte)
 * and bridges to Python auditor script with deterministic JS fallback.
 */

import fs from 'node:fs';
import path from 'node:path';
import { spawnSync } from 'node:child_process';

const UI_EXT_REGEX = /\.(tsx|jsx|ts|js|vue|svelte|html|css)$/i;

export function collectUiFiles(inputPaths) {
  const results = [];
  for (const p of inputPaths) {
    const abs = path.resolve(p);
    if (!fs.existsSync(abs)) continue;
    const stat = fs.statSync(abs);
    if (stat.isFile()) {
      results.push(abs);
    } else if (stat.isDirectory()) {
      const stack = [abs];
      while (stack.length > 0) {
        const dir = stack.pop();
        for (const entry of fs.readdirSync(dir, { withFileTypes: true })) {
          if (
            entry.name === 'node_modules' ||
            entry.name === '.git' ||
            entry.name === 'dist' ||
            entry.name === '.next'
          )
            continue;
          const full = path.join(dir, entry.name);
          if (entry.isDirectory()) stack.push(full);
          else if (UI_EXT_REGEX.test(entry.name)) results.push(full);
        }
      }
    }
  }
  return results;
}

export const SLOP_RULES = [
  {
    id: 'SLOP-001',
    severity: 'error',
    title: 'Forbidden transition-all (main-thread layout jitter)',
    regex: /\btransition-all\b|transition\s*:\s*all\b/g,
    fix: (text) =>
      text
        .replace(/\btransition-all\b/g, 'transition-[transform,opacity]')
        .replace(/transition\s*:\s*all\b/g, 'transition: transform, opacity')
  },
  {
    id: 'SLOP-002',
    severity: 'error',
    title: '100vh viewport trap on mobile (use 100dvh)',
    regex: /\b(h-screen|min-h-screen)\b|100vh\b/g,
    fix: (text) =>
      text
        .replace(/\bh-screen\b/g, 'h-[100dvh]')
        .replace(/\bmin-h-screen\b/g, 'min-h-[100dvh]')
        .replace(/100vh\b/g, '100dvh')
  },
  {
    id: 'SLOP-003',
    severity: 'warn',
    title: 'Focus ring removed without accessible focus-visible replacement',
    regex: /\boutline-none\b(?![^\n"']*focus(-visible)?:ring)/g,
    fix: (text) =>
      text.replace(
        /\boutline-none\b(?![^\n"']*focus(-visible)?:ring)/g,
        'outline-none focus-visible:ring-2'
      )
  },
  {
    id: 'SLOP-004',
    severity: 'warn',
    title: 'AI Slop purple/cyan neon gradient cliche',
    regex: /\bfrom-(purple|indigo|violet)-[456]00\s+[^\n"']*to-(pink|cyan|fuchsia)-[456]00\b/g,
    fix: null
  },
  {
    id: 'SLOP-005',
    severity: 'warn',
    title: 'Modal animated from scale-0 (use scale-95)',
    regex: /\bscale-0\b/g,
    fix: (text) => text.replace(/\bscale-0\b/g, 'scale-95')
  }
];

export function runJsFallbackAudit(paths, fixMode = false) {
  const files = collectUiFiles(paths);
  const violations = [];
  const fixedFiles = [];

  for (const file of files) {
    let content = fs.readFileSync(file, 'utf8');
    let modified = false;

    if (fixMode) {
      for (const rule of SLOP_RULES) {
        if (rule.fix && rule.regex.test(content)) {
          rule.regex.lastIndex = 0;
          const next = rule.fix(content);
          if (next !== content) {
            content = next;
            modified = true;
          }
        }
        rule.regex.lastIndex = 0;
      }
      if (modified) {
        fs.writeFileSync(file, content, 'utf8');
        fixedFiles.push(file);
      }
    }

    const lines = content.split(/\r?\n/);
    lines.forEach((line, idx) => {
      for (const rule of SLOP_RULES) {
        rule.regex.lastIndex = 0;
        if (rule.regex.test(line)) {
          violations.push({
            file: path.relative(process.cwd(), file),
            line: idx + 1,
            rule_id: rule.id,
            severity: rule.severity,
            message: rule.title,
            snippet: line.trim().slice(0, 120)
          });
        }
        rule.regex.lastIndex = 0;
      }
    });
  }

  const penalty = violations.reduce((acc, v) => acc + (v.severity === 'error' ? 2 : 1), 0);
  const score = Math.max(0, 20 - penalty);
  return {
    engine: 'js-fallback-auditor',
    files_scanned: files.length,
    fixed_files: fixedFiles.map((f) => path.relative(process.cwd(), f)),
    impeccable_score: `${score}/20`,
    score_numeric: score,
    passed: score >= 16 && !violations.some((v) => v.severity === 'error'),
    violations
  };
}

export function invokePythonOrFallbackAuditor(paths, options = { strict: false, fix: false }, kitRoot = null) {
  const auditorScript = kitRoot
    ? path.join(kitRoot, 'skills', 'core', 'adk-ui-craft', 'scripts', 'ui_slop_auditor.py')
    : null;

  if (auditorScript && fs.existsSync(auditorScript)) {
    const pyCandidates = process.platform === 'win32' ? ['py', 'python'] : ['python3', 'python'];
    for (const cmd of pyCandidates) {
      const pyArgs = [];
      if (cmd === 'py') pyArgs.push('-3');
      pyArgs.push('-B', auditorScript, ...paths, '--json');
      if (options.strict) pyArgs.push('--strict');
      if (options.fix) pyArgs.push('--fix');

      const res = spawnSync(cmd, pyArgs, { encoding: 'utf8', timeout: 15000 });
      if (!res.error && res.stdout && res.stdout.trim().startsWith('{')) {
        try {
          return JSON.parse(res.stdout.trim());
        } catch (e) {
          // Fall through to JS fallback
        }
      }
    }
  }
  return runJsFallbackAudit(paths, Boolean(options.fix));
}
