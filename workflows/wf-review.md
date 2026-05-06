---
id: review
type: stage
stage-number: 4
entry-command: /wf-review
next: null
prev: impl
input-from: impl-summary
output-format: review-summary
gate-after: gate-3
skills-suggested:
  - core/sk-regression-checklist
  - core/sk-api-contract-guard
modifiers:
  --fast: Review-lite — chỉ Layer 1 + 3, bỏ Layer 2 + 4, quick ship decision
  --deep: Full 4-layer review + kiểm tra cross-module impact + blast radius
  --auto: Tự động approve nếu 0 Critical + 0 Major
  --red-team: Bổ sung adversarial review — 4 personas (Security, Failure Mode, Assumption, Scope)
  --contract: Bổ sung Cross-Agent Contract Verification (chỉ dùng trong swarm/multi-agent mode)
agents-suggested:
  - reviewer
  - red-team
---

# /wf-review

**Mục tiêu:** Review code theo 4 layers, severity-based routing, evidence-driven.

## Input tối thiểu

- Output từ `/wf-impl` (impl-summary + checklist)
- Changed files list (code diff)
- Build verification result (PASS required)

> **[QUAN TRỌNG] CONTEXT ISOLATION:**
> Agent chạy Review ưu tiên evidence từ **code diff** và **project rules**.
> - **Không lean vào memory** từ plan/impl phase — review bằng mắt mới.
> - **Chỉ nạp:** Code diff, Implementation Plan ban đầu, Bộ Rules chuẩn của dự án.
> - **Nếu swarm mode:** Spawn reviewer agent riêng, không share context với implementer.

---

## Bước 0: Chuẩn Bị Review

### 0.1 — Severity Routing

Xác định change size → quyết định layers cần chạy.

| Change Size | Tiêu chí | Layers | Ghi chú |
|-------------|---------|--------|---------|
| **Patch/Hotfix** | <10 lines, 1 file | Layer 1 + 3 (quick) | Không cần architecture check |
| **Small Fix** | <50 lines, ≤3 files | Layer 1 + 2 + 3 | Đủ cho bugfix, minor feature |
| **Feature/Refactor** | >50 lines HOẶC >3 files | Layer 1-4 (full) | Review toàn diện |
| **Architecture change** | Thay đổi base class, folder structure, core pattern | Layer 1-4 + **mandatory user review** | Agent KHÔNG tự approve |

### 0.2 — Task-Feature Detection + Mapping Rules

Agent xác định task-features từ changed files:

1. Scan diff → detect features: `data-table`, `form-submit`, `delete-action`, `api-change`, `auth`, `i18n`...
2. Tra `quality/mapping-rules.md` → load checklist items tương ứng
3. Merge vào review checklist cho Layer 1 + Layer 3

> **Reference:** Xem [mapping-rules.md](../quality/mapping-rules.md) cho danh sách đầy đủ task-features + checklist items.

### 0.3 — Accelerator Detection (Optional)

Agent tự check:

- Có `.gitnexus/` → dùng GitNexus cho targeted pattern lookup (Layer 2) + cross-reference (Layer 4)
- Có `graphify-out/GRAPH_REPORT.md` → dùng Graphify cho god node detection (Bước 0.1 auto-escalate) + blast radius (Layer 4)
- Không có → manual scan (hoạt động đầy đủ, chỉ chậm hơn)

> **Lưu ý:** Accelerators là **optional enhancement**, không phải dependency.
> Review PHẢI hoạt động đầy đủ không cần Graphify/GitNexus.

### 0.4 — Review Package Assembly

Agent tổng hợp:

```
- Changed files list (diff)
- Checklist từ /wf-impl + mapping-rules items
- Architecture rules (từ .agents/context/architecture.md)
- Template rules (từ .agents/context/templates/)
- Accelerator data (nếu có)
```

> Nếu project chưa có `.agents/context/` → hỏi user:
> "Project chưa có context files. Bạn muốn tạo bằng sk-context-create trước, hay review generic?"

