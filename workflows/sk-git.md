---
id: git
type: utility
entry-command: /sk-git
description: Git operations — commit message, PR description, changelog
modifiers:
  --commit: Chỉ tạo commit message (conventional commit format)
  --pr: Tạo PR description từ diff
  --changelog: Update changelog từ commits
---

# /sk-git

**Mục tiêu:** Tự động hóa git operations — commit messages, PR descriptions, changelog.

## Khi nào dùng

- Sau `/sk-impl` — tạo commit message chuẩn
- Chuẩn bị submit PR — tạo PR description
- Release — compile changelog

## Quy trình

### Bước 1: Analyze — Đọc changes

Agent thu thập:

- `git diff` hoặc `git diff --staged`
- Files changed list
- Previous commit messages (pattern reference)

### Bước 2: Categorize — Phân loại

Agent phân loại changes theo Conventional Commits:

| Prefix | Khi nào |
|---|---|
| `feat:` | Thêm feature mới |
| `fix:` | Sửa bug |
| `refactor:` | Refactor không đổi behavior |
| `docs:` | Chỉ update docs |
| `chore:` | Config, dependencies, build |
| `test:` | Thêm/sửa tests |
| `style:` | Format, naming (không đổi logic) |

### Bước 3: Generate — Tạo output

Tùy modifier:

**`--commit`:**
```
feat(module-name): mô tả ngắn gọn

- Chi tiết thay đổi 1
- Chi tiết thay đổi 2

Refs: #issue-number (nếu có)
```

**`--pr`:**
```markdown
## Mô tả
[Tóm tắt PR]

## Changes
- [File/module] — [thay đổi gì]

## Testing
- [ ] Build pass
- [ ] Tests pass

## Screenshots
(nếu FE changes)
```

**`--changelog`:**
```markdown
## [version] — YYYY-MM-DD

### Added
- ...
### Fixed
- ...
### Changed
- ...
```

### Bước 4: Confirm — User xác nhận

Agent trình output → user review → approve hoặc edit trước khi execute.

## Output bắt buộc

- Commit message hoặc PR description hoặc changelog entry
- Luôn trình user trước khi execute git commands

## Guardrails

- KHÔNG tự execute git commands (commit, push, merge) mà không có user approval
- Commit messages phải follow Conventional Commits
- PR description phải có testing checklist
- Không gộp nhiều concerns vào 1 commit message
