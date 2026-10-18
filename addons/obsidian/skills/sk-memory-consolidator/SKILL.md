---
name: sk-memory-consolidator
description: |
  Kỹ năng chưng cất tri thức (Dream Phase) và quản lý bộ nhớ dài hạn.
  Ghi nhận nhật ký tương tác chat-by-chat và nén thành tri thức tinh gọn lưu vào Obsidian Vault.
output: markdown (Tri thức nén lưu vào Obsidian Vault/00_Raw/)
---

# 🧠 Chưng Cất Tri Thức & Quản Lý Bộ Nhớ — sk-memory-consolidator

## 🎯 Mục tiêu

Giúp AI Agent tự động ghi nhận tri thức từ các cuộc hội thoại làm việc hàng ngày, loại bỏ thông tin rác (chat rác) và tự động chưng cất thành các ghi chú tri thức có giá trị lâu dài để lưu trữ vào [Obsidian Vault](file:///<path-to-vault>).

---

## ⚙️ Cơ chế hoạt động 2 Pha

### Pha 1: Ghi nhận Nóng (Chat-by-Chat Log)
*   **Trigger:** Mỗi khi có lượt tương tác (User gửi Prompt và Agent phản hồi).
*   **Hành động của Agent:** 
    *   Tự động ghi nối tiếp (append) toàn bộ nội dung chat hiện tại vào file log tạm thời tại: `[project-root]/.agents/scratch/current_session.log`.
    *   Giữ nguyên định dạng Markdown của cuộc hội thoại để lưu trữ ngữ cảnh thô đầy đủ nhất.

### Pha 2: Chưng cất Tri thức (Consolidation - Dream Phase)
*   **Trigger:** Khi kết thúc một Task lớn (khi User gõ `/done`, `/ship` hoặc hoàn thành Gate 3 của workflow).
*   **Quy trình của Agent:**
    1.  **Ingestion:** Đọc file log tạm thời `.agents/scratch/current_session.log`.
    2.  **Fact Extraction (LLM-based):** Sử dụng LLM để phân tích toàn bộ log và lọc ra các nội dung cốt lõi bao gồm:
        *   *Quyết định kiến trúc (Architectural Decisions):* Tại sao lại chọn giải pháp này thay vì giải pháp kia?
        *   *Sửa lỗi quan trọng (Bug Fix Insights):* Lỗi gì đã xảy ra, nguyên nhân gốc rễ và cách khắc phục?
        *   *Quy ước dự án (Convention Insights):* Các quy tắc, convention mới được thiết lập trong quá trình làm việc.
    3.  **Deduplication & Format:** Loại bỏ các thông tin rác (như chào hỏi, code nháp bị lỗi, fix lỗi cú pháp nhỏ). Đóng gói tri thức thành định dạng Ghi chú tri thức (Knowledge Note) kèm theo tags, ngày tạo và dự án tham chiếu.
    4.  **Sync to Obsidian Vault:** 
        *   Ghi file ghi chú mới vào thư mục `Obsidian Vault/00_Raw/` dưới tên file có format: `[yyyy-mm-dd]_[tên-tri-thức-tóm-tắt].md`.
        *   Cập nhật liên kết file mới vào file chỉ mục `Obsidian Vault/01_Wiki/01_AI_Agents/INDEX.md` hoặc `AI_INDEX.md`.
    5.  **Reset:** Xóa rỗng file `.agents/scratch/current_session.log` để chuẩn bị cho session làm việc tiếp theo.

---

## 📝 Định dạng file Tri thức lưu vào Obsidian Vault (Output Template)

```markdown
---
type: raw_knowledge
domain: [tên-dự-án-tham-chiếu]
tags: [tag-chủ-đề, ví-dụ: memory, bug-fix, c-sharp]
created: YYYY-MM-DD
---

# [Tiêu đề Tri thức Tóm tắt]

## 1. Bối cảnh & Vấn đề (Context & Issue)
[Mô tả vấn đề hoặc lý do phát sinh quyết định thiết kế này]

## 2. Giải pháp & Tri thức chưng cất (Key Insight)
[Chi tiết giải pháp, code snippet chuẩn, hoặc bài học kinh nghiệm rút ra]

## 3. Tham chiếu (References)
- Project: [Tên dự án]
- Session date: YYYY-MM-DD
```
