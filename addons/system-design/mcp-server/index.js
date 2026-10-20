#!/usr/bin/env node
import fs from 'node:fs';
import path from 'node:path';
import readline from 'node:readline';
import { fileURLToPath } from 'node:url';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

// Tải cơ sở tri thức patterns & blueprints
const patternsPath = path.join(__dirname, 'data', 'patterns.json');
const blueprintsPath = path.join(__dirname, 'data', 'blueprints.json');

let patternsDb = [];
let blueprintsDb = [];

try {
  patternsDb = JSON.parse(fs.readFileSync(patternsPath, 'utf8')).patterns || [];
} catch (e) {
  console.error('[SystemDesignMCP] Warning: Unable to load patterns.json:', e.message);
}

try {
  blueprintsDb = JSON.parse(fs.readFileSync(blueprintsPath, 'utf8')).blueprints || [];
} catch (e) {
  console.error('[SystemDesignMCP] Warning: Unable to load blueprints.json:', e.message);
}

// -------------------------------------------------------------
// Quản lý Ephemeral Session Scratchpad (Chống trôi Context & Hallucination)
// -------------------------------------------------------------
const CACHE_DIR_NAME = path.join('.agents', '.cache');
const SESSION_FILE_NAME = 'scaffold-session.json';

function saveSessionState(targetDir, state) {
  const cacheDir = path.join(targetDir, CACHE_DIR_NAME);
  if (!fs.existsSync(cacheDir)) {
    fs.mkdirSync(cacheDir, { recursive: true });
  }
  const filePath = path.join(cacheDir, SESSION_FILE_NAME);
  fs.writeFileSync(filePath, JSON.stringify(state, null, 2), 'utf8');
  return filePath;
}

function loadSessionState(targetDir) {
  const possiblePaths = [
    path.join(targetDir, CACHE_DIR_NAME, SESSION_FILE_NAME),
    path.join(process.cwd(), CACHE_DIR_NAME, SESSION_FILE_NAME)
  ];
  for (const p of possiblePaths) {
    if (fs.existsSync(p)) {
      try {
        return { data: JSON.parse(fs.readFileSync(p, 'utf8')), path: p };
      } catch (e) {}
    }
  }
  return null;
}

function clearSessionState(targetDir) {
  const session = loadSessionState(targetDir);
  if (session && fs.existsSync(session.path)) {
    try {
      fs.unlinkSync(session.path);
      console.error('[SystemDesignMCP] Ephemeral session scratchpad automatically wiped:', session.path);
    } catch (e) {}
  }
}

