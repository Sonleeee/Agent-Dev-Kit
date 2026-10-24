export const tool = {
  name: 'search_patterns',
  description:
    'Tìm kiếm mẫu kiến trúc hệ thống (System Design Patterns) chuẩn từ kho tri thức nội bộ đã được thẩm định. Không cần tra cứu internet.',
  inputSchema: {
    type: 'object',
    properties: {
      query: {
        type: 'string',
        description:
          'Từ khóa tìm kiếm (ví dụ: "outbox", "trùng đơn hàng", "idempotency", "cache stampede", "circuit breaker", "pessimistic lock")'
      },
      category: {
        type: 'string',
        description:
          'Phân loại tùy chọn: "data-consistency", "reliability", "caching", "traffic-control", "background-processing", "security-and-api"'
      }
    },
    required: ['query']
  },
  execute(args, ctx) {
    const { patternsDb } = ctx;
    const q = (args.query || '').toLowerCase().trim();
    const cat = (args.category || '').toLowerCase().trim();
    const matched = patternsDb.filter((p) => {
      const matchesQuery =
        p.id.toLowerCase().includes(q) ||
        p.name.toLowerCase().includes(q) ||
        p.summary.toLowerCase().includes(q) ||
        p.tags.some((t) => t.toLowerCase().includes(q));
      const matchesCategory = !cat || p.category.toLowerCase() === cat;
      return matchesQuery && matchesCategory;
    });

    if (matched.length === 0) {
      return {
        content: [
          {
            type: 'text',
            text: `Không tìm thấy pattern nào khớp với từ khóa "${args.query}".\nCác pattern có sẵn: ${patternsDb.map((p) => p.id).join(', ')}`
          }
        ]
      };
    }

    const results = matched
      .map(
        (p) =>
          `### 📌 [${p.id}] ${p.name}\n- **Phân loại**: \`${p.category}\`\n- **Tóm tắt**: ${p.summary}\n- **Tags**: ${p.tags.join(', ')}`
      )
      .join('\n\n');
    return {
      content: [
        {
          type: 'text',
          text: `Tìm thấy ${matched.length} mẫu kiến trúc phù hợp:\n\n${results}\n\n👉 Gọi tool 'get_pattern_details' với pattern_id để xem chi tiết sơ đồ luồng & code mẫu.`
        }
      ]
    };
  }
};
