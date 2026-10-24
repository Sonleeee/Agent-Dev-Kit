---
name: adk-business-discovery
description: Làm rõ mục tiêu, phạm vi và ràng buộc nghiệp vụ khi người dùng muốn chốt yêu cầu hoặc còn quyết định nghiệp vụ có thể đổi giải pháp. Không kích hoạt cho brainstorm mở rộng ý tưởng hay task code đã rõ.
---

# Business Discovery

## Mục tiêu

Chốt vấn đề và các quyết định nghiệp vụ cần thiết để người dùng hoặc coding agent
có thể chọn hướng tiếp theo. Đây là skill discovery riêng, không phải cổng bắt buộc
trước mọi lần implement.

## Khong can project context

Skill này có thể chạy từ mô tả của người dùng, nhưng chỉ kích hoạt khi cần discovery.

## Cách làm

### 1. Chốt vấn đề

Viết lại vấn đề bằng 1–2 câu. Hỏi tối đa 3 câu, chỉ hỏi điều có thể đổi phạm vi,
hành vi người dùng hoặc tiêu chí chấp nhận.

### 2. Phạm vi

- In-scope
- Out-of-scope

### 3. Rủi ro và ràng buộc

Liệt kê các rủi ro, ràng buộc và edge case nghiệp vụ đáng kể.

### 4. Câu hỏi và giả định

Chỉ ghi câu hỏi còn mở và giả định đang dùng. Không ép user phải qua bước lập kế hoạch riêng (`adk-solution-planning`) nếu
họ đã yêu cầu làm luôn và không còn quyết định cần họ chốt.

### 5. Ảnh hưởng kỹ thuật nếu đã biết

Chỉ đánh dấu trạng thái API/data contract nếu thông tin đã có:

- `Yes`
- `No`
- `Unknown`

## Đầu ra

Trình bày gọn trong hội thoại. Chỉ tạo clarify record bằng template
`templates/clarify-record.md.template` khi người dùng yêu cầu artifact hoặc task
cần lưu lại quyết định.

## Guardrails

- Không tạo plan kỹ thuật chi tiết.
- Không mở rộng thành analysis dài.
- Không kích hoạt chỉ vì task code còn vài chi tiết có thể giả định an toàn.
- Brainstorm ý tưởng thuộc `adk-brainstorm`; PRD/Epic/Stories thuộc `adk-agile-ba`.
