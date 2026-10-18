# Agent System — Agent-Dev-Kit

Bộ agent dùng chung cho mọi project và mọi platform/IDE.

## Cách hoạt động

```text
.agents/ (KIT — clone từ repo)
    ├── rules/          ← Global rules & Executable gates
    ├── skills/         ← Skills tái sử dụng
    ├── workflows/      ← Các workflow chuẩn (/wf-clarify, /wf-plan, /wf-impl, /wf-review...)
    ├── agents/         ← System agent personas
    ├── templates/      ← Output & Contract templates
    ├── schemas/        ← Database schemas (evolution.db)
    ├── tools/          ← CLI tools (evolution_db.py, validate-kit.ps1)
    ├── config/         ← Config templates
    └── addons/         ← Mở rộng tùy chọn (codegraph, archify, database...)

[project-root]/
    ├── AGENTS.md       ← "Passport" của project (tech stack, conventions, reference modules)
    └── .agents/
        ├── runtime/    ← Execution contracts & task ledgers
        └── developer.local.md ← (Tùy chọn) Override style cá nhân cho riêng repo này

~/.agents/ (User Home)
    └── developer.md    ← Global Developer Profile (Gu code, tone áp dụng cho MỌI repo)
```

## Luồng agent khi nhận task

### Thứ tự workflow chuẩn:
```text
/wf-clarify -> /wf-plan -> /wf-impl -> /wf-review
```

### Pre-flight Context Resolution (Nạp ngữ cảnh trước khi hành động):
1. **Global Guardrails:** `rules/global.md` (Tối cao: Executable gates, Hard invariants, Zero-warning).
2. **Project Pattern:** `[project-root]/AGENTS.md` (Stack, Reference modules, Team conventions).
3. **Developer Profile (Personal Style):**
   - Đọc `.agents/developer.local.md` nếu có (Local override cho repo này).
   - Nếu không có: Đọc `~/.agents/developer.md` hoặc `%USERPROFILE%\.agents\developer.md` (Global Profile).
4. **Codebase Intelligence:** Gọi CodeGraph (`mcp__codegraph.codegraph_explore` / `codegraph_node`) để lấy AST và Ground Truth code patterns thực tế.
5. **Task Execution Contract:** Khóa scope, invariants và verification command vào `.agents/runtime/<task-id>/execution-contract.md`.

### Thứ tự ưu tiên giải quyết xung đột (Conflict Resolution Priority):
$$\text{Global Guardrails (Tối cao)} > \text{Project Conventions (Team)} > \text{Developer Personal Style (Cá nhân)} > \text{Agent Default}$$

### Execution Contract — Always-On

Đây là lớp bắt buộc để agent không “trôi” khỏi yêu cầu sau nhiều lượt hoặc sau
context compaction. Chi tiết nằm ở `skills/core/sk-execution-contract/SKILL.md`.

Trước hành động đầu tiên của task có thay đổi, agent phải:

1. Đọc `AGENTS.md`, `SYSTEM.md`, `rules/global.md` và `context/manifest.md` nếu có.
2. Chọn workflow/skill phù hợp và nêu ngắn mục đích.
3. Tạo execution contract trong `.agents/runtime/<task-id>/` với objective, scope,
   acceptance criteria, risk, context pack và verification commands.
4. Giữ progress ledger; khi resume sau compaction đọc ledger trước và không chạy lại
   task đã complete.

Mỗi task implementation phải có bước verify độc lập. Chỉ báo `READY` khi có
acceptance evidence, changed files, unplanned-change decision và review result.

### Skill routing trước hành động

Agent phải kiểm tra skill/workflow liên quan trước khi hỏi, đọc code hoặc sửa file.
Nếu host không hỗ trợ invocation tự động, dùng skill markdown tương ứng như SOP và
ghi tên skill vào execution contract. User instruction luôn có quyền ưu tiên cao nhất.

### Plan và subtask contract

Plan nhiều bước phải chia thành task bounded, có file/symbol, output và lệnh verify cụ
thể; không dùng placeholder kiểu “implement later”. Khi task độc lập, dùng fresh
subagent với context tối thiểu; sau mỗi subtask chạy **spec compliance review** rồi
**code quality review**. Không fan-out nếu các task cùng sửa một file hoặc contract
chưa rõ. Host không có subagent thì chạy inline theo cùng contract và review gates.

### Minimality checkpoint

Trước khi thêm abstraction/dependency, agent phải kiểm tra: có cần tồn tại không,
đã có helper/pattern chưa, standard library/native feature có đủ không, và cách nào
ít file/state nhất. Không được giản lược validation ở trust boundary, security,
accessibility, error handling chống mất dữ liệu hoặc yêu cầu user nêu rõ.

### CodeGraph-First Scout

Khi task cần đọc, hiểu, sửa, review hoặc debug source code, agent phải scout bằng CodeGraph trước khi dùng công cụ đọc/tìm truyền thống:

