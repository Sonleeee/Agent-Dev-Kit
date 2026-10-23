---
name: sk-systematic-debugging
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
5. Sửa nguyên nhân trong scope, thêm regression test khi phù hợp, rồi chạy reproduction
   hoặc kiểm chứng sát nhất.

## Đầu ra

Nêu nguyên nhân bằng một câu, sửa đổi chính, kiểm chứng đã chạy và rủi ro còn lại.
Không tạo report dài cho lỗi nhỏ đã được tái hiện rõ.

## Ranh giới

- Không kích hoạt cho mọi yêu cầu có chữ “bug” nếu nguyên nhân và cách sửa đã rõ.
- Không patch symptom khi chưa hiểu behavior liên quan.
- Không delegate theo số file/layer cố định.
