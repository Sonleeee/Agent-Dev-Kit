---
name: context-create
description: |
  Khởi tạo, định nghĩa và tổng hợp Context chuẩn cho dự án.
  Dùng khi dự án mới bắt đầu, hoặc khi phát hiện một Feature/Domain hoàn toàn mới
  chưa có kiến trúc/mẫu chuẩn trong `.agents/context/`.
context-required: optional
output: markdown (tạo các file trong `.agents/context/`)
---

# Khởi Tạo Context (Context Creation)

## Mục tiêu

Xây dựng kho tàng kiến thức (Architecture, Code Templates, Rules) để toàn bộ các Agents khác có thể follow theo khi implement code.

## Khi nào sử dụng?

- Khi onboard một project hoàn toàn mới vào Agent-Dev-Kit.
- Khi một Module/Domain hoàn toàn mới ra đời, mang theo các setup kiến trúc chưa từng có (Pattern mới, Thư viện mới).

## Quy trình khởi tạo (Creation Workflow)

### Bước 1 - Phân tích đầu vào (Input Analysis)

- Yêu cầu cung cấp hoặc quét mã nguồn 1 module mẫu đã được review tốt.
- Xác định Tech Stack dùng cho front-end, back-end.
- Nhận dạng Layering (VD: Controller -> Handler -> Repository).

### Bước 2 - Định nghĩa Kiến trúc (Architecture Setup)

Tạo hoặc cập nhật file `.agents/context/architecture.md`:
- Chỉ rõ flow dữ liệu đi qua các layer.
- Nêu rõ thư viện/phụ thuộc cốt lõi cho module này.
- Mô tả các Anti-patterns (Những gì tuyệt đối KHÔNG được làm).

### Bước 3 - Thiết lập Checklist (Quality Bar)

Tạo hoặc cập nhật file `.agents/context/checklist.md`:
- Đưa ra các yếu tố "Must-have" cho module này (Validation, Transactions, Permissions).
- Ghi chú các edge cases phổ biến.

### Bước 4 - Tạo Code Templates 

Extract mã nguồn từ module mẫu thành các file `*.template` nằm trong `.agents/context/templates/`:
- Làm sạch template: Loại bỏ logic nghiệp vụ tĩnh, thay bằng biến placeholder như `[EntityName]`, `[PropType]`.
- Thêm file `.md.template` làm Master Guide hướng dẫn Agent cách sử dụng những template code này nếu thấy cần.

## Output

Báo cáo tóm tắt dưới dạng Markdown các thay đổi/file được thêm mới trong hệ thống File System (chủ yếu nằm ở thư mục `.agents/context/`).

## Guardrails (Nguyên tắc)

- **Không copy mù quáng**: Đảm bảo loại bỏ logic rác khỏi code template.
- **Tiêu cự**: Tập trung mô tả KIẾN TRÚC chứ không mô tả DATA DOMAIN (không mô tả bảng user có cột gì, mà mô tả cách query bảng ra sao).
