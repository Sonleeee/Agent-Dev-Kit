---
name: Architecture Recall
description: Truy vấn quyết định kiến trúc, integration, data flow, service ownership
---

# Architecture Recall

## Công dụng
Truy vấn các quyết định kiến trúc, integration, data flow, service ownership, technical constraints.

## MCP Tools
- `notebook_query` — hỏi về kiến trúc, boundaries, ownership

## Input
- Module, service, feature hoặc luồng hệ thống cần tra cứu

## Output
- Kiến trúc liên quan, dependencies, ownership, constraints

## Khi nào dùng
- Refactor, bug khó, thiết kế feature mới, review thay đổi lớn

## Lưu ý
- Tránh sửa sai boundary
- Giữ implementation sát với thiết kế hệ thống
