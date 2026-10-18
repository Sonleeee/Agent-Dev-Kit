# Global Rules

Tất cả rules trong file này áp dụng cho mọi project và mọi platform. Những quy tắc này là "tòa tối cao" của hệ thống.

Mỗi rule được đánh dấu:
- `[PROTECTED]` — không thể override.
- `[OVERRIDABLE]` — project có thể override qua `rule-overrides.approved.md`.

---

## Nhóm 1 — Delivery Gates [PROTECTED]

### Gate 1 — Ready [PROTECTED]
Không được bắt đầu implement khi thiếu: Problem statement, Scope in/out, Implementation plan, Acceptance Criteria và Verification Command.

### Gate 2 — Dev Done [PROTECTED]
Không được chuyển sang review khi chưa hoàn thành self-check và chạy verify lệnh thực thi.

### Gate 3 — Ship Ready [PROTECTED]
- **Blocked**: Khi còn finding Critical hoặc lệnh verification/tests fail.
- **Pass có điều kiện**: Không có Critical, nếu có Major phải nêu rõ lý do và residual risks.

### Executable Verification Gate [PROTECTED]
Chất lượng code bắt buộc phải được chứng minh bằng lệnh thực thi thật của project (compiler, linter, tests):
- Build/Compilation phải pass với Zero Warnings (hoặc treat warnings as errors).
- Linter/Typecheck (npm run lint, tsc --noEmit, dotnet format, ruff check...) phải pass 100%.
- Unit/Integration Tests liên quan phải pass 100%.

### Minimum Acceptance Criteria [PROTECTED]
- Feature: Tối thiểu 2 happy paths + 2 edge cases trong scope + 1 error handling/user message.
- Bugfix: Root cause rõ ràng + tối thiểu 1 anti-regression test case + xác nhận bug gốc không còn tái diễn.

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

### R-MINIMAL-CODE — Ponytail Rule [PROTECTED]
Triết lý: *"Đoạn code tốt nhất là đoạn code không phải viết."*

Ràng buộc bắt buộc:
1. **Cấm tự ý tạo abstraction thừa:** Không tự tạo helper function, utility wrapper,
   base class hoặc middleware layer khi chưa có ít nhất 3 use cases thực tế hoặc chỉ
   định rõ ràng từ user. Một hàm chỉ được gọi 1 lần không cần wrapper.
2. **Thứ tự ưu tiên giải pháp:** Built-in / standard library → tính năng có sẵn của
   framework → dependency đã cài sẵn trong project → mới cân nhắc thêm package mới.
3. **Xóa trước, viết sau:** Khi refactor hoặc thêm tính năng, ưu tiên loại bỏ code
   thừa, dead code, unused imports trước khi viết code mới.
4. **Cấm design pattern cho single implementation:** Không áp dụng Factory, Strategy,
   Observer, Mediator hoặc bất kỳ pattern nào khi chỉ có duy nhất 1 concrete
   implementation và không có kế hoạch mở rộng rõ ràng trong scope hiện tại.

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

## Nhóm 5 — Automation & Browser Discipline [PROTECTED]

### R-BROWSER-ISOLATION — Trình duyệt tự động hoá tách biệt [PROTECTED]
- Tuyệt đối không can thiệp, đóng hoặc gán cờ debug vào trình duyệt cá nhân người dùng đang mở.
- Luôn dùng trình duyệt chuyên biệt cho tự động hoá (Chrome for Testing hoặc trình duyệt do Playwright/Puppeteer quản lý riêng).

### R-BROWSER-CLEANUP — Giải phóng tài nguyên trong finally [PROTECTED]
- Mọi luồng mở browser tự động hoá bắt buộc phải bọc trong `try ... finally` với lệnh đóng tường minh (`await browser.close()` / `driver.quit()`).
- Tắt sạch dev server / preview server (Vite, Next, Flask, Uvicorn, v.v.) ngay khi hoàn thành kiểm thử hoặc phiên tác vụ.

### R-SAFE-PROCESS-TERMINATION — Dừng tiến trình mồ côi an toàn [PROTECTED]
- TUYỆT ĐỐI KHÔNG kill hàng loạt theo tên tiến trình (cấm `taskkill /f /im chrome.exe` hoặc `pkill chrome`).
- Chỉ dừng đúng từng PID cụ thể đã xác định là mồ côi (tiến trình cha đã mất).
- Ưu tiên tắt đúng cách (tắt server / tiến trình cha để browser tự thoát bình thường).

### R-TEMP-PROFILE-CLEANUP — Dọn dẹp thư mục tạm an toàn [PROTECTED]
- Thư mục profile tạm thời (`--user-data-dir` tạm, `scoped_dir*`) chỉ được xoá khi đã kiểm tra chắc chắn không còn tiến trình nào đang chiếm giữ (InUse = False).

---

## Cách AI đọc rules
1. **Global Rules**: Luôn load đầu tiên.
2. **Modular Rules**: Tự động load thêm `frontend.md` hoặc `backend.md` dựa vào path của file đang làm việc.
3. **Project Context**: Load từ `.agents/context/` để override (nếu là `[OVERRIDABLE]`).