---

## Bước 1: Review 4 Layers

### Layer 1 — Completeness & Existence

**Câu hỏi:** "Code đã implement đúng và đủ theo plan chưa?"

**Cách thực hiện:**

1. Lấy từng item trong impl checklist
2. Cho MỖI item: **ĐỌC CODE thực tế** (không chỉ check file exists)
3. Verify: code có đúng intent của checklist item không?
4. Ghi evidence: `file:line` + code snippet ngắn

**Status:**

| Status | Nghĩa | Khi nào dùng |
|--------|-------|-------------|
| ✅ PASS | Code đúng và đủ | Code match intent của checklist item |
| ❌ FAIL | Thiếu hoặc sai | File không có, code sai logic, chưa implement |
| ⚠️ PARTIAL | Có nhưng chưa đủ | Code tồn tại nhưng thiếu edge case, missing validation |

---

### Layer 2 — Architecture & Pattern Compliance

**Câu hỏi:** "Code có follow đúng kiến trúc và pattern của dự án không?"

**Cách thực hiện:**

**Step 1: Pre-check (lightweight, nhanh)**
1. Từ code diff → extract: class names, exception types, folder locations, DI patterns
2. Match với section "Known Anti-Patterns" trong `architecture.md`
3. **Nếu no match** → `"Architecture Compliance: PASS (quick)"` → **SKIP full check**
4. **Nếu has match** → proceed to full check

**Step 2: Full Check (chỉ khi pre-check flags)**
1. Đọc **relevant sections** của architecture.md (không đọc hết)
2. Đọc template file tương ứng nếu có
3. Cross-reference diff vs context rules:
   - Layer responsibilities: code có nằm đúng layer không?
   - Naming conventions: class/method names đúng pattern không?
   - Exception handling: dùng đúng exception types không?
   - Folder structure: file đặt đúng chỗ không?
4. Report violations với severity

**Khi có accelerator:**
- GitNexus: `query("pattern for [type of changed code]")` → so sánh targeted, tiết kiệm tokens
- Graphify: Cluster membership → load đúng context section

---

### Layer 3 — Logic, Quality & Edge Cases

**Câu hỏi:** "Business logic đúng chưa? Error handling ổn chưa?"

**Cách thực hiện:**

1. **Business Logic**: Đọc code → so sánh vs requirements trong plan
   - Happy path: input → expected output?
   - Unhappy path: invalid input → proper error?

2. **Task-Feature Specific Checks** (từ mapping-rules.md):
   - `data-table` → filter, sort, paging, empty state
   - `form-submit` → validation, duplicate submit, error messages
   - `delete-action` → confirmation, permission, post-action behavior
   - `api-change` → chạy `sk-api-contract-guard`
   - (xem mapping-rules.md cho danh sách đầy đủ)

3. **Error Handling**: Exception types đúng? Catch đúng layer? Error messages rõ ràng?

4. **Edge Cases**: Null checks? Boundary values? Concurrent access?

5. **Performance** (nếu relevant): N+1 queries? Unnecessary loops? Large payload?

---

### Layer 4 — Scope & Drift Detection

**Câu hỏi:** "Có code ngoài scope không? Code có drift so với context không?"

**Cách thực hiện:**

**Part A: Unplanned Code Detection**
1. So sánh diff vs plan → tìm code KHÔNG nằm trong plan
2. **Noise filter** — KHÔNG flag những thứ hiển nhiên cần:
   - Helper methods phục vụ trực tiếp plan items
   - Import statements, using directives
   - Config/DI registration cho code mới
3. **CHỈ flag** code concerning:
   - Endpoint mới không trong scope
   - Entity/table mới không được plan
   - Permission/auth changes không được đề cập
   - Dependency mới

**Part B: Conflict Detection (Code vs Context)**

> Chỉ chạy khi project có `.agents/context/` files.

