---
name: sk-docs-seeker
description: |
  Tìm và tổng hợp docs cho library/framework đang dùng trong project.
  Dùng khi: cần docs mới nhất, debug library issue, tìm API usage examples.
  Trigger: "tìm docs", "docs cho [library]", "API reference", "cách dùng [library]".
context-required: false
output: docs-summary
---

# Docs Seeker

## Mục tiêu
Tìm, đọc, và tổng hợp documentation mới nhất cho library/framework cụ thể.

## Khi nào chạy
- Cần docs mới nhất cho library đang dùng
- Debug — cần tìm API reference
- Dùng library lần đầu — cần quickstart
- Version migration — cần migration guide

## Quy Trình

### Bước 1: Identify

Xác định:

- Library/framework tên gì? Version nào?
- Câu hỏi cụ thể cần trả lời?
- Scope: quickstart, API reference, migration guide, troubleshooting?

### Bước 2: Search

Tìm docs theo thứ tự ưu tiên:

1. **Context7 docs** — dùng MCP context7 tools nếu có
2. **Official docs site** — documentation chính thức
3. **GitHub README/Wiki** — từ repo gốc
4. **Release notes** — changelog cho version cụ thể
5. **Community** — Stack Overflow, GitHub Discussions (chỉ khi official docs thiếu)

### Bước 3: Synthesize

Tổng hợp findings:

- Câu trả lời trực tiếp cho câu hỏi user
- Code snippets relevant từ docs
- Version-specific notes (breaking changes, deprecations)
- Links tham khảo

### Bước 4: Output

Format output:

```markdown
## [Library] — [Topic]

### Trả lời
[Câu trả lời ngắn gọn]

### Code Example
[Snippet từ docs]

### Version Notes
[Breaking changes, deprecations nếu có]

### References
- [Link 1]
- [Link 2]
```

## Output
- Docs summary với câu trả lời và code examples
- Source citations (URLs)
- Version-specific warnings

## Guardrails
- Ưu tiên official docs — KHÔNG dùng blog posts làm source chính
- Ghi rõ version docs refer to — tránh outdated info
- Nếu docs thiếu/unclear → nói rõ, đề xuất alternatives
- KHÔNG hallucinate API — nếu không chắc thì nói không chắc
