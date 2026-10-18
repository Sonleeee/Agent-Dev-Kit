---
name: sk-mobile-capture
description: Bóc tách và phân loại nội dung capture từ iPhone qua NotebookLM (📥 Inbox)
---

# Mobile Capture

## Công dụng
Xử lý dữ liệu capture từ iPhone thông qua notebook `📥 Inbox`.
Hỗ trợ 4 loại input: Quick Notes, Voice Recording, Social Clips (Facebook/Web), Links.

## MCP Tools
- `notebook_get` — lấy thông tin notebook Inbox
- `note(action=list)` — liệt kê notes trong Inbox
- `source_get_content` — đọc nội dung thô (audio transcript, web scrape)
- `source_describe` — lấy AI summary cho từng source
- `notebook_query` — hỏi AI phân loại content

## Quy trình

### Bước 1: Scan Inbox
```
note(notebook_id=INBOX_ID, action=list)
→ Lấy danh sách notes + sources chưa xử lý
```

### Bước 2: Phân loại (Classification)
Dùng `notebook_query` để hỏi AI:
```
"Phân loại từng item trong notebook này thành:
 IDEA / TASK / NOTE / KNOWLEDGE / SOCIAL_CLIP.
 Trả về dạng bảng: [item] | [category] | [summary 1 dòng]"
```

### Bước 3: Extract Content
- **Notes** → đọc trực tiếp nội dung note
- **URL Sources** → `source_get_content` để lấy full text
- **Audio Sources** → `source_get_content` để lấy transcript
- **Drive Sources** → `source_get_content` để lấy nội dung doc

### Bước 4: Handoff
Nếu Knowledge addon đã bật, truyền kết quả phân loại + nội dung cho `sk-vault-steward` (Hướng C: Phone-Direct)
để ghi vào Obsidian Vault.

## Output
- Danh sách items đã phân loại kèm category
- Nội dung đã extract sẵn sàng ghi vào vault

## Khi nào dùng
- Mỗi sáng khi ngồi vào bàn làm việc
- Khi có nhiều content chưa xử lý trong Inbox
- Được gọi bởi workflow `/wf-phone-sync`

## Lưu ý
- Notebook `📥 Inbox` có tag `inbox` — dùng tag để tìm đúng notebook
- Không xóa sources/notes trên NotebookLM — chỉ đánh dấu "đã xử lý" bằng cách thêm note
