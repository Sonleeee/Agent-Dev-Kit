---
description: "BA: Biến transcript, email, workshop notes thành PRD có cấu trúc"
---

# Chaos-to-Order PRD

**Role**: Business Analyst

## Skills sử dụng
- Knowledge Ingestion, Context Query, Requirement Extraction, Cross-Notebook Validation, Artifact Generation

## MCP Tools
- `source_add`, `notebook_query`, `cross_notebook_query`, `studio_create`, `export_artifact`

## Input
- Meeting transcript, email khách hàng, workshop notes, file khảo sát yêu cầu

## Output
- PRD draft, user flow summary, edge case list, open questions

## Các bước thực thi
1. Nạp toàn bộ nguồn requirement vào notebook bằng `source_add`
2. Dùng `notebook_query` để trích functional requirements và non-functional requirements
3. Dùng `notebook_query` tiếp để tìm mâu thuẫn và chỗ mơ hồ
4. Dùng `studio_create` tạo `briefing_doc` (report_format = "Briefing Doc")
5. Dùng `export_artifact` để xuất ra Google Docs cho team

## Guardrails
- Không đưa thẳng output thành PRD final nếu chưa review với stakeholder
- Phải đánh dấu rõ assumption và unresolved questions

## Definition of Done
- [ ] Có PRD draft
- [ ] Có acceptance direction sơ bộ
- [ ] Có edge case list
- [ ] Có danh sách điểm cần stakeholder chốt

## Khi nào dùng
- Sau kick-off, sau discovery workshop, sau sprint planning
