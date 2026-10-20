---
id: status
type: utility
entry-command: /wf-status
description: Tóm tắt nhanh trạng thái hiện tại (đang làm gì, đã xong gì, còn gì chặn)
---

> [!IMPORTANT]
> ## Delegation Policy � �?c TRU?C khi b?t d?u
>
> | �i?u ki?n | H�nh d?ng B?T BU?C |
> |:---|:---|
> | Session r?t d�i (= 30 turns) c?n t?ng h?p | **PH?I** `invoke_subagent(TypeName="research", Role="Session Summarizer")` |
> | Session ng?n ho?c v?a | Ch?y inline, KH�NG c?n subagent |


# /wf-status

**Mục tiêu:** Cung cấp cái nhìn tổng quan nhanh chóng về tiến độ công việc trong session hiện tại. Port từ concept `ck:watzup` của VividKit.

## Khi nào dùng

- Sau khi quay lại task từ một quãng nghỉ.
- Khi session quá dài và cần "re-sync" lại context.
- Trước khi thực hiện `/wf-review` để tóm tắt các thay đổi đã thực hiện.

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

## Pre-completion Checklist (PH?I verify tru?c khi output)

- [ ] �� ki?m tra Delegation Policy ? d?u file?
- [ ] Report = 20 d�ng?
- [ ] Format nh?t qu�n?
