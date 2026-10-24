import fs from 'node:fs';
import path from 'node:path';

export const tool = {
  name: 'inject_pattern',
  description:
    'Ghi code pattern vào target_dir/src/patterns/<pattern>.<ext>. Mặc định không ghi đè file cùng tên nếu đã tồn tại (overwrite=false).',
  inputSchema: {
    type: 'object',
    properties: {
      pattern_id: {
        type: 'string',
        description: 'ID của pattern cần nhúng'
      },
      target_dir: {
        type: 'string',
        description: 'Thư mục dự án đang phát triển'
      },
      overwrite: {
        type: 'boolean',
        description: 'Cho phép ghi đè file pattern đã tồn tại hay không (mặc định: false)'
      }
    },
    required: ['pattern_id', 'target_dir']
  },
  execute(args, ctx) {
    const { patternsDb } = ctx;
    const p = patternsDb.find(
      (item) => item.id.toLowerCase() === args.pattern_id.toLowerCase().trim()
    );
    if (!p) {
      return {
        isError: true,
        content: [
          {
            type: 'text',
            text: `Không tìm thấy pattern "${args.pattern_id}" để nhúng.`
          }
        ]
      };
    }

    const targetPath = path.resolve(args.target_dir);
    const allowOverwrite = args.overwrite === true;
    const patternsDir = path.join(targetPath, 'src', 'patterns');
    if (!fs.existsSync(patternsDir)) {
      fs.mkdirSync(patternsDir, { recursive: true });
    }

    const ext =
      p.code_snippet?.language === 'typescript'
        ? 'ts'
        : p.code_snippet?.language === 'lua'
          ? 'lua'
          : 'js';
    const filename = `${p.id}.${ext}`;
    const fullPath = path.join(patternsDir, filename);
    if (fs.existsSync(fullPath) && !allowOverwrite) {
      return {
        isError: true,
        content: [
          {
            type: 'text',
            text: `⚠️ Chặn ghi đè an toàn: File \`${path.join('src', 'patterns', filename)}\` đã tồn tại. Truyền \`overwrite: true\` nếu bạn thực sự muốn ghi đè.`
          }
        ]
      };
    }
    fs.writeFileSync(fullPath, p.code_snippet?.code || '', 'utf8');

    return {
      content: [
        {
          type: 'text',
          text: `✅ Đã nhúng pattern **${p.name}** vào thư mục dự án:\n📄 File: \`${path.join('src', 'patterns', filename)}\`\n\nBạn có thể import và sử dụng trực tiếp trong mã nguồn.`
        }
      ]
    };
  }
};
