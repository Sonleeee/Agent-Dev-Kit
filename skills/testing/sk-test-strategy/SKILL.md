---
name: sk-test-strategy
description: |
  Đề xuất test strategy cho module — loại test, coverage target, priority.
  Dùng khi: module mới cần test plan, review test coverage, đánh giá test quality.
  Trigger: "test strategy", "testing plan", "coverage analysis", "cần test gì".
---

# Test Strategy

## Mục tiêu
Xác định chiến lược testing phù hợp cho module — test gì, ở level nào, coverage bao nhiêu.

## Khi nào chạy
- Module mới — cần test plan trước khi viết tests
- Review test coverage — có đủ chưa?
- Đánh giá test quality — tests có value không?
- Trước refactor lớn — đảm bảo safety net

## Quy Trình

### Bước 1: Analyze Module

Phân tích module theo:

- **Complexity**: McCabe complexity, number of branches
- **Risk**: business critical? data sensitive? user-facing?
- **Dependencies**: external services, DB, file system
- **Change frequency**: thường xuyên thay đổi?

### Bước 2: Testing Pyramid

Đề xuất phân bổ tests theo pyramid:

```
         /  E2E  \        ← Ít nhất, đắt nhất nhưng real nhất
        / Integr.  \      ← Vừa phải — test boundaries
       /   Unit     \     ← Nhiều nhất, nhanh nhất, rẻ nhất
```

| Module type | Unit | Integration | E2E |
|---|---|---|---|
| Pure logic (utils, helpers) | 80% | 10% | 10% |
| Service layer (business logic) | 50% | 40% | 10% |
| API endpoints | 20% | 60% | 20% |
| UI components | 40% | 30% | 30% |
| Data layer (repo, ORM) | 20% | 70% | 10% |

### Bước 3: Priority Matrix

Ưu tiên test cho:

1. **Must test**: Business rules, auth/authorization, data validation
2. **Should test**: Error handling, edge cases, integrations
3. **Nice to test**: UI rendering, logging, metrics
4. **Skip**: Trivial getters/setters, framework auto-generated

### Bước 4: Coverage Targets

Đề xuất coverage targets:

| Level | Target |
|---|---|
| Critical modules | 80%+ |
| Standard modules | 60%+ |
| Utility modules | 70%+ |
| Overall project | 60%+ |

### Bước 5: Output Test Strategy Doc

Tạo test strategy document:

- Module risk assessment
- Test pyramid distribution
- Priority list (test gì trước)
- Coverage targets
- Testing tools recommendation (matching tech stack)
- Estimated effort

## Output
- Test strategy document cho module
- Priority list: test gì trước
- Coverage targets
- Testing tools khuyến nghị

## Guardrails
- Không over-test — 100% coverage không phải mục tiêu
- Test strategy phải pragmatic — phù hợp team size và timeline
- Focus test business value, không test implementation details
- Coverage target là guideline, không phải hard rule