// -------------------------------------------------------------
// Khai báo danh mục MCP Tools
// -------------------------------------------------------------
const TOOLS = [
  {
    name: 'search_patterns',
    description: 'Tìm kiếm mẫu kiến trúc hệ thống (System Design Patterns) chuẩn từ kho tri thức nội bộ đã được thẩm định. Không cần tra cứu internet.',
    inputSchema: {
      type: 'object',
      properties: {
        query: {
          type: 'string',
          description: 'Từ khóa tìm kiếm (ví dụ: "outbox", "trùng đơn hàng", "idempotency", "cache stampede", "circuit breaker", "pessimistic lock")'
        },
        category: {
          type: 'string',
          description: 'Phân loại tùy chọn: "data-consistency", "reliability", "caching", "traffic-control", "background-processing", "security-and-api"'
        }
      },
      required: ['query']
    }
  },
  {
    name: 'get_pattern_details',
    description: 'Lấy chi tiết toàn diện của 1 Pattern: Vấn đề thực tế, Sơ đồ luồng (Mermaid), Nguyên tắc & Invariants bắt buộc, Trade-offs và Code mẫu chuẩn.',
    inputSchema: {
      type: 'object',
      properties: {
        pattern_id: {
          type: 'string',
          description: 'ID của pattern (ví dụ: "transactional-outbox", "idempotency-key", "db-backed-queue", "hmac-webhook-verification", "pessimistic-locking")'
        }
      },
      required: ['pattern_id']
    }
  },
  {
    name: 'evaluate_interview',
    description: 'Đánh giá kết quả phỏng vấn kiến trúc (12 trụ cột), tính điểm độ phức tạp (Complexity Score), tự động lưu trữ Ephemeral Scratchpad (.agents/.cache/scaffold-session.json) chống trôi context và sinh sẵn tài liệu ADR-001.md.',
    inputSchema: {
      type: 'object',
      properties: {
        answers: {
          type: 'object',
          description: 'Các lựa chọn của dev: { scale: "A"|"B"|"C", consistency: "A"|"B", background_jobs: "A"|"B"|"C", protocols: ["1","2","3"] }'
        },
        project_dir: {
          type: 'string',
          description: 'Thư mục dự án mục tiêu (mặc định là thư mục hiện tại)'
        },
        project_name: {
          type: 'string',
          description: 'Tên dự án'
        }
      },
      required: ['answers']
    }
  },
  {
    name: 'list_architectures',
    description: 'Liệt kê danh sách các bộ khung kiến trúc source base chuẩn (Blueprints) có sẵn để khởi tạo dự án mới.',
    inputSchema: {
      type: 'object',
      properties: {}
    }
  },
  {
    name: 'scaffold_project',
    description: 'Tự động giải nén và dựng toàn bộ cây thư mục source base chuẩn ra đĩa (Clean Architecture, Docker, config, entities, use cases, ADRs). Tự động nạp cấu hình từ Ephemeral Scratchpad nếu có và dọn sạch cache sau khi hoàn tất.',
    inputSchema: {
      type: 'object',
      properties: {
        architecture_id: {
          type: 'string',
          description: 'ID kiến trúc: "clean-arch-ts" (TypeScript/Node.js) hoặc "clean-arch-fastapi" (Python/FastAPI)'
        },
        target_dir: {
          type: 'string',
          description: 'Đường dẫn thư mục đích muốn tạo source code'
        },
        project_name: {
          type: 'string',
          description: 'Tên dự án'
        }
      },
      required: ['architecture_id', 'target_dir', 'project_name']
    }
  },
  {
    name: 'inject_pattern',
    description: 'Nhúng trực tiếp mã nguồn của 1 pattern (ví dụ: outbox worker, idempotency middleware, db queue) vào dự án hiện tại.',
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
        }
      },
      required: ['pattern_id', 'target_dir']
    }
  },
  {
    name: 'recommend_architecture',
    description: 'Tư vấn lựa chọn kiến trúc tối ưu dựa trên quy mô người dùng, số lượng kỹ sư và yêu cầu nghiệp vụ để chống over-engineering.',
    inputSchema: {
      type: 'object',
      properties: {
        estimated_ccu: {
          type: 'number',
          description: 'Lượng người dùng đồng thời ước tính'
        },
        team_size: {
          type: 'number',
          description: 'Số lượng dev tham gia dự án'
        },
        business_type: {
          type: 'string',
          description: 'Loại hình dự án: "ecommerce", "ai-platform", "fintech", "crud-saas"'
        }
      },
      required: ['estimated_ccu', 'team_size']
    }
  }
];

