# 📦 Addons — Mở rộng tùy chọn

Addons là các tính năng bổ sung cho Agent-Dev-Kit. Chỉ bật khi bạn cần.

Core Kit (rules, skills và lệnh tương thích) hoạt động **độc lập** — không cần addon nào.

---

## Danh sách Addons khả dụng

| Addon | Mô tả | Cần cài thêm? |
|---|---|---|
| [system-design/](./system-design/) | Kho kiến trúc tham khảo và skill scaffold source base theo yêu cầu (MCP) | Đã tích hợp sẵn (hoặc `adk full`) |
| `codegraph/` | Semantic Code Intelligence: lập chỉ mục AST, call graph & symbols (19+ ngôn ngữ) | `npx -y @colbymchenry/codegraph install -y -i --target=antigravity,codex` (hoặc `adk full`) |
| [database/](./database/) | Tra cứu schema, quan hệ bảng và query SQL an toàn | Cần kết nối Gridex MCP Server |
| [notebooklm/](./notebooklm/) | Research & Synthesis, đọc tài liệu dày, sync ghi chú | Cần NotebookLM MCP Server |
| [obsidian/](./obsidian/) | Skill đọc/lưu tri thức và ADR vào Obsidian Vault theo yêu cầu | Cài đặt qua `adk addon add obsidian` |
| [maintainer/](./maintainer/) | Health check kit (validate-kit.ps1) và tạo skill | Bộ script nội bộ bảo trì kit |

---

## 📓 Addon Obsidian

Addon `obsidian` giúp kết nối Agent với Obsidian Vault của bạn:
- Tự động chưng cất tri thức, ADR, bug pattern từ quá trình code vào vault.
- Các skill: `adk-vault-steward`, `adk-context-cache`, `adk-memory-consolidator`; `/wf-vault-sync` chỉ còn là adapter thủ công cho host hỗ trợ workflow.
- Chi tiết xem tại [addons/obsidian/README.md](./obsidian/README.md).

---

## Cách dùng Addon

1. Dùng lệnh `adk addon add <tên>` để xem hướng dẫn hoặc cài đặt tương tác.
2. Đọc `README.md` trong từng thư mục addon để nắm chi tiết.
