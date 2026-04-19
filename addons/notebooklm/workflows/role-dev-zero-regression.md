---
description: "Senior Dev / Tech Lead: Phân tích chéo tài liệu kiến trúc và SDK mới để giảm regression trước khi code"
---

# Zero-Regression System Design

**Role**: Senior Developer / Tech Lead

## Skills sử dụng
- Knowledge Ingestion, Structured Research, Cross-Notebook Validation, Context Query, Architecture Recall

## MCP Tools
- `source_add`, `research_start`, `research_status`, `research_import`, `cross_notebook_query`, `notebook_query`

## Input
- URL API hoặc SDK mới, `architecture.md`, design notes, code diff hoặc change intent

## Output
- Risk assessment, constraint list, implementation brief

## Các bước thực thi
1. Nạp tài liệu thư viện mới và tài liệu kiến trúc hiện tại bằng `source_add`
2. Dùng `research_start` để tải và nghiên cứu tài liệu thư viện hoặc API mới
3. Chờ `research_status` hoàn tất, dùng `research_import` để import sources
4. Dùng `cross_notebook_query` để đối chiếu giữa tài liệu mới và kiến trúc dự án
5. Dùng `notebook_query` hỏi rõ shared constraints, backward compatibility, side effects
6. Tạo brief trước khi bắt đầu sửa code

## Guardrails
- Không xem output là cam kết tuyệt đối zero-regression
- Luôn review lại với codebase thật và test hiện có
- Chỉ coi đây là gate trước coding, không phải thay thế testing

## Definition of Done
- [ ] Có danh sách constraints rõ
- [ ] Có risk list rõ
- [ ] Có các giả định cần xác minh
- [ ] Có implementation brief đủ để giao việc hoặc bắt đầu code

## Khi nào dùng
- Tích hợp công nghệ mới, đổi SDK, sửa logic core business, refactor module có ràng buộc cao
