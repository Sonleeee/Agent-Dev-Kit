import fs from 'node:fs';
import path from 'node:path';
import { compileDesignTokens } from '../strategies/token-compiler.js';

export const tool = {
  name: 'scaffold_design_contract',
  description:
    'Sinh file hợp đồng thiết kế DESIGN.md chuẩn vào thư mục dự án (target_dir/DESIGN.md). Mặc định bảo vệ an toàn không ghi đè nếu file đã tồn tại (overwrite=false).',
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
};
