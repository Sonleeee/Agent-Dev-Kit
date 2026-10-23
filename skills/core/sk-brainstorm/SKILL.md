---
name: sk-brainstorm
description: >-
  Dùng khi người dùng chủ động muốn brainstorm, mở rộng ý tưởng, hoặc so sánh
  nhiều hướng giải quyết trước khi quyết định. Khám phá và trình bày các lựa chọn
  khác biệt trong hội thoại; không tự chuyển thành làm rõ yêu cầu để code,
  implementation plan hay triển khai. Không kích hoạt chỉ vì task còn mơ hồ
  hoặc người dùng yêu cầu thực hiện một thay đổi đã rõ.
---

# Brainstorm ý tưởng

## Mục tiêu

Giúp người dùng nhìn thấy những hướng có thể đi, hiểu chúng khác nhau ở đâu,
rồi tự chọn điều muốn đào sâu. Brainstorm tạo **ứng viên để cân nhắc**, không
chốt quyết định thay người dùng và không phải bước bắt buộc trước khi code.

## Khi nào dùng

- Người dùng gọi brainstorm hoặc yêu cầu cùng nghĩ ý tưởng.
- Người dùng muốn có nhiều cách tiếp cận, hướng sản phẩm, cải tiến quy trình,
  giải pháp kỹ thuật hoặc phương án thiết kế để cân nhắc.
- Người dùng chưa muốn chốt một giải pháp và muốn mở rộng không gian lựa chọn.

Không kích hoạt chỉ vì yêu cầu thiếu chi tiết. Nếu người dùng đã chọn hướng và
yêu cầu thực hiện, hãy làm theo yêu cầu đó mà không chen thêm phiên brainstorm.

## Cách làm

### 1. Đóng khung vừa đủ

- Dùng yêu cầu, câu trả lời trước đó và ngữ cảnh sẵn có để hiểu mục tiêu,
  đối tượng, giới hạn và điều người dùng muốn tránh.
- Nếu đang làm trong một dự án, chỉ xem phần tài liệu hoặc mã nguồn có thể
  làm thay đổi các ý tưởng được đề xuất. Không quét rộng repo theo mặc định.
- Nêu giả định quan trọng như giả định; không trình bày chúng như điều người
  dùng đã xác nhận.
- Chỉ hỏi khi một thông tin thiếu có thể làm thay đổi đáng kể các hướng đề xuất.
  Nếu có thể tiếp tục an toàn, nói rõ giả định và đưa ra vòng ý tưởng đầu tiên.

### 2. Mở rộng lựa chọn

- Tạo riêng các hướng khác nhau về cơ chế, phạm vi hoặc cách tiếp cận; không
  đổi tên cùng một ý tưởng để tạo cảm giác có nhiều lựa chọn.
- Thường trình bày 2–4 hướng gọn. Điều chỉnh số lượng theo yêu cầu của người dùng.
- Cân nhắc cả hướng đơn giản hơn, làm từng phần hoặc chưa thay đổi gì khi chúng
  là lựa chọn thực tế.
- Không vội chọn một hướng. Chỉ nêu đề xuất tạm thời khi người dùng hỏi,
  hoặc đã có tiêu chí rõ để so sánh.

### 3. Làm rõ khác biệt

Với mỗi hướng, giải thích ngắn:

- Ý tưởng cốt lõi và vấn đề nó nhắm tới.
- Lợi ích chính.
- Đánh đổi, rủi ro hoặc giả định cần đúng để hướng đó có hiệu quả.

Chỉ thêm bảng, sơ đồ, ví dụ giao diện hoặc nghiên cứu nguồn bên ngoài khi chúng
giúp người dùng phân biệt lựa chọn tốt hơn. Không gọi ý tưởng là đã được kiểm
chứng nếu chưa có bằng chứng.

### 4. Tiếp tục theo phản hồi

- Để người dùng chọn, sửa, kết hợp hoặc bác bỏ các hướng.
- Nếu họ muốn tiếp tục khám phá, phát triển vòng ý tưởng tiếp theo dựa trên
  phản hồi; không lặp lại phần đã thống nhất.
- Hỏi từng câu ngắn khi cần câu trả lời của người dùng. Không dùng bảng hỏi
  cố định hoặc hỏi đủ một bộ câu hỏi theo nghi thức.

## Đầu ra mặc định

Giữ gọn trong hội thoại:

1. Cách hiểu hiện tại về mục tiêu, kèm giả định nếu có.
2. Các hướng đề xuất và điểm khác nhau đáng cân nhắc.
3. Câu hỏi hoặc lựa chọn còn mở, nếu thực sự có.

Không bắt buộc tạo file hay template. Chỉ ghi thành design brief, PRD, decision
record hoặc tài liệu khác khi người dùng yêu cầu.

## Ranh giới

- Không biến brainstorm thành clarify record: không ép chốt in/out of scope,
  API status hay đủ điều kiện sẵn sàng code.
- Không biến brainstorm thành BA: không tự chạy 5 Whys, RICE, INVEST, Gherkin,
  PRD hoặc sơ đồ nghiệp vụ.
- Không biến brainstorm thành solution plan: không tự chọn approach cuối,
  liệt kê file cần sửa, chia task, đặt test obligations hoặc done criteria.
- Không biến brainstorm thành research có dẫn chứng: nếu người dùng muốn biết
  hướng nào phù hợp theo tài liệu, codebase hoặc prior art, chuyển sang skill
  research phù hợp sau khi xác nhận câu hỏi cần kiểm chứng.
- Không sửa code, tạo spike hay gọi luồng delivery chỉ vì người dùng thích một
  ý tưởng. Chỉ chuyển sang planning hoặc implementation khi người dùng yêu cầu.

## Handoff khi người dùng muốn đi tiếp

- Muốn xác minh hướng theo pattern, thư viện hoặc prior art: `sk-pattern-researcher`
  hoặc `sk-docs-seeker`.
- Muốn chốt vấn đề và yêu cầu nghiệp vụ: `sk-business-discovery`.
- Muốn PRD, Epic hoặc User Stories: `sk-agile-ba`.
- Muốn chốt approach và chuẩn bị triển khai: `sk-solution-planning`.
- Muốn sửa code: chuyển sang skill/workflow triển khai phù hợp với yêu cầu.

Chỉ handoff khi người dùng chọn hoặc yêu cầu bước tiếp theo; không tự chạy chuỗi
handoff cho mọi phiên brainstorm.
