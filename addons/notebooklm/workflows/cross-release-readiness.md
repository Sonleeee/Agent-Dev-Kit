---
description: "Cross-role: Kiểm tra release scope đã có đủ cơ sở để sign-off chưa"
---

# Release Readiness Review

## Skills sử dụng
- Context Query, Cross-Notebook Validation, Risk Radar, Artifact Generation, Operational Notes

## MCP Tools
- `notebook_query`, `cross_notebook_query`, `note`

## Các bước thực thi
1. Dùng `notebook_query` lấy expected behavior từ docs
2. Dùng `cross_notebook_query` đối chiếu với change scope và test scope
3. Liệt kê unresolved risks và rollback concerns
4. Ghi checklist hoặc sign-off note bằng `note` (action=create)

## Khi nào dùng
- Trước staging sign-off, trước production release
