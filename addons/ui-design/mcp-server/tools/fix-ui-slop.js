import { invokePythonOrFallbackAuditor } from '../services/slop-auditor.js';

export const tool = {
  name: 'fix_ui_slop',
  description:
    'Tự động sửa các lỗi UI Anti-Slop tĩnh (như transition-all, 100vh, thiếu focus-visible ring, scale-0) trên các đường dẫn chỉ định.',
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
  },
  execute(args, ctx) {
    const paths = Array.isArray(args.paths) && args.paths.length > 0 ? args.paths : ['.'];
    const report = invokePythonOrFallbackAuditor(
      paths,
      {
        strict: false,
        fix: true
      },
      ctx.kitRoot
    );
    return {
      content: [{ type: 'text', text: JSON.stringify(report, null, 2) }]
    };
  }
};
