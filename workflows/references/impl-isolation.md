# Git Worktree Isolation & Local Brainwash — Chi tiết

> Tài liệu tham khảo cho `/wf-impl` Bước 2. Agent đọc file này khi cần hiểu rationale.

## Git Worktree Isolation

AI thực hiện task trên một phân vùng độc lập để bảo vệ mã nguồn chính.

- **Lệnh khởi tạo:** `git worktree add ../temp-[task_id] [branch_name] [base_branch]`
- **Lợi ích:** Tránh xung đột file với User, tạo sandbox an toàn cho AI thực thi các lệnh build/test.
- **Dọn dẹp:** Sau khi `/wf-review` hoàn tất (PASS hoặc FAIL), worktree và nhánh tạm này PHẢI được xóa bỏ để giải phóng tài nguyên.

## Tẩy Não Cục Bộ (Local Brainwash)

Khi Antigravity điều phối các Sub-agent (qua `gemini-cli`, `opencode-cli` hoặc `invoke_subagent`):

- **Minimal Context:** Chỉ truyền `implementation-plan-lite` và nội dung của **duy nhất** các file cần sửa.
- **No Chat History:** TUYỆT ĐỐI không gửi kèm lịch sử chat của phiên chính để triệt tiêu bias và ảo giác luỹ kế.

### Rationale

- Gửi kèm chat history → bias luỹ kế → hallucination tăng theo số turn
- Gửi toàn bộ codebase → context bloat → giảm accuracy trên mỗi instruction
- Chỉ gửi plan-lite + đúng files cần sửa → subagent tập trung 100% vào task
