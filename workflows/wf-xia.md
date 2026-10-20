---
id: xia
type: utility
entry-command: /wf-xia
description: Phân tích external repo → port feature vào local project theo local conventions
modifiers:
  --compare: Chỉ so sánh kiến trúc 2 repos — không port code
  --port: Lấy ý tưởng, code lại theo local conventions (default)
  --copy: Bê nguyên cấu trúc, chỉ adapt naming + style
  --improve: Copy + refactor + áp dụng best practices
---

# /wf-xia

**Mục tiêu:** Phân tích feature từ external repo → port vào local project, đảm bảo phù hợp conventions và architecture local.

## Khi nào dùng

- Tìm thấy repo có feature muốn học hỏi
- Muốn port design pattern từ project khác
- So sánh kiến trúc 2 repos (tìm điểm cải thiện)
- Integrate/adapt third-party code vào local project

## Input

- URL hoặc path đến external repo/file
- Feature/module cụ thể muốn port
- (Optional) Mode: `--compare`, `--port`, `--copy`, `--improve`
- Local target: nơi sẽ đặt code mới

## Modes

### `--compare` — So sánh kiến trúc

Chỉ phân tích, không tạo code:

- Structure comparison (folder layout, naming)
- Pattern comparison (design patterns, state management)
- Tech stack comparison
- Strengths/weaknesses mỗi bên
- Recommendations có thể áp dụng

### `--port` — Lấy ý tưởng, code lại (DEFAULT)

Hiểu concept → implement lại theo local style:

- Đọc external code → hiểu logic core
- Thiết kế lại API/interface theo local conventions
- Code lại hoàn toàn — không copy paste
- Đảm bảo consistency với architecture hiện tại

### `--copy` — Bê nguyên, adapt naming

Copy structure và logic, chỉ sửa:

- Naming conventions (camelCase/PascalCase/snake_case)
- Import paths
- Config format
- Coding style (linting rules)

### `--improve` — Copy + refactor

Copy xong áp dụng improvements:

- Refactor theo SOLID principles
- Thêm error handling thiếu
- Optimize performance
- Thêm types/validation nếu thiếu

## Quy trình

### Bước 1: Analyze External

Agent phân tích external source:

- File structure mapping
- Dependencies used
- Core logic flow
- Public API / interface
- Tests (nếu có)

### Bước 2: Gap Analysis

So sánh external vs local:

- Tech stack differences (framework, language version)
- Architecture pattern differences
- Convention differences (naming, structure)
- Dependency mismatches
- Missing infrastructure (auth, logging, error handling)

### Bước 3: Adaptation Plan

Agent tạo plan chuyển đổi:

- Files sẽ tạo/sửa
- Dependencies cần thêm/bỏ
- Transformations cần áp dụng
- Tests cần viết
- Potential issues / trade-offs

### Bước 4: Execute (trừ `--compare` mode)

Agent thực hiện chuyển đổi:

- Tạo files mới theo local structure
- Adapt code theo conventions
- Wire up với existing codebase
- Thêm tests cơ bản

### Bước 5: Verify

Agent verify kết quả:

- Build pass?
- Existing tests không break?
- New code integrates đúng?
- API contract nhất quán?

## Output bắt buộc

### Cho `--compare` mode:

```markdown
## 🔄 Compare Report

### Structure
| Aspect | External | Local |
|---|---|---|
| [aspect] | [external approach] | [local approach] |

### Patterns
[design pattern comparison]

### Recommendations
[gì local nên học từ external và ngược lại]
```

### Cho `--port` / `--copy` / `--improve`:

```markdown
## 🔀 Xia Report

### Source
- Repo: [URL/path]
- Feature: [feature name]
- Mode: [port/copy/improve]

### Adaptation Summary
- Files created: [list]
- Files modified: [list]
- Dependencies added: [list]

### Gap Analysis
[differences found + how resolved]

### Changes Made
[summary of transformations applied]

### Verify
- Build: PASS/FAIL
- Tests: PASS/FAIL
- Integration: OK/Issues

### ⚠️ Manual Attention
[items user cần review manually]
```

## Guardrails

- KHÔNG copy code verbatim khi dùng `--port` — phải code lại
- Kiểm tra license external repo trước khi copy/improve
- Nếu external repo dùng tech stack khác biệt lớn → recommend `--port` thay vì `--copy`
- Dependencies mới phải được user approve
- `--compare` KHÔNG sửa bất kỳ code nào — chỉ analysis
- Giữ consistency với local architecture — không import "ngoại lai" patterns

## Pre-completion Checklist (PHẢI verify trước khi report)

- [ ] Đã kiểm tra Delegation Policy ở đầu file?
- [ ] Nếu external repo lớn → ĐÃ invoke analyzer subagent?
- [ ] Nếu `--compare` → ĐÃ invoke 2 parallel research subagents?
- [ ] Gap analysis hoàn thành?
- [ ] Build PASS (trừ `--compare` mode)?
