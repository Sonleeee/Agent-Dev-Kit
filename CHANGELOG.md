# Changelog

## v2.3.0 — 2026-04-19

### 🔮 Phase 3 — Advanced Workflows (3)

- `/sk-predict` — Expert Debate: 5 personas (Architect, Security, Performance, UX, Ops) tranh luận impact trước khi implement
- `/sk-xia` — Port Features: phân tích external repo → compare/port/copy/improve vào local project
- `/sk-retro` — Sprint Retrospective: git metrics analysis → health scores → insights → action items

### 🎛️ New Modifiers (8)

- `--focus` (predict) — Chỉ chạy personas liên quan nhất
- `--compare` (xia) — Chỉ so sánh kiến trúc, không port code
- `--port` (xia) — Lấy ý tưởng, code lại theo local conventions (default)
- `--copy` (xia) — Bê nguyên structure, adapt naming
- `--improve` (xia) — Copy + refactor + best practices
- `--period` (retro) — Chỉ định khoảng thời gian phân tích
- `--team` (retro) — Focus phân tích theo contributor
- `--churn` (retro) — Focus files thay đổi nhiều nhất

### 📄 System Updates

- `SYSTEM.md` updated: Advanced workflows section, 8 modifiers mới
- Tổng: 20 workflows, 13 skills, 16 modifiers, 6 system agents

---

## v2.2.0 — 2026-04-19

### 🤖 System Agents (6)

- `agents/planner/AGENT.md` — Chuyên lập plan, phân tích scope, chọn approach
- `agents/implementer/AGENT.md` — Code theo plan, bám sát template, self-check
- `agents/reviewer/AGENT.md` — Review 5-layer, tri-state checklist, ship decision
- `agents/debugger/AGENT.md` — Root cause analysis, không patch symptoms
- `agents/tester/AGENT.md` — Test generation, coverage analysis, scenario-driven
- `agents/red-team/AGENT.md` — 4 adversarial personas: Security, Failure Mode, Assumption Destroyer, Scope Critic

### 🔴 Red-Team Review

- Thêm `--red-team` modifier vào `/sk-review` workflow
- 4 personas review độc lập → dedup → rank findings
- Verdict: PASS / CONDITIONAL PASS / FAIL

### 🍳 Auto-Pipeline `/sk-cook`

- New workflow: `/sk-cook` — auto chain: clarify → plan → impl → test → review
- Modifiers: `--fast`, `--tdd`, `--no-review`, `--no-test`
- Auto-pause khi cần user input hoặc có Critical findings
- Output: Cook Report với delivery summary

### 📄 System Updates

- `SYSTEM.md` updated: agents/ in structure, System Agents section, /sk-cook in shortcuts
- Mode Modifiers table: thêm `--red-team`, `--no-review`
- Tổng: 17 workflows, 13 skills, 8 modifiers, 6 system agents

---

## v2.1.0 — 2026-04-19

### 🎛️ Mode Modifiers

- Thêm `modifiers:` vào YAML frontmatter cho: `/sk-plan`, `/sk-impl`, `/sk-review`, `/sk-delivery`, `/sk-delivery-lite`
- Modifiers: `--fast`, `--deep`, `--auto`, `--tdd`, `--parallel`, `--no-test`
- Agent đọc modifier → điều chỉnh behavior tương ứng

### 🔧 New Workflows (7)

- `/sk-fix` — Structured debug pipeline: scout → diagnose → fix → verify → prevent
- `/sk-test` — Generate & run tests: scan → analyze → generate → run → report
- `/sk-docs` — Generate/update documentation: scan → detect drift → generate → review
- `/sk-git` — Git automation: commit messages, PR descriptions, changelog
- `/sk-scout` — Edge case discovery: data flows, error paths, severity classification
- `/sk-security` — Security scan: OWASP Top 10, secrets detection, auth review
- `/sk-research` — Research & docs: search → synthesize → recommend → document

### 🧩 New Skill Categories (4) + Skills (8)

