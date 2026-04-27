---
id: delivery-lite
type: shortcut
entry-command: /wf-delivery-lite
stages: clarify-lite -> plan-lite -> impl -> review-lite
description: Task rõ ràng — đi nhanh
modifiers:
  --fast: Rút gọn tối đa — clarify 1 câu, plan 3 dòng, review chỉ build check
  --no-test: Bỏ test obligations, chỉ build pass là đủ
---

# /wf-delivery-lite

**Mục tiêu:** Shortcut cho task đơn giản, rõ ràng, đi nhanh.

## Khi nào dùng

- Task rõ scope (thêm field, fix bug nhỏ, thêm validation)
- Không cần clarify dài
- Risk thấp

## Flow

```text
clarify-lite → plan-lite → /wf-impl → review-lite
```

### clarify-lite
- 1–2 câu problem statement
- Scope in/out ngắn gọn

### plan-lite
- Approach 1 câu
- Files cần sửa
- Template nếu cần

### review-lite
- Checklist subset (không full 38 items)
- Build pass check
- Quick ship decision

## Output

`../templates/wf-delivery-report.md.template`
