---
name: Context Query
description: Hỏi đáp nhanh theo ngữ cảnh của notebook đã chọn
---

# Context Query

## Công dụng
Hỏi đáp nhanh theo ngữ cảnh của notebook đã chọn.

## MCP Tools
- `notebook_query` — hỏi AI về sources trong notebook
- `notebook_get` — xem chi tiết notebook
- `source_get_content` — lấy nội dung thô khi cần trích chính xác

## Input
- Câu hỏi + notebook_id

## Output
- Câu trả lời có căn cứ từ nguồn

## Khi nào dùng
- Dev cần hiểu logic, BA cần xác minh rule, PM cần hiểu scope

## Lưu ý
- Giảm thời gian đọc tài liệu thủ công
- Luôn kiểm tra nguồn trích dẫn
