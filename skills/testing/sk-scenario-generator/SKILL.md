---
name: sk-scenario-generator
description: |
  Generate test scenarios từ requirements — happy path, edge cases, error cases.
  Dùng khi: viết acceptance criteria, tạo QA checklist, generate test cases.
  Trigger: "generate scenarios", "test cases", "acceptance criteria", "QA checklist".
context-required: optional
output: test-scenarios-list
---

# Scenario Generator

## Mục tiêu
Generate test scenarios toàn diện từ requirements — đảm bảo không bỏ sót cases.

## Khi nào chạy
- Nhận requirement mới — cần acceptance criteria
- Trước `/sk-test` — xác định test cases cần viết
- QA review — checklist kiểm tra
- Sprint planning — estimate test effort

## Quy Trình

### Bước 1: Parse Requirements

Từ requirement, extract:

- **Actors** — ai dùng? (user, admin, system, external service)
- **Actions** — làm gì? (create, read, update, delete, search, export...)
- **Objects** — trên data gì? (order, product, user, file...)
- **Rules** — ràng buộc gì? (validation, permission, business rules)

### Bước 2: Generate Happy Paths

Cho mỗi Action → Object:

- Input hợp lệ → expected result
- Các biến thể chính (different params, different states)
- Pagination / filtering / sorting (nếu list)

### Bước 3: Generate Edge Cases

Theo 12 dimensions:

| Dimension | Examples |
|---|---|
| **Null/Empty** | null input, empty string, empty array |
| **Boundary** | min, max, 0, -1, MAX_INT |
| **Format** | wrong type, invalid format, special chars, Unicode |
| **State** | wrong state (edit deleted item, submit twice) |
| **Permission** | unauthorized user, wrong role, expired token |
| **Concurrency** | 2 users edit same item simultaneously |
| **Dependency** | external service down, DB timeout |
| **Volume** | 0 items, 1 item, 1000 items, max items |
| **Time** | timezone, date boundary, daylight saving |
| **Sequence** | out of order operations, skip steps |
| **Duplicate** | same request twice, duplicate data |
| **Cleanup** | cancelled operation, partial completion, rollback |

### Bước 4: Generate Error Cases

- Validation failures → proper error message?
- Auth failures → 401/403 đúng?
- Not found → 404?
- Business rule violations → clear error?
- Server errors → graceful degradation?

### Bước 5: Format Output

Output bảng scenarios:

```markdown
| # | Category | Scenario | Input | Expected | Priority |
|---|---|---|---|---|---|
| 1 | Happy | Create valid order | {...} | 201 + order data | Must |
| 2 | Edge | Create with null name | {name: null} | 400 + validation error | Must |
| 3 | Permission | Create as guest | no token | 401 | Must |
| 4 | Boundary | Name 256 chars | {name: "a"*256} | 400 + max length error | Should |
```

## Output
- Test scenarios list (bảng structured)
- Priority: Must / Should / Nice
- Coverage map: dimension → covered?
- Summary: X happy + Y edge + Z error = total scenarios

## Guardrails
- Scenarios phải testable — có input và expected output rõ
- Priority Must → phải test trước ship, không bỏ qua
- Không generate quá nhiều — focus high-value scenarios
- Scenarios phải independent — mỗi scenario chạy được riêng lẻ
