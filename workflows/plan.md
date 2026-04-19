---
id: plan
type: stage
stage-number: 2
entry-command: /plan
next: impl
prev: clarify
input-from: clarify-record
output-format: implementation-plan-lite
gate-after: gate-1
skills-suggested:
  - core/solution-planning
modifiers:
  --fast: Bỏ qua phân tích sâu, plan-lite 3-5 dòng, không quality card chi tiết
  --deep: Research kỹ trước khi plan — đọc thêm docs, tìm precedent trong codebase
  --auto: Tự động approve plan, không hỏi user confirmation
---

# /plan

**Mục tiêu:** Chốt approach, chọn template, xác định scope thay đổi.

## Input tối thiểu

- Output từ `/clarify` (hoặc clarify-lite)
- Project context đã load (architecture.md, templates/)

## Quy trình

### Bước 1: Phân tích scope

Agent xác định:

- Modules/files bị ảnh hưởng
- Pattern nào cần follow (từ `context/templates/`)
- Dependencies và side effects

### Bước 2: Chọn approach

Agent đề xuất:

- Approach chính (1 câu rõ ràng)
- Template selection cho từng scope (BE/FE)
- Task breakdown theo thứ tự
- Test obligations

### Bước 3: Quality Card

Tạo Pre-Implementation Quality Card:

- Checklist subset phù hợp với task
- API contract risk assessment
- Known pitfalls liên quan

## Output bắt buộc

- Approach (1 câu)
- Impacted files/modules list
- Template selection
- Task breakdown (theo thứ tự)
- Pre-Implementation Quality Card
- `API contract risk: None / Low / High`

## Template

`../templates/implementation-plan-lite.md.template`

## Gate sau bước này (Gate 1 — Ready)

- [ ] Problem statement rõ
- [ ] Scope in/out xác định
- [ ] Plan có thứ tự task
- [ ] Quality card tồn tại

## Guardrails

- Plan phải bounded — không mở rộng scope ngoài yêu cầu
- Template selection là bắt buộc nếu project có `context/templates/`
- Nếu task đơn giản, plan có thể rút gọn thành plan-lite (3–5 dòng)
