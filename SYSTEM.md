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
        ├── architecture.md   ← Kiến trúc project
        ├── checklist.md      ← Checklist riêng
        └── templates/        ← Code templates
```

## Luồng agent khi nhận task

1. Đọc `AGENTS.md` ở project root
2. Tra `registry/index.md`
3. Load `rules/global.md`
4. Load `.agents/context/architecture.md`
5. Load `.agents/context/templates/*` nếu có
6. Chọn workflow phù hợp

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

- `/wf-delivery-lite` — task rõ ràng, đi nhanh
- `/wf-delivery` — task phức tạp, cần plan kỹ

## Auto-Route (Intent → Workflow)

Khi user mô tả task bằng ngôn ngữ tự nhiên (không gõ `/wf-`),
agent phân loại intent và chọn workflow phù hợp.
Agent **THÔNG BÁO** cho user workflow đang dùng trước khi bắt đầu.

| Tín hiệu từ user | Workflow |
|---|---|
| fix, bug, lỗi, crash, exception, sai | `/wf-fix` |
| thêm, tạo mới, feature, implement | `/wf-delivery` hoặc `/wf-delivery-lite` |
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
| `--fast` | Rút gọn, bỏ bước không critical | plan, impl, review, delivery, delivery-lite, cook, predict |
| `--deep` | Research kỹ, kiểm tra sâu | plan, review, predict |
| `--auto` | Tự approve gates, không hỏi user | plan, review, delivery |
| `--tdd` | Viết test trước rồi code | impl, cook |
| `--parallel` | Multi-agent song song (cần swarm) | impl, delivery |
| `--no-test` | Bỏ test obligations | impl, delivery-lite, cook |
| `--red-team` | Adversarial review 4 personas | review |
| `--no-review` | Bỏ review step | cook |
| `--focus` | Chỉ chạy personas liên quan nhất | predict |
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
| `core/` | Discovery, planning, guard, regression, context management, vault sync | Không |
| `meta/` | Tạo/cải thiện agent system | Không |
| `devops/` | CI/CD pipeline, Docker review | Không |
| `security/` | OWASP scan, secret detection | Không |
| `testing/` | Test strategy, scenario generation | Tùy chọn |
| `research/` | Docs lookup, pattern research | Không |

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
| `/wf-delivery-lite` | Quick flow cho task đơn giản |
| `/wf-cook` | Auto pipeline: clarify → plan → impl → test → review (1 lệnh) |

### Utilities

| Workflow | Mô tả |
|---|---|
| `/wf-brainstorm` | So sánh options, trade-off analysis |
| `/wf-enhance` | Enhancement/refactor có chủ đích |
| `/wf-deploy` | Deploy checklist |
| `/wf-fix` | Debug pipeline: scout → diagnose → fix → verify → prevent |
| `/wf-test` | Generate & run tests cho module |
| `/wf-docs` | Generate/update documentation |
| `/wf-git` | Git commit messages, PR descriptions, changelog |
| `/wf-scout` | Edge case discovery, error path analysis |
| `/wf-security` | Security scan: OWASP, secrets, auth review |
| `/wf-research` | Research docs, best practices, compare approaches |

### Advanced

| Workflow | Mô tả |
|---|---|
| `/wf-predict` | Expert debate: 5 personas tranh luận impact trước khi implement |
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
| **AUTO** | Root cause đã xác nhận, bug/pitfall lặp, architecture decision, context drift đã approved, pattern có thể tái sử dụng | Gọi `sk-vault-steward` hoặc `sk-context-cache`, ghi summary ngắn rồi report lại |
| **ASK** | Research summary, delivery summary, prediction/debate, plan có quyết định chưa chắc chắn | Tạo Memory Candidate và hỏi user trước khi ghi |
| **SKIP** | Status tạm thời, raw command output, progress nhỏ, failed attempt không có lesson rõ | Không ghi |

### Default Workflow Policy

| Workflow/Skill | Default | Ghi gì |
|---|---|---|
| `/wf-fix` | AUTO nếu root cause confirmed | root cause, prevention, bug pattern |
| `/wf-review` | AUTO nếu có Critical/Major hoặc repeated finding; ASK nếu review clean nhưng có insight | review pattern, architecture violation, drift |
| `/wf-retro` | AUTO | health insight, hotspot, action items |
| `sk-context-update` | AUTO với items user approved | context drift, legacy rule, new pattern |
| `sk-context-cache` | AUTO khi trigger cache match | pattern/review/decision cache |
| `/wf-cook` | ASK | delivery lesson hoặc reusable pattern |
| `/wf-research` | ASK | sourced research finding hoặc decision record |
| `/wf-predict` | ASK | debate outcome và risks |
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
