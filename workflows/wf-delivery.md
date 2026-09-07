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

## Knowledge Checkpoint

`/wf-delivery` không ghi từng stage riêng lẻ. Sau khi `/wf-review` kết thúc, agent tổng hợp writeback theo `SYSTEM.md` → Brain Writeback Policy:

| Điều kiện | Mode | Hành động |
|-----------|------|-----------|
| Review tạo AUTO checkpoint hoặc delivery sinh architecture decision | `AUTO` | Nếu Knowledge addon bật, gọi `sk-vault-steward` một lần với summary cuối flow; nếu không thì report `SKIP` |
| Task có lesson/pattern đáng nhớ nhưng không critical | `ASK` | Trình Memory Candidate |
| Task thường ngày, không có lesson mới | `SKIP` | Không ghi |

Nội dung ghi tối đa:
- Task objective
- Decision/pattern/lesson mới
- Files/modules liên quan
- Verification result
- Link tới review/fix finding nếu có

## Output

`../templates/wf-delivery-report.md.template`
