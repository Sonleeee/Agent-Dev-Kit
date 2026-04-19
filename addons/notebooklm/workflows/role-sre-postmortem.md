---
description: "SRE/DevOps: Biến logs, alerts và timeline thành RCA, mind map và runbook"
---

# Post-Mortem and Runbook Automation

**Role**: System Operator / DevOps / SRE

## Skills sử dụng
- Knowledge Ingestion, Context Query, Artifact Generation, Operational Notes

## MCP Tools
- `source_add`, `notebook_query`, `studio_create`, `note`

## Input
- Raw server logs, Grafana/CloudWatch alerts, incident chat timeline, commands đã dùng khi cứu hỏa

## Output
- RCA summary, incident timeline, `mind_map`, runbook note

## Các bước thực thi
1. Nạp logs, alerts và chat timeline vào notebook bằng `source_add`
2. Dùng `notebook_query` để tái dựng timeline và root cause
3. Ghi lại commands và steps vào `note` (action=create)
4. Tạo `mind_map` bằng `studio_create` (artifact_type="mind_map")
5. Nếu cần, tạo `flashcards` bằng `studio_create` (artifact_type="flashcards") phục vụ đào tạo on-call

## Guardrails
- Không dùng NotebookLM để thay thế log forensics chuyên sâu
- Dữ liệu nhạy cảm phải được scrub trước khi nạp
- Phải có review của người chịu trách nhiệm hệ thống

## Definition of Done
- [ ] Có timeline sự cố
- [ ] Có root cause hypothesis rõ
- [ ] Có action items
- [ ] Có runbook hoặc note có thể tái sử dụng

## Khi nào dùng
- Trong vòng 24h sau incident, sau khi xử lý xong critical production bug