// -------------------------------------------------------------
// Hàm xử lý Tool Calls
// -------------------------------------------------------------
function handleToolCall(name, args) {
  switch (name) {
    case 'search_patterns': {
      const q = (args.query || '').toLowerCase().trim();
      const cat = (args.category || '').toLowerCase().trim();
      const matched = patternsDb.filter(p => {
        const matchesQuery = p.id.toLowerCase().includes(q) ||
          p.name.toLowerCase().includes(q) ||
          p.summary.toLowerCase().includes(q) ||
          p.tags.some(t => t.toLowerCase().includes(q));
        const matchesCategory = !cat || p.category.toLowerCase() === cat;
        return matchesQuery && matchesCategory;
      });

      if (matched.length === 0) {
        return {
          content: [{
            type: 'text',
            text: `Không tìm thấy pattern nào khớp với từ khóa "${args.query}".\nCác pattern có sẵn: ${patternsDb.map(p => p.id).join(', ')}`
          }]
        };
      }

      const results = matched.map(p => `### 📌 [${p.id}] ${p.name}\n- **Phân loại**: \`${p.category}\`\n- **Tóm tắt**: ${p.summary}\n- **Tags**: ${p.tags.join(', ')}`).join('\n\n');
      return {
        content: [{
          type: 'text',
          text: `Tìm thấy ${matched.length} mẫu kiến trúc phù hợp:\n\n${results}\n\n👉 Gọi tool 'get_pattern_details' với pattern_id để xem chi tiết sơ đồ luồng & code mẫu.`
        }]
      };
    }

    case 'get_pattern_details': {
      const id = (args.pattern_id || '').toLowerCase().trim();
      const p = patternsDb.find(item => item.id.toLowerCase() === id);
      if (!p) {
        return {
          isError: true,
          content: [{
            type: 'text',
            text: `Lỗi: Không tìm thấy pattern có ID "${args.pattern_id}". Danh sách khả dụng: ${patternsDb.map(x => x.id).join(', ')}`
          }]
        };
      }

      let details = `# 🏗️ ${p.name} (\`${p.id}\`)\n\n`;
      details += `> **Phân loại:** \`${p.category}\` | **Tags:** ${p.tags.join(', ')}\n\n`;
      details += `## 1. Bản chất & Tóm tắt\n${p.summary}\n\n`;
      details += `## 2. Bài toán thực tế (Problem)\n${p.problem}\n\n`;
      details += `## 3. Giải pháp kỹ thuật (Solution)\n${p.solution}\n\n`;
      details += `## 4. Sơ đồ kiến trúc (Mermaid)\n\`\`\`mermaid\n${p.mermaid}\n\`\`\`\n\n`;
      details += `## 5. Các nguyên tắc bất biến (Invariants & Rules)\n${p.rules_and_invariants.map(r => `* ${r}`).join('\n')}\n\n`;
      details += `## 6. Trade-offs\n- **Ưu điểm**: ${p.trade_offs.pros.join(', ')}\n- **Nhược điểm & Chi phí**: ${p.trade_offs.cons.join(', ')}\n\n`;
      if (p.code_snippet) {
        details += `## 7. Code mẫu chuẩn (${p.code_snippet.title})\n\`\`\`${p.code_snippet.language}\n${p.code_snippet.code}\n\`\`\``;
      }

      return {
        content: [{ type: 'text', text: details }]
      };
    }

    case 'evaluate_interview': {
      const answers = args.answers || {};
      const scale = (answers.scale || 'B').toUpperCase();
      const consistency = (answers.consistency || 'A').toUpperCase();
      const jobs = (answers.background_jobs || 'B').toUpperCase();
      const protocols = Array.isArray(answers.protocols) ? answers.protocols : ['1'];
      const targetDir = args.project_dir ? path.resolve(args.project_dir) : process.cwd();
      const projName = args.project_name || path.basename(targetDir);

      // 1. Tính toán Complexity Score (/10)
      let score = 1.0; // Điểm base Clean Monolith
      if (scale === 'A') score += 0.5;
      else if (scale === 'B') score += 1.0;
      else if (scale === 'C') score += 3.0;

      if (consistency === 'A') score += 1.5; // Strong ACID + Pessimistic Lock
      else score += 0.5;

      if (jobs === 'A') score += 0.0; // In-memory
      else if (jobs === 'B') score += 0.5; // DB Queue
      else if (jobs === 'C') score += 2.0; // Redis Queue

      if (protocols.includes('3')) score += 1.0; // Webhook HMAC
      if (protocols.includes('2')) score += 1.0; // WebSocket

      score = Math.min(10, Math.max(1, score));

      // 2. Feature Flags
      const features = {
        hasPessimisticLock: consistency === 'A',
        hasDbQueue: jobs === 'B',
        hasRedisQueue: jobs === 'C',
        hasHmacWebhook: protocols.includes('3'),
        hasWebSocket: protocols.includes('2'),
        hasIdempotency: consistency === 'A' || protocols.includes('3')
      };

      // 3. Khuyến nghị kiến trúc
      let archId = 'clean-arch-ts';
      let archName = 'Pragmatic Clean Monolith';
      if (scale === 'C' || jobs === 'C') {
        archName = 'High-Scale Event-Driven Service';
      }

      // 4. Tạo nội dung ADR-001 chi tiết cá nhân hóa
      const adrContent = `# ADR-001: Kiến Trúc Lựa Chọn Dựa Trên Khảo Sát Kỹ Thuật

- **Dự án**: ${projName}
- **Trạng thái**: Accepted
- **Ngày lập**: ${new Date().toISOString().split('T')[0]}
- **Độ phức tạp hệ thống**: ${score.toFixed(1)} / 10

## 1. Kết quả khảo sát đầu vào (Interview Inputs)
- **Quy mô người dùng (Scale)**: ${scale === 'A' ? 'Nội bộ / MVP (< 100 users)' : scale === 'B' ? 'Vừa / Khởi nghiệp (1.000 - 10.000 users/ngày)' : 'Lớn / Flash-sale (50.000 - 100.000+ users)'}
- **Tính nhất quán dữ liệu**: ${consistency === 'A' ? 'Chính xác tức thời (Strong Consistency - Tiền tệ / Tồn kho)' : 'Chấp nhận trễ vài giây (Eventual Consistency)'}
- **Tác vụ ngầm**: ${jobs === 'A' ? 'In-Memory (0 đồng hạ tầng)' : jobs === 'B' ? 'PostgreSQL DB-backed Queue (Bền vững, 0 đồng Redis)' : 'Distributed Redis/RabbitMQ'}
- **Giao thức kết nối**: ${protocols.map(p => p === '1' ? 'RESTful JSON' : p === '2' ? 'WebSocket Realtime' : p === '3' ? 'HMAC Webhook Receiver' : p).join(', ')}

## 2. Quyết định kiến trúc cốt lõi
1. **Mô hình mã nguồn**: Áp dụng **Clean Architecture** (Domain -> Application -> Infrastructure -> Interfaces). Ranh giới nghiệp vụ được cô lập tuyệt đối khỏi Web Framework và DB Driver.
2. **Quản lý dữ liệu**: ${features.hasPessimisticLock ? 'Sử dụng PostgreSQL ACID Transactions + `SELECT ... FOR UPDATE` khi trừ tồn kho / số dư để triệt tiêu Race Condition.' : 'Áp dụng Optimistic Lock hoặc Eventual Consistency.'}
3. **Xử lý tác vụ ngầm**: ${features.hasDbQueue ? 'Tạo bảng `background_jobs` với `SELECT ... FOR UPDATE SKIP LOCKED` để worker xử lý ngầm mà không cần tốn tiền cài đặt cụm Redis riêng.' : features.hasRedisQueue ? 'Kết nối Redis Queue (BullMQ).' : 'Xử lý non-blocking trong memory event loop.'}
4. **Bảo mật Webhook & Giao tiếp**: ${features.hasHmacWebhook ? 'Bắt buộc xác thực chữ ký số HMAC SHA-256 bằng `crypto.timingSafeEqual` và kiểm tra `idempotency_key` trước khi cộng tiền / duyệt đơn.' : 'Chuẩn hóa REST API DTOs.'}

## 3. Ranh giới bất biến (Invariants)
- Tầng Domain tuyệt đối không import Express, FastAPI hay bất kỳ thư viện bên ngoài nào.
- Mọi thao tác thay đổi số dư hoặc trừ tồn kho phải nằm trong Transaction.
- Mọi Webhook từ cổng thanh toán phải được verify chữ ký trước khi chạm tới Use Case.
`;

      // 5. Lưu vào Ephemeral Scratchpad
      const sessionState = {
        session_id: `scaffold_${Date.now()}`,
        timestamp: new Date().toISOString(),
        answers,
        complexity_score: score,
        architecture_id: archId,
        features,
        adr_content: adrContent,
        status: 'READY_TO_SCAFFOLD'
      };

      const cachePath = saveSessionState(targetDir, sessionState);

      let summaryText = `### 📊 Đánh giá Kiến Trúc & Độ Phức Tạp: **${score.toFixed(1)} / 10**\n\n`;
      summaryText += `* **Kiến trúc khuyến nghị:** \`${archName}\` (\`${archId}\`)\n`;
      summaryText += `* **Độ phức tạp:** ${score <= 3 ? '🟢 Rất thấp (1 dev gánh mượt)' : score <= 6 ? '🟡 Vừa phải (Thực dụng, 1-2 dev tối ưu)' : '🔴 Cao (Cần team từ 3-5 dev)'}\n\n`;
      summaryText += `#### 🛠️ Các khối kỹ thuật sẽ được kích hoạt:\n`;
      if (features.hasPessimisticLock) summaryText += `- ✅ **Pessimistic Lock (\`SELECT FOR UPDATE\`):** Khóa dòng DB an toàn, chống bán trùng tồn kho.\n`;
      if (features.hasDbQueue) summaryText += `- ✅ **DB-Backed Job Queue:** Hàng đợi lưu trực tiếp trong PostgreSQL (0 đồng thêm server, server sập bật lại không mất job).\n`;
      if (features.hasHmacWebhook) summaryText += `- ✅ **HMAC Webhook Receiver:** Xác thực chữ ký số SHA-256 + Idempotency chống fake giao dịch Momo/Stripe.\n`;
      if (features.hasIdempotency) summaryText += `- ✅ **Idempotency Guard:** Chống double-charge khi người dùng bấm liên tục.\n`;
      summaryText += `\n💾 **Đã lưu trạng thái vào Ephemeral Scratchpad:** \`${cachePath}\`\n*(Context được bảo vệ chống trôi/ảo giác; file tạm này sẽ tự động xóa ngay sau khi scaffold hoàn tất)*\n\n`;
      summaryText += `👉 Bạn có thể gọi tool \`scaffold_project\` để bắt đầu sinh mã nguồn theo chuẩn này!`;

      return {
        content: [{ type: 'text', text: summaryText }]
      };
    }

    case 'list_architectures': {
      const list = blueprintsDb.map(b => `### 🏛️ \`${b.id}\` — ${b.name}\n- **Tech Stack**: ${b.techStack}\n- **Mô tả**: ${b.description}\n- **Phù hợp nhất**: ${b.idealFor}`).join('\n\n');
      return {
        content: [{
          type: 'text',
          text: `## 📦 Danh sách các Source Base Blueprints có sẵn:\n\n${list}\n\n👉 Dùng tool 'scaffold_project' để tự động tạo cây thư mục và sinh mã nguồn ra đĩa.`
        }]
      };
    }

    case 'scaffold_project': {
      const bp = blueprintsDb.find(b => b.id.toLowerCase() === args.architecture_id.toLowerCase().trim());
      if (!bp) {
        return {
          isError: true,
          content: [{
            type: 'text',
            text: `Lỗi: Không tìm thấy kiến trúc "${args.architecture_id}". Danh sách khả dụng: ${blueprintsDb.map(b => b.id).join(', ')}`
          }]
        };
      }

      const targetPath = path.resolve(args.target_dir);
      const projName = args.project_name || path.basename(targetPath);

      if (!fs.existsSync(targetPath)) {
        fs.mkdirSync(targetPath, { recursive: true });
      }

      // Kiểm tra xem có Ephemeral Scratchpad phiên phỏng vấn trước đó không
      const session = loadSessionState(targetPath);
      let adrCustomContent = null;
      let features = {};

      if (session && session.data) {
        adrCustomContent = session.data.adr_content;
        features = session.data.features || {};
      }

      let createdFiles = [];
      for (const [relPath, contentTemplate] of Object.entries(bp.files)) {
        const fullFilePath = path.join(targetPath, relPath);
        const dir = path.dirname(fullFilePath);
        if (!fs.existsSync(dir)) {
          fs.mkdirSync(dir, { recursive: true });
        }
        let finalContent = contentTemplate.replace(/\{\{PROJECT_NAME\}\}/g, projName);

        // Nếu file là ADR và có nội dung tùy biến từ phiên phỏng vấn thì ghi nội dung tùy biến
        if (relPath.includes('ADR-001') && adrCustomContent) {
          finalContent = adrCustomContent;
        }

        fs.writeFileSync(fullFilePath, finalContent, 'utf8');
        createdFiles.push(relPath);
      }

      // Nhúng các module điều kiện từ interview nếu có
      if (features.hasHmacWebhook) {
        const hmacPath = path.join(targetPath, 'src', 'interfaces', 'http', 'middlewares', 'hmac-verify.middleware.ts');
        const hmacDir = path.dirname(hmacPath);
        if (!fs.existsSync(hmacDir)) fs.mkdirSync(hmacDir, { recursive: true });
        const hmacSnippet = patternsDb.find(p => p.id === 'hmac-webhook-verification')?.code_snippet?.code;
        if (hmacSnippet) {
          fs.writeFileSync(hmacPath, hmacSnippet, 'utf8');
          createdFiles.push('src/interfaces/http/middlewares/hmac-verify.middleware.ts');
        }
      }

      if (features.hasDbQueue) {
        const queuePath = path.join(targetPath, 'src', 'infrastructure', 'jobs', 'db-queue.worker.ts');
        const queueDir = path.dirname(queuePath);
        if (!fs.existsSync(queueDir)) fs.mkdirSync(queueDir, { recursive: true });
        const queueSnippet = patternsDb.find(p => p.id === 'db-backed-queue')?.code_snippet?.code;
        if (queueSnippet) {
          fs.writeFileSync(queuePath, queueSnippet, 'utf8');
          createdFiles.push('src/infrastructure/jobs/db-queue.worker.ts');
        }
      }

      // TỰ ĐỘNG DỌN DẸP EPHEMERAL SCRATCHPAD (Auto Eviction)
      clearSessionState(targetPath);

      return {
        content: [{
          type: 'text',
          text: `✅ **Khởi tạo thành công Source Base [${bp.name}]!**\n\n📁 **Thư mục:** \`${targetPath}\`\n🚀 **Số file đã sinh:** ${createdFiles.length}\n🧹 **Trạng thái:** Đã tự động dọn dẹp sạch sẽ Ephemeral Scratchpad (0% context pollution).\n\n**Danh sách file:**\n${createdFiles.map(f => `- \`${f}\``).join('\n')}\n\n👉 Giờ bạn chỉ cần cd vào thư mục và bắt đầu phát triển tính năng!`
        }]
      };
    }

    case 'inject_pattern': {
      const p = patternsDb.find(item => item.id.toLowerCase() === args.pattern_id.toLowerCase().trim());
      if (!p) {
        return {
          isError: true,
          content: [{
            type: 'text',
            text: `Không tìm thấy pattern "${args.pattern_id}" để nhúng.`
          }]
        };
      }

      const targetPath = path.resolve(args.target_dir);
      const patternsDir = path.join(targetPath, 'src', 'patterns');
      if (!fs.existsSync(patternsDir)) {
        fs.mkdirSync(patternsDir, { recursive: true });
      }

      const ext = p.code_snippet?.language === 'typescript' ? 'ts' : (p.code_snippet?.language === 'lua' ? 'lua' : 'js');
      const filename = `${p.id}.${ext}`;
      const fullPath = path.join(patternsDir, filename);
      fs.writeFileSync(fullPath, p.code_snippet?.code || '', 'utf8');

      return {
        content: [{
          type: 'text',
          text: `✅ Đã nhúng pattern **${p.name}** vào thư mục dự án:\n📄 File: \`${path.join('src', 'patterns', filename)}\`\n\nBạn có thể import và sử dụng trực tiếp trong mã nguồn.`
        }]
      };
    }

    case 'recommend_architecture': {
      const ccu = args.estimated_ccu || 100;
      const team = args.team_size || 2;
      const type = (args.business_type || '').toLowerCase();

      let recommendation = '';
      if (team <= 3 && ccu < 5000) {
        recommendation = `### 🎯 Kiến nghị: **Modular Monolith (hoặc Clean Architecture Monolith)**\n- **Lý do**: Đội ngũ nhỏ (${team} người), tải chưa quá lớn (< 5k CCU). Tránh lãng phí 80% thời gian cho network latency và devops.\n- **Blueprint đề xuất**: \`clean-arch-ts\` hoặc \`clean-arch-fastapi\`.`;
      } else if (team > 5 || ccu >= 10000 || type === 'fintech') {
        recommendation = `### 🎯 Kiến nghị: **Event-Driven Architecture / Microservices với Transactional Outbox**\n- **Patterns bắt buộc**: \`transactional-outbox\`, \`idempotency-key\`, \`circuit-breaker\`.`;
      } else {
        recommendation = `### 🎯 Kiến nghị: **Clean Architecture Service**\n- **Blueprint đề xuất**: \`clean-arch-ts\`.`;
      }

      return {
        content: [{ type: 'text', text: recommendation }]
      };
    }

    default:
      return {
        isError: true,
        content: [{ type: 'text', text: `Tool không tồn tại: ${name}` }]
      };
  }
}

