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

## Flow chuẩn

Flow ưu tiên:

```text
/sk-clarify -> /sk-plan -> /sk-impl -> /sk-review
```

Shortcut:

- `/sk-delivery-lite` — task rõ ràng, đi nhanh
- `/sk-delivery` — task phức tạp, cần plan kỹ

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

Cách dùng: `/sk-impl --fast` hoặc `/sk-delivery --parallel --auto`

## Gates

### Gate 1 — Ready (sau /sk-plan)

Không code nếu thiếu:

- Problem statement rõ
- Scope in/out
- Plan theo thứ tự
- Quality card
- Task assignment rõ (nếu multi-agent)

### Gate 2 — Dev Done (sau /sk-impl)

Không review nếu thiếu:

- Build pass
- Self-check pass
- API contract status rõ

### Gate 3 — Ship Ready (sau /sk-review)

Blocked nếu:

- Còn finding Critical
- Còn FAIL items chưa fix
- UNPLANNED items chưa được user review

## Phân loại skills

| Nhóm | Mô tả | Cần project context? |
|---|---|---|
| `core/` | Discovery, planning, guard, regression | Không |
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
| `/sk-clarify` | Thu thập requirements, xác nhận scope | — |
| `/sk-plan` | Chốt approach, chọn template | Gate 1 |
| `/sk-impl` | Implement code theo plan | Gate 2 |
| `/sk-review` | Review 5-layer, ship decision | Gate 3 |

### Shortcuts & Auto-pipeline

| Workflow | Mô tả |
|---|---|
| `/sk-delivery` | Full flow: clarify → plan → impl → review |
| `/sk-delivery-lite` | Quick flow cho task đơn giản |
| `/sk-cook` | Auto pipeline: clarify → plan → impl → test → review (1 lệnh) |

### Utilities

| Workflow | Mô tả |
|---|---|
| `/sk-brainstorm` | So sánh options, trade-off analysis |
| `/sk-enhance` | Enhancement/refactor có chủ đích |
| `/sk-deploy` | Deploy checklist |
| `/sk-fix` | Debug pipeline: scout → diagnose → fix → verify → prevent |
| `/sk-test` | Generate & run tests cho module |
| `/sk-docs` | Generate/update documentation |
| `/sk-git` | Git commit messages, PR descriptions, changelog |
| `/sk-scout` | Edge case discovery, error path analysis |
| `/sk-security` | Security scan: OWASP, secrets, auth review |
| `/sk-research` | Research docs, best practices, compare approaches |

### Advanced

| Workflow | Mô tả |
|---|---|
| `/sk-predict` | Expert debate: 5 personas tranh luận impact trước khi implement |
| `/sk-xia` | Port features từ external repos (compare/port/copy/improve) |
| `/sk-retro` | Sprint retrospective: git metrics → health scores → action items |

## Nếu project chưa có AGENTS.md

Agent chạy ở generic mode:

- Dùng global rules
- Hỏi user về context cần thiết
- Gợi ý onboard project bằng `_project-template/`

## System Agents

Kit cung cấp 6 agent personas trong `agents/`. Mỗi agent là 1 `AGENT.md` chứa persona, skills, và quy trình riêng.

| Agent | Role | Khi nào dùng |
|---|---|---|
| `planner` | Lập plan, phân tích scope, chọn approach | `/sk-clarify`, `/sk-plan` |
| `implementer` | Code theo plan, bám sát template | `/sk-impl` |
| `reviewer` | Review 5-layer, ship decision | `/sk-review` |
| `debugger` | Debug root cause, không patch bừa | `/sk-fix` |
| `tester` | Generate tests, coverage analysis | `/sk-test` |
| `red-team` | 4 adversarial personas tấn công code | `/sk-review --red-team` |

**IDE-agnostic:** `AGENT.md` chỉ chứa persona + instructions dạng markdown.
- IDE hỗ trợ subagent → tự invoke agent phù hợp
- IDE không hỗ trợ → user copy persona prompt thủ công
- Swarm setup → xem `addons/swarm/README.md`

## Multi-Agent (tùy chọn)

> Nếu IDE/tool hỗ trợ multi-agent (swarm, sub-agents...):
> Xem `addons/swarm/README.md` để biết cách thiết lập orchestration,
> routing rules, payload contracts, và file conflict policy.
