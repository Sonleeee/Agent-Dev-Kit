import fs from 'node:fs';
import path from 'node:path';
import os from 'node:os';
import { fileURLToPath } from 'node:url';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

const mcpServerJs = path.join(__dirname, 'mcp-server', 'index.js');

if (!fs.existsSync(mcpServerJs)) {
  console.error(`[Error] Không tìm thấy MCP server entrypoint: ${mcpServerJs}`);
  process.exit(1);
}

const userHome = os.homedir();

// 1. Cấu hình cho Antigravity (~/.gemini/config/mcp_config.json)
const geminiConfigDir = path.join(userHome, '.gemini', 'config');
const geminiConfigFile = path.join(geminiConfigDir, 'mcp_config.json');

try {
  if (!fs.existsSync(geminiConfigDir)) {
    fs.mkdirSync(geminiConfigDir, { recursive: true });
  }

  let geminiConfig = { mcpServers: {} };
  if (fs.existsSync(geminiConfigFile)) {
    try {
      geminiConfig = JSON.parse(fs.readFileSync(geminiConfigFile, 'utf8'));
      if (!geminiConfig.mcpServers) geminiConfig.mcpServers = {};
    } catch (e) {
      geminiConfig = { mcpServers: {} };
    }
  }

  geminiConfig.mcpServers['ui-design'] = {
    command: 'node',
    args: [mcpServerJs]
  };

  fs.writeFileSync(geminiConfigFile, JSON.stringify(geminiConfig, null, 2), 'utf8');
  console.log(`✅ [Antigravity] Đã đăng ký 'ui-design' MCP vào: ${geminiConfigFile}`);
} catch (err) {
  console.warn(`[Warning] Không thể ghi file config Antigravity: ${err.message}`);
}

