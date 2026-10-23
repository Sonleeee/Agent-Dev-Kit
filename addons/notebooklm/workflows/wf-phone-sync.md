---
description: "Alias cũ để đồng bộ iPhone Inbox và Daily Ops từ NotebookLM sang Obsidian"
entry-command: /wf-phone-sync
replacement-skill: sk-notebooklm-phone-sync
status: deprecated
invocation: explicit-only
---

# Adapter cũ: `/wf-phone-sync`

Workflow này chỉ còn là alias tương thích khi người dùng gọi trực tiếp. Nó không tự chạy theo lịch và không được kích hoạt chỉ bởi câu "check đầu ngày".

Khi được gọi trực tiếp, làm theo [`sk-notebooklm-phone-sync`](../sk-notebooklm-phone-sync/SKILL.md). Lệnh gọi tường minh cho phép thực hiện sync được yêu cầu, nhưng không cho phép xóa sources/notes hoặc sửa NotebookLM ngoài phạm vi đã nêu.
