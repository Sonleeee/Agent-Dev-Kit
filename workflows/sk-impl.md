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
  --parallel: Chạy multi-agent song song (cần swarm addon)
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

### Bước 2: Implementation

Agent thực hiện implement theo:

1. Đọc plan đã approved
2. Chọn đúng template từ `context/templates/` cho từng file
3. Implement code **bám sát template pattern**
4. Đảm bảo naming conventions theo `architecture.md`
5. Không sửa files ngoài scope plan

### Bước 3: Self-Check

Agent tự verify:

- [ ] Code follow template pattern
- [ ] Không vi phạm anti-patterns trong architecture.md
- [ ] Naming conventions đúng
- [ ] Không hardcode text (nếu project yêu cầu i18n)
- [ ] Error handling đúng taxonomy

### Bước 4: Build Verification

Agent chạy build để verify:

```
# Ví dụ BE (.NET)
dotnet build [project path]

# Ví dụ FE (Node)
cd [fe-path] && npm run build
```

- **Build PASS** → sang `/sk-review`
- **Build FAIL** → phân tích error, fix, retry (max 3 lần)

### Bước 5: Dev Done

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

> [Multi-agent] Nếu dùng swarm addon, có thể fan-out tasks cho
> nhiều agents song song. Xem `addons/swarm/` để biết:
> - Task matrix + assignment rules
> - File conflict policy (không 2 agents cùng sửa 1 file)
> - Cross-agent contracts
> - Fan-in merge + build verify
