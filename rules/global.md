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

### Execution Evidence [PROTECTED]
Không được báo `READY`/"đã hoàn tất" nếu chưa có execution contract hoặc output
tương đương chứa objective, acceptance criteria, changed files, verification command
và review result. Nếu không thể chạy verify, status phải là `BLOCKED` hoặc
`NEEDS_USER_DECISION`, kèm lý do cụ thể.

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

### Minimality Checkpoint [PROTECTED]
Trước abstraction hoặc dependency mới, phải kiểm tra nhu cầu thực, khả năng tái sử
dụng helper hiện có, standard library/native feature và phương án ít file/state nhất.
Không giản lược validation, security, accessibility, error handling chống mất dữ liệu
hoặc yêu cầu rõ của user.

### Task Ledger [PROTECTED]
Task nhiều bước phải có progress ledger. Mỗi task bounded chỉ được đánh dấu complete
sau verify; khi resume sau context compaction, đọc ledger và không chạy lại task đã
complete.

### Respect Project Context [PROTECTED]
Luôn ưu tiên tuân thủ kiến trúc và convention hiện có của project trong `.agents/context/`.

### Context Manifest [PROTECTED]
Nếu project có `.agents/context/manifest.md`, agent phải đọc manifest trước khi nạp
TIER-1/TIER-2. Manifest là bản đồ load context; code/test đang chạy vẫn là ground truth.

---

## Nhóm 4 — Codebase Exploration [PROTECTED]

### Graph-First Principle [PROTECTED]
Khi làm việc trên source code, TUYỆT ĐỐI không sử dụng các công cụ quét thô (`grep`, `grep_search`, `list_dir`, `find`, `read_file`, `Get-Content`, `ls`...) một cách mù quáng để khám phá cấu trúc hoặc tìm kiếm file.

Hãy tuân thủ quy trình **Graph-First**:

1. Gọi **CodeGraph MCP Server trước** để định vị class, function, method, component, api route, hoặc luồng gọi liên quan.
2. Dùng đúng tool theo mục đích:
   - `mcp__codegraph.codegraph_explore`: lựa chọn mặc định cho câu hỏi "X hoạt động thế nào?", "flow này đi qua đâu?", hoặc trước khi sửa nhiều symbol liên quan.
   - `mcp__codegraph.codegraph_node`: đọc một file đã biết hoặc một symbol cụ thể, ưu tiên hơn đọc file truyền thống.
   - `mcp__codegraph.codegraph_callers`: phân tích impact/caller trước khi đổi behavior, signature, hoặc contract.
   - `mcp__codegraph.codegraph_search`: tìm nhanh vị trí symbol khi chưa đủ thông tin để explore.
3. Nếu CodeGraph đã trả về source của file/symbol, coi đó như nội dung đã đọc từ disk; không đọc lại bằng `read_file`, `Get-Content`, hoặc tool tương đương trừ khi có lý do cụ thể.
4. Chỉ fallback sang công cụ truyền thống khi:
   - File không phải source code/symbol tốt, ví dụ `.md`, `.json`, `.yml`, `.env.example`, migration raw SQL, asset, generated file.
   - Cần tìm literal text, i18n key, config key, hoặc nội dung không có symbol rõ ràng.
   - Cần kiểm tra git status/diff/log hoặc thao tác filesystem.
   - CodeGraph không index được khu vực cần xem hoặc trả thiếu thông tin.
5. Việc lạm dụng quét thô trên toàn bộ codebase lớn mà không gọi CodeGraph trước sẽ bị coi là vi phạm chất lượng nghiêm trọng.

Decision table nhanh:

| Nhu cầu | Tool ưu tiên |
|---|---|
| Hiểu feature/flow/khu vực code | `mcp__codegraph.codegraph_explore` |
| Tìm class/function/component | `mcp__codegraph.codegraph_explore` hoặc `mcp__codegraph.codegraph_search` |
| Đọc source một symbol | `mcp__codegraph.codegraph_node` với `includeCode=true` |
| Đọc source một file đã biết | `mcp__codegraph.codegraph_node` với `file` |
| Xem ai gọi function/method | `mcp__codegraph.codegraph_callers` |
| Tìm text/config/docs không phải symbol | `rg` hoặc tool đọc file phù hợp |
| Kiểm tra thay đổi git | `git status`, `git diff`, `git log` |

---

## Cách AI đọc rules
1. **Global Rules**: Luôn load đầu tiên.
2. **Modular Rules**: Tự động load thêm `frontend.md` hoặc `backend.md` dựa vào path của file đang làm việc.
3. **Project Context**: Load từ `.agents/context/` để override (nếu là `[OVERRIDABLE]`).
