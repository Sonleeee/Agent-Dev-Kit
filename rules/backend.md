---
trigger: glob
paths:
  - "**/src/backend/**/*"
  - "**/api/**/*"
  - "**/*.{go,py,java,cs,php,rb}"
---

# Backend Rules

Các quy tắc áp dụng riêng cho Logic, API và Database.

## Nhóm 1 — API Contract [PROTECTED]

### Contract Status [PROTECTED]
- Phải đánh dấu `API contract: OK` hoặc `API contract: Risk` trước khi kết thúc task.
- Chặn mọi breaking change không được phê duyệt trong plan.

## Nhóm 2 — Security & Data [PROTECTED]

### Secret Management [PROTECTED]
- Tuyệt đối không hardcode credentials/keys.
- Luôn sử dụng env variables hoặc secret manager.

### Destructive Ops [PROTECTED]
- Các lệnh xóa dữ liệu hàng loạt hoặc drop table phải có bước xác nhận rõ ràng với user.

## Nhóm 3 — Engineering Excellence [PROTECTED]

### TDD Hybrid (Core Logic) [PROTECTED]
- Phải viết Unit Test và chạy FAIL trước khi viết code cho các logic cốt lõi.
- Đảm bảo coverage cho các nhánh rẽ quan trọng.

### Error Taxonomy [OVERRIDABLE]
- Phân loại lỗi rõ ràng: Input validation, Not Found, Business Logic, System Error.
- Map đúng HTTP Status Codes.
