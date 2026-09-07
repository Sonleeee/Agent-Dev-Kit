# Agent System — Agent-Dev-Kit

Bộ agent dùng chung cho mọi project và mọi platform/IDE.

## Cách hoạt động

```text
.agents/ (KIT — clone từ repo)
    ├── rules/          ← Quality gates chung
    ├── skills/         ← Skills tái sử dụng
    ├── workflows/      ← Các workflow chuẩn
    ├── agents/         ← System agent personas
    ├── quality/        ← Master checklists
    ├── templates/      ← Output templates
    ├── registry/       ← Project type registry
    ├── _project-template/ ← Template cho project mới
    └── addons/         ← Mở rộng tùy chọn (swarm, obsidian...)

[project-root]/
    ├── AGENTS.md       ← "Passport" của project
    └── .agents/context/
        ├── manifest.md          ← Context map L0
        ├── architecture.md   ← Kiến trúc project
        ├── checklist.md      ← Checklist riêng
        └── templates/        ← Code templates
```

## Luồng agent khi nhận task

1. Đọc `AGENTS.md` ở project root
2. Tra `registry/index.md`
3. Load `rules/global.md`
4. Load `.agents/context/manifest.md` nếu có
5. Load `.agents/context/architecture.md` theo TIER-1 tag liên quan
6. Load `.agents/context/templates/*` nếu có
7. Chọn workflow phù hợp và ghi vào execution contract

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
| NLM, notebook, sync | `/wf-vault-sync` |
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

> Context cache, vault writeback, database inspection và kit maintenance nằm trong
> các addon tùy chọn dưới `addons/`; core không yêu cầu chúng để chạy delivery.

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
- Gợi ý onboard project bằng `_project-template/`

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

## Truth Hierarchy — Dual Mode

### Lookup Order (tìm thông tin ở đâu trước? → tiết kiệm token)

1. 🥇 `SecondBrain/03_Cache/` — cached analysis (nếu có, check TTL)
2. 🥈 `.agents/context/` — tóm tắt rules, đã curate
3. 🥉 Code thực tế — ground truth nhưng tốn token

### Review Priority (check pattern compliance theo thứ tự nào?)

1. 🥇 Code mới impl (diff) — subject đang review
2. 🥈 `.agents/context/` — tiêu chuẩn check

### Khi có Conflict (Code ≠ Context)

- KHÔNG tự quyết định
- Luôn trình **Conflict Report** cho user (xem `templates/conflict-report.md.template`)
- User chọn: Fix code / Update context / Keep both + tag [Legacy]

---

## Brain Writeback Policy

SecondBrain là lớp trí nhớ dài hạn. Agent-Dev-Kit chỉ ghi lại tri thức đã chưng cất, không ghi mọi trạng thái tạm thời của session.

### Vault Discovery

Khi workflow cần ghi về SecondBrain:

1. Đọc `AGENTS.md` của project hiện tại.
2. Tìm `vault-path` trong section Integrations.
3. Verify vault có `00_Raw/`, `01_Wiki/`, `02_Brain/`.
4. Nếu thiếu `vault-path` hoặc verify fail → hỏi user trước khi ghi.

### Writeback Levels

| Level | Khi dùng | Hành vi |
|---|---|---|
| **AUTO** | Root cause đã xác nhận, bug/pitfall lặp, architecture decision, context drift đã approved, pattern có thể tái sử dụng | Nếu bật Knowledge addon thì gọi `sk-vault-steward` hoặc `sk-context-cache`; nếu không thì report `SKIP` |
| **ASK** | Research summary, delivery summary, prediction/debate, plan có quyết định chưa chắc chắn | Tạo Memory Candidate và hỏi user trước khi ghi |
| **SKIP** | Status tạm thời, raw command output, progress nhỏ, failed attempt không có lesson rõ | Không ghi |

### Default Workflow Policy

| Workflow/Skill | Default | Ghi gì |
|---|---|---|
| `/wf-fix` | AUTO nếu root cause confirmed | root cause, prevention, bug pattern |
| `/wf-review` | AUTO nếu có Critical/Major hoặc repeated finding; ASK nếu review clean nhưng có insight | review pattern, architecture violation, drift |
| `/wf-retro` | AUTO | health insight, hotspot, action items |
| `sk-context-cache` (Knowledge addon) | AUTO khi trigger cache match | pattern/review/decision cache |
| `/wf-research` | ASK | sourced research finding hoặc decision record |
| `/wf-plan` | ASK nếu có architecture decision | decision rationale |
| `/wf-status`, `/wf-test`, `/wf-git`, `/wf-clarify` | SKIP mặc định | chỉ ghi nếu workflow phát hiện lesson rõ và nâng lên ASK |

### Memory Candidate Format

Khi chưa chắc có nên ghi, agent trình user một candidate ngắn:

```markdown
## Memory Candidate
- Type: bugfix | research | review | implementation | retro | decision | pattern
- Value: AUTO | ASK
- Title: ...
- Summary: ...
- Evidence: files/sources/commands
- Suggested target: 00_Raw + 01_Wiki | 03_Cache/patterns | 03_Cache/reviews | 03_Cache/decisions | 02_Brain/log.md
```

---

## Multi-Agent (tùy chọn)

> Nếu IDE/tool hỗ trợ multi-agent (swarm, sub-agents...):
> Xem `addons/swarm/README.md` để biết cách thiết lập orchestration,
> routing rules, payload contracts, và file conflict policy.
