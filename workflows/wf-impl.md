---
id: impl
type: stage
stage-number: 3
entry-command: /wf-impl
next: review
prev: plan
input-from: implementation-plan-lite
output-format: impl-summary
gate-after: gate-2
skills-suggested:
  - core/sk-execution-contract
  - core/sk-api-contract-guard
  - core/sk-delegation-validator
  - core/sk-compressed-delegation
modifiers:
  --fast: Bỏ qua research, code luôn từ context sẵn có, self-check rút gọn
  --parallel: Chạy multi-agent song song qua Terminal (Antigravity run_command)
  --no-test: Không bắt buộc test — dùng khi prototype/spike
---

> [!IMPORTANT]
> ## Mandatory Delegation Policy — Đọc TRƯỚC khi bắt đầu
>
> | Điều kiện trong plan | Hành động BẮT BUỘC |
> |:---|:---|
> | Plan có ≥ 2 subtasks ĐỘC LẬP (không sửa cùng file) | **PHẢI** `invoke_subagent(TypeName="self")` cho mỗi subtask, `Workspace="branch"`. Mỗi subagent chỉ nhận plan-lite + file scope |
> | Sau mỗi subtask hoàn thành | **PHẢI** invoke reviewer subagent để chạy spec compliance review |
> | Plan chỉ có 1 task HOẶC các task sửa CÙNG file | Chạy inline. Tự chạy spec compliance checklist trước Dev Done |
> | Modifier `--parallel` được dùng | **PHẢI** delegate qua subagent, KHÔNG chạy tuần tự |
>
> **Subagent context rule:** Chỉ gửi plan-lite + file scope. KHÔNG gửi chat history. Vi phạm = lỗi quy trình.

# /wf-impl

**Mục tiêu:** Implement code theo plan đã approved, build verification tự động.

## Input tối thiểu

- Output từ `/wf-plan` (approved)
- Danh sách files/modules cần thay đổi
- Pre-Implementation Quality Card
- Template selection cho từng scope

## Quy trình

### Bước 0: Resume-safe ledger

Đọc execution contract trước khi implement. Task đã đánh dấu `complete` trong ledger
không được re-dispatch; task đang dở phải tiếp tục từ bước cuối có evidence.

### Bước 1: Load Context

Agent load project context:

- `AGENTS.md` — project identity + tech stack
- `context/architecture.md` — kiến trúc + anti-patterns
- `context/templates/` — code templates (ground truth)
- `context/checklist.md` — checklist riêng (nếu có)

### Bước 2: Chuẩn bị Môi trường & Cách ly

1. **Worktree Isolation:** `git worktree add ../temp-[task_id] [branch] [base]` — Dọn sau review.
2. **Subagent Context (Local Brainwash):** Chỉ gửi plan-lite + file scope. **KHÔNG** gửi chat history. **KHÔNG** gửi file ngoài scope.

> Chi tiết rationale và lệnh mẫu: xem `references/impl-isolation.md`

### Bước 3: Implementation

Agent thực hiện implement theo:

1. Đọc plan đã approved và template tương ứng.
2. Implement code **bám sát template pattern** để đảm bảo tính nhất quán.
3. Đảm bảo naming conventions theo `architecture.md`
4. Không sửa files ngoài scope plan.

### Bước 4: Subtask Delegation & Review

Agent thực hiện CHÍNH XÁC các bước sau:

1. **Routing Decision:** Đếm subtasks trong plan. Các subtasks có sửa CÙNG file không?
2. **Nếu ≥ 2 subtasks ĐỘC LẬP** → Pha A: Parallel Delegation
   - **PHẢI** gọi `invoke_subagent(TypeName="self", Workspace="branch")` cho mỗi subtask
   - Mỗi subagent nhận: plan-lite cho subtask đó + chỉ file cần sửa
   - Sau khi tất cả hoàn thành: **PHẢI** gọi `invoke_subagent(TypeName="self", Role="Spec Reviewer")` để review
