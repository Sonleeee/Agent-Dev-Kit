---
id: test
type: utility
entry-command: /wf-test
description: Generate tests cho module — unit, integration, edge cases
modifiers:
  --unit: Chỉ unit tests
  --integration: Chỉ integration tests
  --edge: Focus edge cases và error paths
  --coverage: Phân tích coverage gaps trước khi generate
---

> [!IMPORTANT]
> ## Delegation Policy — Đọc TRƯỚC khi bắt đầu
>
> | Điều kiện | Hành động BẮT BUỘC |
> |:---|:---|
> | Module cần test có ≥ 5 public API surfaces | **PHẢI** `invoke_subagent(TypeName="self", Role="Test Generator")` để sinh tests song song |
> | Modifier `--coverage` cần analyze gaps trước | **PHẢI** `invoke_subagent(TypeName="research", Role="Coverage Analyzer")` |
> | Module nhỏ ≤ 3 methods | Chạy inline, KHÔNG cần subagent |
>
> **Subagent context:** Chỉ gửi module source code + test conventions. KHÔNG gửi chat history.

# /wf-test

**Mục tiêu:** Generate và chạy tests cho module — đảm bảo code coverage và correctness.

## Khi nào dùng

- Module mới cần test
- Sau `/wf-impl` — bổ sung tests
- Trước `/wf-review` — tăng confidence
- Tìm untested paths trong code đang có

## Quy trình

### Bước 1: Scan — Đọc module code

Agent xác định:

- Public API surfaces (methods, endpoints, handlers)
- Dependencies và external calls
- Error handling paths
- Data transformations

### Bước 2: Analyze — Tìm gaps

Agent phân tích:

- Happy paths chưa có test
- Error/edge cases chưa cover: null, empty, boundary, overflow
- Integration points chưa test (DB, external service, file I/O)
- Existing tests (nếu có) → tránh duplicate

### Bước 3: Generate — Tạo test files

Agent tạo tests:

1. Follow project test conventions (naming, structure, framework)
2. Mỗi test case: Arrange → Act → Assert rõ ràng
3. Test names mô tả behavior, không implementation
4. Mock/stub external dependencies đúng level

### Bước 4: Run — Chạy tests

Agent chạy tests:

```
# Ví dụ .NET
dotnet test [test-project]

# Ví dụ Node
npm test

# Ví dụ specific
npm test -- --grep "[pattern]"
```

- **All PASS** → report coverage
- **FAIL** → analyze failure, fix test hoặc report code bug

### Bước 5: Report

Agent output:

- Tests created: số lượng + tên files
- Test results: pass / fail / skip
- Coverage estimate (nếu tool hỗ trợ)
- Recommended next: thêm tests nào nữa

## Output bắt buộc

- Danh sách test files đã tạo
- Test run results
- Coverage gaps còn lại (nếu analyse được)
- Recommendations

## Guardrails

- Tests phải independent — không depend on execution order
- Không test private/internal methods trực tiếp
- Mock ở đúng boundary — không over-mock
- Test names phải readable — describe behavior không implementation

## Pre-completion Checklist (PHẢI verify trước khi report)

- [ ] Đã kiểm tra Delegation Policy ở đầu file?
- [ ] Nếu module lớn → ĐÃ invoke test generator subagent?
- [ ] Tests independent (không depend execution order)?
- [ ] All tests PASS?
- [ ] Coverage gaps documented?
