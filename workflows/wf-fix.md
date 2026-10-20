---
id: fix
type: utility
entry-command: /wf-fix
description: Pipeline debug có cấu trúc — scout → diagnose → fix → verify → prevent
modifiers:
  --fast: Bỏ qua scout, diagnose luôn từ error message, fix nhanh
  --deep: Research root cause kỹ, tìm related issues trong codebase
---

> [!IMPORTANT]
> ## Delegation Policy — Đọc TRƯỚC khi bắt đầu
>
> | Điều kiện | Hành động BẮT BUỘC |
> |:---|:---|
> | Modifier `--deep` được dùng | **PHẢI** `invoke_subagent(TypeName="research", Role="Root Cause Researcher")` để research kỹ |
> | Bug đụng ≥ 3 files hoặc ≥ 2 layers | **PHẢI** `invoke_subagent(TypeName="research", Role="Cross-Layer Debugger")` |
> | Fix đơn giản ≤ 1 file | Chạy inline, KHÔNG cần subagent |
>
> **Subagent context:** Chỉ gửi error logs + stack trace + file scope. KHÔNG gửi chat history.

# /wf-fix

**Mục tiêu:** Debug có cấu trúc — không patch bừa, tìm root cause rồi mới fix.

## Khi nào dùng

- Bug cần fix (exception, logic sai, data sai)
- Build fail chưa rõ nguyên nhân
- Regression sau khi thay đổi code

## Quy trình

### Bước 1: Scout — Thu thập context

Agent thu thập:

- Error logs / stack trace / error message
- File(s) liên quan đến lỗi
- Recent changes (git diff nếu có)
- Reproduction steps (hỏi user nếu chưa rõ)

### Bước 2: Diagnose — Xác định root cause

Agent phân tích:

1. Phân loại lỗi: logic / config / data / dependency / infrastructure
2. Trace error path từ symptom → root cause
3. Xác định scope ảnh hưởng — 1 file hay nhiều files
4. List ra các hypotheses, chọn hypothesis có evidence mạnh nhất

### Bước 3: Fix — Implement sửa lỗi

Agent implement fix:

1. Fix bám sát root cause — không patch symptom
2. Follow project templates/conventions (nếu có `context/templates/`)
3. Giữ scope nhỏ — chỉ fix đúng lỗi, không refactor kèm
4. Ghi rõ **tại sao** fix theo cách này

### Bước 4: Verify — Xác nhận fix đúng

Agent verify:

- [ ] Build pass sau khi fix
- [ ] Error gốc không còn reproduce
- [ ] Không gây regression ở chỗ khác
- [ ] Test liên quan pass (nếu có)

### Bước 5: Prevent — Đề xuất phòng ngừa

Agent đề xuất (tùy chọn):

- Test case mới để catch lỗi tương tự
- Guard / validation bổ sung
- Documentation update nếu lỗi do hiểu sai

### Bước 6: Knowledge Checkpoint

Áp dụng `SYSTEM.md` → Brain Writeback Policy.

| Điều kiện | Mode | Hành động |
|-----------|------|-----------|
| Root cause đã xác nhận và fix verify PASS | `AUTO` | Không ghi mặc định; addon có thể mở rộng |
| Bug chưa verify PASS nhưng có hypothesis đáng lưu | `ASK` | Trình Memory Candidate, hỏi user trước khi ghi |
| Lỗi tạm thời, build noise, typo nhỏ không có lesson | `SKIP` | Không ghi |

Nội dung tối thiểu khi ghi:
- Root cause
- Symptom ban đầu
- Files liên quan
- Fix summary
- Prevention recommendation
- Verification result

## Output bắt buộc

- Root cause (1-2 câu rõ ràng)
- Loại lỗi: logic / config / data / dependency
- Files đã sửa + tóm tắt thay đổi
- Build verification result
- Prevention recommendation (nếu có)
- Knowledge Checkpoint: AUTO / ASK / SKIP + target

## Guardrails

- KHÔNG patch bừa khi chưa hiểu root cause
- KHÔNG mở rộng scope — fix xong thì dừng, refactor là task riêng
- Nếu fix > 3 files → cân nhắc chuyển sang `/wf-impl` workflow
- Build verify là bắt buộc
- Chỉ AUTO ghi khi root cause đã có evidence và fix đã verify PASS


## Pre-completion Checklist (PHẢI verify trước khi báo fix done)

- [ ] Đã kiểm tra Delegation Policy ở đầu file?
- [ ] Nếu `--deep` → ĐÃ invoke research subagent?
- [ ] Root cause xác định rõ (không patch bừa)?
- [ ] Build PASS sau fix?
- [ ] Regression check done?
