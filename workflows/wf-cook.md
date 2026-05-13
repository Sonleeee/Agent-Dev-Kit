---
id: cook
type: composite
entry-command: /wf-cook
description: Full auto pipeline — clarify → plan → impl → test → review trong 1 lệnh
stages: clarify -> plan -> impl -> test -> review
agents-suggested:
  - planner
  - implementer
  - tester
  - reviewer
modifiers:
  --fast: Mỗi stage chạy --fast, rút gọn tối đa
  --tdd: Test trước code — plan → test → impl → review
  --no-review: Bỏ review step — chỉ build pass là xong
  --no-test: Bỏ test step — impl → review
---

# /wf-cook

**Mục tiêu:** Full auto pipeline — từ task description đến ready-to-commit trong 1 lệnh.

## Khi nào dùng

- Task rõ ràng, muốn đi nhanh end-to-end
- Prototype/spike — cần output nhanh
- Task lặp lại (CRUD, thêm field, thêm endpoint)

## Input

- Task description (1-3 câu)
- Project context đã load (AGENTS.md + context files)

## Pipeline

```text
/wf-cook "thêm field PhoneNumber vào Customer"
  │
  ├─ Step 1: Auto Clarify
  │  └─ Nếu task rõ → skip (clarify-lite 1 câu)
  │  └─ Nếu task mơ hồ → hỏi user tối đa 3 câu
  │
  ├─ Step 1.5: Cook Proposal — Trình User Phê Duyệt
  │  Agent trình bày COOK PROPOSAL:
  │
  │  | Mục | Nội dung |
  │  |---|---|
  │  | **🎯 Task** | [Mô tả task sau clarify] |
  │  | **📐 Approach** | [Hướng tiếp cận chính] |
  │  | **📁 Files ảnh hưởng** | [Danh sách files dự kiến] |
  │  | **🧪 Test plan** | [Sẽ test gì, hoặc SKIP nếu --no-test] |
  │  | **⚠️ Risks** | [Rủi ro nếu có, "Không" nếu không] |
  │
  │  > ⏸️ PAUSE — Chờ user approve.
  │  > Reject → dừng pipeline, quay lại clarify.
  │  > User có thể chỉnh sửa Proposal trước khi approve.
  │
  ├─ Step 2: Auto Plan
  │  └─ Plan-lite: approach + files + template selection
  │  └─ Quality card subset
  │  └─ Gate 1 check (auto-approve nếu đủ)
  │
  ├─ Step 3: Auto Implement
  │  └─ Code theo plan + template
  │  └─ Self-check
  │  └─ Build verify
  │  └─ Gate 2 check
  │
  ├─ Step 4: Auto Test (optional)
  │  └─ Generate test scenarios cho changes
  │  └─ Write + run tests
  │  └─ Report results
  │
  ├─ Step 5: Auto Review
  │  └─ Review-lite: checklist + build + architecture
  │  └─ Ship decision
  │  └─ Gate 3 check
  │
  ├─ Step 6: Knowledge Checkpoint
  │  Áp dụng SYSTEM.md → Brain Writeback Policy
  │  ├─ ASK nếu task sinh lesson/pattern/decision đáng nhớ
  │  │  └─ trình Memory Candidate rồi chờ user duyệt
  │  └─ SKIP nếu chỉ là task thường ngày
  │
  └─ Output: Delivery Report
```

## Flow Control

### Auto-pause conditions

Pipeline tự dừng khi:

- **Clarify needed** — task quá mơ hồ, cần user input
- **Plan conflict** — nhiều approaches, cần user chọn
- **Build fail 3 lần** — agent không tự fix được
- **Review FAIL** — có Critical findings

Khi pause → agent report status + chờ user input → resume.

### Modifier behavior

| Modifier | Thay đổi pipeline |
|---|---|
| `--fast` | Skip clarify, plan-lite 3 dòng, review-lite |
| `--tdd` | Đổi thứ tự: plan → **test → impl** → review |
| `--no-review` | Bỏ Step 5, output sau build pass |
| `--no-test` | Bỏ Step 4, impl → review trực tiếp |

## Output bắt buộc

Delivery report tổng hợp:

```markdown
## 🍳 Cook Report

### Task
[Task description]

### Steps Completed
1. ✅ Clarify — [summary]
2. ✅ Plan — [approach]
3. ✅ Impl — [files changed]
4. ✅ Test — [X pass / Y fail] (hoặc SKIPPED)
5. ✅ Review — [ship decision]

### Files Changed
- [file1] — [change summary]
- [file2] — [change summary]

### Build: PASS
### Tests: X/Y PASS
### Ship Decision: Ready / Blocked

### Ready to commit:
`git add . && git commit -m "feat(module): [description]"`
```

## Guardrails

- `/wf-cook` là shortcut, KHÔNG phải magic — vẫn follow từng stage workflow
- Auto-approve gates CHỈ khi 0 issues — bất kỳ issue nào → pause + ask user
- Nếu task phức tạp (>5 files, nhiều modules) → recommend `/wf-delivery` thay vì `/wf-cook`
- Không swallow errors — mọi failure phải visible trong report
- User có thể interrupt bất kỳ lúc nào → agent dừng + report progress
- TUYỆT ĐỐI không chạy pipeline khi user chưa approve Cook Proposal
- User có thể chỉnh sửa Cook Proposal (thêm/bỏ file, đổi approach) trước khi approve
