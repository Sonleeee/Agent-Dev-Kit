import { compileDesignTokens } from '../strategies/token-compiler.js';

export const tool = {
  name: 'get_design_tokens',
  description:
    'Biên dịch động bộ Design Tokens của một Archetype ra định dạng chuẩn: Google Labs DESIGN.md ("design-md"), Tailwind v4 @theme ("tailwind-v4"), CSS Variables ("css-vars"), hoặc W3C DTCG JSON ("dtcg-json").',
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
  },
  execute(args, ctx) {
    const { archetypesDb } = ctx;
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
};