// -------------------------------------------------------------
// Chế độ CLI
// -------------------------------------------------------------
const cliArgs = process.argv.slice(2);
if (cliArgs.length > 0 && !cliArgs.includes('--stdio')) {
  const cmd = cliArgs[0].toLowerCase();
  if (cmd === '--help' || cmd === '-h' || cmd === 'help') {
    console.log(`
Agent-Dev-Kit System Design CLI & MCP Server
Cách dùng:
  node index.js search <từ_khóa>          : Tìm kiếm pattern
  node index.js get <pattern_id>          : Xem chi tiết pattern
  node index.js blueprints                : Liệt kê các bộ source base
  node index.js scaffold <id> <thư_mục>   : Sinh source base dự án ra đĩa
  node index.js                           : Khởi chạy dưới dạng MCP Server (Stdio)
`);
    process.exit(0);
  } else if (cmd === 'search') {
    const q = cliArgs.slice(1).join(' ');
    const res = handleToolCall('search_patterns', { query: q });
    console.log(res.content[0].text);
    process.exit(0);
  } else if (cmd === 'get') {
    const id = cliArgs[1];
    const res = handleToolCall('get_pattern_details', { pattern_id: id });
    console.log(res.content[0].text);
    process.exit(0);
  } else if (cmd === 'blueprints') {
    const res = handleToolCall('list_architectures', {});
    console.log(res.content[0].text);
    process.exit(0);
  } else if (cmd === 'scaffold') {
    const archId = cliArgs[1];
    const target = cliArgs[2] || './new-project';
    const res = handleToolCall('scaffold_project', {
      architecture_id: archId,
      target_dir: target,
      project_name: path.basename(target)
    });
    console.log(res.content[0].text);
    process.exit(0);
  }
}

