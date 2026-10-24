---
name: adk-pattern-researcher
description: |
  Research design patterns phù hợp cho use case cụ thể — so sánh approaches.
  Dùng khi: chọn architecture pattern, compare libraries, evaluate trade-offs.
  Trigger: "nên dùng pattern nào", "so sánh approaches", "kiến trúc cho [use case]",
  "compare [A] vs [B]", "evaluate trade-offs".
---

# Pattern Researcher

## Mục tiêu
Research và so sánh design patterns/approaches cho use case cụ thể — giúp chọn hướng đi đúng.

## Khi nào chạy
- Trước khi lập kế hoạch (`adk-solution-planning`) — cần chọn architecture pattern
- Compare libraries/frameworks cho cùng use case
- Evaluate trade-offs khi có nhiều options
- Tìm best practices cho specific scenario

## Quy Trình

### Bước 1: Define Use Case

Xác định rõ:

- Problem statement — đang giải quyết gì?
- Constraints — tech stack, team size, timeline, scale
- Non-functional requirements — performance, maintainability, scalability
- Existing patterns — project đang dùng patterns gì?

### Bước 2: Research Options

Tìm kiếm:

1. **Official patterns** — GoF, POSA, DDD, microservices patterns
2. **Framework-specific** — patterns recommended bởi framework đang dùng
3. **Community consensus** — patterns phổ biến cho use case tương tự
4. **Case studies** — real-world examples từ companies/projects tương tự

### Bước 3: Compare

Tạo comparison matrix:

```markdown
| Criteria | Option A | Option B | Option C |
|---|---|---|---|
| Complexity | Low | Medium | High |
| Scalability | Medium | High | High |
| Maintainability | High | Medium | Low |
| Learning curve | Low | Medium | High |
| Team familiarity | ✅ Yes | ⚠️ Partial | ❌ No |
| Risk | Low | Medium | High |
| Effort estimate | 2 days | 5 days | 10 days |
```

### Bước 4: Recommend

Output:

- **Recommended option** — với lý do rõ ràng
- **Evidence** — sources, case studies, benchmarks
- **Trade-offs** — cái gì phải đánh đổi
- **Migration path** — nếu cần chuyển pattern sau này
- **Decision record** — ghi lại context + decision + consequences

### Bước 5: ADR (Architecture Decision Record)

Nếu decision quan trọng, tạo ADR:

```markdown
# ADR-[number]: [Decision title]

## Status: Proposed / Accepted / Deprecated

## Context
[Problem + constraints]

## Decision
[Chọn option nào, tại sao]

## Consequences
[+ Positive] / [- Negative] / [~ Neutral]
```

## Output
- Comparison matrix
- Recommendation + evidence
- ADR (nếu decision lớn)

## Guardrails
- Research phải có evidence — không recommendation dựa trên opinion
- So sánh fair — không bias option nào
- Phải consider team context — pattern tốt nhất ≠ pattern phù hợp nhất
- Constraints quan trọng hơn theory — pragmatic over perfect
