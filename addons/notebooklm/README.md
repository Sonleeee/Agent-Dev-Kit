# NotebookLM Addon — Research & Synthesis

Addon tích hợp NotebookLM MCP để đọc, truy vấn và tạo artifact từ các notebooks. Cài MCP server và đăng nhập theo cấu hình hiện có trước khi dùng các skill.

## Skills hiện có

| Skill | Dùng cho |
|---|---|
| `adk-knowledge-ingestion` | Thêm tài liệu vào notebook khi người dùng yêu cầu |
| `adk-mobile-capture` | Đọc và phân loại nội dung trong iPhone Inbox; mặc định chỉ preview |
| `adk-daily-task-sync` | Đọc Daily Ops; cập nhật task list chỉ khi user yêu cầu sync |
| `adk-notebooklm-phone-sync` | Đồng bộ Inbox và Daily Ops sang Obsidian theo yêu cầu tường minh |
| `adk-notebooklm-mcp` | Tham chiếu tool/API và troubleshooting NotebookLM MCP |

Procedure nằm trong `SKILL.md` tương ứng; tài liệu MCP tổng quan ở `addons/notebooklm/SKILL.md`. Với thao tác ghi, import, sync hoặc xóa, yêu cầu phải nêu rõ hành động; không tự thay đổi NotebookLM hay Obsidian do auto-trigger.

## Alias tương thích

`/wf-phone-sync` vẫn tồn tại tạm thời dưới dạng adapter deprecated, chỉ chạy khi được gọi trực tiếp. Nội dung chuẩn nằm trong `adk-notebooklm-phone-sync`.

Cụm "check đầu ngày" hoặc "xem Inbox" chỉ yêu cầu đọc/tạo preview; không tự ghi vault, thêm note "đã xử lý" hay xóa source.

## Giới hạn

- NotebookLM không đồng bộ realtime với Obsidian.
- Chỉ dùng các thao tác MCP được host cung cấp; nếu MCP/auth chưa sẵn sàng, báo rõ và không giả lập kết quả.
- Đọc quy tắc vault và xác nhận đúng đường dẫn trước khi ghi Obsidian.
