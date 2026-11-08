---
name: adk-source-ingest
description: Giao thức tiếp nhận nguồn thông tin mới, đối soát danh mục nhóm chuẩn và hỏi ý kiến người dùng trước khi phân loại vào SecondBrain & NotebookLM.
---

# 📥 ADK Source Ingestion & Group Routing Contract

Kỹ năng điều hướng nguồn tài liệu mới vào SecondBrain và NotebookLM.

## 🛑 Invariant: No Silent / Arbitrary Classification
1. Khi người dùng cung cấp link, repo, video hoặc bài viết:
   - **BẮT BUỘC** bóc tách bản chất kỹ thuật thực sự của nguồn.
   - **BẮT BUỘC** hiển thị danh sách các nhóm chuẩn hiện có (từ `02_Brain/GROUPS_INDEX.md`).
   - **BẮT BUỘC** highlight nhóm đề xuất `(Recommended)` kèm 1 dòng lý do kỹ thuật.
   - **DỪNG LẠI HỎI Ý KIẾN NGƯỜI DÙNG**, không tự ý gán bừa hay tự động đưa vào file khi chưa được người dùng xác nhận.
