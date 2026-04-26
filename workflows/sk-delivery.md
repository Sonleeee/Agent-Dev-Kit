---
id: delivery
type: shortcut
entry-command: /sk-delivery
stages: clarify -> plan -> impl -> review
description: Task phức tạp — full flow
modifiers:
  --fast: Mỗi stage chạy ở chế độ --fast, rút gọn tối đa
  --parallel: Stage /sk-impl chạy multi-agent song song (Antigravity run_command via Terminal)
  --auto: Tự động approve tất cả gates, không hỏi user
---

# /sk-delivery

**Mục tiêu:** Full delivery flow cho task phức tạp.

## Khi nào dùng

- Task nhiều modules
- Cần plan kỹ trước khi code
- Có risk cao (API contract change, breaking change)
- Cần review đầy đủ 5 layers

## Flow

```text
/sk-clarify → /sk-plan → /sk-impl → /sk-review
```

Mỗi stage chạy đầy đủ theo workflow riêng.

## Output

`../templates/sk-delivery-report.md.template`
