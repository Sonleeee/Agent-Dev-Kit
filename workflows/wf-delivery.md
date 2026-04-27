---
id: delivery
type: shortcut
entry-command: /wf-delivery
stages: clarify -> plan -> impl -> review
description: Task phức tạp — full flow
modifiers:
  --fast: Mỗi stage chạy ở chế độ --fast, rút gọn tối đa
  --parallel: Stage /wf-impl chạy multi-agent song song (Antigravity run_command via Terminal)
  --auto: Tự động approve tất cả gates, không hỏi user
---

# /wf-delivery

**Mục tiêu:** Full delivery flow cho task phức tạp.

## Khi nào dùng

- Task nhiều modules
- Cần plan kỹ trước khi code
- Có risk cao (API contract change, breaking change)
- Cần review đầy đủ 5 layers

## Flow

```text
/wf-clarify → /wf-plan → /wf-impl → /wf-review
```

Mỗi stage chạy đầy đủ theo workflow riêng.

## Output

`../templates/wf-delivery-report.md.template`