- `skills/devops/ci-pipeline-check` — Review CI/CD config, best practices
- `skills/devops/docker-review` — Review Dockerfile + docker-compose
- `skills/sk-security/owasp-scan` — OWASP Top 10 checklist cho codebase
- `skills/sk-security/secret-detection` — Tìm hardcoded secrets, API keys
- `skills/testing/sk-test-strategy` — Test strategy, coverage targets, priority
- `skills/testing/scenario-generator` — Generate test scenarios từ requirements
- `skills/sk-research/sk-docs-seeker` — Tìm docs cho library/framework
- `skills/sk-research/pattern-researcher` — Compare design patterns, ADR

### 📄 System Updates

- `SYSTEM.md` updated: Mode Modifiers section, new skill categories, new workflows
- Tổng: 16 workflows (từ 9), 13 skills (từ 5), 6 mode modifiers

---

## v2.0.0 — 2026-04-18

### 🚀 Agent-Dev-Kit

Chuyển đổi từ project-specific sang **Agent-Dev-Kit** — dùng được cho mọi project, mọi IDE/editor.

### Architecture

- Áp dụng **3-layer architecture**: Core Kit → Project Layer → Second Brain (optional)
- SYSTEM.md refactored thành generic agent behavior spec — không còn hardcode agent names
- Tất cả workflows refactored — bỏ MCP-specific calls, dùng generic instructions

### Restructure

- Tạo `addons/` directory với 4 addons: swarm, obsidian, notebooklm, graphify
- Di chuyển swarm files (SWARM-INTEGRATION, FLOW-REVIEW, orchestration skills...) → `addons/swarm/`
- Di chuyển NotebookLM skills + workflows → `addons/notebooklm/`
- Domain skills (backend/frontend) xóa khỏi core → project tự quản lý
- Files cũ archived vào `_archive/`

### Onboarding

- Thêm `README.md` quickstart guide (tiếng Việt)
- Thêm `addons/README.md` — danh sách addons + cách dùng
- Thêm `_project-template/` với templates đầy đủ:
  - `AGENTS.md` template
  - `context/architecture.md.template`
  - `context/checklist.md.template`
  - `context/rule-overrides.approved.md.template`

### Documentation

- README cho từng addon: swarm, obsidian, notebooklm, graphify
- Obsidian vault template với structure: north-star, decisions (ADR), knowledge, projects
- Registry index extensible — hướng dẫn thêm project type mới

### Ngôn ngữ

- Toàn bộ core kit viết bằng **tiếng Việt 100%**

---

## v1.1.0 — 2026-03-29

### Flow Review

- Added `FLOW-REVIEW.md` — deep review workflow design

### New Workflows

- Added `workflows/sk-clarify.md`
- Added `workflows/sk-plan.md`
- Added `workflows/sk-delivery-lite.md`
- Added `workflows/sk-review.md`

### Swarm Refactor

- Refactored agent organization: orchestrator + implementer + reviewer
- Removed deprecated workflows: `biz-research`, `solution`, `solution-plan`, `preview`
- Removed deprecated templates: `solution-record`, `quality-gate-card`

### Integration

- Added swarm integration docs and example config
- Added minimal templates for clarify, plan, impl, review
- Simplified delivery report output

---

## v1.0.0 — 2026-03-09

### Khởi tạo

- Chưng cất từ project-specific `.agents/` (generic patterns)
- Global `.agents/` + per-project `AGENTS.md` + `.agents/context/`
- Rules phân loại `[PROTECTED]` / `[OVERRIDABLE]` trong `global.md`
- User approve overrides qua `rule-overrides.approved.md`
- Workflow files có metadata frontmatter
- `quality/mapping-rules.md` dùng decision-tree format

### Skills

- **core**: business-discovery, solution-planning, api-contract-guard, regression-checklist
- **meta**: skill-creator (8-phase pipeline)

### Workflows

- Stage pipeline: clarify → plan → impl → review
- Shortcuts: delivery (full), delivery-lite (quick)
- Utilities: brainstorm, enhance, deploy
