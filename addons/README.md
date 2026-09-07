# 📦 Addons — Mở rộng tùy chọn

Addons là các tính năng bổ sung cho Agent-Dev-Kit. Chỉ bật khi bạn cần.

Core Kit (workflows, rules, quality gates) hoạt động **độc lập** — không cần addon nào.

---

## Danh sách Addons (6 Addons khả dụng)

| Addon | Mô tả | Cần cài thêm? |
|-------|--------|----------------|
| [archify/](./archify/) | Architecture/workflow HTML tự chứa (self-contained) | Cần cài Archify skill (`npx skills add tt-a1i/archify -g`) |
| [database/](./database/) | Tra cứu schema, quan hệ bảng và query SQL an toàn | Cần kết nối Gridex MCP Server |
| [obsidian/](./obsidian/) | Ghi nhận tri thức, sync hai chiều với Second Brain | Cần app Obsidian & cấu hình vault-path |
| [notebooklm/](./notebooklm/) | Research & Synthesis, đọc tài liệu dày, sync ghi chú | Cần NotebookLM MCP Server |
| [knowledge/](./knowledge/) | Context cache, memory consolidation, vault writeback | Đi kèm với Second Brain / Obsidian |
| [maintainer/](./maintainer/) | Health check kit (validate-kit.ps1) và tạo skill | Bộ script nội bộ bảo trì kit |

---

## Cách dùng Addon

1. Dùng lệnh `adk addon add <tên>` để xem link hướng dẫn hoặc cài đặt tương tác.
2. Đọc `README.md` trong từng thư mục addon để nắm chi tiết.
3. Các workflow trong core kit đã có note `[Second Brain]` hoặc `[Gridex]` ở cuối để liên kết sang addon khi cần.
