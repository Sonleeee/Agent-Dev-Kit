---
name: adk-code-review
description: Review code changes when the user requests an independent review or the change has substantial security, data, API, architecture, or cross-agent risk. Report findings; do not edit code unless asked.
---

# Code review

## Phạm vi

Review là nhiệm vụ độc lập: tìm lỗi và trình bày evidence. Không phụ thuộc quy trình implement trước đó,
execution contract hay build pass trước đó. Không kích hoạt chỉ vì vừa sửa code; phần
rà diff ngắn cuối task thuộc đường implement mặc định.

## Cách review

1. Xác định phạm vi review từ yêu cầu, diff và quy ước liên quan của repo.
2. Đọc code path bị ảnh hưởng và callers/consumers cần thiết để kiểm tra tác động.
3. Tìm lỗi correctness, security, data loss, API compatibility, regression và thiếu
   xử lý lỗi có thể tái hiện. Chọn độ sâu theo blast radius, không theo số dòng/file.
4. Chạy kiểm tra chỉ đọc hoặc lệnh phù hợp khi cần evidence; không sửa finding trừ khi
   người dùng yêu cầu review kèm fix.
5. Kết thúc bằng các finding có thể hành động; nếu không có, nêu phạm vi đã xem và
   những giới hạn kiểm chứng còn lại.

## Định dạng finding

Mỗi finding gồm:

- Mức độ: Critical, High, Medium hoặc Low.
- Vị trí cụ thể (file và dòng khi xác định được).
- Điều kiện kích hoạt và tác động thực tế.
- Lý do đây là lỗi, có liên hệ tới yêu cầu hoặc behavior nào.

Đưa finding nghiêm trọng nhất lên trước. Không liệt kê giả định chung, style preference
hoặc lint nits nếu chúng không gây lỗi/chi phí đáng kể.

## Ranh giới

- Không biến review thành implementation.
- Không yêu cầu đủ bốn layer, nhiều reviewer hay red-team cho mọi change.
- Chỉ dùng `adk-owasp-scan`, `adk-secret-detection` hoặc `adk-api-contract-guard` khi
  nội dung thay đổi thực sự chạm tới phạm vi đó.
- Không tuyên bố review toàn diện nếu chỉ xem một phần diff.
