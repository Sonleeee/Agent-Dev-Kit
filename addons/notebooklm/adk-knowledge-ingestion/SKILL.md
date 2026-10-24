---
name: adk-knowledge-ingestion
description: Import tài liệu người dùng chỉ định vào một notebook NotebookLM khi người dùng yêu cầu thêm/import rõ ràng. Không tự tạo notebook, thêm source, đổi tag hay sync Drive từ một yêu cầu research thông thường.
---

# Knowledge Ingestion

Dùng khi người dùng yêu cầu đưa tài liệu cụ thể vào NotebookLM để làm nguồn tri thức.

## Trước khi ghi

- Xác định notebook đích và source đầu vào (URL, text, Drive hoặc file). Nếu notebook chưa rõ, hỏi hoặc dùng `notebook_list` để đề xuất; không tạo notebook mới nếu chưa được yêu cầu.
- Chỉ gọi `source_add`, `source_sync_drive`, `notebook_create`, `notebook_rename` hoặc `tag(action=add)` theo đúng thao tác người dùng đã yêu cầu.
- Trước khi sync Drive, xác định đúng notebook/source và phạm vi sync. Không xóa/ghi đè source để xử lý lỗi trùng nếu chưa có yêu cầu riêng.

## Import

1. Kiểm tra notebook tồn tại và có đúng mục đích.
2. Thêm source đã được người dùng cung cấp/chỉ định; giữ source attribution.
3. Gán tag chỉ khi người dùng yêu cầu hoặc đã có convention rõ trong notebook.
4. Báo source nào đã thêm hoặc thao tác nào thất bại. Không query notebook rỗng như thể đã có dữ liệu.