1. Dùng `mcp__codegraph.codegraph_explore` cho feature/flow/khu vực code liên quan.
2. Dùng `mcp__codegraph.codegraph_node` khi đã biết file hoặc symbol cụ thể cần đọc.
3. Dùng `mcp__codegraph.codegraph_callers` để phân tích impact trước khi đổi behavior, signature, hoặc contract.
4. Chỉ fallback sang `rg`, `Get-Content`, `ls`, `find` khi CodeGraph không phù hợp: docs/config/assets, literal text/i18n key, git diff/status, hoặc file chưa được index.

Output từ CodeGraph có source hiện tại thì được xem như đã đọc file; không đọc lại cùng nội dung bằng tool khác nếu không có lý do rõ ràng.

## Flow chuẩn

Flow ưu tiên:

```text
/wf-clarify -> /wf-plan -> /wf-impl -> /wf-review
```

Shortcut:

- `/wf-delivery --fast` — task rõ ràng, đi nhanh
- `/wf-delivery` — task cần plan và verification đầy đủ

## Auto-Route (Intent → Workflow)

Khi user mô tả task bằng ngôn ngữ tự nhiên (không gõ `/wf-`),
agent phân loại intent và chọn workflow phù hợp.
Agent **THÔNG BÁO** cho user workflow đang dùng trước khi bắt đầu.

| Tín hiệu từ user | Workflow |
|---|---|
| fix, bug, lỗi, crash, exception, sai | `/wf-fix` |
| thêm, tạo mới, feature, implement | `/wf-delivery` |
| refactor, optimize, cải thiện | `/wf-clarify` → `/wf-plan` → `/wf-impl` |
| nghiên cứu, research, tìm hiểu | `/wf-research` |
| review, kiểm tra code | `/wf-review` |
| test, viết test | `/wf-test` |
| deploy, release | `/wf-deploy` |
| commit, PR, changelog | `/wf-git` |
| trạng thái, đang làm gì | `/wf-status` |

> Nếu intent không rõ → hỏi user. Không đoán bừa.

## Mode Modifiers

Nhiều workflows hỗ trợ mode modifiers để điều chỉnh hành vi:

| Modifier | Ý nghĩa | Dùng ở |
|---|---|---|
| `--fast` | Rút gọn, bỏ bước không critical | plan, impl, review, delivery |
| `--deep` | Research kỹ, kiểm tra sâu | plan, review, predict |
| `--auto` | Tự approve gates, không hỏi user | plan, review, delivery |
| `--tdd` | Viết test trước rồi code | impl, delivery |
| `--parallel` | Multi-agent song song (cần swarm) | impl, delivery |
| `--no-test` | Bỏ test obligations | impl, delivery |
| `--red-team` | Adversarial review 4 personas | review |
| `--no-review` | Bỏ review step | cook |
| `--compare` | Chỉ so sánh, không port code | xia |
| `--port` | Lấy ý tưởng, code lại (default) | xia |
| `--copy` | Bê nguyên structure, adapt naming | xia |
| `--improve` | Copy + refactor + best practices | xia |
| `--period` | Chỉ định khoảng thời gian phân tích | retro |
| `--team` | Focus phân tích theo contributor | retro |
| `--churn` | Focus files thay đổi nhiều nhất | retro |
| `--full` | Phân tích đầy đủ tất cả dimensions | retro |

Cách dùng: `/wf-impl --fast` hoặc `/wf-delivery --parallel --auto`

## Gates

### Gate 1 — Ready (sau /wf-plan)

Không code nếu thiếu:

- Problem statement rõ
- Scope in/out
- Plan theo thứ tự
- Quality card
- Task assignment rõ (nếu multi-agent)

### Gate 2 — Dev Done (sau /wf-impl)

Không review nếu thiếu:

- Build pass
- Self-check pass
- API contract status rõ

### Gate 3 — Ship Ready (sau /wf-review)

Blocked nếu:

- Còn finding Critical
- Còn FAIL items chưa fix
- UNPLANNED items chưa được user review

## Phân loại skills

| Nhóm | Mô tả | Cần project context? |
|---|---|---|
| `core/` | Discovery, planning, execution contract, guard, regression | Không |
| `meta/` | Tạo/cải thiện agent system | Không |
| `devops/` | CI/CD pipeline, Docker review | Không |
| `security/` | OWASP scan, secret detection | Không |
| `testing/` | Test strategy, scenario generation | Tùy chọn |
| `research/` | Docs lookup, document parsing, pattern research | Không |

> Context cache, vault writeback, database inspection, kit maintenance và
> **self-evolution** nằm trong các addon tùy chọn dưới `addons/`;
> core không yêu cầu chúng để chạy delivery.

> **Ghi chú:** Domain skills (backend/frontend) không nằm trong core kit.
> Mỗi project tự tạo domain skills riêng trong `.agents/context/` hoặc repo riêng.

## Workflows

### Stage pipeline (core flow)

