---
name: adk-api-contract-guard
description: |
  Bảo vệ API contract khi implement hoặc fix bug. Dùng khi thay đổi endpoint,
  DTO, status code, response shape để tránh breaking change ngoài ý muốn.
  Hoạt động với mọi tech stack — không cần project context.
---

# API Contract Guard

## Mục tiêu
Phát hiện breaking change trước khi ship, tránh FE/BE drift không kiểm soát.

## Khi nào chạy
- `API contract changed: Yes` trong discovery report
- `API contract changed: Unknown` — chạy để xác nhận
- Bất cứ khi nào thay đổi: route, method, status code, request schema, response schema

## Checklist

### Route & Method
- [ ] Route cũ có bị đổi không? (path params, query params)
- [ ] HTTP method có thay đổi? (GET→POST...)
- [ ] Route mới có conflict với route khác không?

### Status Code
- [ ] Status code thành công có thay đổi? (200→201, 200→204...)
- [ ] Status code lỗi có thay đổi behavior? (400→422, 404→400...)
- [ ] Error response format có thay đổi structure?

### Request Schema
- [ ] Field bắt buộc có được thêm vào (breaking cho caller cũ)?
- [ ] Field có bị đổi tên hoặc đổi type?
- [ ] Enum values có bị bỏ hoặc đổi tên?
- [ ] Nullability có thay đổi? (required → optional hoặc ngược lại)

### Response Schema
- [ ] Field có bị đổi tên hoặc bị xóa?
- [ ] Field có bị đổi type hoặc format?
- [ ] Nested structure có thay đổi?
- [ ] Array vs object có thay đổi?
- [ ] Null/empty behavior có thay đổi?

### Pagination & Filter
- [ ] Pagination response format có thay đổi? (page/pageSize/total...)
- [ ] Filter params có thay đổi tên hoặc behavior?
- [ ] Default values của filter có thay đổi?

### Hyrum's Law (Hành vi Ngầm định — Implicit Behavioral Contract)
> *"Với một số lượng người dùng đủ lớn, mọi hành vi quan sát được của hệ thống đều sẽ có bên phụ thuộc vào nó, bất kể tài liệu chính thức viết gì."*
- [ ] Thứ tự sắp xếp mặc định (default sort order) của danh sách trả về có bị thay đổi không?
- [ ] Định dạng chuỗi lỗi (`error message` / `error code`), định dạng ngày giờ (ISO-8601 timezone `Z` vs `+07:00`) có bị đổi ngầm không?
- [ ] Hành vi phân biệt hoa-thường (case-sensitivity) hoặc tự động `trim()` khoảng trắng của tham số đầu vào có thay đổi không?

## Output
Dùng template `templates/api-contract-checklist.md.template`.

**Kết luận bắt buộc:**
- `Contract: OK` — không có breaking change
- `Contract: Risk` — có thay đổi, đã documented, FE/consumer đã biết

## Guardrails
- Không tự quyết "OK" khi còn uncertainty — ghi rõ Risk + ghi chú
- Nếu breaking change là bắt buộc → document migration path cho consumer
