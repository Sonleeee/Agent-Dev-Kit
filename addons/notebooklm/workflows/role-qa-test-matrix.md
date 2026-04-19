---
description: "QA: Sinh test matrix từ PRD, API contract và bug history"
---

# Test Matrix Generation

**Role**: QA / Senior Tester

## Skills sử dụng
- Knowledge Ingestion, Context Query, Cross-Notebook Validation, Artifact Generation

## MCP Tools
- `source_add`, `notebook_query`, `studio_create`, `export_artifact`

## Input
- PRD, API schema, bug history, release notes

## Output
- Test matrix, happy path list, sad path list, regression scope

## Các bước thực thi
1. Nạp PRD, API contract và bug history vào notebook bằng `source_add`
2. Dùng `notebook_query` truy vấn các scenario chức năng và ngoại lệ
3. Đối chiếu requirement với bug cũ để tìm khu vực dễ vỡ
4. Dùng `studio_create` tạo `data_table` (artifact_type="data_table", description="Test matrix...")
5. Dùng `export_artifact` xuất ra Google Sheets cho QA team

## Guardrails
- Không tuyên bố độ phủ 100%
- Luôn cần QA review thủ công và bổ sung exploratory cases

## Definition of Done
- [ ] Có test matrix dùng được
- [ ] Có grouping theo happy path, sad path, regression path
- [ ] Có danh sách test data hoặc giả định còn thiếu

## Khi nào dùng
- Ngay sau khi API contract ổn định, trước SIT, trước UAT
