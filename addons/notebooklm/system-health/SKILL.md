---
name: System Health
description: Kiểm tra sức khỏe hệ thống MCP, auth và library
---

# System Health

## Công dụng
Kiểm tra sức khỏe hệ thống MCP, auth và library.

## MCP Tools
- `server_info` — kiểm tra version và trạng thái server
- `refresh_auth` — refresh auth tokens khi hết hạn
- `notebook_list` — xem tổng quan notebooks

## Input
- Trạng thái runtime

## Output
- Health status, recovery action

## Khi nào dùng
- Tool lỗi, auth fail, cần kiểm tra status

## Lưu ý
- Giữ công cụ ổn định để team dùng lâu dài
