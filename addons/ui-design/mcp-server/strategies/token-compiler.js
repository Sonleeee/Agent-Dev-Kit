/**
 * Token Compiler Strategy Pattern
 * Encapsulates formatting logic for DESIGN.md, Tailwind v4 @theme,
 * CSS Variables and W3C DTCG JSON tokens.
 */

export function tailwindV4Strategy(archetype) {
  const c = archetype.colors;
  const t = archetype.typography;
  const r = archetype.radius;

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

export function cssVarsStrategy(archetype) {
  const c = archetype.colors;
  const t = archetype.typography;
  const r = archetype.radius;

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

export function dtcgJsonStrategy(archetype) {
  const c = archetype.colors;
  const t = archetype.typography;
  const r = archetype.radius;

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

export function designMdStrategy(archetype, projectName = null) {
  const c = archetype.colors;
  const t = archetype.typography;
  const r = archetype.radius;
  const titleName = projectName ? `${projectName} (${archetype.name})` : archetype.name;

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

const STRATEGIES = {
  'tailwind-v4': (archetype) => tailwindV4Strategy(archetype),
  'css-vars': (archetype) => cssVarsStrategy(archetype),
  'dtcg-json': (archetype) => dtcgJsonStrategy(archetype),
  'design-md': (archetype, projectName) => designMdStrategy(archetype, projectName)
};

export function compileDesignTokens(archetype, format = 'design-md', projectName = null) {
  const fmt = (format || 'design-md').toLowerCase().trim();
  const strategy = STRATEGIES[fmt] || STRATEGIES['design-md'];
  return strategy(archetype, projectName);
}
