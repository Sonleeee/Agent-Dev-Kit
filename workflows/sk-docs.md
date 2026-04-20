---
id: docs
type: utility
entry-command: /sk-docs
description: Generate hoặc update documentation cho module/API/project
modifiers:
  --api: Chỉ API docs (endpoints, params, responses)
  --readme: Chỉ update README
  --changelog: Chỉ update CHANGELOG
  --full: Generate tất cả docs
---

# /sk-docs

**Mục tiêu:** Generate hoặc update documentation đồng bộ với code hiện tại.

## Khi nào dùng

- Sau `/sk-impl` — document những gì đã thay đổi
- API mới cần docs
- README outdated
- Cần changelog entry

## Quy trình

### Bước 1: Scan — Đọc code + existing docs

Agent thu thập:

- Source code (public APIs, exports, endpoints)
- Existing documentation (README, CHANGELOG, doc comments)
- Recent changes (git diff nếu có)
- Project conventions cho docs format

### Bước 2: Detect — Phát hiện docs drift

Agent so sánh:

- Docs vs code: có gì outdated?
- Missing docs: code có nhưng docs chưa có?
- Orphan docs: docs có nhưng code đã xóa?

### Bước 3: Generate — Tạo/update docs

Agent thực hiện:

1. **API docs** — endpoints, params, response schemas, error codes
2. **README sections** — setup, usage, configuration
3. **CHANGELOG entry** — theo conventional changelog format
4. **Code comments** — JSDoc / XML doc comments cho public APIs

### Bước 4: Review — Self-check accuracy

Agent verify:

- [ ] Docs phản ánh đúng code hiện tại
- [ ] Examples chạy được (nếu có)
- [ ] Links và references đúng
- [ ] Format consistent với existing docs

## Output bắt buộc

- Danh sách docs files đã tạo/update
- Drift report (outdated items đã fix)
- Missing items vẫn còn (nếu ngoài scope)

## Guardrails

- Docs phải match code — KHÔNG viết wishful thinking
- KHÔNG xóa docs sections mà user đã custom
- Changelog format theo Conventional Changelog hoặc project convention
- Nếu project có docs template → follow template
