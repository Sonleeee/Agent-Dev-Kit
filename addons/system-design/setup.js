import fs from 'node:fs';
import path from 'node:path';
import os from 'node:os';
import { fileURLToPath } from 'node:url';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

const kitRoot = path.resolve(__dirname, '..', '..');
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

  geminiConfig.mcpServers['system-design'] = {
    command: 'node',
    args: [mcpServerJs]
  };

  fs.writeFileSync(geminiConfigFile, JSON.stringify(geminiConfig, null, 2), 'utf8');
  console.log(`✅ [Antigravity] Đã đăng ký 'system-design' MCP vào: ${geminiConfigFile}`);
} catch (err) {
  console.warn(`[Warning] Không thể ghi file config Antigravity: ${err.message}`);
}

// 2. Sinh Tool Schemas cho Antigravity Lazy Loading (~/.gemini/antigravity/mcp/system-design)
const antigravityMcpDir = path.join(userHome, '.gemini', 'antigravity', 'mcp', 'system-design');
try {
  if (!fs.existsSync(antigravityMcpDir)) {
    fs.mkdirSync(antigravityMcpDir, { recursive: true });
  }

  const tools = [
    {
      name: "search_patterns",
      description: "Tìm kiếm mẫu kiến trúc hệ thống (System Design Patterns) chuẩn từ kho tri thức nội bộ đã được thẩm định. Không cần tra cứu internet.",
      parameters: {
        type: "object",
        properties: {
          query: { type: "string", description: "Từ khóa tìm kiếm (ví dụ: 'outbox', 'idempotency', 'circuit breaker', 'cache stampede')" },
          category: { type: "string", description: "Phân loại tùy chọn" }
        },
        required: ["query"]
      }
    },
    {
      name: "get_pattern_details",
      description: "Lấy chi tiết toàn diện của 1 Pattern: Vấn đề thực tế, Sơ đồ luồng (Mermaid), Nguyên tắc & Invariants bắt buộc, Trade-offs và Code mẫu chuẩn.",
      parameters: {
        type: "object",
        properties: {
          pattern_id: { type: "string", description: "ID của pattern (ví dụ: 'transactional-outbox', 'idempotency-key', 'circuit-breaker')" }
        },
        required: ["pattern_id"]
      }
    },
    {
      name: "evaluate_interview",
      description: "Đánh giá kết quả phỏng vấn kiến trúc (12 trụ cột), tính điểm độ phức tạp (Complexity Score), tự động lưu trữ Ephemeral Scratchpad (.agents/.cache/scaffold-session.json) chống trôi context và sinh sẵn tài liệu ADR-001.md.",
      parameters: {
        type: "object",
        properties: {
          answers: {
            type: "object",
            description: "Các lựa chọn của dev: { scale, consistency, background_jobs, protocols }"
          },
          project_dir: { type: "string", description: "Thư mục dự án mục tiêu" },
          project_name: { type: "string", description: "Tên dự án" }
        },
        required: ["answers"]
      }
    },
    {
      name: "list_architectures",
      description: "Liệt kê danh sách các bộ khung kiến trúc source base chuẩn (Blueprints) có sẵn để khởi tạo dự án mới.",
      parameters: {
        type: "object",
        properties: {}
      }
    },
    {
      name: "scaffold_project",
      description: "Tự động giải nén và dựng toàn bộ cây thư mục source base chuẩn cho dự án mới ra đĩa (Clean Architecture, Docker, config, entities, use cases, ADRs). Chuẩn xác 100% không lo lỗi syntax.",
      parameters: {
        type: "object",
        properties: {
          architecture_id: { type: "string", description: "ID kiến trúc: 'clean-arch-ts' hoặc 'clean-arch-fastapi'" },
          target_dir: { type: "string", description: "Đường dẫn thư mục đích muốn tạo source code" },
          project_name: { type: "string", description: "Tên dự án" }
        },
        required: ["architecture_id", "target_dir", "project_name"]
      }
    },
    {
      name: "inject_pattern",
      description: "Nhúng trực tiếp mã nguồn của 1 pattern (ví dụ: outbox worker, idempotency middleware) vào dự án hiện tại.",
      parameters: {
        type: "object",
        properties: {
          pattern_id: { type: "string", description: "ID của pattern cần nhúng" },
          target_dir: { type: "string", description: "Thư mục dự án đang phát triển" }
        },
        required: ["pattern_id", "target_dir"]
      }
    },
    {
      name: "recommend_architecture",
      description: "Tư vấn lựa chọn kiến trúc tối ưu dựa trên quy mô người dùng (CCU), số lượng kỹ sư và yêu cầu nghiệp vụ để chống over-engineering.",
      parameters: {
        type: "object",
        properties: {
          estimated_ccu: { type: "number", description: "Lượng người dùng đồng thời ước tính" },
          team_size: { type: "number", description: "Số lượng dev tham gia dự án" },
          business_type: { type: "string", description: "Loại hình dự án" }
        },
        required: ["estimated_ccu", "team_size"]
      }
    }
  ];

  for (const tool of tools) {
    const targetFile = path.join(antigravityMcpDir, `${tool.name}.json`);
    fs.writeFileSync(targetFile, JSON.stringify(tool, null, 2), 'utf8');
  }

  const instructions = `# System Design MCP Server Instructions
Sử dụng server này khi:
1. Cần tra cứu kiến trúc hệ thống, patterns (outbox, idempotency, circuit breaker, caching) thay vì tìm kiếm ngoài internet.
2. Cần dựng khung source base mới (scaffold_project) theo chuẩn Clean Architecture (TypeScript hoặc Python).
3. Cần nhúng pattern mẫu vào codebase hiện tại (inject_pattern).
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
    claudeConfig.mcpServers['system-design'] = {
      command: 'node',
      args: [mcpServerJs]
    };
    fs.writeFileSync(claudeConfigFile, JSON.stringify(claudeConfig, null, 2), 'utf8');
    console.log(`✅ [Claude Code] Đã đăng ký 'system-design' MCP vào: ${claudeConfigFile}`);
  }
} catch (err) {
  // Bỏ qua nếu Claude không có
}

console.log('🎉 Hoàn tất cấu hình System Design MCP Server cho Agent-Dev-Kit!');
