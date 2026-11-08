---
name: adk-test-authoring
description: Viết hoặc mở rộng automated tests khi người dùng yêu cầu test authoring, tìm coverage gap, hoặc bổ sung test cho một module. Không thay thế TDD trực tiếp trong task implement thông thường.
---

# Test authoring

## Cách làm

1. Xác định behavior cần bảo vệ và convention test đang dùng trong repo.
2. **The Beyoncé Rule ("Nếu hành vi đó quan trọng, phải đặt một bài test tự động lên nó"):**
   Ưu tiên bảo vệ các bất biến nghiệp vụ cốt lõi, happy path quan trọng, boundary/error path
   liên quan và regression đã biết. Không tạo quota hoặc test cho mọi tổ hợp input.
3. **Ưu tiên DAMP hơn DRY trong Unit Test (Descriptive And Meaningful Phrases over DRY):**
   Viết từng bài test nhỏ, độc lập, tự chứa đầy đủ ngữ cảnh `Arrange-Act-Assert` để khi
   test đỏ có thể đọc hiểu ngay tại chỗ; dùng fixture/factory đơn giản hiện có nhưng tuyệt
   đối không gom chung helper/vòng lặp/if-else phức tạp bên trong code test khiến bài test
   mất tính tường minh.
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
