---
name: context-update
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

## Quy trình cập nhật (Update Workflow)

### Bước 1 - Load Context hiện tại

- Phải đọc trước nội dung các file hiện có như `architecture.md`, `checklist.md` hay file template cụ thể liên quan để nắm hiện trạng.

### Bước 2 - Đánh giá Mức độ tác động

- Đánh giá kiến thức mới này thuộc nhóm nào: Định lý kiến trúc (Architecture), Quy tắc Check-list (Checklist), hay Đoạn code tái sử dụng (Code Templates)?
- Xem xét có gây mâu thuẫn (Conflict/Override) với rule hiện tại không, nếu có: Yêu cầu ghi chú rõ lý do deprecate rule cũ.

### Bước 3 - Tiến hành Chỉnh sửa (Patching)

Thực hiện chỉnh sửa file thuộc thư mục `.agents/context/`:
- **Architecture**: Bổ sung gạch đầu dòng những lưu ý mới.
- **Checklist**: Thêm thẻ (ví dụ `T15`, `T16`) cho những rào cản chất lượng mới phát hiện.
- **Templates**: Chỉnh sửa mã nguồn trong folder `templates/` thành cấu trúc mới mẻ, an toàn hơn.

### Bước 4 - Khôi phục đồng bộ

- Rà soát lại tất cả các file sau khi edit để chắc chắn formatting Markdown đang đúng và dễ hiểu cho các lần đọc sau của LLM.

## Output

Sinh ra một Markdown Review Report gọn gàng chứa:
- Tên các file được tác động.
- Điểm nội dung mới được cập nhật (Tóm lược).
- Lý do thay đổi (Tại sao đổi / Thêm vào vì bài học gì).

## Guardrails (Nguyên tắc)

- **Nguyên tắc kế thừa**: Không bao giờ tẩy xóa hoàn toàn các ghi chú cũ nếu chúng vẫn đúng cho các module legacy (hãy đánh dấu `[Legacy]` nếu cần).
- **Luôn kiểm định lý do**: Đừng gộp các fix bug cá nhân thành "Architecture Rule", chỉ cập nhật rule nếu bug mang tính hệ thống cao.