1. So sánh code change vs context rules
2. Nếu KHÁC:
   - Code dùng pattern **LEGACY** mà context đã update → Flag violation
   - Code dùng pattern **MỚI** mà context chưa có → Flag potential evolution

3. Nếu phát hiện conflict → sinh **Conflict Report**:

```markdown
## ⚠️ CONFLICT DETECTED

### Conflict #1: {Tên}
| Nguồn | Nội dung |
|-------|----------|
| **Code (diff)** | `{code snippet}` |
| **Context** | Rule: "{rule trích dẫn}" |

**Phân tích:** {Giải thích tại sao conflict}

**Options:**
- [ ] A: Fix code theo Context (recommended nếu context mới hơn)
- [ ] B: Update Context theo code (nếu code là evolution)
- [ ] C: Giữ cả hai, tag [Legacy] trong Context

→ **CHỜ user chọn.**
```

**Khi có accelerator:**
- Graphify: Dependency graph → blast radius: file X changed → files Y, Z bị ảnh hưởng
- GitNexus: `query("other modules using same pattern")` → detect drift scope

---

## Bước 2: Severity Classification

Agent phân loại MỖI finding theo 4 mức:

| Severity | Nghĩa | Ví dụ | Ship Impact |
|----------|-------|-------|-------------|
| 🔴 **Critical** | Security, data loss, breaking change | SQL injection, xóa data sai, breaking API | **Block ship** |
| 🟠 **Major** | Logic sai, architecture violation | Query trong handler, missing validation, wrong exception type | **Block ship** |
| 🟡 **Minor** | Code smell, convention deviation | Sai naming, thiếu comment, inconsistent style | **Warn, không block** |
| 🔵 **Info** | Suggestion, nice-to-have | Refactor suggestion, performance optimization idea | **Note only** |

**Hướng dẫn phân loại:**
- Ảnh hưởng user data? → Critical
- Logic sai nhưng không mất data? → Major
- Code chạy đúng nhưng không đẹp? → Minor
- Có thể cải thiện nhưng không cần thiết? → Info

---

## Bước 3: Ship Decision

| Điều kiện | Decision |
|-----------|---------|
| 0 Critical + 0 Major | ✅ **Ready** — ship (Minor/Info items ghi nhận) |
| Có Major (0 Critical) | ❌ **Blocked** — fix Major items, re-review |
| Có Critical | ❌ **Blocked** — fix Critical items, re-review |
| Có Conflict chưa resolved | ⏳ **Pending** — chờ user quyết định conflict |

---

## Output bắt buộc

- Review checklist 4 layers
- Severity summary: critical / major / minor / info counts
- Ship decision: Ready / Blocked / Pending
- Fix suggestions cho mỗi Critical/Major finding
- Conflict Report (nếu có)

## Templates

- Checklist: `../templates/review-checklist.md.template`
- Summary: `../templates/review-summary.md.template`
- Conflict Report: `../templates/conflict-report.md.template`

## Gate sau bước này (Gate 3 — Ship Ready)

- [ ] 0 Critical findings
- [ ] 0 Major findings (hoặc đã fix)
- [ ] Conflicts đã resolved (user đã chọn option)
- [ ] Ship decision: Ready

## Guardrails

- Review KHÔNG sửa code trực tiếp — chỉ report findings
- Findings PHẢI có evidence (file:line, code snippet)
- Không FAIL mà không có fix suggestion
- UNPLANNED ≠ BAD — báo user quyết định, không tự xóa/sửa
- Conflict → LUÔN trình user, không tự quyết

## Re-review Protocol

Khi chạy lại review sau fix:

1. **Chỉ re-verify** các items đã FAIL/Critical/Major — không chạy lại toàn bộ
2. **Check regression**: Fix có tạo ra vấn đề mới không?
3. **Check scope**: Fix có tạo code UNPLANNED mới không?
4. **Nếu clean** → update ship decision

> [Terminal Orchestration] Nếu IDE hỗ trợ, có thể chạy dual review
> (primary + secondary reviewer) song song. Xem `addons/swarm/`.
