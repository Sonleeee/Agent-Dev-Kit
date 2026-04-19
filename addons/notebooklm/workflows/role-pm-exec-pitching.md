---
description: "PM/PO: Chuyển PRD, OKR, market analysis thành slide, briefing doc hoặc audio"
---

# Exec Pitching and Team Alignment

**Role**: Product Manager / Product Owner

## Skills sử dụng
- Knowledge Ingestion, Artifact Generation, Context Query

## MCP Tools
- `source_add`, `studio_create`, `export_artifact`, `download_artifact`

## Input
- PRD, market analysis, roadmap summary, sprint or OKR report

## Output
- `slide_deck`, `briefing_doc`, `audio` deep-dive

## Các bước thực thi
1. Cập nhật notebook bằng `source_add` với nguồn dữ liệu mới nhất
2. Tạo `briefing_doc` cho nội bộ team bằng `studio_create` (artifact_type="report")
3. Tạo `slide_deck` cho stakeholder bằng `studio_create` (artifact_type="slide_deck")
4. Nếu cần, tạo `audio` deep-dive bằng `studio_create` (artifact_type="audio", audio_format="deep_dive")
5. Dùng `download_artifact` hoặc `export_artifact` để chia sẻ

## Guardrails
- Slide đẹp không đồng nghĩa với nội dung đúng
- PM/PO phải review message, metric và wording trước khi phát hành

## Definition of Done
- [ ] Có 1 artifact cho stakeholder
- [ ] Có 1 artifact cho team delivery
- [ ] Message giữa hai bản không mâu thuẫn

## Khi nào dùng
- Chuẩn bị QBR, chuẩn bị launch, đầu quý, onboarding initiative mới
