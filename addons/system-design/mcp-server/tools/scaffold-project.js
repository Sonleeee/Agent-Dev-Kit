import fs from 'node:fs';
import path from 'node:path';
import { loadSessionState, clearSessionState } from '../services/session-manager.js';

export const tool = {
  name: 'scaffold_project',
  description:
    'Ghi source base từ blueprint vào target_dir. Mặc định không ghi đè file đã tồn tại (overwrite=false). Chỉ gọi khi người dùng yêu cầu tạo source base.',
  inputSchema: {
    type: 'object',
    properties: {
      architecture_id: {
        type: 'string',
        description:
          'ID kiến trúc: "clean-arch-ts" (TypeScript/Node.js) hoặc "clean-arch-fastapi" (Python/FastAPI)'
      },
      target_dir: {
        type: 'string',
        description: 'Đường dẫn thư mục đích muốn tạo source code'
      },
      project_name: {
        type: 'string',
        description: 'Tên dự án'
      },
      overwrite: {
        type: 'boolean',
        description: 'Cho phép ghi đè file đã tồn tại hay không (mặc định: false)'
      }
    },
    required: ['architecture_id', 'target_dir', 'project_name']
  },
  execute(args, ctx) {
    const { blueprintsDb, patternsDb } = ctx;
    const bp = blueprintsDb.find(
      (b) => b.id.toLowerCase() === args.architecture_id.toLowerCase().trim()
    );
    if (!bp) {
      return {
        isError: true,
        content: [
          {
            type: 'text',
            text: `Lỗi: Không tìm thấy kiến trúc "${args.architecture_id}". Danh sách khả dụng: ${blueprintsDb.map((b) => b.id).join(', ')}`
          }
        ]
      };
    }

    const targetPath = path.resolve(args.target_dir);
    const projName = args.project_name || path.basename(targetPath);
    const allowOverwrite = args.overwrite === true;

    if (!fs.existsSync(targetPath)) {
      fs.mkdirSync(targetPath, { recursive: true });
    }

    const session = loadSessionState(targetPath);
    let adrCustomContent = null;
    let features = {};

    if (session && session.data) {
      adrCustomContent = session.data.adr_content;
      features = session.data.features || {};
    }

    let createdFiles = [];
    let skippedFiles = [];
    for (const [relPath, contentTemplate] of Object.entries(bp.files)) {
      const fullFilePath = path.join(targetPath, relPath);
      if (fs.existsSync(fullFilePath) && !allowOverwrite) {
        skippedFiles.push(relPath);
        continue;
      }
      const dir = path.dirname(fullFilePath);
      if (!fs.existsSync(dir)) {
        fs.mkdirSync(dir, { recursive: true });
      }
      let finalContent = contentTemplate.replace(/\{\{PROJECT_NAME\}\}/g, projName);

      if (relPath.includes('ADR-001') && adrCustomContent) {
        finalContent = adrCustomContent;
      }

      fs.writeFileSync(fullFilePath, finalContent, 'utf8');
      createdFiles.push(relPath);
    }

    if (features.hasHmacWebhook) {
      const hmacRel = 'src/interfaces/http/middlewares/hmac-verify.middleware.ts';
      const hmacPath = path.join(targetPath, hmacRel);
      if (fs.existsSync(hmacPath) && !allowOverwrite) {
        skippedFiles.push(hmacRel);
      } else {
        const hmacDir = path.dirname(hmacPath);
        if (!fs.existsSync(hmacDir)) fs.mkdirSync(hmacDir, { recursive: true });
        const hmacSnippet = patternsDb.find((p) => p.id === 'hmac-webhook-verification')?.code_snippet?.code;
        if (hmacSnippet) {
          fs.writeFileSync(hmacPath, hmacSnippet, 'utf8');
          createdFiles.push(hmacRel);
        }
      }
    }

    if (features.hasDbQueue) {
      const queueRel = 'src/infrastructure/jobs/db-queue.worker.ts';
      const queuePath = path.join(targetPath, queueRel);
      if (fs.existsSync(queuePath) && !allowOverwrite) {
        skippedFiles.push(queueRel);
      } else {
        const queueDir = path.dirname(queuePath);
        if (!fs.existsSync(queueDir)) fs.mkdirSync(queueDir, { recursive: true });
        const queueSnippet = patternsDb.find((p) => p.id === 'db-backed-queue')?.code_snippet?.code;
        if (queueSnippet) {
          fs.writeFileSync(queuePath, queueSnippet, 'utf8');
          createdFiles.push(queueRel);
        }
      }
    }

    clearSessionState(targetPath);

    const skippedNotice =
      skippedFiles.length > 0
        ? `\n⚠️ **Số file đã bỏ qua do trùng tên (overwrite=false):** ${skippedFiles.length} (${skippedFiles.map((f) => `\`${f}\``).join(', ')})`
        : '';

    return {
      content: [
        {
          type: 'text',
          text: `✅ **Khởi tạo thành công Source Base [${bp.name}]!**\n\n📁 **Thư mục:** \`${targetPath}\`\n🚀 **Số file đã sinh:** ${createdFiles.length}${skippedNotice}\n🧹 **Trạng thái:** Đã tự động dọn dẹp sạch sẽ Ephemeral Scratchpad (0% context pollution).\n\n**Danh sách file đã tạo:**\n${createdFiles.map((f) => `- \`${f}\``).join('\n') || '- (Không có file mới)'}\n\n👉 Giờ bạn chỉ cần cd vào thư mục và bắt đầu phát triển tính năng!`
        }
      ]
    };
  }
};
