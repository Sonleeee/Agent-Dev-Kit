# 🔗 Obsidian Hooks

> Các hooks/scripts để kết nối agent với Obsidian vault.

## Ý tưởng hooks

### 1. Post-Review Hook
Sau `/wf-review`, agent tự động tạo note trong vault:
- File: `brain/projects/[project]/wf-review-YYYY-MM-DD.md`
- Nội dung: summary findings, pass/fail status

### 2. ADR Auto-Create Hook
Khi `/wf-clarify --compare` chốt được approach, agent tạo ADR:
- File: `brain/decisions/ADR-NNN-ten-decision.md`

### 3. Knowledge Extract Hook
Khi giải quyết xong bug khó hoặc learn pattern mới:
- Agent hỏi: "Bạn muốn ghi lại knowledge này không?"
- Nếu đồng ý → tạo note trong `brain/knowledge/`

## Cách implement

Hooks là markdown instructions mà agent đọc khi cần.
Không cần script thật — agent đọc hướng dẫn ở đây và thực thi.

> Đây là feature nâng cao. Bắt đầu dùng vault trước, thêm hooks sau.
