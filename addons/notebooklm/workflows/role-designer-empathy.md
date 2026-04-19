---
description: "Designer: Tổng hợp feedback thành pain points, persona và insight thiết kế"
---

# User Empathy and Persona Extraction

**Role**: UI/UX Designer

## Skills sử dụng
- Knowledge Ingestion, Cross-Notebook Validation, Artifact Generation, Context Query, UX Rule Extractor

## MCP Tools
- `source_add`, `cross_notebook_query`, `studio_create`, `notebook_query`

## Input
- User feedback, survey results, interview transcripts, product usage notes

## Output
- Persona summary, pain-point map, `infographic`, UX insight brief

## Các bước thực thi
1. Nạp feedback và interview data vào notebook bằng `source_add`
2. Dùng `notebook_query` để tìm top pain points, recurring confusion, unmet needs
3. Nếu có nhiều nhóm user, dùng `cross_notebook_query` đối chiếu chéo
4. Dùng `studio_create` tạo `infographic` (infographic_style="bento_grid" hoặc "editorial")
5. Chốt lại thành UX insight brief cho team

## Guardrails
- Không xem phản hồi người dùng là đại diện tuyệt đối cho toàn bộ tập user
- Cần kết hợp analytics và business context

## Definition of Done
- [ ] Có pain points rõ
- [ ] Có nhóm persona hoặc behavioral segments rõ
- [ ] Có UX brief đủ để dẫn dắt thiết kế tiếp theo

## Khi nào dùng
- Discovery phase, trước wireframe, trước redesign
