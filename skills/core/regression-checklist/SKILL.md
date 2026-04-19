---
name: regression-checklist
description: |
  Checklist regression trước khi bàn giao. Dùng sau implement để xác nhận
  luồng chính, edge cases và các luồng liên quan không bị phá vỡ.
  Hoạt động với mọi project — không cần context cụ thể.
context-required: false
output: regression-report
---

# Regression Checklist

## Mục tiêu
Xác nhận thay đổi mới không làm hỏng luồng cũ quan trọng.

## Quy trình

### Bước 1 — Happy Path
Xác nhận luồng chính của tính năng vừa thay đổi hoạt động đúng:
- Input hợp lệ → output đúng
- Luồng từ đầu đến cuối không bị gián đoạn

### Bước 2 — Edge Cases Liên Quan Task
Kiểm tra các edge case được chốt trong quality card:
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
