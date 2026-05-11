---
id: modernize
type: setup
entry-command: /wf-modernize
description: Nâng cấp dự án hiện tại lên Agent-Dev-Kit Phase 3 (Automation & Tiered Context).
---

# /wf-modernize — Project Modernization

**Mục tiêu:** Nâng cấp cấu trúc context của dự án cũ để tương thích với các tính năng tự động hóa (Phase 3) và kiến trúc Tiered Context (tiết kiệm token).

## Khi nào dùng

- Khi bạn muốn áp dụng các tính năng mới (predict, retro, vault sync) cho một dự án đã có context từ trước.
- Khi muốn tối ưu token bằng cách chuyển sang Tiered Architecture format.

## Flow

```
Bước 1: Passport Connection (AGENTS.md)
  ├─ Agent đọc AGENTS.md hiện tại
  ├─ Thêm/Update vault-path và kit-path
  └─ Output: Kết nối thành công với SecondBrain

Bước 2: Architecture Tiering (Tiered Context)
  ├─ Đọc architecture.md cũ
  ├─ Phân loại nội dung vào TIER-0 (Core), TIER-1 (Detail), TIER-2 (Reference)
  ├─ Áp dụng TAG markers cho TIER-1
  └─ Output: architecture.md chuẩn Phase 3

Bước 3: Context Drift Sync (sk-context-update)
  ├─ Chạy sk-context-update (Batch-of-3)
  ├─ So sánh context vừa tier-hóa với source code thực tế
  └─ Trình user approve các thay đổi/pattern mới
  └─ Output: Context đồng bộ 100% với Code

Bước 4: Connectivity Test
  ├─ Test gọi sk-vault-steward (thử ghi 1 log nhỏ vào vault)
  └─ Verify các lệnh /wf-predict, /wf-retro đã sẵn sàng

Bước 5: Final Report & Cleanup
```

## Chi tiết Bước 2: Quy tắc Tiering

Khi chuyển đổi `architecture.md`, Agent tuân thủ:
- **TIER-0**: Chỉ giữ lại Naming, Layers, và Folder structure (giới hạn ≤200 lines).
- **TIER-1**: Chuyển các chi tiết về coding patterns vào đây, bọc trong `[TAG: name]`.
- **TIER-2**: Chuyển các ví dụ Code (✅/❌), Pitfalls, và baseline modules vào đây.

## Chi tiết Bước 3: Drift Detection

Agent chủ động tìm:
- Các pattern mới xuất hiện trong code nhưng chưa có trong architecture cũ.
- Các rule cũ trong architecture nhưng thực tế code đã không còn dùng (Legacy).

## Guardrails

- **Không ghi đè mù quáng**: Luôn backup hoặc dùng `replace_file_content` cẩn thận.
- **Giữ lại logic cũ**: Không được làm mất các quy tắc đặc thù của dự án khi phân tầng.
- **User Confirmation**: Mọi bước thay đổi cấu trúc file PHẢI được user approve.
- **Tiếng Việt**: Tóm tắt thay đổi luôn bằng Tiếng Việt.
