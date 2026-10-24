#!/usr/bin/env node
import fs from 'node:fs';
import path from 'node:path';
import readline from 'node:readline';
import { fileURLToPath } from 'node:url';
import { spawnSync } from 'node:child_process';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);
const kitRoot = path.resolve(__dirname, '..', '..', '..');

const archetypesPath = path.join(__dirname, 'data', 'archetypes.json');
const motionRecipesPath = path.join(__dirname, 'data', 'motion-recipes.json');
const componentBlueprintsPath = path.join(__dirname, 'data', 'component-blueprints.json');

let archetypesDb = [];
let motionRecipesDb = [];
let componentBlueprintsDb = [];

try {
  archetypesDb = JSON.parse(fs.readFileSync(archetypesPath, 'utf8')).archetypes || [];
} catch (e) {
  console.error('[UIDesignMCP] Warning: Unable to load archetypes.json:', e.message);
}

try {
  motionRecipesDb = JSON.parse(fs.readFileSync(motionRecipesPath, 'utf8')).recipes || [];
} catch (e) {
  console.error('[UIDesignMCP] Warning: Unable to load motion-recipes.json:', e.message);
}

try {
  componentBlueprintsDb = JSON.parse(fs.readFileSync(componentBlueprintsPath, 'utf8')).blueprints || [];
} catch (e) {
  console.error('[UIDesignMCP] Warning: Unable to load component-blueprints.json:', e.message);
}

