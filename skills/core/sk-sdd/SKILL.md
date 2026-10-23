---
name: sk-sdd
description: Tạo technical spec khi người dùng yêu cầu spec-driven development hoặc một thay đổi kiến trúc, API hay dữ liệu cần chốt quyết định thiết kế trước khi implement. Không kích hoạt cho feature thông thường đã rõ.
---

# Spec-Driven Development (SDD) — sk-sdd

## 🎯 Mục tiêu

Giúp người dùng xem xét các quyết định kỹ thuật có ảnh hưởng lớn trước khi thay đổi
codebase. Skill này chỉ dùng khi được yêu cầu hoặc khi còn một quyết định kiến trúc,
API hay dữ liệu mà agent không thể chốt an toàn từ yêu cầu/context hiện có.

---

## 🚀 Quy Trình Thực Thi Của Agent

### Bước 1: Soạn spec phù hợp
Khi spec được yêu cầu, tạo hoặc cập nhật file tại đường dẫn:
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

### Bước 3: Chốt quyết định còn thuộc về người dùng
Nếu user yêu cầu spec-only/approval gate, dừng sau khi trình spec. Nếu yêu cầu
implement nhưng còn một quyết định có thể đổi contract, dữ liệu hoặc kiến trúc,
chỉ hỏi đúng quyết định đó trước khi tiếp tục. Không tạo pause gate chỉ vì đã có file spec.

Khi cần approval, nêu rõ:
    > "Tôi đã thiết lập bản đặc tả kỹ thuật (Spec) tại `.agents/sdd/design_spec.md`. Vui lòng xem qua và phê duyệt bằng cách phản hồi 'Approved' hoặc 'Proceed' để tôi bắt đầu viết code."
*   Chỉ dừng khi cần approval thật sự; nếu không, tiếp tục trong phạm vi đã được giao.

---

## 🛡️ Guardrails

*   Spec không phải điều kiện bắt buộc cho task thông thường.
*   **Đúng trọng tâm kỹ thuật:** Spec tập trung vào cấu trúc code, DB, API, validation — không viết lan man sang phân tích nghiệp vụ dài dòng.
*   **Bám sát template dự án:** Đọc kỹ `.agents/context/templates/` (nếu có) để định nghĩa cấu trúc Spec đúng chuẩn dự án.
