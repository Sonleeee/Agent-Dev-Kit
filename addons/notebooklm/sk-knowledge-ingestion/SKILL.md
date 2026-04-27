---
name: sk-knowledge-ingestion
description: Đưa tài liệu thô vào notebook để tạo nền tri thức
---

# Knowledge Ingestion

## Công dụng
Đưa tài liệu thô vào notebook để tạo nền tri thức.

## MCP Tools
- `source_add` — thêm sources (url, text, drive, file)
- `source_sync_drive` — đồng bộ Drive sources
- `notebook_create` — tạo notebook mới
- `notebook_rename` — đổi tên/cập nhật notebook
- `notebook_list` — liệt kê notebooks hiện có
- `tag` (action=add) — gán tags để phân loại

## Input
- URL tài liệu, meeting transcript, PRD, API docs, feedback, logs

## Output
- Notebook đã có nguồn dữ liệu đúng ngữ cảnh

## Khi nào dùng
- Đầu dự án, đầu workflow mới, khi có tài liệu mới cần cập nhật

## Lưu ý
- Không query trên dữ liệu rỗng hoặc sai notebook
- Luôn gán tags để dễ tìm lại
