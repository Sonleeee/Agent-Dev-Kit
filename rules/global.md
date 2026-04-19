---
trigger: glob
---

# Global Rules

Tất cả rules trong file này áp dụng cho mọi project và mọi platform.

Mỗi rule được đánh dấu:
- `[PROTECTED]` — không thể override, kể cả khi có trong `rule-overrides.approved.md`
- `[OVERRIDABLE]` — project có thể override qua `rule-overrides.approved.md`

Khi AI gặp rule `[PROTECTED]` trong file override của project:
→ Bỏ qua override đó, giải thích lý do với user, tiếp tục enforce.

---

## Nhóm 1 — Delivery Gates [PROTECTED]

### Gate 1 — Ready [PROTECTED]
Không được bắt đầu implement khi thiếu bất kỳ điều kiện nào sau:
- Problem statement rõ ràng (1–2 câu, không mơ hồ)
- Scope in/out được xác định
- Implementation plan có thứ tự task
- Pre-Implementation Quality Card tồn tại

Lý do PROTECTED: code không có context dẫn đến rework tốn kém gấp 5–10x so với làm đúng ngay từ đầu.

### Gate 2 — Dev Done [PROTECTED]
Không được chuyển sang verify khi:
- Chưa self-check theo quality card
- API contract status chưa được đánh dấu (OK / Risk)

Lý do PROTECTED: bỏ qua self-check → bug phát hiện muộn → cost cao hơn.

### Gate 3 — Ship Ready [PROTECTED minimum]
Không được ship khi còn finding Critical.

Lý do PROTECTED: Critical = rủi ro production, không có exception.

**[OVERRIDABLE]** — Threshold cho Major finding:
Default: Major phải được resolve trước khi ship.
Override: project có thể cho phép ship với Major nếu có risk acceptance rõ ràng.

---

## Nhóm 2 — Bugfix Discipline [PROTECTED]

### Root Cause First [PROTECTED]
Bugfix phải xác định root cause trước khi sửa code.
Format bắt buộc: "Input X → Output Y hiện tại → Output Z mong muốn → Layer gây lỗi: [layer]"

Lý do PROTECTED: fix symptom tạo tech debt và tái phát bug.

### Anti-Regression Case [OVERRIDABLE]
Default: bugfix phải có ít nhất 1 anti-regression case.
Override: emergency hotfix có thể skip nếu khai báo rõ trong override + ghi ticket follow-up.

---

## Nhóm 3 — API Contract [PROTECTED]

### Contract Status Bắt Buộc [PROTECTED]
Trước khi đóng bất kỳ task nào liên quan đến API, phải đánh dấu:
- `API contract: OK` — không thay đổi contract
- `API contract: Risk` — có thay đổi, đã kiểm tra + documented

Lý do PROTECTED: không đánh dấu → FE/BE drift không kiểm soát được.

### Breaking Change [PROTECTED]
Không được thay đổi API contract (route, status code, response shape, request schema) ngoài phạm vi yêu cầu của task.

---

## Nhóm 4 — Security [PROTECTED]

### No Secrets in Code [PROTECTED]
Không commit API keys, passwords, tokens, credentials vào source code.

### No Destructive Commands Without Confirm [PROTECTED]
Không sinh code thực thi lệnh phá hủy (DROP TABLE, rm -rf, delete all records) mà không có confirmation step.

---

## Nhóm 5 — Architecture [OVERRIDABLE]

### Architecture Pattern [OVERRIDABLE]
Default: phân tầng rõ ràng — không để business logic ở layer sai.
Override: project khai báo pattern cụ thể trong `.agents/context/architecture.md`

### Exception / Error Taxonomy [OVERRIDABLE]
Default: phân loại lỗi theo input/not-found/business, map đúng HTTP status.
Override: project khai báo taxonomy riêng trong `.agents/context/architecture.md`

### Naming Convention [OVERRIDABLE]
Default: theo convention phổ biến của tech stack (camelCase JS, PascalCase C#...).
Override: project khai báo trong `.agents/context/architecture.md`

---

## Nhóm 6 — Code Quality [OVERRIDABLE]

### i18n Requirement [OVERRIDABLE]
Default: không hardcode text trong UI — dùng i18n keys.
Override: project có thể tắt nếu là internal tool hoặc MVP.

### No Debug Logs in Production Code [PROTECTED]
Không để lại console.log / Debug.Print / print statements dư thừa trong code ship.

### Minimal Change Principle [OVERRIDABLE]
Default: thay đổi tối thiểu đúng phạm vi yêu cầu — không mở rộng scope tự phát.
Override: project có thể cho phép refactor kèm theo nếu khai báo rõ.

---

## Nhóm 7 — Checklist [OVERRIDABLE]

### Master Checklist [OVERRIDABLE]
Default: dùng `quality/master-checklist.md` (38 items).
Override: project có thể dùng subset hoặc extend trong `.agents/context/checklist.md`

---

## Cách AI đọc file này

1. Load toàn bộ rules từ file này khi bắt đầu task
2. Load `rule-overrides.approved.md` từ project (nếu có)
3. Với mỗi override trong file đó:
   - Nếu rule là `[PROTECTED]` → ignore override, log cảnh báo
   - Nếu rule là `[OVERRIDABLE]` → apply override, log để user biết
4. Execute với merged rule set