// -------------------------------------------------------------
// Chế độ MCP Server (JSON-RPC qua Stdio)
// -------------------------------------------------------------
const rl = readline.createInterface({
  input: process.stdin,
  output: process.stdout,
  terminal: false
});

function sendResponse(id, result, error = null) {
  const response = { jsonrpc: '2.0', id };
  if (error) {
    response.error = error;
  } else {
    response.result = result;
  }
  process.stdout.write(JSON.stringify(response) + '\n');
}

rl.on('line', (line) => {
  const trimmed = line.trim();
  if (!trimmed) return;

  let request;
  try {
    request = JSON.parse(trimmed);
  } catch (err) {
    sendResponse(null, null, { code: -32700, message: 'Parse error' });
    return;
  }

  const { id, method, params } = request;

  switch (method) {
    case 'initialize':
      sendResponse(id, {
        protocolVersion: '2024-11-05',
        capabilities: {
          tools: {}
        },
        serverInfo: {
          name: 'system-design',
          version: '1.1.0'
        }
      });
      break;

    case 'notifications/initialized':
      break;

    case 'ping':
      sendResponse(id, {});
      break;

    case 'tools/list':
      sendResponse(id, { tools: TOOLS });
      break;

    case 'tools/call': {
      if (!params || !params.name) {
        sendResponse(id, null, { code: -32602, message: 'Missing tool name' });
        break;
      }
      try {
        const result = handleToolCall(params.name, params.arguments || {});
        sendResponse(id, result);
      } catch (callErr) {
        sendResponse(id, {
          isError: true,
          content: [{ type: 'text', text: `Tool error: ${callErr.message}` }]
        });
      }
      break;
    }

    default:
      if (id !== undefined && id !== null) {
        sendResponse(id, null, { code: -32601, message: `Method not found: ${method}` });
      }
      break;
  }
});

console.error('[SystemDesignMCP] Server v1.1.0 initialized with Ephemeral Scratchpad support.');
