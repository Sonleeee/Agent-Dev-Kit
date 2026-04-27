---
name: NotebookLM MCP Skills
description: Bộ skills sử dụng NotebookLM MCP để quản trị tri thức, tạo artifact và hỗ trợ delivery cho các vai trò Senior
---

# NotebookLM MCP Skills

Bộ skills này biến NotebookLM từ công cụ hỏi đáp thành hệ thống quản trị tri thức và hỗ trợ delivery.

## Nguyên tắc

- Không xem NotebookLM là nơi trả lời thay con người
- Xem NotebookLM là nơi tổng hợp tri thức và tạo artifact để con người ra quyết định nhanh hơn
- Mọi workflow quan trọng đều cần guardrails và definition of done

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
| 1 | Knowledge Ingestion | `knowledge-ingestion/` | Đưa tài liệu thô vào notebook |
| 2 | Context Query | `context-query/` | Hỏi đáp theo ngữ cảnh notebook |
| 3 | Spec Summarizer | `spec-summarizer/` | Tóm tắt PRD, BRD, API spec |
| 4 | Cross-Notebook Validation | `cross-notebook-validation/` | So sánh chéo nhiều notebooks |
| 5 | Requirement Extraction | `requirement-extraction/` | Trích yêu cầu từ tài liệu |
| 6 | Risk Radar | `risk-radar/` | Xác định rủi ro và unknowns |
| 7 | Meeting-to-Action | `meeting-to-action/` | Chuyển biên bản thành action items |
| 8 | Architecture Recall | `architecture-recall/` | Truy vấn quyết định kiến trúc |
| 9 | UX Rule Extractor | `ux-rule-extractor/` | Bóc tách flow, edge case, validation |
| 10 | Structured Research | `structured-research/` | Nghiên cứu tài liệu mới |
| 11 | Artifact Generation | `artifact-generation/` | Tạo deliverable từ tri thức |
| 12 | Operational Notes | `operational-notes/` | Ghi runbook, checklist vận hành |
| 13 | System Health | `system-health/` | Kiểm tra sức khỏe MCP system |
| 14 | Mobile Capture | `mobile-capture/` | Bóc tách & phân loại content từ iPhone (📥 Inbox) |
| 15 | Daily Task Sync | `daily-task-sync/` | Đồng bộ tasks từ 📋 Daily Ops về local |

## Gợi ý theo Role

| Role | Skills ưu tiên |
|------|---------------|
| Dev / Tech Lead | Context Query, Architecture Recall |
| BA | Requirement Extraction, Spec Summarizer, Cross-Notebook Validation |
| PM / PO | Risk Radar, Meeting-to-Action, Artifact Generation |
| QA | Context Query, Cross-Notebook Validation, Artifact Generation |
| SRE / DevOps | Operational Notes, Context Query, Artifact Generation |
| Designer | UX Rule Extractor, Cross-Notebook Validation |
| Personal / Mobile | Mobile Capture, Daily Task Sync, Knowledge Ingestion |

## Workflows liên quan

Xem `c:\Sonlee\.agents\workflows\notebooklm\` hoặc dùng `/notebooklm_senior_roles` để xem danh sách workflows.

### Phone Sync (iPhone → SecondBrain)
- `/sk-phone-sync` — Đồng bộ nhanh từ iPhone qua NotebookLM về SecondBrain (xem `workflows/phone-sync.md`)
