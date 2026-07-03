---
name: sk-sdd
description: |
  Thiết lập thiết kế kỹ thuật (Technical Spec) chi tiết trước khi code.
  Buộc Agent ghi nhận spec vào `.agents/sdd/design_spec.md` và chờ User phê duyệt.
inputs:
  - requirement: Yêu cầu nghiệp vụ hoặc mô tả task đã làm rõ
output:
  - design_spec: File thiết kế `.agents/sdd/design_spec.md`
---

# Spec-Driven Development (SDD) — sk-sdd

## 🎯 Mục tiêu

Đảm bảo tính đồng thuận về mặt kỹ thuật giữa Người và AI trước khi thay đổi codebase. Agent bắt buộc phải thiết lập bản đặc tả kỹ thuật chi tiết (Technical Spec) và nhận được sự phê duyệt (Approved) của User trước khi viết bất kỳ dòng mã nguồn production nào.

---

## 🚀 Quy Trình Thực Thi Của Agent

### Bước 1: Khởi tạo/Cập nhật tài liệu Spec
Khi nhận task có độ phức tạp trung bình trở lên (có thay đổi DB, thêm API, đổi logic luồng chính), Agent tạo hoặc cập nhật file spec tại đường dẫn:
```
[project-root]/.agents/sdd/design_spec.md
```

### Bước 2: Cấu trúc bắt buộc của design_spec.md
Bản Spec kỹ thuật phải định rõ các nội dung sau (nếu liên quan):
1.  **Database Changes:**
    - Schema bảng mới hoặc thay đổi cột (nếu có).
    - Các trường dữ liệu, kiểu dữ liệu, ràng buộc (Nullability, Unique, Foreign Key).
    - Ý định migration script.
2.  **API Handler & CQRS Pattern:**
    - Cấu trúc Controller, Route Endpoint, Http Method (POST, GET, PUT, DELETE).
    - MediatR Request (Command/Query) và Response.
    - Logic nghiệp vụ xử lý chính của Handler.
3.  **DTOs & Contracts:**
    - Danh sách thuộc tính của Request DTO và Response DTO.
    - Kiểu dữ liệu tương ứng.
4.  **Validation Rules:**
    - Các luật ràng buộc dữ liệu đầu vào (ví dụ: FluentValidation trong C# hoặc Zod Schema trong JS).
    - Các thông điệp báo lỗi (Error Messages).

### Bước 3: Đợi User Phê Duyệt (PAUSE Gate)
*   Sau khi viết xong Spec, Agent **TUYỆT ĐỐI KHÔNG** được tự động chuyển sang viết code logic.
*   Agent hiển thị thông báo rõ ràng cho User:
    > "Tôi đã thiết lập bản đặc tả kỹ thuật (Spec) tại `.agents/sdd/design_spec.md`. Vui lòng xem qua và phê duyệt bằng cách phản hồi 'Approved' hoặc 'Proceed' để tôi bắt đầu viết code."
*   Agent dừng lại và chờ phản hồi từ User.

---

## 🛡️ Guardrails

*   **Không code trước spec:** Vi phạm SDD (viết code trước khi chốt spec) là lỗi nghiêm trọng.
*   **Đúng trọng tâm kỹ thuật:** Spec tập trung vào cấu trúc code, DB, API, validation — không viết lan man sang phân tích nghiệp vụ dài dòng.
*   **Bám sát template dự án:** Đọc kỹ `.agents/context/templates/` (nếu có) để định nghĩa cấu trúc Spec đúng chuẩn dự án.
