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
modifiers:
  --fast: Bỏ qua research, code luôn từ context sẵn có, self-check rút gọn
  --parallel: Chạy multi-agent song song qua Terminal (Antigravity run_command)
  --no-test: Không bắt buộc test — dùng khi prototype/spike
---

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

### Bước 2: Chuẩn bị Môi trường & Cách ly (Superpowers Isolation)

1. **Git Worktree Isolation:** AI thực hiện task trên một phân vùng độc lập để bảo vệ mã nguồn chính.
    - Lệnh khởi tạo: `git worktree add ../temp-[task_id] [branch_name] [base_branch]`
    - **Lợi ích:** Tránh xung đột file với User, tạo sandbox an toàn cho AI thực thi các lệnh build/test.
    - **Dọn dẹp:** Sau khi `/wf-review` hoàn tất (PASS hoặc FAIL), worktree và nhánh tạm này PHẢI được xóa bỏ để giải phóng tài nguyên.
2. **Tẩy Não Cục Bộ (Local Brainwash):** Khi Antigravity điều phối các Sub-agent (qua `gemini-cli`, `opencode-cli`):
    - **Minimal Context:** Chỉ truyền `implementation-plan-lite` và nội dung của **duy nhất** các file cần sửa.
    - **No Chat History:** TUYỆT ĐỐI không gửi kèm lịch sử chat của phiên chính để triệt tiêu bias và ảo giác luỹ kế.

### Bước 3: Implementation

Agent thực hiện implement theo:

1. Đọc plan đã approved và template tương ứng.
2. Implement code **bám sát template pattern** để đảm bảo tính nhất quán.
3. Đảm bảo naming conventions theo `architecture.md`
4. Không sửa files ngoài scope plan.

### Bước 4: Subtask review và Self-Check

Với task độc lập có subagent: review spec compliance trước, rồi review code quality.
Nếu host không có subagent, agent tự chạy hai checklist tuần tự và ghi kết quả vào
ledger trước khi chuyển task kế tiếp.

### Bước 5: Self-Check & Reflexion Hook

1. **Reflexion Hook (Tự phản biện nội bộ):** Ngay sau khi code xong, trước khi chạy build, Agent chạy prompt tự phản biện để tìm lỗi logic thô:
   - Check xem có import/using dư thừa không (nếu có, tự xóa).
   - Kiểm tra xem code có đúng conventions đặt tên (naming conventions) của dự án không.
   - Phát hiện các lỗi cú pháp hoặc gõ nhầm tên thuộc tính/biến (nếu phát hiện, tự động sửa đổi ngay).
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
