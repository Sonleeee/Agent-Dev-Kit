---
id: vault-sync
type: addon-bridge
entry-command: /wf-vault-sync
replacement-skill: adk-vault-steward
status: deprecated
invocation: explicit-only
---

# Adapter cũ: `/wf-vault-sync`

Đây là alias tường minh để tương thích với lệnh cũ; không tự chạy ở cuối workflow hoặc vì agent phát hiện tri thức có thể lưu lại.

Khi người dùng gọi trực tiếp lệnh này, dùng [`adk-vault-steward`](../skills/adk-vault-steward/SKILL.md). Chỉ đọc/chuẩn bị candidate nếu chưa có yêu cầu ghi; trước mọi cập nhật, phải xác định vault và kiểm tra file đích.
