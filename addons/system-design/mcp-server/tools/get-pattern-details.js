export const tool = {
  name: 'get_pattern_details',
  description:
    'Lấy chi tiết toàn diện của 1 Pattern: Vấn đề thực tế, Sơ đồ luồng (Mermaid), Nguyên tắc & Invariants bắt buộc, Trade-offs và Code mẫu chuẩn.',
  inputSchema: {
    type: 'object',
    properties: {
      pattern_id: {
        type: 'string',
        description:
          'ID của pattern (ví dụ: "transactional-outbox", "idempotency-key", "db-backed-queue", "hmac-webhook-verification", "pessimistic-locking")'
      }
    },
    required: ['pattern_id']
  },
  execute(args, ctx) {
    const { patternsDb } = ctx;
    const id = (args.pattern_id || '').toLowerCase().trim();
    const p = patternsDb.find((item) => item.id.toLowerCase() === id);
    if (!p) {
      return {
        isError: true,
        content: [
          {
            type: 'text',
            text: `Lỗi: Không tìm thấy pattern có ID "${args.pattern_id}". Danh sách khả dụng: ${patternsDb.map((x) => x.id).join(', ')}`
          }
        ]
      };
    }

    let details = `# 🏗️ ${p.name} (\`${p.id}\`)\n\n`;
    details += `> **Phân loại:** \`${p.category}\` | **Tags:** ${p.tags.join(', ')}\n\n`;
    details += `## 1. Bản chất & Tóm tắt\n${p.summary}\n\n`;
    details += `## 2. Bài toán thực tế (Problem)\n${p.problem}\n\n`;
    details += `## 3. Giải pháp kỹ thuật (Solution)\n${p.solution}\n\n`;
    details += `## 4. Sơ đồ kiến trúc (Mermaid)\n\`\`\`mermaid\n${p.mermaid}\n\`\`\`\n\n`;
    details += `## 5. Các nguyên tắc bất biến (Invariants & Rules)\n${p.rules_and_invariants.map((r) => `* ${r}`).join('\n')}\n\n`;
    details += `## 6. Trade-offs\n- **Ưu điểm**: ${p.trade_offs.pros.join(', ')}\n- **Nhược điểm & Chi phí**: ${p.trade_offs.cons.join(', ')}\n\n`;
    if (p.code_snippet) {
      details += `## 7. Code mẫu chuẩn (${p.code_snippet.title})\n\`\`\`${p.code_snippet.language}\n${p.code_snippet.code}\n\`\`\``;
    }

    return {
      content: [{ type: 'text', text: details }]
    };
  }
};
