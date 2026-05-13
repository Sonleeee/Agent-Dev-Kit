---
name: sk-context-update
description: |
  Cập nhật Context dự án bằng quy trình Batch-of-3 Comparison.
  Quét source code, đối chiếu với context hiện tại, trình user xác nhận từng batch.
  Có Provenance tracking để phân biệt architecture evolution vs bug fix cá nhân.
context-required: required
output: markdown (cập nhật file trong `.agents/context/`)
accelerators: graphify (optional), gitnexus (optional)
---

# Cập Nhật Context (Context Update) — Batch Comparison Flow

## Mục tiêu

Tránh agents lặp lỗi cũ bằng cách cập nhật rules, templates, pitfalls vào `.agents/context/` — dựa trên dữ liệu thực tế và qua user xác nhận.

## Khi nào sử dụng?

- Sau khi kết thúc Epic/tính năng khó → rút ra điều chỉnh kiến trúc.
- Phát hiện pattern mới tối ưu hơn cách cũ.
- Bug lặp ≥ 2 lần → cần thêm pitfall vào context.

## Flow tổng quan

```
Bước 1: Quét Source & Đối Chiếu Context hiện tại
  ├─ Đọc context files hiện tại
  ├─ Dùng Accelerator/grep scan source code
  └─ Tìm patterns LỆCH hoặc MỚI so với context

Bước 2: ⭐ Batch-of-3 Comparison Loop
  ├─ Mỗi batch 3 changes (Before/After/Evidence)
  ├─ CHỜ user confirm từng batch
  └─ Running Summary accumulator

Bước 3: Patching (chỉ items user approved)
  ├─ Update templates, architecture, checklist
  ├─ Tag [Legacy] nếu module cũ chưa migrate
  └─ Thêm Provenance cho mỗi entry mới

Bước 4: Review Report
```

---

## Bước 1: Quét Source & Đối Chiếu

### 1.1 — Đọc Context hiện tại

- `architecture.md` (TIER-0 + relevant TIER-1 sections)
- `templates/` (code pattern files)
- `checklist.md`
- `TEMPLATES-GUIDE.md` (nếu có)

### 1.2 — Scan Source Code

Detect accelerator (giống sk-context-create Phase 0.3):

| Accelerator | Cách dùng |
|-------------|-----------|
| Graphify | Đọc `GRAPH_REPORT.md` → tìm god nodes mới, clusters thay đổi |
| GitNexus | `query({query: "new patterns"})` → so sánh với context |
| Fallback | Grep + directory scan → diff với context rules |

### 1.3 — Phân loại Changes

| Loại | Mô tả | Xử lý |
|------|-------|-------|
| **LỆCH** | Source code dùng pattern khác context | Trình user chọn: update context hoặc fix code |
| **MỚI** | Pattern mới chưa có trong context | Trình user đánh giá: evolution hay one-off |
| **DEPRECATED** | Context ghi nhưng source đã bỏ | Trình user chọn: remove hoặc tag [Legacy] |

---

## Bước 2: Batch-of-3 Comparison Loop

### Quy tắc BẮT BUỘC

1. **Mỗi batch = 3 changes**.
2. **PHẢI CHỜ user confirm từng batch** — không gộp tất cả.
3. **Smart Grouping**: Nhóm theo category (Architecture, Error Handling, Naming...).
4. **Max 7 batches**. Nếu nhiều hơn → gom vào "Minor Changes" section.

### Format mỗi batch

```markdown
---
**🔄 Update Batch {N}/? — {Category}**

| # | Rule/Pattern Cũ (Context) | Pattern Mới (Source) | Evidence | Loại |
|---|--------------------------|---------------------|----------|------|
| 1 | {pattern cũ} | {pattern mới} | Module X, Y (5 occurrences) | LỆCH |
| 2 | {pattern cũ} | {pattern mới} | Module Z (2 occurrences) | LỆCH |
| 3 | N/A (mới) | {pattern mới} | Module W (3 occurrences) | MỚI |

**Code comparison:**
// Cũ (từ context):
{code cũ}

// Mới (từ source):
{code mới}

**❓ Câu hỏi:**
1. Chấp thuận update nào? (1, 2, 3, "all", hoặc "skip")
2. Update nào là architecture evolution vs bug fix cá nhân?
---
```

