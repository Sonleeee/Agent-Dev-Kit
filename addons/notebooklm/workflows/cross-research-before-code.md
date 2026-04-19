---
description: "Cross-role: Lấy đủ bối cảnh trước khi code hoặc sửa bug lớn"
---

# Research Before Code

## Skills sử dụng
- Context Query, Architecture Recall, Cross-Notebook Validation, Risk Radar

## MCP Tools
- `notebook_query`, `cross_notebook_query`

## Các bước thực thi
1. Chọn notebook dự án (truyền notebook_id)
2. Dùng `notebook_query` hỏi expected behavior
3. Dùng `notebook_query` hỏi kiến trúc và dependencies
4. Dùng `cross_notebook_query` so sánh chéo nếu cần
5. Tổng hợp thành brief trước coding

## Khi nào dùng
- Trước thay đổi quan trọng, trước refactor, trước fix bug có ảnh hưởng rộng
