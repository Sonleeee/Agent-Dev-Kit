---
name: sk-mobile-capture
description: Đọc, trích xuất và phân loại nội dung trong NotebookLM Inbox từ iPhone khi người dùng muốn triage capture. Kết quả mặc định là danh sách/preview; không tự ghi Obsidian, đánh dấu đã xử lý hoặc xóa nguồn.
---

# Mobile Capture

Dùng skill này để hiểu nội dung capture trong notebook `📥 Inbox`, không phải để tự đồng bộ dữ liệu ra vault.

## Quy trình

1. Tìm notebook Inbox bằng `tag(action=select, query="inbox")`; xác nhận đúng notebook trước khi đọc.
2. Dùng `note(action=list)` để liệt kê notes/sources. Đọc nội dung cần thiết bằng `source_get_content` hoặc tóm tắt bằng `source_describe`.
3. Phân loại từng item thành `IDEA`, `TASK`, `NOTE`, `KNOWLEDGE` hoặc `SOCIAL_CLIP`; giữ link/source và ghi rõ phần nào chưa đọc được.
4. Trả bảng ngắn: item, category, project (nếu xác định được), summary và đề xuất đích lưu.

## Ranh giới

- Đọc và phân loại không cho phép sửa NotebookLM hay Obsidian.
- Không xóa nguồn/note, đổi tag, thêm note "đã xử lý" hoặc ghi vault nếu người dùng chưa yêu cầu rõ.
- Nếu người dùng muốn đồng bộ cả Inbox và Daily Ops, dùng `sk-notebooklm-phone-sync`. Nếu chỉ muốn lưu kết quả Inbox, dùng `sk-vault-steward` sau khi người dùng yêu cầu ghi; nếu skill steward không discover được, dừng ở preview.
