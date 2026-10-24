# Global Rules

Tất cả rules trong file này áp dụng cho mọi project và mọi platform. Những quy tắc này là "tòa tối cao" của hệ thống.

Mỗi rule được đánh dấu:
- `[PROTECTED]` — không thể override.
- `[OVERRIDABLE]` — project có thể override qua `rule-overrides.approved.md`.

---

## Nhóm 1 — Task Quality & Evidence [PROTECTED]

### Scope và cách kiểm chứng
- Task rõ được implement trực tiếp; không bắt buộc tạo problem statement, scope record, plan artifact hoặc quality card.
- Chỉ hỏi khi thiếu quyết định có thể đổi hành vi, phạm vi hoặc ranh giới an toàn. Giả định nhỏ, dễ đảo ngược có thể nêu ra và tiếp tục.
- Chọn build, lint, typecheck hoặc tests theo loại thay đổi, hướng dẫn repo và yêu cầu user. Không yêu cầu chạy toàn bộ bộ lệnh cho thay đổi không liên quan.
- Báo chính xác lệnh đã chạy và kết quả. Không suy ra PASS từ code review hoặc từ một lệnh kiểm chứng chưa chạy.
- Full code review và ship decision chỉ chạy khi user yêu cầu hoặc risk cần góc nhìn độc lập; rà diff ngắn vẫn thuộc bước hoàn tất bình thường.

### Frontend & UI Craft Gate [PROTECTED]
Chỉ kích hoạt khi task có thay đổi/xây mới mã nguồn Frontend/UI (`.html`, `.css`, `.tsx`, `.jsx`, `.vue`, `.svelte`):
- **Bắt buộc nạp `adk-ui-craft` và bám sát `DESIGN.md`:** Cấm tuyệt đối AI UI Slop (dải màu `from-purple-600 to-blue-600`, raw emoji trong nút/badge, `outline: none` không có `focus-visible`).
- **Objective Gate Verification:** Bắt buộc đảm bảo Zero Horizontal Overflow (320px–1920px), đủ 4 trạng thái tương tác (`default`, `:hover`, `:focus-visible`, `:active`/`:disabled`), touch target $\ge 44\times44$px, và chạy script kiểm định `adk-ui-craft/scripts/ui_slop_auditor.py` trên các file UI đã sửa.

### Minimum Acceptance Criteria [PROTECTED]
- Xác định happy path, edge case và lỗi có ý nghĩa với phạm vi cụ thể; không áp dụng quota cố định cho mọi feature.
- Bugfix: kiểm tra nguyên nhân và xác nhận lỗi không còn xảy ra bằng test/reproduction phù hợp khi có thể.

### Execution Evidence [PROTECTED]
Không được khẳng định đã chạy build/test/review nếu chưa có bằng chứng. Nếu chưa thể
kiểm chứng, ghi rõ điều đã kiểm tra, điều chưa chạy và lý do; không bắt buộc tạo
execution contract hoặc trạng thái `READY` cho task ngắn.

---

## Nhóm 2 — Bugfix Discipline [PROTECTED]

### Root Cause First [PROTECTED]
Với bug chưa rõ, thu thập evidence đủ để xác định layer/nguyên nhân trước khi sửa.
Không bắt buộc viết report theo một format cố định cho lỗi hiển nhiên, phạm vi hẹp.

### Anti-Regression Case [PROTECTED]
Thêm hoặc chạy anti-regression case khi test infra và phạm vi bug phù hợp; nếu không,
dùng reproduction hoặc kiểm chứng sát nhất và nêu giới hạn.

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
Chỉ tạo progress ledger khi task kéo dài qua nhiều lượt, cần resume/context
compaction, có nhiều nhánh cần theo dõi hoặc có rủi ro cao. Task nhiều bước nhưng
ngắn, liền mạch và dễ kiểm chứng không cần ledger. Khi đã có ledger, cập nhật nó
đủ để resume đúng vị trí và chỉ đánh dấu complete sau kiểm chứng phù hợp.

### Respect Project Passport [PROTECTED]
Luôn ưu tiên tuân thủ kiến trúc, conventions và ranh giới an toàn (Always / Never / Ask First) được định nghĩa trong file `AGENTS.md` tại root dự án. Code/test đang chạy thực tế vẫn là ground truth tối cao.

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

## Nhóm 6 — Autonomous Evolution & Dev Style [PROTECTED]

### R-AUTONOMOUS-DEV-STYLE — Tự giác thích ứng và ghi nhận phong cách Dev [PROTECTED]
- **Tự giác nạp gu code:** Đầu mỗi phiên làm việc, luôn ưu tiên đọc `~/.agents/developer.md` (hoặc `.agents/developer.local.md`) để tuân thủ phong cách giao tiếp, tech stack và quy ước của Developer.
- **Tự động bắt Preference:** Khi Developer đưa ra góp ý chỉnh sửa phong cách, chỉ dẫn công nghệ hoặc quy ước mới trong lúc chat, Agent có thể chủ động ghi nhận vào `evolution.db` và profile cá nhân mà không bắt người dùng phải gọi workflow thủ công.
- **Lifecycle Hook Curator:** Sau mỗi phiên làm việc hoặc khi luồng tác vụ kết thúc, hệ thống hook ngầm (`tools/session_curator.py`) tự động trích xuất Session Summary, Dev Preferences và Friction Points vào `~/.adk/evolution.db`.

---

## Cách AI đọc rules
1. **Global Rules**: Luôn load đầu tiên (`.agents/rules/global.md`).
2. **Project Passport**: Nạp conventions và ranh giới an toàn từ `AGENTS.md` tại root dự án.
3. **Developer Profile**: Nạp gu cá nhân từ `~/.agents/developer.md` hoặc `.agents/developer.local.md`.