3. **Nếu 1 subtask HOẶC sửa cùng file** → Pha B: Inline
   - Implement tuần tự
   - Tự chạy spec compliance checklist trước Dev Done
   - Ghi kết quả review vào ledger

### Bước 5: Self-Check & Reflexion Hook

1. **Reflexion Hook (Tự phản biện nội bộ):** Ngay sau khi code xong, trước khi chạy build, Agent chạy prompt tự phản biện để tìm lỗi logic thô:
   - Check xem có import/using dư thừa không (nếu nghi ngờ, **liệt kê** trong output để user xác nhận trước khi xóa).
   - Kiểm tra xem code có đúng conventions đặt tên (naming conventions) của dự án không.
   - Phát hiện các lỗi cú pháp hoặc gõ nhầm tên thuộc tính/biến (nếu phát hiện, **liệt kê rõ** trong output và chỉ sửa khi user confirm hoặc khi build/lint đã xác nhận lỗi).
2. **Self-Check Checklist:**
   - [ ] Code follow template pattern
   - [ ] Không vi phạm anti-patterns trong architecture.md
   - [ ] Naming conventions đúng
   - [ ] Không hardcode text (nếu project yêu cầu i18n)
   - [ ] Error handling đúng taxonomy
   - [ ] Đã chạy Reflexion và tự động fix hết lỗi thô.

### Bước 6: Build Verification

Agent chạy build để verify:

```bash
# Ví dụ BE (.NET)
dotnet build [project path]

# Ví dụ FE (Node)
cd [fe-path] && npm run build
```

- **Build PASS** → sang `/wf-review`
- **Build FAIL** → phân tích error, fix, retry (max 3 lần)

### Bước 7: Dev Done

Kết luận Dev Done khi:

- [ ] Implementation hoàn tất theo plan
- [ ] Build PASS
- [ ] Self-check pass theo quality card
- [ ] API contract status rõ

### Bước 8: Implementation Knowledge Checkpoint

`/wf-impl` mặc định không ghi tri thức vì implementation summary thường là trạng thái tạm thời:

| Điều kiện | Mode | Hành động |
|-----------|------|-----------|
| Trong lúc implement phát hiện reusable pattern, pitfall, hoặc context drift rõ ràng | `ASK` | Trình Memory Candidate, target `03_Cache/patterns` hoặc `03_Cache/decisions` |
| Không có lesson mới ngoài thay đổi code theo plan | `SKIP` | Không ghi |

Nếu workflow cha là `/wf-delivery`, để workflow cha tổng hợp writeback cuối flow.

## Output bắt buộc

- Danh sách thay đổi đã implement
- Build verification result
- Kết quả self-check theo quality card
- `API contract: OK / Risk`
- Danh sách assumptions/blockers (nếu có)
- Implementation Knowledge Checkpoint: ASK / SKIP

## Template

- Output: `../templates/wf-impl-summary.md.template`

## Gate sau bước này (Gate 2 — Dev Done)

- [ ] Build pass
- [ ] Self-check pass
- [ ] API contract status rõ

## Guardrails

- `/wf-impl` không phải là review step
- Nếu project có `context/templates/`, đây là input bắt buộc
- Build verification là gate bắt buộc, không được skip
- Không mở rộng scope ngoài plan đã approved

## Pre-completion Checklist (PHẢI verify trước khi báo Dev Done)

- [ ] Đã kiểm tra Delegation Policy ở đầu file?
- [ ] Nếu plan có ≥ 2 subtasks độc lập → ĐÃ invoke subagent cho mỗi task?
- [ ] Mỗi subtask ĐÃ qua spec compliance review (subagent hoặc inline)?
- [ ] KHÔNG gửi chat history cho subagent?
- [ ] Build PASS?
- [ ] Self-check pass theo quality card?
