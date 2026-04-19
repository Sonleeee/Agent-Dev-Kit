# Agent System — Universal Kit

Bộ agent dùng chung cho mọi project và mọi platform/IDE.

## Cách hoạt động

```text
.agents/ (KIT — clone từ repo)
    ├── rules/          ← Quality gates chung
    ├── skills/         ← Skills tái sử dụng
    ├── workflows/      ← Các workflow chuẩn
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
/clarify -> /plan -> /impl -> /review
```

Shortcut:

- `/delivery-lite` — task rõ ràng, đi nhanh
- `/delivery` — task phức tạp, cần plan kỹ

## Gates

### Gate 1 — Ready (sau /plan)

Không code nếu thiếu:

- Problem statement rõ
- Scope in/out
- Plan theo thứ tự
- Quality card
- Task assignment rõ (nếu multi-agent)

### Gate 2 — Dev Done (sau /impl)

Không review nếu thiếu:

- Build pass
- Self-check pass
- API contract status rõ

### Gate 3 — Ship Ready (sau /review)

Blocked nếu:

- Còn finding Critical
- Còn FAIL items chưa fix
- UNPLANNED items chưa được user review

## Phân loại skills

| Nhóm | Mô tả | Cần project context? |
|---|---|---|
| `core/` | Discovery, planning, guard, regression | Không |
| `meta/` | Tạo/cải thiện agent system | Không |

> **Ghi chú:** Domain skills (backend/frontend) không nằm trong core kit.
> Mỗi project tự tạo domain skills riêng trong `.agents/context/` hoặc repo riêng.

## Nếu project chưa có AGENTS.md

Agent chạy ở generic mode:

- Dùng global rules
- Hỏi user về context cần thiết
- Gợi ý onboard project bằng `_project-template/`

## Multi-Agent (tùy chọn)

> Nếu IDE/tool hỗ trợ multi-agent (swarm, sub-agents...):
> Xem `addons/swarm/README.md` để biết cách thiết lập orchestration,
> routing rules, payload contracts, và file conflict policy.

## Utilities

Workflow utility:

- `/brainstorm` để compare options khi cần
- `/deploy` cho deploy checklist
- `/enhance` cho enhancement/refactor có chủ đích
