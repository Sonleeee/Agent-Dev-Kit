---
id: scaffold
type: addon-bridge
entry-command: /wf-scaffold
replacement-skill: sk-system-design-scaffold
status: deprecated
invocation: explicit-only
---

# Adapter cũ: `/wf-scaffold`

Lệnh này được giữ tạm để tương thích khi người dùng gọi trực tiếp `/wf-scaffold`. Đây là adapter tường minh, không phải trigger mặc định cho câu hỏi kiến trúc.

Khi được gọi trực tiếp, hãy làm theo [`sk-system-design-scaffold`](../skills/sk-system-design-scaffold/SKILL.md). Adapter không chứa procedure riêng và không cho phép ghi đè thư mục đích đã có nội dung.
