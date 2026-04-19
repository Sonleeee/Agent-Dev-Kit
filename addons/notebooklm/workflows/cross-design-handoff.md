---
description: "Cross-role: Kiểm tra thiết kế có khớp với sản phẩm và kỹ thuật không"
---

# Design Handoff Validation

## Skills sử dụng
- UX Rule Extractor, Cross-Notebook Validation, Context Query

## MCP Tools
- `notebook_query`, `cross_notebook_query`

## Các bước thực thi
1. Dùng `notebook_query` bóc tách UI flow và states
2. Dùng `cross_notebook_query` đối chiếu với PRD và API docs
3. Tổng hợp các điểm lệch
4. Tạo danh sách câu hỏi cho BA, PO, dev

## Khi nào dùng
- Trước khi bắt đầu implement frontend
