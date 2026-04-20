---
id: cook
type: composite
entry-command: /sk-cook
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

# /sk-cook

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
/sk-cook "thêm field PhoneNumber vào Customer"
  │
  ├─ Step 1: Auto Clarify
  │  └─ Nếu task rõ → skip (clarify-lite 1 câu)
  │  └─ Nếu task mơ hồ → hỏi user tối đa 3 câu
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

- `/sk-cook` là shortcut, KHÔNG phải magic — vẫn follow từng stage workflow
- Auto-approve gates CHỈ khi 0 issues — bất kỳ issue nào → pause + ask user
- Nếu task phức tạp (>5 files, nhiều modules) → recommend `/sk-delivery` thay vì `/sk-cook`
- Không swallow errors — mọi failure phải visible trong report
- User có thể interrupt bất kỳ lúc nào → agent dừng + report progress
