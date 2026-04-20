---
id: research
type: utility
entry-command: /sk-research
description: Research kỹ trước khi implement — web docs, best practices, examples
skills-suggested:
  - research/sk-docs-seeker
  - research/pattern-researcher
modifiers:
  --docs: Chỉ tìm official docs
  --examples: Tìm code examples thực tế
  --compare: So sánh nhiều approaches, output bảng trade-off
---

# /sk-research

**Mục tiêu:** Research kỹ trước khi implement — tìm docs, best practices, examples.

## Khi nào dùng

- Trước `/sk-plan` — cần research approach
- Dùng library/framework mới — cần tìm docs
- So sánh nhiều solutions — cần evidence
- Debug — cần tìm known issues, workarounds

## Quy trình

### Bước 1: Define — Xác định câu hỏi

Agent xác định:

- Câu hỏi chính cần trả lời (1-3 câu)
- Scope: library/framework nào? Version nào?
- Output mong muốn: docs, examples, comparison

### Bước 2: Search — Tìm kiếm

Agent tìm theo thứ tự ưu tiên:

1. **Official docs** — documentation chính thức (context7, API docs)
2. **Code examples** — repos, snippets từ official sources
3. **Community** — Stack Overflow, GitHub issues, discussions
4. **Articles** — blog posts, tutorials từ reputable sources

> Agent dùng các tools sẵn có: web search, context7 docs lookup, MCP tools.

### Bước 3: Synthesize — Tổng hợp

Agent tổng hợp:

- Câu trả lời ngắn gọn cho câu hỏi chính
- Key findings từ multiple sources
- Code snippets relevant nhất
- Caveats / gotchas / known issues

### Bước 4: Recommend — Đề xuất

Agent output:

- Recommendation rõ ràng (approach nào, library nào, pattern nào)
- Evidence cho recommendation (source citations)
- Alternatives nếu recommendation không phù hợp
- Risks / limitations cần lưu ý

### Bước 5: Document — Ghi lại

Agent ghi lại research notes:

- Sources đã tìm (URLs, doc versions)
- Key takeaways
- Decision record (nếu đã chọn approach)

## Output bắt buộc

- Câu trả lời tổng hợp cho câu hỏi research
- Source citations (URLs hoặc doc references)
- Recommendation kèm evidence
- Research notes (cho reference sau)

## Guardrails

- KHÔNG recommend dựa trên training data cũ — luôn verify với docs mới nhất
- Source citations là bắt buộc — mọi claim cần evidence
- Nếu không tìm thấy docs reliable → nói rõ uncertainty
- KHÔNG mix research với implementation — research xong mới code
