---
name: sk-context-update
description: |
  Đưa những bài học, quy chuẩn hoặc Code Templates mới phát sinh trong quá trình
  tạo Feature/Sửa Lỗi (Build Time) vào tài liệu Context chung chuẩn hóa của dự án.
context-required: required
output: markdown (cập nhật file trong `.agents/context/`)
---

# Cập Nhật Context (Context Update)

## Mục tiêu

Tránh việc các Agents cứ lặp đi lặp lại một lỗi cũ, hoặc sử dụng hệ thống code cũ chưa được refactor bằng cách cập nhật quy định lập trình, code snippet tốt nhất vào sổ tay `.agents/context/`.

## Khi nào sử dụng?

- Sau khi kết thúc một Epic, tính năng khó và Rút ra được kết luận/điều chỉnh trong kiến trúc (ví dụ: Quyết định chuyển từ Date sang DateTimeOffset, hay chốt cách quản lý Error Handling mới).
- Khi phát hiện một đoạn code/pattern mới tối ưu hơn cách cũ, muốn Agent lần tới dùng cách mới này thay vì làm theo lối mòn.

## Quy trình cập nhật (Global Scan & Cross-Reference Workflow)

Tương tự như quá trình khởi tạo, việc cập nhật Context không được làm tĩnh hoặc suy đoán mù quáng mà phải dựa trên dữ liệu thực tế (Data-driven) và qua trung gian phê duyệt:

### Bước 1 - Quét Toàn Bộ Source & Đối Chiếu Chỉ Mục

- Read Context: Đọc file chỉ mục gốc (ví dụ `.agents/context/TEMPLATES-GUIDE.md`) cùng các file Architecture/Checklist.
- Quét và Đối chiếu chéo (Cross-reference): Rà soát toàn bộ source code xem có những đoạn code, luồng, hoặc pattern nào ĐANG LỆCH so với quy chuẩn trong chỉ mục, hoặc ĐƯỢC SINH MỚI (Pattern/Thư viện tối ưu hơn) trong quá trình Maintain/Feature mới.

### Bước 2 - Lập Bảng So Sánh (Comparison Table)

- Từ dữ liệu Bước 1, tạo ra một **Bảng So Sánh (Before / After)** rõ ràng:
  - **Cột 1: Pattern/Rule Cũ** (Theo file Context hiện tại).
  - **Cột 2: Pattern/Rule Mới** (Phát hiện trên Source code thực tế).
  - **Cột 3: Ghi chú/Minh chứng** (Cho biết đang nằm ở các module nào, tần suất bao nhiêu).

### Bước 3 - User Review & Selection (Chấp Thuận)

- Trình diễn Comparison Table này cho User (Show Preview).
- **Review sự chuẩn xác của code (Pattern Review):** Trước khi quyết định update, Agent và User phải cùng rà soát đoạn code/pattern mới xem có thực sự viết đúng pattern chuẩn không, có chứa code smell hay vi phạm nguyên tắc hệ thống không.
- **CHỜ XÁC NHẬN:** User sẽ đóng vai trò Reviewer, đọc bảng và tick chọn những update nào thực sự là sự **tiến hóa của kiến trúc** (Architecture Evolution) cần chuẩn hóa, và loại bỏ những bad-practice/fix bug cá nhân rẻ tiền.

### Bước 4 - Patching & Cập Nhật Chỉ Mục

Thực hiện chỉnh sửa `.agents/context/` dựa ĐÚNG trên các điểm User đã chọn:
- Ghi đè hoặc tạo mới Code Templates (`*.template`).
- **Cập nhật lại file Chỉ Mục (`TEMPLATES-GUIDE.md`)** chứa mô tả (Description) rõ ràng về template mới, để AI/Dev sau này gọi đúng ngữ cảnh.
- Thay đổi `architecture.md` / `checklist.md` nếu liên quan (Bảo lưu rule cũ bằng tag `[Legacy]` nếu các module cũ chưa kịp migrate).

## Output

Sinh ra một Markdown Review Report gọn gàng chứa:
- Tên các file được tác động.
- Điểm nội dung mới được cập nhật (Tóm lược).
- Lý do thay đổi (Tại sao đổi / Thêm vào vì bài học gì).

## Guardrails (Nguyên tắc)

- **Nguyên tắc kế thừa**: Không bao giờ tẩy xóa hoàn toàn các ghi chú cũ nếu chúng vẫn đúng cho các module legacy (hãy đánh dấu `[Legacy]` nếu cần).
- **Luôn kiểm định lý do**: Đừng gộp các fix bug cá nhân thành "Architecture Rule", chỉ cập nhật rule nếu bug mang tính hệ thống cao.
