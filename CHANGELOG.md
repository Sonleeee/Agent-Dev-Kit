# Changelog

## v2.1.0 — 2026-04-19

### 🎛️ Mode Modifiers

- Thêm `modifiers:` vào YAML frontmatter cho: `/plan`, `/impl`, `/review`, `/delivery`, `/delivery-lite`
- Modifiers: `--fast`, `--deep`, `--auto`, `--tdd`, `--parallel`, `--no-test`
- Agent đọc modifier → điều chỉnh behavior tương ứng

### 🔧 New Workflows (7)

- `/fix` — Structured debug pipeline: scout → diagnose → fix → verify → prevent
- `/test` — Generate & run tests: scan → analyze → generate → run → report
- `/docs` — Generate/update documentation: scan → detect drift → generate → review
- `/git` — Git automation: commit messages, PR descriptions, changelog
- `/scout` — Edge case discovery: data flows, error paths, severity classification
- `/security` — Security scan: OWASP Top 10, secrets detection, auth review
- `/research` — Research & docs: search → synthesize → recommend → document

### 🧩 New Skill Categories (4) + Skills (8)

- `skills/devops/ci-pipeline-check` — Review CI/CD config, best practices
- `skills/devops/docker-review` — Review Dockerfile + docker-compose
- `skills/security/owasp-scan` — OWASP Top 10 checklist cho codebase
- `skills/security/secret-detection` — Tìm hardcoded secrets, API keys
- `skills/testing/test-strategy` — Test strategy, coverage targets, priority
- `skills/testing/scenario-generator` — Generate test scenarios từ requirements
- `skills/research/docs-seeker` — Tìm docs cho library/framework
- `skills/research/pattern-researcher` — Compare design patterns, ADR

### 📄 System Updates

- `SYSTEM.md` updated: Mode Modifiers section, new skill categories, new workflows
- Tổng: 16 workflows (từ 9), 13 skills (từ 5), 6 mode modifiers

---

## v2.0.0 — 2026-04-18

### 🚀 Universal Kit

Chuyển đổi từ project-specific sang **Universal Agent Kit** — dùng được cho mọi project, mọi IDE/editor.

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

- Added `workflows/clarify.md`
- Added `workflows/plan.md`
- Added `workflows/delivery-lite.md`
- Added `workflows/review.md`

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
