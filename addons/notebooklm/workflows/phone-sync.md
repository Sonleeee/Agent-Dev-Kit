---
description: "Đồng bộ nhanh iPhone → NotebookLM → SecondBrain (quét Inbox + Daily Ops)"
---

# /sk-phone-sync

Workflow sync dữ liệu từ iPhone (qua NotebookLM) về SecondBrain local.

## Skills sử dụng
- Mobile Capture, Daily Task Sync, Knowledge Ingestion

## MCP Tools
- `tag(action=select)`, `notebook_get`, `note(action=list)`
- `source_get_content`, `source_describe`, `notebook_query`

## Các bước thực thi

### Step 1: Scan 📥 Inbox
1. Dùng `tag(action=select, query="inbox")` để tìm notebook Inbox
2. Dùng `note(action=list)` để đọc notes mới
3. Dùng `notebook_get` để xem sources mới (URLs, audio, files)
4. Dùng `notebook_query` để AI phân loại: IDEA / TASK / NOTE / KNOWLEDGE / SOCIAL_CLIP

### Step 2: Scan 📋 Daily Ops
1. Dùng `tag(action=select, query="daily-ops")` để tìm notebook Daily Ops
2. Dùng `note(action=list)` để đọc daily notes + backlog
3. Dùng `notebook_query` để AI tổng hợp pending tasks

### Step 3: Ghi vào SecondBrain
Gọi `sk-vault-steward` (Hướng C: Phone-Direct):
- IDEA / NOTE / SOCIAL_CLIP → `00_Raw/Incoming/`
- KNOWLEDGE → `00_Raw/Incoming/` → trigger synthesis vào `01_Wiki/`
- TASK → `02_Brain/Task Systems.md`

### Step 4: Báo cáo
```
[PROTOCOL REPORT]
- Context: [[02_Brain/Projects]]
- Action: /sk-phone-sync
- Result: X items từ Inbox, Y tasks từ Daily Ops
- Files changed: [danh sách]
- Next Step: [đề xuất]
```

## Khi nào dùng
- Mỗi sáng: "check đầu ngày" hoặc gọi trực tiếp `/sk-phone-sync`
- Khi thấy Inbox trên NotebookLM có nhiều items chưa xử lý
