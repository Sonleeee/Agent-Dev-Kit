export const tool = {
  name: 'search_design_archetypes',
  description:
    'Tìm kiếm và xếp hạng Design Archetypes theo từ khóa, lĩnh vực (domain) và khoảng cách Euclid với bộ 3 thông số Dials (variance, motion, density 1-10).',
  inputSchema: {
    type: 'object',
    properties: {
      query: {
        type: 'string',
        description:
          'Từ khóa tìm kiếm (ví dụ: "dark", "fintech", "editorial", "brutalist", "mobile", "enterprise")'
      },
      domain: {
        type: 'string',
        description: 'Lĩnh vực ứng dụng (ví dụ: "saas", "fintech", "erp", "publishing", "consumer-app")'
      },
      dials: {
        type: 'object',
        description:
          'Bộ 3 thông số điều khiển thiết kế từ 1 đến 10: { variance?: number, motion?: number, density?: number }',
        properties: {
          variance: { type: 'number' },
          motion: { type: 'number' },
          density: { type: 'number' }
        }
      }
    }
  },
  execute(args, ctx) {
    const { archetypesDb } = ctx;
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
      const matchesDomain = !dom || a.domains.some((d) => d.toLowerCase().includes(dom));
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
};
