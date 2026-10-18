---
name: sk-daily-task-sync
description: Đồng bộ tasks từ notebook 📋 Daily Ops về Obsidian Vault local
---

# Daily Task Sync

## Công dụng
Đọc tasks từ notebook `📋 Daily Ops` trên NotebookLM và đồng bộ
về file `02_Brain/Task Systems.md` trong Obsidian Vault.

## MCP Tools
- `notebook_get` — lấy thông tin notebook Daily Ops
- `note(action=list)` — liệt kê tất cả notes (daily + backlog)
- `notebook_query` — hỏi AI tổng hợp trạng thái tasks

## Quy trình

### Bước 1: Tìm notebook Daily Ops
```
tag(action=select, query="daily-ops")
→ Lấy notebook_id của 📋 Daily Ops
```

### Bước 2: Đọc notes
```
note(notebook_id=DAILY_OPS_ID, action=list)
→ Lấy danh sách notes: daily notes + Backlog
```

### Bước 3: Extract tasks
Dùng `notebook_query` để hỏi AI:
```
"Liệt kê tất cả tasks chưa hoàn thành ([ ]) từ mọi notes.
 Nhóm theo project. Format: [project] | [task] | [ngày tạo]"
```

### Bước 4: Sync về local
Ghi output vào `02_Brain/Task Systems.md`:
- Tasks mới → append vào section tương ứng
- Tasks đã hoàn thành ([x]) → đánh dấu done
- Backlog items → section riêng "Backlog"

## Output
- File `02_Brain/Task Systems.md` đã cập nhật
- Báo cáo: X tasks mới, Y tasks hoàn thành, Z backlog

## Khi nào dùng
- Khi cần snapshot tasks về local
- Khi cần review tuần qua
- Được gọi bởi workflow `/wf-phone-sync`

## Lưu ý
- Notes trong Daily Ops dùng format checkbox markdown: `- [ ]` / `- [x]`
- Notebook `📋 Daily Ops` có tag `daily-ops`