| Workflow | Mô tả | Gate |
|---|---|---|
| `/wf-clarify` | Thu thập requirements, xác nhận scope | — |
| `/wf-plan` | Chốt approach, chọn template | Gate 1 |
| `/wf-impl` | Implement code theo plan | Gate 2 |
| `/wf-review` | Review 5-layer, ship decision | Gate 3 |

### Shortcuts & Auto-pipeline

| Workflow | Mô tả |
|---|---|
| `/wf-delivery` | Full flow: clarify → plan → impl → review |
| `/wf-delivery` | Full flow; dùng `--fast` cho task nhỏ và `--deep` cho task rủi ro cao |

### Utilities

| Workflow | Mô tả |
|---|---|
| `/wf-enhance` | Enhancement/refactor có chủ đích |
| `/wf-deploy` | Deploy checklist |
| `/wf-fix` | Debug pipeline: scout → diagnose → fix → verify → prevent |
| `/wf-test` | Generate & run tests cho module |
| `/wf-docs` | Generate/update documentation |
| `/wf-git` | Git commit messages, PR descriptions, changelog |
| `/wf-security` | Security scan: OWASP, secrets, auth review |
| `/wf-research` | Research docs, best practices, compare approaches |

### Advanced

| Workflow | Mô tả |
|---|---|
| `/wf-xia` | Port features từ external repos (compare/port/copy/improve) |
| `/wf-retro` | Sprint retrospective: git metrics → health scores → action items |

## Nếu project chưa có AGENTS.md

Agent chạy ở generic mode:

- Dùng global rules
- Hỏi user về context cần thiết
- Gợi ý onboard project bằng `templates/AGENTS.md.template` và khởi tạo `.agents/context/`

## System Agents

Kit cung cấp 6 agent personas trong `agents/`. Mỗi agent là 1 `AGENT.md` chứa persona, skills, và quy trình riêng.

| Agent | Role | Khi nào dùng |
|---|---|---|
| `planner` | Lập plan, phân tích scope, chọn approach | `/wf-clarify`, `/wf-plan` |
| `implementer` | Code theo plan, bám sát template | `/wf-impl` |
| `reviewer` | Review 4-layer, severity-based, ship decision | `/wf-review` |
| `debugger` | Debug root cause, không patch bừa | `/wf-fix` |
| `tester` | Generate tests, coverage analysis | `/wf-test` |
| `red-team` | 4 adversarial personas tấn công code | `/wf-review --red-team` |

**IDE-agnostic:** `AGENT.md` chỉ chứa persona + instructions dạng markdown.
- IDE hỗ trợ subagent → tự invoke agent phù hợp
- IDE không hỗ trợ → user copy persona prompt thủ công
- Swarm setup → xem `addons/swarm/README.md`

## Tiered Context Loading

Khi project có `architecture.md` theo TIER format, agent load theo nhu cầu:

| Tier | Nội dung | Load khi nào | Token ước tính |
|------|---------|-------------|:--------------:|
| **TIER-0** | Core rules, naming, folder, anti-pattern index | Luôn luôn | ≤1,000 |
| **TIER-1** | Pattern detail theo [TAG] | Theo task-feature | ~500-1,000 |
| **TIER-2** | Full examples, decision tree, legacy notes | On-demand | ~0-2,000 |

### Loading Protocol

```
1. LUÔN đọc TIER-0 (≤200 lines)
2. Xác định task-feature → tìm [TAG] phù hợp → đọc TIER-1 section đó
3. Chỉ đọc TIER-2 khi:
   - Cần ✅/❌ code examples
   - Cần decision tree cho pattern có variants
   - Cần kiểm tra baseline modules
```

> Nếu `architecture.md` CHƯA theo TIER format → đọc toàn bộ (fallback).

---

## Truth Hierarchy & Resolution

### Truth Resolution Order (Thứ tự chân lý):

1. 🥇 **Executable Verification:** Build/Tests/Linters thực tế đang chạy trên máy (Zero-warning).
2. 🥈 **CodeGraph Intelligence:** Đồ thị AST, quan hệ hàm (call graph) và symbol relationships thực tế của codebase.
3. 🥉 **Project Conventions:** File `AGENTS.md` (Passport và reference modules).
4. 🏅 **Developer Profile:** `~/.agents/developer.md` hoặc `.agents/developer.local.md`.

### Khi có xung đột:
- Global Guardrails luôn thắng Project Conventions.
- Project Conventions luôn thắng Developer Personal Style.
- Nếu code thực tế mâu thuẫn với yêu cầu trong task: Trình **Conflict Report** cho user (xem `templates/conflict-report.md.template`).

---

## Addon Hooks

Các addon (obsidian, codegraph, database...) có thể mở rộng workflow bằng hook riêng.
Xem `addons/<tên>/README.md` để biết chi tiết.

---

## Multi-Agent (tùy chọn)

> Nếu IDE/tool hỗ trợ multi-agent (swarm, sub-agents...):
> Xem `addons/swarm/README.md` để biết cách thiết lập orchestration,
> routing rules, payload contracts, và file conflict policy.
