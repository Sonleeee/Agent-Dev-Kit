---
name: adk-system-design-scaffold
description: Tạo source base mới bằng system-design MCP khi người dùng yêu cầu scaffold hoặc generate project một cách tường minh. Dùng cho việc chọn blueprint và khởi tạo thư mục dự án mới; không dùng cho câu hỏi kiến trúc/pattern thông thường hoặc để tự sửa một project đang tồn tại.
---

# System Design Scaffold

Dùng skill này chỉ khi người dùng yêu cầu tạo source base mới. Tư vấn kiến trúc và tra cứu pattern thuộc `adk-system-architect` ở core.

## Chốt đầu vào

- Xác định tên project, đường dẫn đích và stack/blueprint. Nếu chưa rõ stack, dùng `list_architectures` để xem các blueprint hiện có rồi hỏi người dùng chọn; không tự chọn microservices hay blueprint phức tạp.
- Dùng `recommend_architecture` nếu người dùng cần gợi ý. Xem đó là gợi ý dựa trên input, không phải cam kết về tải hay chi phí.
- Không gọi `evaluate_interview` trong luồng thường: tool này ghi `.agents/.cache/scaffold-session.json` vào `project_dir` và lưu nội dung ADR để lần scaffold sau dùng. Chỉ gọi khi người dùng yêu cầu rõ quy trình interview/chấm điểm và đã biết side effect đó.

## Kiểm tra trước khi ghi

`scaffold_project` ghi đè các file blueprint bằng `writeFileSync` mà không kiểm tra file đích đã tồn tại hay chưa.

- Xác định đúng đường dẫn đích và kiểm tra nó không tồn tại hoặc là thư mục rỗng.
- Nếu thư mục có nội dung, không gọi tool. Đề xuất thư mục mới rỗng hoặc chuyển sang chỉnh sửa thủ công có phạm vi rõ; không ghi đè chỉ vì người dùng muốn scaffold.
- Nếu không thể kiểm tra đường dẫn đích, hỏi người dùng trước khi tiếp tục.
- Không dùng đường dẫn hiện tại làm mặc định ngầm. Truyền đủ `architecture_id`, `target_dir` và `project_name`.

## Tạo và bàn giao

Sau khi người dùng đã yêu cầu tạo project, blueprint và thư mục đích đã rõ, gọi `scaffold_project` một lần. Không gọi `inject_pattern` như một phần mặc định của scaffold; việc nhúng code vào project hiện có cần yêu cầu riêng và kiểm tra xung đột riêng.

Sau khi tool trả kết quả:

- Báo đường dẫn đích và danh sách file tool cho biết đã tạo.
- Kiểm tra một vài file đại diện nếu thư mục làm việc cho phép; không tuyên bố toàn bộ source base đã build hoặc chạy được nếu chưa kiểm chứng.
- Không tự cài dependency, chạy server, hoặc tiếp tục sang workflow khác nếu người dùng chưa yêu cầu.
