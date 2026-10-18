# 📦 Addons — Mở rộng tùy chọn

Addons là các tính năng bổ sung cho Agent-Dev-Kit. Chỉ bật khi bạn cần.

Core Kit (workflows, rules, quality gates) hoạt động **độc lập** — không cần addon nào.

---

## Danh sách Addons khả dụng

| Addon | Mô tả | Cần cài thêm? |
|---|---|---|
| `codegraph/` | Semantic Code Intelligence: lập chỉ mục AST, call graph & symbols (19+ ngôn ngữ) | `npx -y @colbymchenry/codegraph install -y -i --target=antigravity,codex` (hoặc `adk full`) |
| [archify/](./archify/) | Architecture/workflow HTML tự chứa (self-contained) | Cần cài Archify skill (`npx skills add tt-a1i/archify -g`) |
| [database/](./database/) | Tra cứu schema, quan hệ bảng và query SQL an toàn | Cần kết nối Gridex MCP Server |
| [notebooklm/](./notebooklm/) | Research & Synthesis, đọc tài liệu dày, sync ghi chú | Cần NotebookLM MCP Server |
| [maintainer/](./maintainer/) | Health check kit (validate-kit.ps1) và tạo skill | Bộ script nội bộ bảo trì kit |

---

## 📓 Tích hợp Second Brain (Obsidian Vault)

Second Brain (`C:\Sonlee\AI\SecondBrain`) là kho tri thức, tài liệu và ADR độc lập của bạn:
- Kit kết nối với Obsidian vault thông qua đường dẫn `vault-path` trong file `AGENTS.md`.
- Khi cần chưng cất bài học từ task vào Second Brain, sử dụng workflow `/wf-vault-sync`.

---

## Cách dùng Addon

1. Dùng lệnh `adk addon add <tên>` để xem link hướng dẫn hoặc cài đặt tương tác.
2. Đọc `README.md` trong từng thư mục addon để nắm chi tiết.
3. Các workflow trong core kit đã có note `[Second Brain]` hoặc `[Gridex]` ở cuối để liên kết sang addon khi cần.
