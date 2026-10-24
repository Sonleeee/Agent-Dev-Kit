---
name: adk-notebooklm-mcp
description: Tham chiếu danh mục tool và cách quản trị NotebookLM MCP khi người dùng hỏi về khả năng server, auth hoặc cách chọn tool. Với triage Inbox, Daily Ops và sync, dùng các skill chuyên biệt thay vì nạp toàn bộ tài liệu này.
---

# NotebookLM MCP Skills

Bộ skills này biến NotebookLM từ công cụ hỏi đáp thành hệ thống quản trị tri thức và hỗ trợ delivery.

## Nguyên tắc

- Không xem NotebookLM là nơi trả lời thay con người
- Xem NotebookLM là nơi tổng hợp tri thức và tạo artifact để con người ra quyết định nhanh hơn
- Mọi quy trình quan trọng đều cần guardrails và definition of done
- Đây là tài liệu MCP tham khảo; thao tác tạo/sửa/xóa/sync/import cần yêu cầu tường minh của người dùng. Skill được kích hoạt không tự cấp quyền ghi.

## Tool API Reference

| Nhóm | Tool | Mô tả |
|------|------|-------|
| **Notebook** | `notebook_create` | Tạo notebook mới |
| | `notebook_list` | Liệt kê tất cả notebooks |
| | `notebook_get` | Xem chi tiết notebook + sources |
| | `notebook_describe` | Lấy AI summary cho notebook |
| | `notebook_rename` | Đổi tên notebook |
| | `notebook_delete` | Xóa notebook (cần confirm) |
| | `notebook_query` | Hỏi AI về sources trong notebook |
| **Source** | `source_add` | Thêm source (url, text, drive, file) |
| | `source_delete` | Xóa source |
| | `source_describe` | Lấy AI summary cho source |
| | `source_get_content` | Lấy nội dung thô của source |
| | `source_rename` | Đổi tên source |
| | `source_list_drive` | Liệt kê Drive sources |
| | `source_sync_drive` | Đồng bộ Drive sources |
| **Cross-notebook** | `cross_notebook_query` | Hỏi chéo nhiều notebooks |
| **Research** | `research_start` | Tìm sources mới từ web/drive |
| | `research_status` | Theo dõi tiến trình research |
| | `research_import` | Import sources từ research |
| **Studio** | `studio_create` | Tạo artifact (audio, video, slide, report, quiz...) |
| | `studio_status` | Kiểm tra trạng thái artifact |
| | `studio_delete` | Xóa artifact |
| | `studio_revise` | Sửa slide deck |
| | `download_artifact` | Tải artifact về file |
| | `export_artifact` | Xuất artifact sang Google Docs/Sheets |
| **Notes** | `note` | Tạo, sửa, xóa, liệt kê notes |
| **Tags** | `tag` | Gán, xóa, tìm notebooks theo tags |
| **Batch** | `batch` | Thao tác hàng loạt trên nhiều notebooks |
| **Pipeline** | `pipeline` | Chạy chuỗi bước tự động |
| **Chat** | `chat_configure` | Cấu hình chat settings |
| **Auth/System** | `refresh_auth` | Refresh auth tokens |
| | `server_info` | Kiểm tra version và trạng thái server |

## Danh sách Skills

| # | Skill | Thư mục | Mô tả |
|---|-------|---------|-------|
| 1 | Knowledge Ingestion | `adk-knowledge-ingestion/SKILL.md` | Đưa tài liệu thô vào notebook |
| 2 | Mobile Capture | `adk-mobile-capture/SKILL.md` | Đọc và phân loại capture trong Inbox; mặc định chỉ preview |
| 3 | Daily Task Sync | `adk-daily-task-sync/SKILL.md` | Đọc Daily Ops; ghi task list chỉ khi user yêu cầu sync |
| 4 | NotebookLM Phone Sync | `adk-notebooklm-phone-sync/SKILL.md` | Điều phối sync Inbox + Daily Ops sang Obsidian theo yêu cầu tường minh |
| 5 | NotebookLM Research | `adk-notebooklm-research/SKILL.md` | Truy vấn và tổng hợp tri thức chuyên sâu từ notebook đã chọn |

## Alias tương thích

`/wf-phone-sync` được giữ trong `workflows/wf-phone-sync.md` như adapter deprecated, chỉ chạy khi người dùng gọi trực tiếp. Procedure chuẩn nằm trong `adk-notebooklm-phone-sync`. Câu "check đầu ngày" hoặc yêu cầu xem trạng thái chỉ tạo preview, không ghi Obsidian hay sửa NotebookLM.

Các skill chuyên biệt có thể được gọi trực tiếp theo cơ chế của host. Không giả định slash command của Antigravity và cách gọi skill của Codex là một cú pháp chung.
