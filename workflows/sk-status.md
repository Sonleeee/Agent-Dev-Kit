---
id: status
type: utility
entry-command: /sk-status
description: Tóm tắt nhanh trạng thái hiện tại (đang làm gì, đã xong gì, còn gì chặn)
---

# /sk-status

**Mục tiêu:** Cung cấp cái nhìn tổng quan nhanh chóng về tiến độ công việc trong session hiện tại. Port từ concept `ck:watzup` của VividKit.

## Khi nào dùng

- Sau khi quay lại task từ một quãng nghỉ.
- Khi session quá dài và cần "re-sync" lại context.
- Trước khi thực hiện `/sk-review` để tóm tắt các thay đổi đã thực hiện.

## Quy trình

### Bước 1: Analyze History
Agent quét lịch sử hội thoại và file `task.md` (nếu có) để xác định:
- Task chính hiện tại.
- Các sub-tasks đã hoàn thành.
- Các task đang dang dở.

### Bước 2: Context Snapshot
Agent kiểm tra các file đã thay đổi (git diff) và các artifacts đã tạo.

### Bước 3: Synthesize
Agent tạo bản tóm tắt theo format:

```markdown
## ⚡ Quick Status Report

### 🎯 Objective Hiện Tại
[Mục tiêu chính đang thực hiện]

### ✅ Đã Hoàn Thành
- [Task 1]
- [Task 2]

### 🚧 Đang Thực Hiện / Còn Lại
- [Task 3]
- [Task 4]

### 🛑 Blockers / Lưu Ý
- [Vấn đề cần user giải quyết hoặc lưu ý quan trọng]
```

## Output bắt buộc
- Bản tóm tắt ngắn gọn (không quá 20 dòng).
- Tập trung vào sự thay đổi và trạng thái, không phải chi tiết code.

## Guardrails
- KHÔNG liệt kê mọi tool call — chỉ liệt kê logic nghiệp vụ/task.
- Giữ format nhất quán để user dễ đọc.
