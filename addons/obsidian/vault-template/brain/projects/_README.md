# 🗂️ Projects Hub

> Mỗi project có 1 subfolder ở đây. Link tới `.agents/context/` của project.

## Cấu trúc mỗi project

```
projects/
├── [project-a]/
│   ├── overview.md        ← Tóm tắt project, tech stack, team
│   ├── learnings.md       ← Bài học rút ra từ project
│   └── links.md           ← Quick links (repo, docs, deploy URL)
└── [project-b]/
    └── ...
```

## Template file overview.md

```markdown
# [Tên Project]

- **Repo:** [link]
- **Tech:** [.NET + React / Node + Vue / ...]
- **Vai trò:** [của bạn trong project]
- **Thời gian:** [bắt đầu — kết thúc]

## Architecture
→ Xem [[../../../[project-path]/.agents/context/architecture.md]]

## Key Decisions
→ [[ADR-001-...]]
→ [[ADR-002-...]]

## Learnings
→ [[learnings]]
```

> Copy template trên cho mỗi project mới.
