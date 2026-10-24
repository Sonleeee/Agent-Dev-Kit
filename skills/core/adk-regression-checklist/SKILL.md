---
name: adk-regression-checklist
description: Lập checklist regression cho thay đổi có blast radius đáng kể hoặc khi người dùng yêu cầu QA checklist. Không kích hoạt sau mọi task nhỏ.
---

# Regression Checklist

## Mục tiêu
Xác định những luồng cũ có khả năng bị ảnh hưởng và kiểm tra chúng theo rủi ro.
Không chạy toàn bộ checklist nếu task chỉ chạm một hành vi cô lập.

## Quy trình

### Bước 1 — Happy Path
Xác nhận luồng chính của tính năng vừa thay đổi hoạt động đúng:
- Input hợp lệ → output đúng
- Luồng từ đầu đến cuối không bị gián đoạn

### Bước 2 — Edge cases liên quan
Kiểm tra edge cases liên quan đến yêu cầu và code path:
- Empty / null inputs
- Boundary values
- Concurrent actions
- Permission boundaries

### Bước 3 — Luồng Lân Cận
Kiểm tra các luồng KHÔNG thay đổi nhưng có thể bị ảnh hưởng:
- Các feature dùng chung component/service vừa sửa
- Luồng đọc/ghi dữ liệu liên quan
- Các màn hình sử dụng cùng API endpoint

### Bước 4 — API Contract (nếu có thay đổi)
- Consumer phía FE vẫn hoạt động đúng với response mới
- Không có field mới nào bị FE hiểu sai

### Bước 5 — Ghi Residual Risks
Những gì chưa verify được trong task này:
- Lý do chưa verify
- Risk level: Low / Medium / High
- Plan follow-up nếu cần

## Output
Dùng template `templates/regression-report.md.template`.

## Guardrails
- Không skip regression check dù task nhỏ — luồng lân cận hay bị quên
- Ghi rõ "đã check" hoặc "chưa check + lý do", không để trống
- Residual risk Medium/High phải có plan xử lý trước ship