// -------------------------------------------------------------
// WCAG 2.2 Relative Luminance & Color Contrast Math Engine
// -------------------------------------------------------------
function normalizeHex(hexStr) {
  if (!hexStr || typeof hexStr !== 'string') return null;
  let clean = hexStr.trim().replace(/^#/, '');
  if (/^[0-9a-fA-F]{3}$/.test(clean)) {
    clean = clean.split('').map(c => c + c).join('');
  }
  if (!/^[0-9a-fA-F]{6}$/.test(clean)) return null;
  return '#' + clean.toUpperCase();
}

function hexToRgb(hex) {
  const norm = normalizeHex(hex);
  if (!norm) return null;
  const num = parseInt(norm.slice(1), 16);
  return {
    r: (num >> 16) & 255,
    g: (num >> 8) & 255,
    b: num & 255
  };
}

function rgbToHex(r, g, b) {
  const clamp = (n) => Math.max(0, Math.min(255, Math.round(n)));
  return (
    '#' +
    [clamp(r), clamp(g), clamp(b)]
      .map((v) => v.toString(16).padStart(2, '0'))
      .join('')
      .toUpperCase()
  );
}

function srgbChannelToLinear(channel8Bit) {
  const c = channel8Bit / 255;
  return c <= 0.04045 ? c / 12.92 : Math.pow((c + 0.055) / 1.055, 2.4);
}

function getRelativeLuminance(hex) {
  const rgb = hexToRgb(hex);
  if (!rgb) return null;
  const R = srgbChannelToLinear(rgb.r);
  const G = srgbChannelToLinear(rgb.g);
  const B = srgbChannelToLinear(rgb.b);
  return 0.2126 * R + 0.7152 * G + 0.0722 * B;
}

function getContrastRatio(fgHex, bgHex) {
  const l1 = getRelativeLuminance(fgHex);
  const l2 = getRelativeLuminance(bgHex);
  if (l1 === null || l2 === null) return null;
  const lighter = Math.max(l1, l2);
  const darker = Math.min(l1, l2);
  return (lighter + 0.05) / (darker + 0.05);
}

function rgbToHsl(r, g, b) {
  r /= 255;
  g /= 255;
  b /= 255;
  const max = Math.max(r, g, b);
  const min = Math.min(r, g, b);
  let h = 0;
  let s = 0;
  const l = (max + min) / 2;
  if (max !== min) {
    const d = max - min;
    s = l > 0.5 ? d / (2 - max - min) : d / (max + min);
    switch (max) {
      case r:
        h = (g - b) / d + (g < b ? 6 : 0);
        break;
      case g:
        h = (b - r) / d + 2;
        break;
      case b:
        h = (r - g) / d + 4;
        break;
    }
    h /= 6;
  }
  return { h, s, l };
}

function hslToRgb(h, s, l) {
  let r, g, b;
  if (s === 0) {
    r = g = b = l;
  } else {
    const hue2rgb = (p, q, t) => {
      if (t < 0) t += 1;
      if (t > 1) t -= 1;
      if (t < 1 / 6) return p + (q - p) * 6 * t;
      if (t < 1 / 2) return q;
      if (t < 2 / 3) return p + (q - p) * (2 / 3 - t) * 6;
      return p;
    };
    const q = l < 0.5 ? l * (1 + s) : l + s - l * s;
    const p = 2 * l - q;
    r = hue2rgb(p, q, h + 1 / 3);
    g = hue2rgb(p, q, h);
    b = hue2rgb(p, q, h - 1 / 3);
  }
  return { r: Math.round(r * 255), g: Math.round(g * 255), b: Math.round(b * 255) };
}

function suggestAccessibleForeground(fgHex, bgHex, targetRatio) {
  const fgRgb = hexToRgb(fgHex);
  const bgLum = getRelativeLuminance(bgHex);
  if (!fgRgb || bgLum === null) return null;

  const { h, s } = rgbToHsl(fgRgb.r, fgRgb.g, fgRgb.b);
  // Determine whether darkening or lightening reaches the target ratio better
  const preferLighter = bgLum < 0.5;
  const directions = preferLighter ? ['lighter', 'darker'] : ['darker', 'lighter'];

  for (const dir of directions) {
    let low = dir === 'lighter' ? 0 : 0;
    let high = dir === 'lighter' ? 1 : 1;
    let bestHex = null;

    for (let step = 0; step <= 100; step++) {
      const l = dir === 'lighter' ? step / 100 : 1 - step / 100;
      const rgb = hslToRgb(h, s, l);
      const candidateHex = rgbToHex(rgb.r, rgb.g, rgb.b);
      const ratio = getContrastRatio(candidateHex, bgHex);
      if (ratio !== null && ratio >= targetRatio) {
        bestHex = candidateHex;
        break;
      }
    }
    if (bestHex) return bestHex;
  }

  return preferLighter ? '#FFFFFF' : '#000000';
}

// -------------------------------------------------------------
// Token Compiler (DESIGN.md, Tailwind v4, CSS Vars, DTCG JSON)
// -------------------------------------------------------------
function compileDesignTokens(archetype, format = 'design-md', projectName = null) {
  const c = archetype.colors;
  const t = archetype.typography;
  const r = archetype.radius;
  const fmt = (format || 'design-md').toLowerCase().trim();
  const titleName = projectName ? `${projectName} (${archetype.name})` : archetype.name;

  if (fmt === 'tailwind-v4') {
    return `@import "tailwindcss";

@theme {
  /* Archetype: ${archetype.name} (${archetype.id}) */
  --font-sans: ${t.font_sans};
  --font-mono: ${t.font_mono};

  --color-background: ${c.background};
  --color-surface: ${c.surface};
  --color-surface-border: ${c.surface_border};
  --color-text-primary: ${c.text_primary};
  --color-text-muted: ${c.text_muted};

  --color-primary: ${c.primary};
  --color-primary-foreground: ${c.primary_fg};
  --color-secondary: ${c.secondary};
  --color-secondary-foreground: ${c.secondary_fg};
  --color-accent: ${c.accent};
  --color-accent-foreground: ${c.accent_fg};

  --color-status-draft-bg: ${c.status.draft.bg};
  --color-status-draft-fg: ${c.status.draft.fg};
  --color-status-pending-bg: ${c.status.pending.bg};
  --color-status-pending-fg: ${c.status.pending.fg};
  --color-status-success-bg: ${c.status.success.bg};
  --color-status-success-fg: ${c.status.success.fg};
  --color-status-error-bg: ${c.status.error.bg};
  --color-status-error-fg: ${c.status.error.fg};
  --color-status-info-bg: ${c.status.info.bg};
  --color-status-info-fg: ${c.status.info.fg};

  --radius-sm: ${r.sm};
  --radius-md: ${r.md};
  --radius-lg: ${r.lg};
}`;
  }

  if (fmt === 'css-vars') {
    return `:root {
  /* Archetype: ${archetype.name} (${archetype.id}) */
  --font-sans: ${t.font_sans};
  --font-mono: ${t.font_mono};
  --heading-weight: ${t.heading_weight};
  --tracking-tight: ${t.tracking};
  --line-height-base: ${t.line_height};

  --bg-canvas: ${c.background};
  --bg-surface: ${c.surface};
  --border-surface: ${c.surface_border};
  --text-primary: ${c.text_primary};
  --text-muted: ${c.text_muted};

  --color-primary: ${c.primary};
  --color-primary-fg: ${c.primary_fg};
  --color-secondary: ${c.secondary};
  --color-secondary-fg: ${c.secondary_fg};
  --color-accent: ${c.accent};
  --color-accent-fg: ${c.accent_fg};

  --status-draft-bg: ${c.status.draft.bg};
  --status-draft-fg: ${c.status.draft.fg};
  --status-pending-bg: ${c.status.pending.bg};
  --status-pending-fg: ${c.status.pending.fg};
  --status-success-bg: ${c.status.success.bg};
  --status-success-fg: ${c.status.success.fg};
  --status-error-bg: ${c.status.error.bg};
  --status-error-fg: ${c.status.error.fg};
  --status-info-bg: ${c.status.info.bg};
  --status-info-fg: ${c.status.info.fg};

  --radius-sm: ${r.sm};
  --radius-md: ${r.md};
  --radius-lg: ${r.lg};
}`;
  }

  if (fmt === 'dtcg-json') {
    const dtcg = {
      $schema: 'https://tr.designtokens.org/format/',
      meta: {
        archetype_id: archetype.id,
        name: archetype.name,
        dials: archetype.dials
      },
      color: {
        background: { $value: c.background, $type: 'color' },
        surface: { $value: c.surface, $type: 'color' },
        surface_border: { $value: c.surface_border, $type: 'color' },
        text_primary: { $value: c.text_primary, $type: 'color' },
        text_muted: { $value: c.text_muted, $type: 'color' },
        primary: { $value: c.primary, $type: 'color' },
        primary_fg: { $value: c.primary_fg, $type: 'color' },
        secondary: { $value: c.secondary, $type: 'color' },
        secondary_fg: { $value: c.secondary_fg, $type: 'color' },
        accent: { $value: c.accent, $type: 'color' },
        accent_fg: { $value: c.accent_fg, $type: 'color' },
        status: Object.fromEntries(
          Object.entries(c.status).map(([k, v]) => [
            k,
            {
              bg: { $value: v.bg, $type: 'color' },
              fg: { $value: v.fg, $type: 'color' },
              border: { $value: v.border, $type: 'color' }
            }
          ])
        )
      },
      typography: {
        font_sans: { $value: t.font_sans, $type: 'fontFamily' },
        font_mono: { $value: t.font_mono, $type: 'fontFamily' },
        heading_weight: { $value: t.heading_weight, $type: 'fontWeight' },
        tracking: { $value: t.tracking, $type: 'dimension' }
      },
      radius: {
        sm: { $value: r.sm, $type: 'dimension' },
        md: { $value: r.md, $type: 'dimension' },
        lg: { $value: r.lg, $type: 'dimension' }
      }
    };
    return JSON.stringify(dtcg, null, 2);
  }

  // Default: Google Labs Stitch DESIGN.md specification
  return `# DESIGN.md — ${titleName}

> **Archetype ID**: \`${archetype.id}\`
> **Domains**: ${archetype.domains.map((d) => `\`${d}\``).join(', ')}
> **Control Dials**: \`DESIGN_VARIANCE=${archetype.dials.variance}/10\` | \`MOTION_INTENSITY=${archetype.dials.motion}/10\` | \`VISUAL_DENSITY=${archetype.dials.density}/10\`

## 1. Aesthetic Direction & Persona
${archetype.aesthetic_persona}

## 2. Color Palette & Atmospheric Polarity (WCAG AA Verified)
- **Canvas Background**: \`${c.background}\`
- **Elevated Surface**: \`${c.surface}\`
- **Hairline Border**: \`${c.surface_border}\`
- **Primary Text**: \`${c.text_primary}\`
- **Muted Text**: \`${c.text_muted}\`
- **Primary Interactive**: \`${c.primary}\` (Foreground: \`${c.primary_fg}\`)
- **Secondary Interactive**: \`${c.secondary}\` (Foreground: \`${c.secondary_fg}\`)
- **Accent Brand**: \`${c.accent}\` (Foreground: \`${c.accent_fg}\`)

### Semantic Status Tokens (5 States)
| State | Background | Foreground | Border |
|---|---|---|---|
| **Draft** | \`${c.status.draft.bg}\` | \`${c.status.draft.fg}\` | \`${c.status.draft.border}\` |
| **Pending** | \`${c.status.pending.bg}\` | \`${c.status.pending.fg}\` | \`${c.status.pending.border}\` |
| **Success** | \`${c.status.success.bg}\` | \`${c.status.success.fg}\` | \`${c.status.success.border}\` |
| **Error** | \`${c.status.error.bg}\` | \`${c.status.error.fg}\` | \`${c.status.error.border}\` |
| **Info** | \`${c.status.info.bg}\` | \`${c.status.info.fg}\` | \`${c.status.info.border}\` |

## 3. Typography & Scannable Hierarchy
- **Sans Font Stack**: \`${t.font_sans}\`
- **Mono Font Stack**: \`${t.font_mono}\`
- **Heading Weight**: \`${t.heading_weight}\`
- **Letter Tracking**: \`${t.tracking}\`
- **Base Line Height**: \`${t.line_height}\`
- **Numeric Discipline**: Enforce \`font-variant-numeric: tabular-nums\` (\`tabular-nums\`) on all numbers, prices, timestamps, and metrics.

## 4. Layout, Spatial Architecture & Radii
- **Radius Small**: \`${r.sm}\`
- **Radius Medium**: \`${r.md}\`
- **Radius Large**: \`${r.lg}\`
- **Borders & Elevation**: ${archetype.borders_and_shadows}

## 5. Motion & Interaction Physics
- **Tactile Press**: \`active:scale-[0.97]\` with \`cubic-bezier(0.16, 1, 0.3, 1)\` (150ms).
- **Modal Entry**: Start from \`scale(0.95)\` + \`opacity: 0\`, never from \`scale(0)\`.
- **Compositor Discipline**: Animate only \`transform\` and \`opacity\`; always honor \`prefers-reduced-motion: reduce\`.

## 6. Anti-Patterns & Forbidden Slop
${archetype.anti_patterns.map((ap) => `- ❌ ${ap}`).join('\n')}
- ❌ Never use \`transition-all\` or \`100vh\` on full-screen mobile shells (use \`100dvh\`).
- ❌ Never use \`font-size < 16px\` on mobile \`<input>\` / \`<textarea>\` elements.
`;
}

