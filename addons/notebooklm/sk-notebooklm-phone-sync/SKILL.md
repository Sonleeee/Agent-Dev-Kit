---
name: sk-notebooklm-phone-sync
description: Đồng bộ cả iPhone Inbox và Daily Ops từ NotebookLM sang Obsidian khi người dùng yêu cầu sync rõ ràng. Không tự chạy theo lịch, vì câu "check đầu ngày", hoặc chỉ vì có capture mới.
---

# NotebookLM Phone Sync

Skill này thay procedure `/wf-phone-sync`. Nó điều phối triage Inbox và tổng hợp Daily Ops; NotebookLM và Obsidian là hai nguồn/đích riêng, không tự sync realtime.

## Chuẩn bị dữ liệu

1. Đọc [`sk-mobile-capture`](../sk-mobile-capture/SKILL.md) và [`sk-daily-task-sync`](../sk-daily-task-sync/SKILL.md); dùng đúng notebook/tag và quy trình trích xuất ở đó, không giả định một skill khác được host tự gọi.
2. Scan `📥 Inbox` để lấy captures mới; scan `📋 Daily Ops` để lấy tasks pending/backlog. Xác nhận đúng notebooks trước khi xử lý.
3. Chuẩn hóa thành preview có nguồn, category, project, summary và trạng thái task. Bỏ qua mục không đọc được và nêu rõ.

## Ranh giới ghi

- Nếu người dùng chỉ nói "check đầu ngày", "xem Inbox" hoặc muốn báo cáo, trả preview; không ghi Obsidian và không sửa NotebookLM.
- Chỉ sync khi người dùng yêu cầu rõ việc đưa các mục sang Obsidian hoặc gọi trực tiếp `/wf-phone-sync`.
- Trước khi ghi, dùng `sk-vault-steward` để tìm `vault-path`, kiểm tra cấu trúc và đọc file đích. Nếu skill steward/Obsidian addon chưa discover hoặc bật, vault không rõ hoặc file đích có xung đột, dừng trước khi ghi.
- Mapping gợi ý, theo cấu trúc vault hiện có: `IDEA`/`NOTE`/`SOCIAL_CLIP`/`KNOWLEDGE` → `00_Raw/Incoming/`; `TASK` từ Inbox và tasks Daily Ops → task list đã cấu hình (thường `02_Brain/Task Systems.md`). Không tự tổng hợp Wiki nếu người dùng không yêu cầu.
- Tránh task trùng; chỉ đánh dấu hoàn thành khi match chắc chắn với task hiện có. Không xóa source/note hoặc tự thêm dấu đã xử lý vào NotebookLM.
- Nếu user yêu cầu cập nhật trạng thái xử lý trong NotebookLM, xem đó là thao tác riêng: xác định chính xác nội dung sẽ thêm và chỉ ghi đúng yêu cầu đó.

## Báo cáo

Sau khi sync, báo số mục Inbox và task đã thêm/cập nhật, file đích, item bị bỏ qua và mọi giới hạn xác minh. Không báo sync thành công nếu chưa kiểm tra file đích.
