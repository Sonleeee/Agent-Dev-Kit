---
name: sk-execution-contract
description: Tạo contract và progress ledger cho task nhiều bước, dài qua nhiều lượt, cần resume hoặc có rủi ro cao. Không dùng cho task ngắn, rõ và dễ kiểm chứng.
---

# Execution Contract — Dùng khi task cần trạng thái bền vững

## Khi nào dùng

Kích hoạt khi task nhiều bước, có thể kéo dài qua nhiều lượt, cần resume sau
context compaction, có rủi ro cao hoặc có nhiều người/agent cùng làm. Không kích
hoạt chỉ vì có sửa code, debug hay review.

## Bootstrap bắt buộc

Khi đã xác định cần contract:

1. Đọc hướng dẫn repo và context liên quan; không quét context ngoài phạm vi.
2. Tạo `.agents/runtime/<task-id>/execution-contract.md` từ template nếu runtime
   artifact phù hợp với task.
3. Ghi objective, scope, tiêu chí hoàn thành, risk và cách kiểm chứng vừa đủ.

Với task vừa phải, contract có thể chỉ là ghi chú ngắn trong hội thoại. Không tạo
file/ledger chỉ để thỏa mãn thủ tục. Nếu host không cho phép ghi runtime artifact,
không giả vờ rằng ledger đã tồn tại.

## Trong khi thực thi

- Giữ scope và cập nhật trạng thái khi có thay đổi đáng kể hoặc cần resume.
- Không ghi stage giả như `clarify`, `plan`, `impl`, `review` nếu chúng không thực sự diễn ra.
- Khi context bị nén hoặc phiên tiếp tục, đọc contract/ledger trước; tiếp tục từ
  bước cuối có evidence thay vì lặp lại việc đã hoàn tất.
- Nếu có delegate, truyền context tối thiểu và dùng `sk-compressed-delegation` khi
  nó giúp giảm handoff noise; không bắt buộc hai vòng review cho mọi subtask.

## Minimality checkpoint

Trước khi thêm code/abstraction/dependency, agent phải trả lời ngắn:

1. Có cần tồn tại không?
2. Đã có helper/pattern trong repo chưa?
3. Standard library hoặc native platform có đủ không?
4. Cách ít file và ít state nhất là gì?

Không được giản lược away validation ở trust boundary, security, accessibility,
error handling chống mất dữ liệu, hoặc điều user yêu cầu rõ ràng.

## Kết thúc

Khi task có contract, kết thúc bằng:

- kết quả và changed files;
- lệnh kiểm chứng đã chạy và kết quả, hoặc lý do chưa chạy;
- blocker/rủi ro hoặc việc ngoài scope nếu có;
- trạng thái đủ rõ để tiếp tục ở lượt sau.

Không tuyên bố đã chạy kiểm chứng nếu chưa có bằng chứng.

## Trace Capture (evolution system)

Khi trace capture được bật và đang thực hiện task cần contract, có thể bổ sung trace
best-effort; không ghi một step cho mỗi hành động nhỏ:

| Thời điểm | Action | Command |
|-----------|--------|---------|
| Bắt đầu task | Tạo session + trace | `evolution_db.py log_session` |
| Bước lớn có ý nghĩa | Ghi step + outcome | `evolution_db.py log_step` |
| Mỗi friction (retry, error, user correction) | Ghi friction point | `evolution_db.py log_friction` |
| Dùng skill | Ghi skill usage | `evolution_db.py log_skill_use` |
| Kết thúc task | Cập nhật outcome | `evolution_db.py update_outcome` |

**Nguyên tắc:** Trace capture là **best-effort, non-blocking**. Chỉ ghi workflow/skill
nếu được ghi nhận là đã dùng; không suy ra từ loại commit hay file thay đổi. Nếu DB unavailable
hoặc lệnh ghi fail, tiếp tục task bình thường — không bao giờ để trace capture
block delivery flow.

Nạp `sk-trace-capture` theo intent nếu cần xem procedure ghi trace.