// -------------------------------------------------------------
// Built-in JS Fallback UI Slop Scanner & Auto-Fixer
// -------------------------------------------------------------
const UI_EXT_REGEX = /\.(tsx|jsx|ts|js|vue|svelte|html|css)$/i;

function collectUiFiles(inputPaths) {
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
          if (entry.name === 'node_modules' || entry.name === '.git' || entry.name === 'dist' || entry.name === '.next') continue;
          const full = path.join(dir, entry.name);
          if (entry.isDirectory()) stack.push(full);
          else if (UI_EXT_REGEX.test(entry.name)) results.push(full);
        }
      }
    }
  }
  return results;
}

const SLOP_RULES = [
  {
    id: 'SLOP-001',
    severity: 'error',
    title: 'Forbidden transition-all (main-thread layout jitter)',
    regex: /\btransition-all\b|transition\s*:\s*all\b/g,
    fix: (text) => text.replace(/\btransition-all\b/g, 'transition-[transform,opacity]').replace(/transition\s*:\s*all\b/g, 'transition: transform, opacity')
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
    fix: (text) => text.replace(/\boutline-none\b(?![^\n"']*focus(-visible)?:ring)/g, 'outline-none focus-visible:ring-2')
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

function runJsFallbackAudit(paths, fixMode = false) {
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

function invokePythonOrFallbackAuditor(paths, options = { strict: false, fix: false }) {
  const auditorScript = path.join(kitRoot, 'skills', 'core', 'adk-ui-craft', 'scripts', 'ui_slop_auditor.py');
  if (fs.existsSync(auditorScript)) {
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
  return runJsFallbackAuditorWrapper(paths, options);
}

function runJsFallbackAuditorWrapper(paths, options) {
  return runJsFallbackAudit(paths, Boolean(options.fix));
}

// -------------------------------------------------------------
// Khai báo danh mục 7 MCP Tools
// -------------------------------------------------------------
const TOOLS = [
  {
    name: 'search_design_archetypes',
    description: 'Tìm kiếm và xếp hạng Design Archetypes theo từ khóa, lĩnh vực (domain) và khoảng cách Euclid với bộ 3 thông số Dials (variance, motion, density 1-10).',
    inputSchema: {
      type: 'object',
      properties: {
        query: {
          type: 'string',
          description: 'Từ khóa tìm kiếm (ví dụ: "dark", "fintech", "editorial", "brutalist", "mobile", "enterprise")'
        },
        domain: {
          type: 'string',
          description: 'Lĩnh vực ứng dụng (ví dụ: "saas", "fintech", "erp", "publishing", "consumer-app")'
        },
        dials: {
          type: 'object',
          description: 'Bộ 3 thông số điều khiển thiết kế từ 1 đến 10: { variance?: number, motion?: number, density?: number }',
          properties: {
            variance: { type: 'number' },
            motion: { type: 'number' },
            density: { type: 'number' }
          }
        }
      }
    }
  },
  {
    name: 'get_design_tokens',
    description: 'Biên dịch động bộ Design Tokens của một Archetype ra định dạng chuẩn: Google Labs DESIGN.md ("design-md"), Tailwind v4 @theme ("tailwind-v4"), CSS Variables ("css-vars"), hoặc W3C DTCG JSON ("dtcg-json").',
    inputSchema: {
      type: 'object',
      properties: {
        archetype_id: {
          type: 'string',
          description: 'ID của archetype (ví dụ: "linear-precision-dark", "stripe-fintech-clarity", "swiss-editorial-grid")'
        },
        format: {
          type: 'string',
          enum: ['design-md', 'tailwind-v4', 'css-vars', 'dtcg-json'],
          description: 'Định dạng xuất token (mặc định: "design-md")'
        }
      },
      required: ['archetype_id']
    }
  },
  {
    name: 'get_component_blueprint',
    description: 'Lấy đặc tả Component Blueprint kết hợp với công thức chuyển động vật lý (Motion Recipe), quy tắc Mobile Native, bộ dữ liệu phá thử giao diện (break-ui payloads) và code mẫu sạch 100% anti-slop.',
    inputSchema: {
      type: 'object',
      properties: {
        component_id: {
          type: 'string',
          description: 'ID của component: "data-table", "modal-dialog", "drawer-sheet", "command-palette", "form-control", "status-badge", "bento-grid"'
        }
      },
      required: ['component_id']
    }
  },
  {
    name: 'verify_color_contrast',
    description: 'Tính toán chính xác tỷ lệ tương phản màu sắc theo công thức toán học WCAG 2.2 Relative Luminance (L = 0.2126R + 0.7152G + 0.0722B), kiểm tra PASS/FAIL cho AA/AAA và tự động đề xuất mã màu foreground đạt chuẩn nếu FAIL.',
    inputSchema: {
      type: 'object',
      properties: {
        foreground_hex: {
          type: 'string',
          description: 'Mã màu chữ/icon (ví dụ: "#A1A1AA" hoặc "#0A2540")'
        },
        background_hex: {
          type: 'string',
          description: 'Mã màu nền (ví dụ: "#09090B" hoặc "#FFFFFF")'
        },
        level: {
          type: 'string',
          enum: ['AA', 'AAA'],
          description: 'Mức chuẩn WCAG cần kiểm tra (mặc định: "AA")'
        }
      },
      required: ['foreground_hex', 'background_hex']
    }
  },
  {
    name: 'audit_ui_code',
    description: 'Quét mã nguồn UI (React/Tailwind/CSS/HTML) bằng trình kiểm toán Anti-Slop để chấm điểm Impeccable 20/20 và phát hiện các lỗi vi phạm thẩm mỹ, a11y, mobile viewport.',
    inputSchema: {
      type: 'object',
      properties: {
        paths: {
          type: 'array',
          items: { type: 'string' },
          description: 'Danh sách đường dẫn file hoặc thư mục cần kiểm tra'
        },
        strict: {
          type: 'boolean',
          description: 'Bật chế độ kiểm tra nghiêm ngặt (mặc định: false)'
        }
      },
      required: ['paths']
    }
  },
  {
    name: 'fix_ui_slop',
    description: 'Tự động sửa các lỗi UI Anti-Slop tĩnh (như transition-all, 100vh, thiếu focus-visible ring, scale-0) trên các đường dẫn chỉ định.',
    inputSchema: {
      type: 'object',
      properties: {
        paths: {
          type: 'array',
          items: { type: 'string' },
          description: 'Danh sách đường dẫn file hoặc thư mục cần sửa lỗi tự động'
        }
      },
      required: ['paths']
    }
  },
  {
    name: 'scaffold_design_contract',
    description: 'Sinh file hợp đồng thiết kế DESIGN.md chuẩn vào thư mục dự án (target_dir/DESIGN.md). Mặc định bảo vệ an toàn không ghi đè nếu file đã tồn tại (overwrite=false).',
    inputSchema: {
      type: 'object',
      properties: {
        archetype_id: {
          type: 'string',
          description: 'ID của archetype muốn khởi tạo'
        },
        target_dir: {
          type: 'string',
          description: 'Thư mục dự án đích'
        },
        project_name: {
          type: 'string',
          description: 'Tên dự án tùy chọn'
        },
        overwrite: {
          type: 'boolean',
          description: 'Cho phép ghi đè nếu DESIGN.md đã tồn tại (mặc định: false)'
        }
      },
      required: ['archetype_id', 'target_dir']
    }
  }
];

// -------------------------------------------------------------
// Hàm xử lý Tool Calls
// -------------------------------------------------------------
function handleToolCall(name, args = {}) {
  switch (name) {
    case 'search_design_archetypes': {
      const q = (args.query || '').toLowerCase().trim();
      const dom = (args.domain || '').toLowerCase().trim();
      const dials = args.dials || null;

      let candidates = archetypesDb.filter((a) => {
        const matchesQuery =
          !q ||
          a.id.toLowerCase().includes(q) ||
          a.name.toLowerCase().includes(q) ||
          a.aesthetic_persona.toLowerCase().includes(q) ||
          a.domains.some((d) => d.toLowerCase().includes(q));
        const matchesDomain =
          !dom || a.domains.some((d) => d.toLowerCase().includes(dom));
        return matchesQuery && matchesDomain;
      });

      if (candidates.length === 0) {
        candidates = [...archetypesDb];
      }

      const scored = candidates.map((a) => {
        let distance = 0;
        if (dials && typeof dials === 'object') {
          const dv = typeof dials.variance === 'number' ? dials.variance - a.dials.variance : 0;
          const dm = typeof dials.motion === 'number' ? dials.motion - a.dials.motion : 0;
          const dd = typeof dials.density === 'number' ? dials.density - a.dials.density : 0;
          distance = Math.sqrt(dv * dv + dm * dm + dd * dd);
        }
        return { archetype: a, distance: Number(distance.toFixed(2)) };
      });

      if (dials) {
        scored.sort((x, y) => x.distance - y.distance);
      }

      const summary = scored
        .map(({ archetype: a, distance }) => {
          const distBadge = dials ? ` | **Dial Distance**: \`${distance}\`` : '';
          return `### 🎨 \`${a.id}\` — ${a.name}${distBadge}\n- **Domains**: ${a.domains.join(', ')}\n- **Dials**: \`variance=${a.dials.variance}\`, \`motion=${a.dials.motion}\`, \`density=${a.dials.density}\`\n- **Persona**: ${a.aesthetic_persona}\n- **Palette**: Bg \`${a.colors.background}\` | Surface \`${a.colors.surface}\` | Primary \`${a.colors.primary}\` | Accent \`${a.colors.accent}\``;
        })
        .join('\n\n');

      return {
        content: [
          {
            type: 'text',
            text: `Tìm thấy ${scored.length} Design Archetype phù hợp:\n\n${summary}\n\n👉 Gọi \`get_design_tokens\` với \`archetype_id\` để xuất bộ token chi tiết (\`design-md\`, \`tailwind-v4\`, \`css-vars\`, \`dtcg-json\`).`
          }
        ]
      };
    }

    case 'get_design_tokens': {
      const id = (args.archetype_id || '').toLowerCase().trim();
      const archetype = archetypesDb.find((a) => a.id.toLowerCase() === id);
      if (!archetype) {
        return {
          isError: true,
          content: [
            {
              type: 'text',
              text: `Lỗi: Không tìm thấy archetype "${args.archetype_id}". Các ID hợp lệ: ${archetypesDb.map((a) => a.id).join(', ')}`
            }
          ]
        };
      }
      const format = args.format || 'design-md';
      const compiled = compileDesignTokens(archetype, format);
      return {
        content: [{ type: 'text', text: compiled }]
      };
    }

    case 'get_component_blueprint': {
      const id = (args.component_id || '').toLowerCase().trim();
      const bp = componentBlueprintsDb.find((b) => b.id.toLowerCase() === id);
      if (!bp) {
        return {
          isError: true,
          content: [
            {
              type: 'text',
              text: `Lỗi: Không tìm thấy component blueprint "${args.component_id}". Danh sách khả dụng: ${componentBlueprintsDb.map((b) => b.id).join(', ')}`
            }
          ]
        };
      }
      const recipe = motionRecipesDb.find((r) => r.id === bp.motion_recipe_id);

      let out = `# 🧩 Component Blueprint: ${bp.name} (\`${bp.id}\`)\n\n`;
      out += `## 1. Bất biến kỹ thuật & Trạng thái (Invariants)\n${bp.invariants.map((i) => `- ✅ ${i}`).join('\n')}\n\n`;
      out += `## 2. Quy tắc Mobile Native & Touch Ergonomics\n${bp.mobile_native_rules.map((m) => `- 📱 ${m}`).join('\n')}\n\n`;

      if (recipe) {
        out += `## 3. Công thức chuyển động vật lý (${recipe.name} — \`${recipe.id}\`)\n`;
        out += `- **Khi sử dụng**: ${recipe.when_to_use}\n`;
        out += `- **Easing**: \`${recipe.physics.easing}\` | **Duration**: \`${recipe.physics.duration_ms}ms\`\n`;
        out += `- **Tailwind Classes**: \`${recipe.tailwind_classes}\`\n`;
        out += `- **Nghiêm cấm (Forbidden Slop)**: ${recipe.forbidden_slop.join('; ')}\n\n`;
      }

      out += `## 4. Bộ dữ liệu cực đoan phá thử giao diện (\`break-ui\` Stress Payloads)\n\`\`\`json\n${JSON.stringify(bp.break_ui_payloads, null, 2)}\n\`\`\`\n\n`;
      out += `## 5. Mẫu code chuẩn Anti-Slop (React + Tailwind)\n\`\`\`tsx\n${bp.tailwind_react_snippet}\n\`\`\``;

      return {
        content: [{ type: 'text', text: out }]
      };
    }

    case 'verify_color_contrast': {
      const fgNorm = normalizeHex(args.foreground_hex);
      const bgNorm = normalizeHex(args.background_hex);
      const level = (args.level || 'AA').toUpperCase() === 'AAA' ? 'AAA' : 'AA';

      if (!fgNorm || !bgNorm) {
        return {
          isError: true,
          content: [
            {
              type: 'text',
              text: `Lỗi: Mã màu Hex không hợp lệ (foreground="${args.foreground_hex}", background="${args.background_hex}"). Hãy truyền định dạng #RRGGBB hoặc #RGB.`
            }
          ]
        };
      }

      const fgLum = getRelativeLuminance(fgNorm);
      const bgLum = getRelativeLuminance(bgNorm);
      const ratio = getContrastRatio(fgNorm, bgNorm);
      const ratioRounded = Number(ratio.toFixed(2));

      const normalTarget = level === 'AAA' ? 7.0 : 4.5;
      const largeTarget = level === 'AAA' ? 4.5 : 3.0;
      const uiTarget = 3.0;

      const normalPass = ratio >= normalTarget;
      const largePass = ratio >= largeTarget;
      const uiPass = ratio >= uiTarget;

      const suggestedFg = normalPass
        ? fgNorm
        : suggestAccessibleForeground(fgNorm, bgNorm, normalTarget);
      const suggestedRatio = suggestedFg
        ? Number(getContrastRatio(suggestedFg, bgNorm).toFixed(2))
        : null;

      const resultObj = {
        foreground_hex: fgNorm,
        background_hex: bgNorm,
        foreground_luminance: Number(fgLum.toFixed(4)),
        background_luminance: Number(bgLum.toFixed(4)),
        contrast_ratio: `${ratioRounded.toFixed(2)}:1`,
        contrast_numeric: ratioRounded,
        target_level: level,
        evaluations: {
          normal_text: {
            required: `${normalTarget.toFixed(1)}:1`,
            status: normalPass ? 'PASS' : 'FAIL'
          },
          large_text: {
            required: `${largeTarget.toFixed(1)}:1`,
            status: largePass ? 'PASS' : 'FAIL'
          },
          ui_component: {
            required: `${uiTarget.toFixed(1)}:1`,
            status: uiPass ? 'PASS' : 'FAIL'
          }
        },
        ...(normalPass
          ? {}
          : {
              suggested_foreground_hex: suggestedFg,
              suggested_contrast_ratio: `${suggestedRatio.toFixed(2)}:1`
            })
      };

      return {
        content: [{ type: 'text', text: JSON.stringify(resultObj, null, 2) }]
      };
    }

    case 'audit_ui_code': {
      const paths = Array.isArray(args.paths) && args.paths.length > 0 ? args.paths : ['.'];
      const report = invokePythonOrFallbackAuditor(paths, {
        strict: Boolean(args.strict),
        fix: false
      });
      return {
        content: [{ type: 'text', text: JSON.stringify(report, null, 2) }]
      };
    }

    case 'fix_ui_slop': {
      const paths = Array.isArray(args.paths) && args.paths.length > 0 ? args.paths : ['.'];
      const report = invokePythonOrFallbackAuditor(paths, {
        strict: false,
        fix: true
      });
      return {
        content: [{ type: 'text', text: JSON.stringify(report, null, 2) }]
      };
    }

    case 'scaffold_design_contract': {
      const id = (args.archetype_id || '').toLowerCase().trim();
      const archetype = archetypesDb.find((a) => a.id.toLowerCase() === id);
      if (!archetype) {
        return {
          isError: true,
          content: [
            {
              type: 'text',
              text: `Lỗi: Không tìm thấy archetype "${args.archetype_id}". Danh sách khả dụng: ${archetypesDb.map((a) => a.id).join(', ')}`
            }
          ]
        };
      }

      const targetDir = path.resolve(args.target_dir || '.');
      const allowOverwrite = args.overwrite === true;
      const designMdPath = path.join(targetDir, 'DESIGN.md');

      if (fs.existsSync(designMdPath) && !allowOverwrite) {
        return {
          isError: true,
          content: [
            {
              type: 'text',
              text: `⚠️ Chặn ghi đè an toàn: File \`${designMdPath}\` đã tồn tại. Truyền \`overwrite: true\` nếu bạn thực sự muốn ghi đè DESIGN.md.`
            }
          ]
        };
      }

      if (!fs.existsSync(targetDir)) {
        fs.mkdirSync(targetDir, { recursive: true });
      }

      const projName = args.project_name || path.basename(targetDir);
      const content = compileDesignTokens(archetype, 'design-md', projName);
      fs.writeFileSync(designMdPath, content, 'utf8');

      return {
        content: [
          {
            type: 'text',
            text: `✅ Đã khởi tạo hợp đồng thiết kế **DESIGN.md** theo archetype \`${archetype.id}\` (${archetype.name}) tại:\n📄 \`${designMdPath}\``
          }
        ]
      };
    }

    default:
      return {
        isError: true,
        content: [{ type: 'text', text: `Tool không tồn tại: ${name}` }]
      };
  }
}

// -------------------------------------------------------------
// Chế độ CLI
// -------------------------------------------------------------
const cliArgs = process.argv.slice(2);
if (cliArgs.length > 0 && !cliArgs.includes('--stdio')) {
  const cmd = cliArgs[0].toLowerCase();

  if (cmd === '--help' || cmd === '-h' || cmd === 'help') {
    console.log(`
Agent-Dev-Kit UI Design Craft CLI & MCP Server
Cách dùng:
  node index.js search [query]                             : Tìm kiếm Design Archetypes
  node index.js tokens <archetype_id> [format]             : Xuất Design Tokens (design-md | tailwind-v4 | css-vars | dtcg-json)
  node index.js component <component_id>                   : Xem Component Blueprint + Motion Physics + break-ui payloads
  node index.js contrast <fg_hex> <bg_hex> [AA|AAA]        : Kiểm tra độ tương phản màu WCAG 2.2 & gợi ý màu sửa
  node index.js audit <path...>                            : Kiểm toán mã nguồn UI chấm điểm Impeccable 20/20
  node index.js fix <path...>                              : Tự động sửa các lỗi UI Anti-Slop tĩnh
  node index.js scaffold <archetype_id> <target_dir> [name]: Sinh hợp đồng thiết kế DESIGN.md vào thư mục đích
  node index.js                                            : Khởi chạy dưới dạng MCP Server (Stdio)
`);
    process.exit(0);
  } else if (cmd === 'search') {
    const q = cliArgs.slice(1).join(' ');
    const res = handleToolCall('search_design_archetypes', { query: q });
    console.log(res.content[0].text);
    process.exit(res.isError ? 1 : 0);
  } else if (cmd === 'tokens') {
    const archetypeId = cliArgs[1];
    const format = cliArgs[2] || 'design-md';
    const res = handleToolCall('get_design_tokens', { archetype_id: archetypeId, format });
    console.log(res.content[0].text);
    process.exit(res.isError ? 1 : 0);
  } else if (cmd === 'component') {
    const componentId = cliArgs[1];
    const res = handleToolCall('get_component_blueprint', { component_id: componentId });
    console.log(res.content[0].text);
    process.exit(res.isError ? 1 : 0);
  } else if (cmd === 'contrast') {
    const fg = cliArgs[1];
    const bg = cliArgs[2];
    const level = cliArgs[3] || 'AA';
    const res = handleToolCall('verify_color_contrast', {
      foreground_hex: fg,
      background_hex: bg,
      level
    });
    console.log(res.content[0].text);
    process.exit(res.isError ? 1 : 0);
  } else if (cmd === 'audit') {
    const rawArgs = cliArgs.slice(1);
    const strict = rawArgs.includes('--strict');
    const paths = rawArgs.filter((a) => a !== '--strict');
    const res = handleToolCall('audit_ui_code', { paths, strict });
    console.log(res.content[0].text);
    process.exit(res.isError ? 1 : 0);
  } else if (cmd === 'fix') {
    const paths = cliArgs.slice(1);
    const res = handleToolCall('fix_ui_slop', { paths });
    console.log(res.content[0].text);
    process.exit(res.isError ? 1 : 0);
  } else if (cmd === 'scaffold') {
    const archetypeId = cliArgs[1];
    const targetDir = cliArgs[2] || '.';
    const projectName = cliArgs[3];
    const overwrite = cliArgs.includes('--overwrite');
    const res = handleToolCall('scaffold_design_contract', {
      archetype_id: archetypeId,
      target_dir: targetDir,
      project_name: projectName,
      overwrite
    });
    console.log(res.content[0].text);
    process.exit(res.isError ? 1 : 0);
  } else {
    console.error(`Lệnh CLI không hợp lệ: "${cmd}". Chạy với --help để xem hướng dẫn.`);
    process.exit(1);
  }
}

// -------------------------------------------------------------
// Chế độ MCP Server (JSON-RPC 2.0 qua Stdio)
// -------------------------------------------------------------
const rl = readline.createInterface({
  input: process.stdin,
  output: process.stdout,
  terminal: false
});

function sendResponse(id, result, error = null) {
  const response = { jsonrpc: '2.0', id };
  if (error) {
    response.error = error;
  } else {
    response.result = result;
  }
  process.stdout.write(JSON.stringify(response) + '\n');
}

rl.on('line', (line) => {
  const trimmed = line.trim();
  if (!trimmed) return;

  let request;
  try {
    request = JSON.parse(trimmed);
  } catch (err) {
    sendResponse(null, null, { code: -32700, message: 'Parse error' });
    return;
  }

  const { id, method, params } = request;

  switch (method) {
    case 'initialize':
      sendResponse(id, {
        protocolVersion: '2024-11-05',
        capabilities: {
          tools: {}
        },
        serverInfo: {
          name: 'ui-design',
          version: '1.0.0'
        }
      });
      break;

    case 'notifications/initialized':
      break;

    case 'ping':
      sendResponse(id, {});
      break;

    case 'tools/list':
      sendResponse(id, { tools: TOOLS });
      break;

    case 'tools/call': {
      if (!params || !params.name) {
        sendResponse(id, null, { code: -32602, message: 'Missing tool name' });
        break;
      }
      try {
        const result = handleToolCall(params.name, params.arguments || {});
        sendResponse(id, result);
      } catch (callErr) {
        sendResponse(id, {
          isError: true,
          content: [{ type: 'text', text: `Tool error: ${callErr.message}` }]
        });
      }
      break;
    }

    default:
      if (id !== undefined && id !== null) {
        sendResponse(id, null, { code: -32601, message: `Method not found: ${method}` });
      }
      break;
  }
});

console.error('[UIDesignMCP] Server v1.0.0 initialized.');
