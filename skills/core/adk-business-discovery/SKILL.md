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

### 1. Chốt vấn đề & Premise Challenge (Thách thức tiền đề)

Viết lại vấn đề bằng 1–2 câu. Trước khi bàn giải pháp, kiểm tra nhanh xem yêu cầu đang mô tả **nỗi đau gốc (pain)** hay chỉ là một **tính năng bề mặt**. Khi bài toán sản phẩm/nghiệp vụ còn rộng hoặc mơ hồ, chọn lọc từ **6 Câu hỏi Ép Thực Tế (6 YC Forcing Questions)** để hỏi tối đa 3 câu đắt giá nhất (chỉ hỏi điều có thể đổi phạm vi, hành vi người dùng hoặc tiêu chí chấp nhận):
1. **Demand Reality:** Ai đang thực sự cần điều này ngay bây giờ và bằng chứng là gì?
2. **Status Quo:** Hiện tại người dùng đang làm thủ công hoặc dùng workaround gì để giải quyết?
3. **Desperate Specificity:** Kịch bản cụ thể nhất mà giải pháp hiện tại làm họ thất vọng là gì?
4. **Narrowest Wedge:** Nhát cắt nhỏ nhất (MVP) có thể bàn giao ngay để tạo giá trị thực là gì?
5. **Observation & Surprise:** Có hành vi thực tế nào của người dùng khác với giả định ban đầu không?
6. **Future-Fit:** Quyết định này mở đường hay khóa chặt hướng phát triển tiếp theo của hệ thống?

### 2. Phạm vi & 4 Chế độ Co Giãn (4 Cognitive Scope Modes)

Xác định rõ:
- **In-scope** & **Out-of-scope**
- Khi cần chốt tư thế triển khai với người dùng, đề xuất 1 trong **4 Chế độ Phạm vi**:
  - `Scope Expansion` (Mở rộng tìm giải pháp 10-sao toàn diện).
  - `Selective Expansion` (Giữ lõi, chỉ thêm 1–2 điểm nhấn giá trị cao).
  - `Hold Scope` (Khóa chặt phạm vi hiện tại, tập trung độ bền và chất lượng tối đa).
  - `Scope Reduction` (Cắt gọt tối đa về đúng *Narrowest Wedge / MVP*).

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
