---
name: sk-docs-maintenance
description: Cập nhật hoặc review documentation theo source of truth của repo khi người dùng yêu cầu sửa docs hoặc tìm drift. Không dùng cho một typo đơn giản nếu coding agent có thể sửa trực tiếp.
---

# Documentation maintenance

1. Xác định audience và source of truth: code, CLI output, config hoặc spec đã được
   duyệt. Không viết tính năng/behavior chưa tồn tại như thể đã triển khai.
2. Chỉ đọc docs và source liên quan; tìm drift trong phần user yêu cầu.
3. Sửa lượng nội dung nhỏ nhất đủ để hướng dẫn đúng cách dùng, giới hạn và ví dụ.
4. Kiểm tra links, command, version hoặc snippet bị ảnh hưởng. Render/preview chỉ khi
   định dạng tài liệu cần kiểm tra layout.
5. Báo docs đã đổi và những chi tiết chưa kiểm chứng.

Không bắt buộc tạo report, gọi subagent hoặc scan toàn bộ tài liệu cho một thay đổi nhỏ.
