---
id: delivery
type: shortcut
entry-command: /delivery
stages: clarify -> plan -> impl -> review
description: Task phức tạp — full flow
modifiers:
  --fast: Mỗi stage chạy ở chế độ --fast, rút gọn tối đa
  --parallel: Stage /impl chạy multi-agent song song (cần swarm addon)
  --auto: Tự động approve tất cả gates, không hỏi user
---

# /delivery

**Mục tiêu:** Full delivery flow cho task phức tạp.

## Khi nào dùng

- Task nhiều modules
- Cần plan kỹ trước khi code
- Có risk cao (API contract change, breaking change)
- Cần review đầy đủ 5 layers

## Flow

```text
/clarify → /plan → /impl → /review
```

Mỗi stage chạy đầy đủ theo workflow riêng.

## Output

`../templates/delivery-report.md.template`
