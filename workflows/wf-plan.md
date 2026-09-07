---
id: plan
type: stage
stage-number: 2
entry-command: /wf-plan
next: impl
prev: clarify
input-from: clarify-record
output-format: implementation-plan-lite
gate-after: gate-1
skills-suggested:
  - core/sk-execution-contract
  - core/sk-solution-planning
  - core/sk-sdd
modifiers:
  --fast: Bỏ qua phân tích sâu, plan-lite 3-5 dòng, không quality card chi tiết
  --deep: Research kỹ trước khi plan — đọc thêm docs, tìm precedent trong codebase
  --auto: Tự động approve plan, không hỏi user confirmation
---

# /wf-plan

**Mục tiêu:** Chốt approach, chọn template, xác định scope thay đổi.

## Input tối thiểu

- Output từ `/wf-clarify` (hoặc clarify-lite)
- Project context đã load (architecture.md, templates/)

## Quy trình

### Bước 0: Execution Contract

Tạo hoặc cập nhật `.agents/runtime/<task-id>/execution-contract.md`. Ghi objective,
scope in/out, acceptance criteria, risk, context pack và lệnh verify dự kiến.

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

Trước khi chốt approach, chạy **Minimality Checkpoint**: reuse pattern hiện có →
standard library/native → dependency đã cài → mới cân nhắc abstraction/dependency mới.

### Bước 3: Quality Card

Tạo Pre-Implementation Quality Card:

- Checklist subset phù hợp với task
- API contract risk assessment
- Known pitfalls liên quan

### Bước 4: Decision Checkpoint

Áp dụng `SYSTEM.md` → Brain Writeback Policy.

| Điều kiện | Mode | Hành động |
|-----------|------|-----------|
| Plan chốt architecture decision, library mới, API contract lớn, hoặc migration approach | `ASK` | Trình Memory Candidate với `type: decision`, target `03_Cache/decisions` |
| Plan chỉ chia task thực thi thông thường | `SKIP` | Không ghi |

### Bước 5: SDD Gate (Spec-Driven Development)

Đối với các task phức tạp (có thay đổi DB, thêm API, đổi logic luồng chính hoặc cấu trúc dữ liệu):
1. Agent gọi `sk-sdd` để lập thiết kế kỹ thuật (Technical Spec) chi tiết.
2. Ghi nhận spec vào file `[project-root]/.agents/sdd/design_spec.md`.
3. Trình Spec cho User và dừng lại chờ User duyệt (Approved/Proceed) mới chuyển sang `/wf-impl`.

## Output bắt buộc

- Approach (1 câu)
- Impacted files/modules list
- Template selection
- Task breakdown (theo thứ tự)
- Pre-Implementation Quality Card
- `API contract risk: None / Low / High`
- Technical Spec file (`.agents/sdd/design_spec.md`) nếu có
- Decision Checkpoint: ASK / SKIP nếu có quyết định đáng lưu

## Template

`../templates/implementation-plan-lite.md.template`

## Gate sau bước này (Gate 1 — Ready)

- [ ] Problem statement rõ
- [ ] Scope in/out xác định
- [ ] Plan có thứ tự task
- [ ] Mỗi task bounded, có file/symbol và bước verify độc lập
- [ ] Quality card tồn tại
- [ ] Technical Spec (`design_spec.md`) đã được tạo và User approved (nếu task phức tạp)

## Guardrails

- Plan phải bounded — không mở rộng scope ngoài yêu cầu
- Template selection là bắt buộc nếu project có `context/templates/`
- Không dùng placeholder kiểu `TBD`, `TODO`, hoặc “implement later” trong plan
- Nếu task đơn giản, plan có thể rút gọn thành plan-lite (3–5 dòng)