// 2. Sinh Tool Schemas cho Antigravity Lazy Loading (~/.gemini/antigravity/mcp/ui-design)
const antigravityMcpDir = path.join(userHome, '.gemini', 'antigravity', 'mcp', 'ui-design');
try {
  if (!fs.existsSync(antigravityMcpDir)) {
    fs.mkdirSync(antigravityMcpDir, { recursive: true });
  }

  const tools = [
    {
      name: 'search_design_archetypes',
      description: 'Tìm kiếm và xếp hạng Design Archetypes theo từ khóa, lĩnh vực (domain) và khoảng cách Euclid với bộ 3 thông số Dials (variance, motion, density 1-10).',
      parameters: {
        type: 'object',
        properties: {
          query: { type: 'string', description: 'Từ khóa tìm kiếm (ví dụ: "dark", "fintech", "editorial", "brutalist", "mobile")' },
          domain: { type: 'string', description: 'Lĩnh vực ứng dụng (ví dụ: "saas", "fintech", "erp", "publishing")' },
          dials: {
            type: 'object',
            description: 'Bộ 3 thông số điều khiển thiết kế từ 1 đến 10: { variance, motion, density }'
          }
        }
      }
    },
    {
      name: 'get_design_tokens',
      description: 'Biên dịch động bộ Design Tokens của một Archetype ra định dạng chuẩn: Google Labs DESIGN.md ("design-md"), Tailwind v4 @theme ("tailwind-v4"), CSS Variables ("css-vars"), hoặc W3C DTCG JSON ("dtcg-json").',
      parameters: {
        type: 'object',
        properties: {
          archetype_id: { type: 'string', description: 'ID của archetype (ví dụ: "linear-precision-dark", "stripe-fintech-clarity")' },
          format: { type: 'string', description: 'Định dạng xuất: "design-md" | "tailwind-v4" | "css-vars" | "dtcg-json"' }
        },
        required: ['archetype_id']
      }
    },
    {
      name: 'get_component_blueprint',
      description: 'Lấy đặc tả Component Blueprint kết hợp với công thức chuyển động vật lý (Motion Recipe), quy tắc Mobile Native, bộ dữ liệu phá thử giao diện (break-ui payloads) và code mẫu sạch 100% anti-slop.',
      parameters: {
        type: 'object',
        properties: {
          component_id: { type: 'string', description: 'ID của component: "data-table", "modal-dialog", "drawer-sheet", "command-palette", "form-control", "status-badge", "bento-grid"' }
        },
        required: ['component_id']
      }
    },
    {
      name: 'verify_color_contrast',
      description: 'Tính toán chính xác tỷ lệ tương phản màu sắc theo công thức toán học WCAG 2.2 Relative Luminance, kiểm tra PASS/FAIL cho AA/AAA và tự động đề xuất mã màu foreground đạt chuẩn nếu FAIL.',
      parameters: {
        type: 'object',
        properties: {
          foreground_hex: { type: 'string', description: 'Mã màu chữ/icon (#RRGGBB)' },
          background_hex: { type: 'string', description: 'Mã màu nền (#RRGGBB)' },
          level: { type: 'string', description: 'Mức chuẩn WCAG: "AA" hoặc "AAA"' }
        },
        required: ['foreground_hex', 'background_hex']
      }
    },
    {
      name: 'audit_ui_code',
      description: 'Quét mã nguồn UI (React/Tailwind/CSS/HTML) bằng trình kiểm toán Anti-Slop để chấm điểm Impeccable 20/20 và phát hiện các lỗi vi phạm thẩm mỹ, a11y, mobile viewport.',
      parameters: {
        type: 'object',
        properties: {
          paths: { type: 'array', items: { type: 'string' }, description: 'Danh sách đường dẫn file hoặc thư mục cần kiểm tra' },
          strict: { type: 'boolean', description: 'Bật chế độ kiểm tra nghiêm ngặt' }
        },
        required: ['paths']
      }
    },
    {
      name: 'fix_ui_slop',
      description: 'Tự động sửa các lỗi UI Anti-Slop tĩnh (như transition-all, 100vh, thiếu focus-visible ring, scale-0) trên các đường dẫn chỉ định.',
      parameters: {
        type: 'object',
        properties: {
          paths: { type: 'array', items: { type: 'string' }, description: 'Danh sách đường dẫn file hoặc thư mục cần sửa lỗi' }
        },
        required: ['paths']
      }
    },
    {
      name: 'scaffold_design_contract',
      description: 'Sinh file hợp đồng thiết kế DESIGN.md chuẩn vào thư mục dự án (target_dir/DESIGN.md). Mặc định bảo vệ an toàn không ghi đè nếu file đã tồn tại (overwrite=false).',
      parameters: {
        type: 'object',
        properties: {
          archetype_id: { type: 'string', description: 'ID của archetype muốn khởi tạo' },
          target_dir: { type: 'string', description: 'Thư mục dự án đích' },
          project_name: { type: 'string', description: 'Tên dự án tùy chọn' },
          overwrite: { type: 'boolean', description: 'Cho phép ghi đè nếu DESIGN.md đã tồn tại (mặc định: false)' }
        },
        required: ['archetype_id', 'target_dir']
      }
    }
  ];

  for (const tool of tools) {
    const targetFile = path.join(antigravityMcpDir, `${tool.name}.json`);
    fs.writeFileSync(targetFile, JSON.stringify(tool, null, 2), 'utf8');
  }

  const instructions = `# UI Design MCP Server Instructions
Sử dụng các tool trong \`ui-design\` khi thiết kế giao diện, chọn bảng màu/token, kiểm tra tương phản WCAG 2.2 hoặc kiểm toán mã nguồn UI chống AI Slop:
- \`search_design_archetypes\` & \`get_design_tokens\`: Tra cứu archetype và xuất token (\`design-md\`, \`tailwind-v4\`, \`css-vars\`, \`dtcg-json\`).
- \`get_component_blueprint\`: Lấy đặc tả component, công thức chuyển động vật lý (Emil Kowalski) và bộ test \`break-ui\`.
- \`verify_color_contrast\`: Kiểm tra toán học độ tương phản màu WCAG 2.2 trước khi chốt màu chữ/nền.
- \`audit_ui_code\` & \`fix_ui_slop\`: Quét và sửa lỗi Anti-Slop trên code thực tế.
- Chỉ gọi \`scaffold_design_contract\` khi cần tạo mới \`DESIGN.md\` trong thư mục dự án.
`;
  fs.writeFileSync(path.join(antigravityMcpDir, 'instructions.md'), instructions, 'utf8');
  console.log(`✅ [Antigravity] Đã sinh tool schemas vào: ${antigravityMcpDir}`);
} catch (err) {
  console.warn(`[Warning] Không thể sinh Antigravity tool schemas: ${err.message}`);
}

// 3. Cấu hình cho Claude Code / Claude Desktop (~/.claude.json nếu có)
const claudeConfigFile = path.join(userHome, '.claude.json');
try {
  if (fs.existsSync(claudeConfigFile)) {
    const claudeRaw = fs.readFileSync(claudeConfigFile, 'utf8');
    const claudeConfig = JSON.parse(claudeRaw || '{}');
    if (!claudeConfig.mcpServers) claudeConfig.mcpServers = {};
    claudeConfig.mcpServers['ui-design'] = {
      command: 'node',
      args: [mcpServerJs]
    };
    fs.writeFileSync(claudeConfigFile, JSON.stringify(claudeConfig, null, 2), 'utf8');
    console.log(`✅ [Claude Code] Đã đăng ký 'ui-design' MCP vào: ${claudeConfigFile}`);
  }
} catch (err) {
  // Bỏ qua nếu Claude không có
}

console.log('🎉 Hoàn tất cấu hình UI Design MCP Server cho Agent-Dev-Kit!');
