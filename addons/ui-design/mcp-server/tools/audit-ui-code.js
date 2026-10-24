import { invokePythonOrFallbackAuditor } from '../services/slop-auditor.js';

export const tool = {
  name: 'audit_ui_code',
  description:
    'Quét mã nguồn UI (React/Tailwind/CSS/HTML) bằng trình kiểm toán Anti-Slop để chấm điểm Impeccable 20/20 và phát hiện các lỗi vi phạm thẩm mỹ, a11y, mobile viewport.',
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
  },
  execute(args, ctx) {
    const paths = Array.isArray(args.paths) && args.paths.length > 0 ? args.paths : ['.'];
    const report = invokePythonOrFallbackAuditor(
      paths,
      {
        strict: Boolean(args.strict),
        fix: false
      },
      ctx.kitRoot
    );
    return {
      content: [{ type: 'text', text: JSON.stringify(report, null, 2) }]
    };
  }
};
