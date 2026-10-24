---
name: adk-solution-planning
description: Lập plan triển khai ngắn khi người dùng yêu cầu chỉ lập kế hoạch, task có nhiều nhánh phụ thuộc hoặc approach chưa hiển nhiên. Không kích hoạt như bước bắt buộc trước task code đã rõ.
---

# Solution Planning

## Mục tiêu

Tạo plan vừa đủ để triển khai task có nhiều bước hoặc quyết định đáng kể, không
biến plan thành cổng approval cho mọi thay đổi.

## Nạp context

Chỉ đọc phần context liên quan. Nếu project có:

- `AGENTS.md`
- `.agents/context/architecture.md`
- `.agents/context/templates/*`

thì dùng chúng khi task chạm đến:

- impacted layers
- pattern constraints
- template selection

## Quy trinh

### 1. Chốt approach

Chon 1 huong lam ngan gon.

### 2. Phạm vi bị ảnh hưởng

Chỉ liệt kê module/file thật sự quan trọng; không cần dự đoán mọi file chính xác
khi implementation có thể khám phá thêm.

### 3. Pattern và template

Nếu project có template/pattern áp dụng:

- ghi rõ tham chiếu nào cần dùng khi implement.

### 4. Kiểm chứng

Chọn lệnh kiểm chứng phù hợp với behavior và phạm vi thay đổi.

### 5. Tiêu chí hoàn thành

Nêu ngắn gọn kết quả mong đợi và các rủi ro cần đóng:

- implementation đáp ứng yêu cầu
- kiểm chứng phù hợp có kết quả rõ
- API/data risk được nêu khi có liên quan

## Đầu ra

Trình bày plan ngắn trong hội thoại. Dùng `templates/implementation-plan-lite.md.template`
chỉ khi người dùng cần artifact plan riêng hoặc task cần lưu quyết định.

## Guardrails

- Không ôm scope quá lớn trong một plan.
- Không yêu cầu user duyệt plan thông thường nếu họ đã giao task implement.
- Nếu task lớn, tách các phần phụ thuộc/độc lập có ích; không chia nhỏ chỉ để delegate.
