---
name: adk-systematic-debugging
description: Điều tra lỗi khi symptom chưa đủ rõ để chọn cách sửa, lỗi đi qua nhiều layer, hoặc người dùng yêu cầu tìm root cause. Bug đã rõ có thể được sửa trực tiếp mà không cần skill này.
---

# Systematic debugging

## Quy trình

1. Thu thập symptom, lỗi, reproduction và thay đổi gần nhất có liên quan.
2. Tái hiện lỗi hoặc xác định đường code có evidence liên quan; không quét rộng repo
   nếu đã khoanh vùng được.
3. Đưa ra giả thuyết dựa trên evidence, loại trừ từng khả năng bằng kiểm tra nhỏ nhất.
   Không cần tạo số lượng giả thuyết tối thiểu.
4. Xác định layer/nguyên nhân gốc trước khi sửa. Nếu evidence chưa đủ, nêu điều còn
   thiếu hoặc hỏi đúng câu có thể thay đổi diagnosis.
5. **Khóa vùng sửa (`freeze_scope` — Directory Freeze Boundary):** Ngay sau khi khoanh vùng
   được thư mục/module chứa nguyên nhân gốc, tự khóa phạm vi chỉnh sửa vào đúng thư mục đó;
   tuyệt đối không sửa lan sang các thư mục lân cận khi đang thử nghiệm bản vá, kết hợp
   thêm regression test và chạy kiểm chứng sát nhất.
6. **Quy tắc 3-Strike Architecture Stop (Ngắt mạch sau 3 lần thử sai):** Nếu đã thử sửa
   tới lần thứ 3 liên tiếp cho cùng một lỗi mà lệnh kiểm chứng vẫn thất bại, **bắt buộc
   DỪNG sửa code ngay lập tức**. Hoàn tác các thay đổi thử nghiệm bị hỏng, báo cáo rõ 3
   giả thuyết đã thử và thảo luận lại với người dùng vì đây thường là lệch giả định kiến
   trúc chứ không phải lỗi cú pháp đơn lẻ.

## Đầu ra

Nêu nguyên nhân bằng một câu, sửa đổi chính, kiểm chứng đã chạy và rủi ro còn lại.
Không tạo report dài cho lỗi nhỏ đã được tái hiện rõ.

## Ranh giới

- Không kích hoạt cho mọi yêu cầu có chữ “bug” nếu nguyên nhân và cách sửa đã rõ.
- Không patch symptom khi chưa hiểu behavior liên quan.
- Không delegate theo số file/layer cố định.
