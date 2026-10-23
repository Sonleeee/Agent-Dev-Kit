---
name: sk-test-authoring
description: Viết hoặc mở rộng automated tests khi người dùng yêu cầu test authoring, tìm coverage gap, hoặc bổ sung test cho một module. Không thay thế TDD trực tiếp trong task implement thông thường.
---

# Test authoring

## Cách làm

1. Xác định behavior cần bảo vệ và convention test đang dùng trong repo.
2. Ưu tiên các trường hợp có ý nghĩa: happy path quan trọng, boundary/error path
   liên quan và regression đã biết. Không tạo quota hoặc test cho mọi tổ hợp input.
3. Viết test nhỏ, độc lập, dễ đọc; dùng fixture/factory hiện có thay vì thêm framework
   hoặc abstraction mới.
4. Chạy test mục tiêu nếu môi trường cho phép. Chỉ mở rộng sang suite lớn hơn khi
   thay đổi hoặc yêu cầu cần thiết.
5. Báo test nào đã thêm, lệnh đã chạy, kết quả và giới hạn còn lại.

## Khi task là TDD

Nếu user đang yêu cầu implementation behavior mới, coding agent nên viết một test
đại diện trước, xác nhận RED, implement tối thiểu để GREEN rồi refactor khi cần.
Không tạo handoff sang tester hoặc gọi workflow riêng cho từng vòng.

## Ranh giới

- Không tăng coverage bằng test trùng lặp hoặc assertion yếu.
- Không sửa production behavior để làm test pass nếu thay đổi đó không thuộc yêu cầu.
- Không khẳng định test suite pass khi chỉ chạy một test mục tiêu.
