---
id: impl
type: stage
stage-number: 3
entry-command: /sk-impl
next: review
prev: plan
input-from: implementation-plan-lite
output-format: impl-summary
gate-after: gate-2
skills-suggested:
  - core/api-contract-guard
modifiers:
  --fast: Bỏ qua research, code luôn từ context sẵn có, self-check rút gọn
  --tdd: Viết test trước, rồi implement code cho pass tests
  --parallel: Chạy multi-agent song song qua Terminal (Antigravity run_command)
  --no-test: Không bắt buộc test — dùng khi prototype/spike
---

# /sk-impl

**Mục tiêu:** Implement code theo plan đã approved, build verification tự động.

## Input tối thiểu

- Output từ `/sk-plan` (approved)
- Danh sách files/modules cần thay đổi
- Pre-Implementation Quality Card
- Template selection cho từng scope

## Quy trình

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
    - **Dọn dẹp:** Sau khi `/sk-review` hoàn tất (PASS hoặc FAIL), worktree và nhánh tạm này PHẢI được xóa bỏ để giải phóng tài nguyên.
2. **Tẩy Não Cục Bộ (Local Brainwash):** Khi Antigravity điều phối các Sub-agent (qua `gemini-cli`, `opencode-cli`):
    - **Minimal Context:** Chỉ truyền `implementation-plan-lite` và nội dung của **duy nhất** các file cần sửa.
    - **No Chat History:** TUYỆT ĐỐI không gửi kèm lịch sử chat của phiên chính để triệt tiêu bias và ảo giác luỹ kế.

### Bước 3: Implementation & TDD

Agent thực hiện implement theo:

1. Đọc plan đã approved và template tương ứng.
2. **TDD Hybrid:** Viết Unit Test và ép chạy fail (Red) trước khi rờ vào logic chính (đặc biệt với Core Logic).
3. Implement code **bám sát template pattern** để test pass (Green).
4. Đảm bảo naming conventions theo `architecture.md`
5. Không sửa files ngoài scope plan

### Bước 4: Self-Check

Agent tự verify:

- [ ] Code follow template pattern
- [ ] Không vi phạm anti-patterns trong architecture.md
- [ ] Naming conventions đúng
- [ ] Không hardcode text (nếu project yêu cầu i18n)
- [ ] Error handling đúng taxonomy

### Bước 5: Build Verification

Agent chạy build để verify:

```
# Ví dụ BE (.NET)
dotnet build [project path]

# Ví dụ FE (Node)
cd [fe-path] && npm run build
```

- **Build PASS** → sang `/sk-review`
- **Build FAIL** → phân tích error, fix, retry (max 3 lần)

### Bước 6: Dev Done

Kết luận Dev Done khi:

- [ ] Implementation hoàn tất theo plan
- [ ] Build PASS
- [ ] Self-check pass theo quality card
- [ ] API contract status rõ

## Output bắt buộc

- Danh sách thay đổi đã implement
- Build verification result
- Kết quả self-check theo quality card
- `API contract: OK / Risk`
- Danh sách assumptions/blockers (nếu có)

## Template

- Output: `../templates/sk-impl-summary.md.template`

## Gate sau bước này (Gate 2 — Dev Done)

- [ ] Build pass
- [ ] Self-check pass
- [ ] API contract status rõ

## Guardrails

- `/sk-impl` không phải là review step
- Nếu project có `context/templates/`, đây là input bắt buộc
- Build verification là gate bắt buộc, không được skip
- Không mở rộng scope ngoài plan đã approved

> [Terminal Orchestration] Antigravity tự động fan-out tasks cho
> nhiều agents song song bằng cách mở các process ẩn qua `run_command`.
> Xem `addons/swarm/` để biết:
> - Task matrix + assignment rules
> - File conflict policy (không 2 agents cùng sửa 1 file)
> - Cross-agent contracts
> - Fan-in merge + build verify
