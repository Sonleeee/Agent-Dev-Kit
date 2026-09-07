---
name: sk-execution-contract
description: |
  Giữ agent bám task contract, context pack và progress ledger trong suốt
  phiên; chống drift, mất vị trí sau compaction và báo done khi chưa có evidence.
context-required: recommended
output: markdown ledger trong .agents/runtime/<task-id>/
---

# Execution Contract — Always-On Task Discipline

## Khi nào dùng

Kích hoạt ở đầu mọi task có thay đổi, debug, review hoặc quyết định kiến trúc.
Với câu hỏi thuần thông tin không sửa project, chỉ cần route tới workflow phù hợp.

## Bootstrap bắt buộc

Trước công cụ đầu tiên:

1. Đọc `AGENTS.md`, `.agents/SYSTEM.md`, `.agents/rules/global.md`.
2. Nếu có, đọc `.agents/context/manifest.md`; sau đó chỉ nạp TIER-1 liên quan.
3. Chọn workflow và ghi rõ trong contract.
4. Tạo `.agents/runtime/<task-id>/execution-contract.md` từ template.
5. Ghi objective, in/out, acceptance criteria, risk và evidence cần thu thập.

Nếu host không cho phép ghi runtime artifact, giữ nguyên contract trong output của
workflow và không giả vờ rằng ledger đã tồn tại.

## Trong khi thực thi

- Mỗi task phải bounded, có file/symbol cụ thể và một bước verify độc lập.
- Không tự mở rộng scope. Phát hiện việc ngoài scope thì ghi `UNPLANNED` và ruling.
- Sau mỗi phase (`clarify`, `plan`, `impl`, `review`) cập nhật ledger một dòng.
- Tác vụ độc lập có thể giao subagent mới; truyền context tối thiểu và không chia sẻ
  lịch sử chat không cần thiết.
- Sau mỗi subtask, chạy hai kiểm tra: **spec compliance** rồi **code quality**.
- Khi context bị nén hoặc phiên tiếp tục, đọc ledger trước; task đã `complete` không
  được chạy lại.

## Minimality checkpoint

Trước khi thêm code/abstraction/dependency, agent phải trả lời ngắn:

1. Có cần tồn tại không?
2. Đã có helper/pattern trong repo chưa?
3. Standard library hoặc native platform có đủ không?
4. Cách ít file và ít state nhất là gì?

Không được giản lược away validation ở trust boundary, security, accessibility,
error handling chống mất dữ liệu, hoặc điều user yêu cầu rõ ràng.

## Kết thúc

Chỉ báo `READY` khi contract có:

- acceptance criteria đã đánh dấu;
- build/test hoặc lý do miễn giảm có evidence;
- changed files và unplanned changes;
- review spec + quality;
- status cuối cùng `READY`, `BLOCKED`, hoặc `NEEDS_USER_DECISION`.

Không dùng các câu như “đã hoàn tất” thay cho lệnh kiểm chứng và kết quả.
