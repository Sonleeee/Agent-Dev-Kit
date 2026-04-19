# Changelog

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
