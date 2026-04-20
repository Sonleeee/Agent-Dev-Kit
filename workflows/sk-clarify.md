---
id: clarify
type: stage
stage-number: 1
entry-command: /sk-clarify
next: plan
prev: null
input-from: user
output-format: clarify-record
gate-after: null
skills-suggested:
  - core/business-discovery
---

# /sk-clarify

**Mục tiêu:** Làm rõ đủ để code đúng, không cần analysis dài quá mức cần thiết.

## Khi nào dùng

- Task còn mơ hồ
- Cần hỏi đáp để lộ risk/edge cases
- Bug chưa rõ root cause
- Chưa chắc API contract có đổi không

## Quy trình

### Câu hỏi nhỏ lẻ: Agent xử lý trực tiếp

```
User hỏi -> Agent trả lời / hỏi lại
```

### Yêu cầu research sâu: Agent scan codebase

```
User yêu cầu -> Agent nhận
  Agent scan files liên quan
  Agent phân tích pattern, trả lời chi tiết
  Agent trình User double check
```

### Khi nào cần research sâu:

- Cần scan nhiều files trong codebase
- Cần hiểu pattern hiện tại trước khi plan
- Cần xác định root cause ở bug phức tạp
- Cần kiểm tra API contract có bị ảnh hưởng không

## Output bắt buộc

- Problem statement
- Scope in/out
- Risks và edge cases chính
- Open questions hoặc assumptions
- Root cause layer nếu là bugfix
- `API contract changed: Yes / No / Unknown`

## Template

`../templates/sk-clarify-record.md.template`

## Guardrails

- Không chốt design chi tiết trong bước này
- Không generate task breakdown dài
- Nếu task đã rất rõ, có thể rút gọn thành clarify-lite rồi sang `/sk-plan`

> [Multi-agent] Nếu dùng swarm addon, có thể delegate research
> cho sub-agent chuyên scan codebase. Xem `addons/swarm/`.
