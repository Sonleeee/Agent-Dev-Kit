---
id: scout
type: utility
entry-command: /sk-scout
description: Phát hiện edge cases, error paths, data flow issues trước khi review
modifiers:
  --data: Focus phân tích data flow — null propagation, type mismatches
  --error: Focus error handling paths — missing catches, swallowed exceptions
  --security: Focus security edge cases — injection, auth bypass, input validation
---

# /sk-scout

**Mục tiêu:** Khám phá edge cases và rủi ro tiềm ẩn trước khi code đi vào review/production.

## Khi nào dùng

- Trước `/sk-review` — tìm edge cases review nên kiểm tra
- Sau `/sk-impl` — double-check implementation
- Module phức tạp — nhiều data flows, error paths
- Trước deploy — scan rủi ro lần cuối

## Quy trình

### Bước 1: Map — Vẽ data flow

Agent mapping:

- Input → Processing → Output cho mỗi public API/endpoint
- Data transformations tại mỗi layer
- External dependencies (DB, API, file system)
- State mutations (nếu có)

### Bước 2: Probe — Tìm edge cases & patterns

Agent kiểm tra theo categories (Inspiration: ck:scout):

**Pattern Exploration [NEW]:**
- Tìm các patterns "ngoại lai" không tuân thủ `.agents/context/`.
- Phát hiện các đoạn code trùng lặp hoặc có thể refactor.
- Kiểm tra tính nhất quán giữa các layers.

**Data edge cases:**
- Null / undefined / empty string
- Boundary values (0, -1, MAX_INT, empty array)
- Unicode, special characters trong input

**Error handling:**
- Missing try-catch blocks
- Swallowed exceptions (catch rỗng)
- Error messages lộ internal info
- Cascading failures — 1 component fail → kéo theo chuỗi

**Logic edge cases:**
- Off-by-one errors
- Division by zero
- Circular dependencies / infinite loops
- Time-zone / date boundary issues

### Bước 3: Trace — Error paths

Agent trace:

- Mỗi catch block → xử lý gì? Log? Rethrow? Swallow?
- Fallback behaviors — có hợp lý không?
- Missing error handlers — method throw nhưng caller không catch
- Cleanup / rollback — có transaction? Có undo failed operations?

### Bước 4: Report — Phân loại findings

Agent output findings theo severity:

| Severity | Mô tả |
|---|---|
| 🔴 Critical | Có thể crash, data loss, security breach |
| 🟠 Major | Logic sai trong common cases |
| 🟡 Minor | Edge case hiếm gặp, low impact |
| ℹ️ Info | Observation, recommendation |

### Bước 5: Suggest — Đề xuất

Agent đề xuất cho mỗi finding:

- Test case cụ thể để verify
- Guard / validation cần thêm
- Error handling cần bổ sung

## Output bắt buộc

- Data flow diagram (text-based)
- Findings list phân loại theo severity
- Suggestions cho từng finding
- Summary: X Critical / Y Major / Z Minor

## Guardrails

- Scout KHÔNG sửa code — chỉ report findings
- Findings phải có evidence (chỉ rõ file:line)
- Không report false positives — chỉ report khi có evidence cụ thể
- Nếu > 5 Critical findings → recommend chuyển sang `/sk-fix` workflow
