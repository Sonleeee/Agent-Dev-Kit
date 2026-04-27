---
id: review
type: stage
stage-number: 4
entry-command: /wf-review
next: null
prev: impl
input-from: impl-summary
output-format: review-summary
gate-after: gate-3
skills-suggested:
  - core/sk-regression-checklist
  - core/sk-api-contract-guard
modifiers:
  --fast: Review-lite — checklist subset, bỏ Layer 4 (Unplanned), quick ship decision
  --deep: Full 5-layer review + kiểm tra cross-module impact
  --auto: Tự động approve nếu 0 FAIL, không hỏi user cho UNPLANNED items
  --red-team: Bổ sung Layer 6 — 4 adversarial personas (Security, Failure Mode, Assumption, Scope)
agents-suggested:
  - reviewer
  - red-team
---

# /wf-review

**Mục tiêu:** Review code theo 5 layers với tri-state checklist.

## Input tối thiểu

- Output từ `/wf-impl` (impl-summary)
- Changed files list (Chỉ file diff)
- Build verification result (PASS required)

> **[QUAN TRỌNG] TẨY NÃO REVIEWER (CONTEXT ISOLATION):** 
> Process Agent chạy Review LÀ MỘT INSTANCE HOÀN TOÀN MỚI. 
> - **Tuyệt đối:** KHÔNG ĐƯỢC NẠP LỊCH SỬ CHAT của bước Plan/Impl.
> - **Chỉ nạp:** Code Diff, Implementation Plan ban đầu, và Bộ Rules chuẩn của dự án.
> - **Mục tiêu:** Đảm bảo tính khách quan cao nhất, triệt tiêu ảo giác luỹ kế từ các bước trước.

## Quy trình

### Bước 1: Chuẩn bị Review Package

Agent tổng hợp:

```
- Changed files list
- Checklist từ /wf-impl
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

- Checklist: `../templates/wf-review-checklist.md.template`
- Summary: `../templates/wf-review-summary.md.template`

## Gate sau bước này (Gate 3 — Ship Ready)

- [ ] 0 Critical findings
- [ ] 0 FAIL items (hoặc đã fix)
- [ ] UNPLANNED items đã được user review
- [ ] Ship decision: Ready

## Guardrails

- Review KHÔNG sửa code trực tiếp
- Nếu có FAIL → fix rồi chạy lại review
- Nếu có UNPLANNED → báo user, KHÔNG tự động xóa/sửa

> [Terminal Orchestration] Antigravity tự động mở nhiều Terminal process
> chạy dual review (primary + secondary reviewer) song song. Xem `addons/swarm/`.
