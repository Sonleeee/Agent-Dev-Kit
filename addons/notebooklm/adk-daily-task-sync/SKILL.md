---
name: adk-daily-task-sync
description: Đọc và tổng hợp tasks từ NotebookLM Daily Ops; chỉ cập nhật Obsidian khi người dùng yêu cầu sync task list một cách tường minh.
---

# Daily Task Sync

## Đọc và tổng hợp

1. Tìm notebook `📋 Daily Ops` bằng `tag(action=select, query="daily-ops")`; xác nhận đúng notebook.
2. Dùng `note(action=list)` để đọc daily notes và backlog. Giữ nguyên trạng thái checkbox, ngày và project nếu có.
3. Dùng `notebook_query` để tổng hợp các task chưa hoàn thành; đối chiếu nội dung nguồn khi kết quả query không rõ.
4. Nếu người dùng chỉ muốn xem trạng thái, trả task list và dừng ở chế độ chỉ đọc.

## Cập nhật Obsidian

Chỉ thực hiện khi người dùng yêu cầu rõ việc sync/update task list. Dùng `adk-vault-steward` để xác định vault và kiểm tra file đích; nếu skill steward không discover được, dừng ở preview. Đường dẫn mặc định theo cấu hình vault, thường là `02_Brain/Task Systems.md`.

- Thêm task mới mà chưa có; đối chiếu project và nội dung để tránh append trùng ở lần sync sau.
- Đánh dấu task hoàn thành chỉ khi cùng task được nhận diện chính xác trong nguồn. Không xóa task hoặc thay đổi NotebookLM.
- Nếu file đích không tồn tại, cấu trúc khác hoặc trạng thái task mâu thuẫn, dừng và hỏi trước khi tạo/ghi.
- Báo số task thêm/cập nhật và đường dẫn sau khi đã xác minh file.

Để đồng bộ cả Inbox và Daily Ops trong một lần, dùng `adk-notebooklm-phone-sync`.
