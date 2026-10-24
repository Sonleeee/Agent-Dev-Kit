# 🔗 Obsidian Hooks

> Các hooks/scripts để kết nối agent với Obsidian vault.

## Ý tưởng hooks

### 1. Lưu review vào vault theo yêu cầu
Khi user yêu cầu lưu kết quả review, agent có thể tạo note trong vault:
- File: `brain/projects/[project]/review-YYYY-MM-DD.md`
- Nội dung: summary findings, pass/fail status

### 2. Lưu ADR theo yêu cầu
Sau khi user chốt approach và yêu cầu ghi lại quyết định, agent có thể tạo ADR:
- File: `brain/decisions/ADR-NNN-ten-decision.md`

### 3. Knowledge Extract Hook
Khi giải quyết xong bug khó hoặc learn pattern mới:
- Agent hỏi: "Bạn muốn ghi lại knowledge này không?"
- Nếu đồng ý → tạo note trong `brain/knowledge/`

## Cách implement

Đây là các ý tưởng tích hợp, không phải hook tự chạy. Agent chỉ đọc chúng khi
user yêu cầu lưu nội dung vào vault; thao tác ghi luôn cần intent rõ ràng.

> Đây là feature nâng cao. Bắt đầu dùng vault trước, thêm hooks sau.
