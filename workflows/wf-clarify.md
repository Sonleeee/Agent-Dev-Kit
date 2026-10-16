---
id: clarify
type: stage
stage-number: 1
entry-command: /wf-clarify
next: plan
prev: null
input-from: user
output-format: clarify-record
gate-after: null
skills-suggested:
  - core/sk-business-discovery
  - core/sk-agile-ba
---

# /wf-clarify

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

### Yêu cầu phân tích nghiệp vụ sâu: Agent gọi sk-agile-ba

```
User mô tả feature mới / epic lớn → Agent gọi sk-agile-ba
  Agent chạy 5 Whys Elicitation để bóc tách yêu cầu gốc
  Agent kiểm tra Solution Bias
  Agent lập PRD, tính RICE, viết User Story chuẩn INVEST
  Agent trình User review & approve
```

### Khi nào cần phân tích nghiệp vụ sâu:

- User mô tả feature mới phức tạp hoặc epic nhiều user story
- Cần tạo PRD / User Story / Acceptance Criteria chuẩn BDD
- Yêu cầu mơ hồ, có dấu hiệu Solution Bias (user đề xuất giải pháp thay vì mô tả vấn đề)
- Cần đánh giá ưu tiên tính năng (RICE scoring)

## Output bắt buộc

- Problem statement
- Scope in/out
- Risks và edge cases chính
- Open questions hoặc assumptions
- Root cause layer nếu là bugfix
- `API contract changed: Yes / No / Unknown`

## Template

`../templates/wf-clarify-record.md.template`

## Guardrails

- Không chốt design chi tiết trong bước này
- Không generate task breakdown dài
- Nếu task đã rất rõ, có thể rút gọn thành clarify-lite rồi sang `/wf-plan`

> [Terminal Orchestration] Antigravity có thể mở Terminal delegate research
> cho sub-agent chuyên scan codebase (ví dụ codex-cli). Xem `addons/swarm/`.
