# 📦 Addons — Mở rộng tùy chọn

Addons là các tính năng bổ sung cho Agent-Dev-Kit. Chỉ bật khi bạn cần.

Core Kit (workflows, rules, quality gates) hoạt động **độc lập** — không cần addon nào.

---

## Danh sách Addons

| Addon | Mô tả | Cần cài thêm? |
|-------|--------|----------------|
| [swarm/](./swarm/) | Multi-agent orchestration | Cần MCP servers (codex-cli, gemini-cli...) |
| [obsidian/](./obsidian/) | Second Brain với Obsidian vault | Cần cài Obsidian |
| [notebooklm/](./notebooklm/) | Research & Synthesis | Cần NotebookLM MCP server |
| [archify/](./archify/) | Architecture/workflow HTML đã validate | Cần cài Archify skill |
| [knowledge/](./knowledge/) | Context cache, memory consolidation, vault writeback | Chỉ cần khi dùng Second Brain |
| [database/](./database/) | Database/schema inspection | Chỉ cần khi project có database |
| [maintainer/](./maintainer/) | Health check kit và tạo skill | Chỉ cần khi maintain kit |

---

## Cách dùng Addon

1. Đọc `README.md` trong thư mục addon
2. Làm theo hướng dẫn setup
3. Các workflow trong core kit đã có note `[Multi-agent]`, `[Second Brain]` ở cuối để liên kết sang addon khi cần
