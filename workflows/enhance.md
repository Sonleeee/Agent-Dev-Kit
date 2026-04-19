---
id: enhance
type: utility
entry-command: /enhance
description: Enhancement/refactor có chủ đích
---

# /enhance

**Mục tiêu:** Cải thiện code hiện tại — refactor, optimize, hoặc nâng cấp pattern.

## Khi nào dùng

- Refactor code để bám pattern mới
- Optimize performance
- Upgrade dependency/pattern
- Tech debt cleanup có chủ đích

## Quy trình

1. **Xác định mục tiêu** — cải thiện gì, tại sao
2. **Đánh giá impact** — files nào ảnh hưởng, risk gì
3. **Plan changes** — approach, template nếu có
4. **Implement** — theo `/impl` flow
5. **Verify** — build pass, không regression

## Guardrails

- Enhancement phải có mục tiêu rõ ràng (không "refactor vì thích")
- Không mở rộng scope ngoài mục tiêu ban đầu
- Phải build pass sau khi enhance
- Nếu thay đổi API contract → phải đánh dấu Risk
