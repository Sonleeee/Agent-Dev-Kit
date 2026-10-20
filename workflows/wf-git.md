---
id: git
type: utility
entry-command: /wf-git
description: Git operations — commit message, PR description, changelog
modifiers:
  --commit: Chỉ tạo commit message (conventional commit format)
  --pr: Tạo PR description từ diff
  --changelog: Update changelog từ commits
---

> [!IMPORTANT]
> ## Delegation Policy � �?c TRU?C khi b?t d?u
>
> | �i?u ki?n | H�nh d?ng B?T BU?C |
> |:---|:---|
> | Modifier `--changelog` c?n compile t? nhi?u commits | **PH?I** `invoke_subagent(TypeName="research", Role="Changelog Compiler")` |
> | Modifier `--pr` cho PR l?n (= 10 files changed) | **PH?I** `invoke_subagent(TypeName="research", Role="PR Analyzer")` d? scan diff |
> | Commit message don gi?n ho?c PR nh? | Ch?y inline, KH�NG c?n subagent |
>
> **Subagent context:** Ch? g?i git diff + commit history. KH�NG g?i chat history.


# /wf-git

**Mục tiêu:** Tự động hóa git operations — commit messages, PR descriptions, changelog.

## Khi nào dùng

- Sau `/wf-impl` — tạo commit message chuẩn
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

## Pre-completion Checklist (PH?I verify tru?c khi execute)

- [ ] �� ki?m tra Delegation Policy ? d?u file?
- [ ] Output d� du?c user review tru?c khi execute git commands?
- [ ] Commit messages follow Conventional Commits?