### Running Summary (accumulator)

```markdown
## Approved Updates (Running)
- ✅ [Architecture] Exception taxonomy → thêm ValidationException — batch 1
- ✅ [Naming] Repository suffix convention thay đổi — batch 1
- ❌ REJECTED Controller caching pattern — batch 2 (one-off optimization)
- ✅ [Template] Handler base class updated — batch 2
...
```

### Kết thúc loop khi:
- Hết changes trong raw list
- HOẶC đạt max 7 batches
- HOẶC user nói "đủ rồi"

---

## Bước 3: Patching

Chỉ patch items user đã approved trong Running Summary.

### 3.1 — Update Context Files

| File | Loại update |
|------|-------------|
| `architecture.md` | Sửa rules, thêm anti-patterns, update TIER sections |
| `templates/*.template` | Ghi đè hoặc tạo mới code templates |
| `checklist.md` | Thêm/sửa checklist items |
| `TEMPLATES-GUIDE.md` | Cập nhật mô tả template mới |

### 3.2 — Legacy Tagging

Nếu module cũ chưa kịp migrate sang pattern mới:
- Đánh dấu `[Legacy]` trong `architecture.md`
- Ghi rõ: module nào đang dùng pattern cũ

### 3.3 — Provenance Tracking

Mỗi entry mới/sửa PHẢI có provenance:

```markdown
| P{n} | {mô tả} | ❌ Sai | ✅ Đúng | Source: {context}, {date} |

## Confidence levels:
- 1 source → ⚠️ Low confidence — re-review sau 3 tháng
- ≥ 3 sources khác module → ✅ High confidence — stable rule
```

---

## Bước 4: Review Report

Output: Markdown report gọn gàng chứa:

```markdown
## 🔄 Context Update Report

### Files tác động
- `architecture.md` — {tóm tắt thay đổi}
- `templates/be/handler.template` — {tóm tắt}

### Changes Applied
| # | Thay đổi | Loại | Confidence | Provenance |
|---|----------|------|------------|------------|
| 1 | {mô tả} | Evolution | High (5 modules) | Feature #123, 2026-05-11 |
| 2 | {mô tả} | New Rule | Low (1 module) | Bug fix, re-review 3 tháng |

### Rejected (không apply)
- {lý do bị reject}

### Legacy Modules (chưa migrate)
- {module} — vẫn dùng pattern cũ
```

### Bước 5: Brain Writeback

Áp dụng `SYSTEM.md` → Brain Writeback Policy.

| Điều kiện | Mode | Hành động |
|-----------|------|-----------|
| Có approved update thuộc architecture evolution, legacy rule, hoặc recurring pitfall | `AUTO` | Gọi `sk-vault-steward` hoặc `sk-context-cache`, target `03_Cache/decisions` hoặc `03_Cache/patterns` |
| Chỉ có minor wording/template cleanup | `SKIP` | Không ghi |

Nội dung ghi:
- Approved update summary
- Before/After ngắn
- Evidence modules
- Confidence/provenance
- Legacy impact nếu có

---

## Guardrails

- **Nguyên tắc kế thừa**: Không tẩy xóa ghi chú cũ nếu vẫn đúng cho legacy modules → đánh dấu `[Legacy]`.
- **Luôn kiểm định lý do**: Chỉ update rule nếu bug/pattern mang tính hệ thống. Không gộp fix bug cá nhân thành Architecture Rule.
- **Provenance bắt buộc**: Mỗi entry mới phải ghi nguồn gốc + confidence level.
- **Mỗi batch PHẢI chờ user**: Tuyệt đối không gộp tất cả changes rồi trình 1 lần.
- **Không phá vỡ TIER format**: Update phải giữ đúng cấu trúc TIER-0/TIER-1/TIER-2 của `architecture.md`.
