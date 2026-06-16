---
trigger: glob
---

# Global Rules

Tất cả rules trong file này áp dụng cho mọi project và mọi platform. Những quy tắc này là "tòa tối cao" của hệ thống.

Mỗi rule được đánh dấu:
- `[PROTECTED]` — không thể override.
- `[OVERRIDABLE]` — project có thể override qua `rule-overrides.approved.md`.

---

## Nhóm 1 — Delivery Gates [PROTECTED]

### Gate 1 — Ready [PROTECTED]
Không được bắt đầu implement khi thiếu: Problem statement, Scope, Implementation plan, Pre-Impl Quality Card.

### Gate 2 — Dev Done [PROTECTED]
Không được chuyển sang verify khi chưa self-check theo quality card.

### Gate 3 — Ship Ready [PROTECTED]
Không được ship khi còn finding Critical.

---

## Nhóm 2 — Bugfix Discipline [PROTECTED]

### Root Cause First [PROTECTED]
Xác định root cause theo format: "Input X → Output Y hiện tại → Output Z mong muốn → Layer gây lỗi" trước khi sửa.

### Anti-Regression Case [PROTECTED]
Bugfix phải có ít nhất 1 anti-regression case để đảm bảo lỗi không tái phát.

---

## Nhóm 3 — General Principles [PROTECTED]

### Minimal Change Principle [PROTECTED]
Thay đổi tối thiểu đúng phạm vi yêu cầu — không mở rộng scope tự phát.

### Respect Project Context [PROTECTED]
Luôn ưu tiên tuân thủ kiến trúc và convention hiện có của project trong `.agents/context/`.

---

## Nhóm 4 — Codebase Exploration [PROTECTED]

### Graph-First Principle [PROTECTED]
Khi làm việc trên codebase, TUYỆT ĐỐI không sử dụng các công cụ quét thô (`grep`, `grep_search`, `list_dir`, `find`, `read_file`...) một cách mù quáng để khám phá cấu trúc hoặc tìm kiếm file.
Hãy tuân thủ quy trình **Graph-First**:
1. Sử dụng các công cụ của **CodeGraph MCP Server** (như `codegraph.search_symbols`, `codegraph.get_definition`, `codegraph.get_callers`, `codegraph.get_callees`) để định vị chính xác vị trí của class, function, api route, hoặc luồng gọi.
2. Chỉ sử dụng công cụ đọc file (`view_file` hoặc `read_file`) khi đã biết chính xác đường dẫn file và dòng code cần đọc/sửa từ kết quả của CodeGraph.
3. Việc lạm dụng quét thô (`grep_search`) trên toàn bộ codebase lớn mà không gọi CodeGraph trước sẽ bị coi là vi phạm chất lượng nghiêm trọng.

---

## Cách AI đọc rules
1. **Global Rules**: Luôn load đầu tiên.
2. **Modular Rules**: Tự động load thêm `frontend.md` hoặc `backend.md` dựa vào path của file đang làm việc.
3. **Project Context**: Load từ `.agents/context/` để override (nếu là `[OVERRIDABLE]`).
