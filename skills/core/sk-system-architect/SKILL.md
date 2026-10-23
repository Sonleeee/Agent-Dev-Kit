---
name: sk-system-architect
description: Tư vấn lựa chọn kiến trúc hoặc tra cứu pattern cho câu hỏi thiết kế hệ thống. Dùng system-design MCP khi addon đã bật; không tự phỏng vấn, scaffold hoặc sửa project.
---

# System Architect

## Mục tiêu

Giúp cân nhắc trade-off kiến trúc và giải thích pattern theo bài toán. Skill này
chỉ tư vấn/tra cứu; scaffold project thuộc `sk-system-design-scaffold` của addon
system-design và chỉ chạy theo yêu cầu rõ ràng.

## Nguyên tắc cốt lõi (Core Invariants)

1. **Dựa trên context và evidence:**
   Dùng project architecture, code hiện tại và yêu cầu làm nền. Nếu addon system-design
   đang bật và câu hỏi phù hợp, có thể tra MCP:
   - `search_patterns(query, category)`: Tìm pattern chuẩn đã được thẩm định.
   - `get_pattern_details(pattern_id)`: Lấy chi tiết bài toán, sơ đồ luồng Mermaid, invariants và code mẫu.

2. **Chọn mức phức tạp theo nhu cầu thực:**
   Cân nhắc team, vận hành, scale và consistency; không áp dụng ngưỡng user/team cố định.
   Ưu tiên giải pháp đơn giản đáp ứng yêu cầu và nêu trade-off.

## Các Công Cụ Khả Dụng (MCP Server: `system-design`)

| Tool Name | Khi Nào Sử Dụng? |
| :--- | :--- |
| `search_patterns` | Khi cần tìm pattern giải quyết một vấn đề (ví dụ: "outbox", "trùng đơn", "idempotency"). |
| `get_pattern_details` | Khi cần xem sơ đồ Mermaid, quy tắc bất biến và code boilerplate của 1 pattern cụ thể. |
| `recommend_architecture` | Khi cần tư vấn chọn mô hình kiến trúc phù hợp với quy mô tải và quy mô team. |

## Quy trình

1. Chốt constraint có ảnh hưởng: consistency, failure mode, throughput, vận hành,
   team và tech stack. Chỉ hỏi khi thiếu thông tin làm đổi lựa chọn.
2. Nếu MCP có sẵn, tìm pattern phù hợp và đọc chi tiết trước khi khuyến nghị.
   Nếu MCP chưa bật, không giả vờ đã tra cứu.
3. So sánh tối đa vài lựa chọn có khác biệt thật; giải thích trade-off và khuyến nghị
   khi user muốn chọn hướng.
4. Với yêu cầu tạo project/source base, chuyển sang `sk-system-design-scaffold`;
   không gọi `evaluate_interview`, `scaffold_project` hoặc `inject_pattern` từ skill này.
