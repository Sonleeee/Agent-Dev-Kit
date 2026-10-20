# 🏗️ Addon: System Design Knowledge Base & Scaffolding Engine

Addon cung cấp **Kho Kiến Trúc Hệ Thống Chuẩn (Ground-Truth System Design)** và **Cỗ Máy Sinh Source Base (Scaffolding Engine)** thông qua giao thức Model Context Protocol (MCP) cho toàn bộ AI Coding Agents (Antigravity, Claude Code, Cursor, Codex,...).

---

## 🎯 Hai Mục Tiêu Cốt Lõi

1. **Chuẩn bị Source Base chuẩn cho dự án mới**:
   - Dựng toàn bộ cây thư mục, Docker, configuration, use cases, domain entities, interfaces và file quyết định kiến trúc (`ADR-001`) theo chuẩn Clean Architecture (TypeScript hoặc Python FastAPI).
   - Tự động hóa 100% qua lệnh hoặc workflow `/wf-scaffold` mà không sợ AI gõ sai cú pháp.

2. **Kho tri thức kiến trúc nội bộ chống AI lan man internet**:
   - Tích hợp sẵn các pattern hệ thống phân tán kinh điển (lấy cảm hứng từ ByteByteGo, Azure Cloud Patterns, DDIA):
     - `transactional-outbox`: Giải quyết bài toán Dual-Write (ghi DB và bắn Kafka/RabbitMQ an toàn).
     - `idempotency-key`: Tránh trừ tiền 2 lần hoặc nhân đôi đơn hàng khi mạng giật retry.
     - `circuit-breaker`: Ngắt mạch tự động khi downstream service bị chậm/sập.
     - `cache-aside-stampede`: Cache-Aside kết hợp giải thuật chống sập DB khi hot key hết hạn (Thundering Herd).
     - `rate-limiter-token-bucket`: Giới hạn lưu lượng chống spam/DDoS qua Redis Lua Script.
     - `saga-orchestration`: Điều phối giao dịch phân tán và kích hoạt giao dịch bù trừ (compensating transaction).

---

## 🛠️ Danh Sách MCP Tools

Khi được kích hoạt, Agent có thể gọi các tool sau:

| Tool Name | Tham số chính | Vai trò |
| :--- | :--- | :--- |
| `search_patterns` | `query`, `category` | Tra cứu pattern chuẩn từ kho tri thức nội bộ. |
| `get_pattern_details` | `pattern_id` | Xem chi tiết bài toán, sơ đồ Mermaid, invariants và code mẫu. |
| `list_architectures` | *(không có)* | Liệt kê các blueprint source base có sẵn (`clean-arch-ts`, `clean-arch-fastapi`). |
| `scaffold_project` | `architecture_id`, `target_dir`, `project_name` | Tự động sinh trọn vẹn source base ra đĩa. |
| `inject_pattern` | `pattern_id`, `target_dir` | Nhúng code mẫu của 1 pattern vào thư mục dự án đang phát triển. |
| `recommend_architecture` | `estimated_ccu`, `team_size`, `business_type` | Tư vấn kiến trúc tối ưu, chống over-engineering. |

---

## 🚀 Cách Cài Đặt & Sử Dụng

### 1. Cài đặt tự động khi cài Full Kit (Khuyến nghị)
Khi cài đặt Agent-Dev-Kit với cờ Full:
```powershell
adk full
# hoặc:
.\install.ps1 -Full
```
Lệnh này sẽ tự động cài đặt CodeGraph VÀ kích hoạt System Design MCP Server cho mọi công cụ AI của bạn.

### 2. Cài đặt riêng lẻ qua Addon Manager
```powershell
adk addon add system-design
# hoặc chạy trực tiếp:
powershell -File .agents/addons/system-design/setup.ps1
```

### 3. Sử dụng trực tiếp từ dòng lệnh (CLI Mode)
Bạn cũng có thể dùng trực tiếp mà không cần qua AI:
```powershell
# Tìm kiếm pattern
node addons/system-design/mcp-server/index.js search outbox

# Xem chi tiết pattern
node addons/system-design/mcp-server/index.js get idempotency-key

# Xem danh sách blueprints
node addons/system-design/mcp-server/index.js blueprints

# Sinh source base dự án mới ra thư mục ./my-app
node addons/system-design/mcp-server/index.js scaffold clean-arch-ts ./my-app
```

### 4. Sử dụng trong Chat với AI
- Gõ lệnh: `/wf-scaffold` để AI hướng dẫn khảo sát và tự động sinh source base cho dự án mới.
- Hoặc hỏi tự nhiên: *"Hệ thống thanh toán cần xử lý network retry thế nào?"* $\to$ AI sẽ tự động kích hoạt MCP tool `search_patterns` và `get_pattern_details` để đưa ra giải pháp Idempotency Key kèm code mẫu chuẩn.
