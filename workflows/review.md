---
id: review
type: stage
stage-number: 4
entry-command: /review
next: null
prev: impl
input-from: impl-summary
output-format: review-summary
gate-after: gate-3
skills-suggested:
  - core/regression-checklist
  - core/api-contract-guard
---

# /review

**Mục tiêu:** Review code theo 5 layers với tri-state checklist.

## Input tối thiểu

- Output từ `/impl` (impl-summary)
- Changed files list
- Build verification result (PASS required)

## Quy trình

### Bước 1: Chuẩn bị Review Package

Agent tổng hợp:

```
- Changed files list
- Checklist từ /impl
- Architecture rules (từ context/architecture.md)
- Template rules (từ context/templates/)
```

### Bước 2: Review 5 Layers

#### Layer 1 — Checklist Verification
Verify từng item trong impl checklist.
Status: **PASS** / **FAIL** / **UNPLANNED**

#### Layer 2 — Code Existence
Verify code thực sự tồn tại trong files.
Không phải chỉ planned mà chưa code.

#### Layer 3 — Architecture Compliance
So sánh code vs template pattern.
Bắt architecture drift.

#### Layer 4 — Unplanned Code Detection
Phát hiện code CÓ nhưng KHÔNG nằm trong plan/template.
Mark: **UNPLANNED** — cần human review.

#### Layer 5 — Logic & Quality
Kiểm tra logic nghiệp vụ đúng theo requirements.
Kiểm tra error handling, edge cases.

### Bước 3: Tổng Hợp

Agent phân loại findings:

- ✅ **PASS** — Code đúng checklist + đúng architecture
- ❌ **FAIL** — Thiếu code / code sai / vi phạm architecture
- ⚠️ **UNPLANNED** — Có code nhưng không nằm trong plan/template

### Bước 4: Ship Decision

| Điều kiện | Decision |
|---|---|
| 0 FAIL + 0 UNPLANNED | ✅ **Ready** — ship |
| 0 FAIL + có UNPLANNED | ⚠️ **Needs Review** — user review các UNPLANNED items |
| Có FAIL | ❌ **Blocked** — fix required |
| Có Critical finding | ❌ **Blocked** — fix required |

## Output bắt buộc

- Review checklist với 5 layers
- Summary: pass count / fail count / unplanned count
- Ship decision: Ready / Blocked / Needs Review
- Fix suggestions cho FAIL items
- Human review list cho UNPLANNED items

## Template

- Checklist: `../templates/review-checklist.md.template`
- Summary: `../templates/review-summary.md.template`

## Gate sau bước này (Gate 3 — Ship Ready)

- [ ] 0 Critical findings
- [ ] 0 FAIL items (hoặc đã fix)
- [ ] UNPLANNED items đã được user review
- [ ] Ship decision: Ready

## Guardrails

- Review KHÔNG sửa code trực tiếp
- Nếu có FAIL → fix rồi chạy lại review
- Nếu có UNPLANNED → báo user, KHÔNG tự động xóa/sửa

> [Multi-agent] Nếu dùng swarm addon, có thể chạy dual review
> (primary + secondary reviewer). Xem `addons/swarm/`.
