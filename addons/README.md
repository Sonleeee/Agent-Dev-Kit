# 📦 Addons — Mở rộng tùy chọn

Addons là các tính năng bổ sung cho Agent-Dev-Kit. Chỉ bật khi bạn cần.

Core Kit (workflows, rules, quality gates) hoạt động **độc lập** — không cần addon nào.

---

## Danh sách Addons khả dụng

| Addon | Mô tả | Cần cài thêm? |
|---|---|---|
| [system-design/](./system-design/) | Kho kiến trúc chuẩn (ByteByteGo/Cloud) & Engine tự động scaffold Clean Architecture (MCP) | Đã tích hợp sẵn (hoặc `adk full`) |
| `codegraph/` | Semantic Code Intelligence: lập chỉ mục AST, call graph & symbols (19+ ngôn ngữ) | `npx -y @colbymchenry/codegraph install -y -i --target=antigravity,codex` (hoặc `adk full`) |
| [archify/](./archify/) | Architecture/workflow HTML tự chứa (self-contained) | Cần cài Archify skill (`npx skills add tt-a1i/archify -g`) |
| [database/](./database/) | Tra cứu schema, quan hệ bảng và query SQL an toàn | Cần kết nối Gridex MCP Server |
| [notebooklm/](./notebooklm/) | Research & Synthesis, đọc tài liệu dày, sync ghi chú | Cần NotebookLM MCP Server |
| [obsidian/](./obsidian/) | Đồng bộ ghi chú, lưu tri thức, ADR vào Obsidian Vault | Cài đặt qua `adk addon add obsidian` |
| [maintainer/](./maintainer/) | Health check kit (validate-kit.ps1) và tạo skill | Bộ script nội bộ bảo trì kit |

---

## 📓 Addon Obsidian

Addon `obsidian` giúp kết nối Agent với Obsidian Vault của bạn:
- Tự động chưng cất tri thức, ADR, bug pattern từ quá trình code vào vault.
- Hỗ trợ workflow `/wf-vault-sync` và các skills: `sk-vault-steward`, `sk-context-cache`, `sk-memory-consolidator`.
- Chi tiết xem tại [addons/obsidian/README.md](./obsidian/README.md).

---

## Cách dùng Addon

1. Dùng lệnh `adk addon add <tên>` để xem hướng dẫn hoặc cài đặt tương tác.
2. Đọc `README.md` trong từng thư mục addon để nắm chi tiết.
