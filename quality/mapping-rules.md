# Mapping Rules — Decision Tree

Dùng để xác định checklist subset cần verify dựa trên đặc điểm của task.
Được dùng bởi: `solution-planning`, `delivery-orchestrator`, `review-workflow`, `regression-checklist`.

## Cách Dùng
1. Xác định task-features của task hiện tại (danh sách dưới)
2. Với mỗi feature có trong task → áp checklist items tương ứng
3. Tổng hợp thành required checklist subset cho task

---

## Decision Tree

### IF task-features includes "data-table"
**Required checklist items:** #7, #8, #9, #16, #17, #18, #19, #20, #28, #29
**Lý do:** Table có nhiều interaction phức tạp hay bị miss: filter badge count, empty state, sort behavior, paging boundaries.

### IF task-features includes "form-submit"
**Required checklist items:** #10, #11, #12, #13, #14, #15, #30, #31
**Lý do:** Form submit là điểm hay có bug: duplicate submit, validation thiếu, error message không thân thiện.

### IF task-features includes "delete-action" OR "approve-action"
**Required checklist items:** #24, #25, #26, #27, #37
**Lý do:** Destructive actions cần confirmation + permission + behavior sau action.

### IF task-features includes "api-change"
**Required checklist items:** chạy `core/api-contract-guard` đầy đủ
**Lý do:** API change là nguồn gốc của FE/BE drift — phải guard riêng.

### IF task-features includes "auth" OR "permission"
**Required checklist items:** #37, unauthorized flow test
**Lý do:** Permission bug thường không visible ở happy path.

### IF task-features includes "navigation" OR "routing"
**Required checklist items:** #6, breadcrumb + deep link test
**Lý do:** Route change hay break backward navigation.

### IF task-features includes "i18n"
**Required checklist items:** #38, all locale files check
**Lý do:** i18n miss: thêm key ở 1 locale nhưng quên locale khác.

### IF task-features includes "file-upload" OR "file-download"
**Required checklist items:** file size limit, file type validation, download behavior, error on invalid file
**Lý do:** File operations có nhiều edge case security và UX.

### IF task-features includes "real-time" OR "websocket"
**Required checklist items:** connection lost behavior, reconnect behavior, stale data handling
**Lý do:** Real-time features hay break khi network unstable.

### IF task-features includes "pagination" OR "infinite-scroll"
**Required checklist items:** #28, #29, empty page, last page behavior
**Lý do:** Boundary cases của pagination hay bị miss.

### IF task-features includes "search"
**Required checklist items:** #9, exact match, partial match, no results, clear search, special characters
**Lý do:** Search có nhiều edge case string handling.

### IF task-features includes "export" OR "report"
**Required checklist items:** empty data export, large dataset, format correctness, filename/headers
**Lý do:** Export hay sai ở edge cases: empty dataset, số lớn, format đặc biệt.

---

## Task Feature Tags (Tham Khảo)

| Tag | Khi nào có |
|---|---|
| `data-table` | Task có list page với table |
| `form-submit` | Task có create/edit form |
| `delete-action` | Task có thao tác xóa |
| `approve-action` | Task có thao tác duyệt/reject |
| `api-change` | Task thay đổi endpoint/DTO/status/response |
| `auth` | Task liên quan login/logout/token |
| `permission` | Task liên quan role/permission check |
| `navigation` | Task thay đổi route/menu |
| `i18n` | Task thêm/đổi text hiển thị |
| `file-upload` | Task có upload file |
| `file-download` | Task có download/export file |
| `real-time` | Task có websocket/SSE/polling |
| `pagination` | Task có phân trang |
| `search` | Task có tìm kiếm |
| `export` | Task có export data |
| `report` | Task có generate report |

---

## Minimum Baseline (mọi task đều cần)

Bất kể task-features là gì, luôn check:
- #30 (crash resistance), #31 (friendly error), #32 (no debug logs)
- Happy path của tính năng chính
- Luồng lân cận trực tiếp (regression)
