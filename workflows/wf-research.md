---
id: research
type: utility
entry-command: /wf-research
description: Research kỹ trước khi implement — web docs, best practices, examples
skills-suggested:
  - research/sk-docs-seeker
  - research/sk-pattern-researcher
modifiers:
  --docs: Chỉ tìm official docs
  --examples: Tìm code examples thực tế
  --compare: So sánh nhiều approaches, output bảng trade-off
---

> [!IMPORTANT]
> ## Delegation Policy — Đọc TRƯỚC khi bắt đầu
>
> | Điều kiện | Hành động BẮT BUỘC |
> |:---|:---|
> | Cần search ≥ 3 nguồn song song (docs + examples + community) | **PHẢI** `invoke_subagent(TypeName="research", Role="Parallel Searcher")` cho mỗi nguồn |
> | Modifier `--compare` cần so sánh ≥ 3 approaches | **PHẢI** `invoke_subagent(TypeName="research")` cho mỗi approach |
> | Research đơn giản 1 nguồn | Chạy inline, KHÔNG cần subagent |
>
> **Subagent context:** Chỉ gửi câu hỏi research cụ thể + scope. KHÔNG gửi chat history.


# /wf-research

**Mục tiêu:** Research kỹ trước khi implement — tìm docs, best practices, examples.

## Khi nào dùng

- Trước `/wf-plan` — cần research approach
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


### Bước 6: Knowledge Checkpoint

Áp dụng `SYSTEM.md` → Brain Writeback Policy.

| Điều kiện | Mode | Hành động |
|-----------|------|-----------|
| Research có source tốt và ảnh hưởng tới decision/implementation | `ASK` | Trình Memory Candidate; addon có thể mở rộng |
| Research chỉ phục vụ câu trả lời tức thời | `SKIP` | Không ghi |

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

## Pre-completion Checklist (PHẢI verify trước khi kết thúc research)

- [ ] Đã kiểm tra Delegation Policy ở đầu file?
- [ ] Nếu multi-source → ĐÃ invoke parallel research subagents?
- [ ] Source citations đầy đủ?
- [ ] Recommendation có evidence?