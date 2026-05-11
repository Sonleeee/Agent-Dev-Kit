---
name: sk-context-create
description: |
  Khởi tạo Context chuẩn cho dự án bằng quy trình 5 Phase.
  Quét toàn bộ codebase, xác nhận patterns theo batch, sinh scaffold output.
  Dùng khi onboard project mới hoặc Domain hoàn toàn mới.
context-required: optional
output: markdown (tạo các file trong `.agents/context/`)
accelerators: graphify (optional), gitnexus (optional)
---

# Khởi Tạo Context (Context Creation) — 5-Phase Flow

## Mục tiêu

Xây dựng kho tàng kiến thức (Architecture, Code Templates, Checklist) từ codebase thực tế, theo quy trình data-driven có user xác nhận từng bước.

## Khi nào sử dụng?

- Onboard project hoàn toàn mới vào Agent-Dev-Kit.
- Module/Domain mới ra đời, mang theo pattern chưa từng có.

## Flow tổng quan

```
Phase 0: Setup
  ├─ Scope (BE? FE? Both?)
  ├─ Gold Module (optional — agent suggest nếu không có)
  ├─ Detect Accelerator (Graphify? GitNexus? None?)
  └─ Đọc Output Scaffold + Quality Rubric

Phase 1: Breadth Scan (Pattern Discovery)
  ├─ Quét codebase theo accelerator hoặc fallback
  └─ Output: Raw Pattern List + Frequency Table

Phase 2: ⭐ Incremental Confirmation (Batch-of-3)
  ├─ Smart Grouping theo layer/category
  ├─ Mỗi batch = 3 patterns + CHỜ user confirm
  ├─ Max 7 batches (~21 patterns)
  └─ Output: Confirmed Pattern Set + Running Summary

Phase 3: Deep Extraction
  ├─ Cho MỖI confirmed pattern: đọc 2-3 module
  ├─ Extract ✅ Best + ❌ Worst implementation
  └─ Output: Enriched Patterns + Pitfalls + Decision Trees

Phase 4: Generate + Validate
  ├─ Fill vào Output Scaffold
  ├─ Self-score bằng Quality Rubric (≥3/5 mỗi tiêu chí)
  └─ Trình user review lần cuối
```

---

## Phase 0: Setup

### Bước 0.1 — Scope

Agent hỏi user:
- "Scope: Backend, Frontend, hay Both?"
- "Ngôn ngữ / Framework chính?"

### Bước 0.2 — Gold Standard Module (optional)

Agent hỏi: "Bạn có module nào đã hoàn chỉnh, đáng làm reference không?"

Nếu user KHÔNG chỉ định:
- Agent scan codebase (hoặc dùng accelerator)
- Suggest 2-3 candidates dựa trên:
  - Module có structure đầy đủ nhất
  - Module follow naming convention nhất quán
  - Module có ít code smell nhất
- Trình: "Tôi suggest Module X, Y làm reference. Đồng ý?"

### Bước 0.3 — Detect Accelerator

Agent tự check:

| Điều kiện | Accelerator | Cách dùng |
|-----------|-------------|-----------|
| Có `graphify-out/GRAPH_REPORT.md` | Graphify | Đọc report → god nodes + clusters |
| Có `.gitnexus/` | GitNexus | Gọi `context()` + `query()` |
| Không có gì | Fallback | Manual grep + directory scan |

> Accelerator là **optional** — skill luôn hoạt động qua fallback.

---

## Phase 1: Breadth Scan (Pattern Discovery)

### Mục tiêu: Tạo Raw Pattern List

### Nếu có Graphify:
1. Đọc `GRAPH_REPORT.md`
2. God nodes → core concepts/patterns
3. Community clusters → module grouping

### Nếu có GitNexus:
1. Gọi `context({repo})` → architectural overview
2. Gọi `query({query: "patterns"})` cho từng layer
3. Clusters = nhóm patterns tự nhiên

### Nếu không có (fallback):
1. Scan directory structure → tạo tree
2. Grep cho: base classes, exception types, DI patterns, common imports
3. Count frequency: pattern nào xuất hiện ở bao nhiêu module?

### Output: Raw Pattern List

| # | Pattern Name | Category | Frequency | Source Modules | Confidence |
|---|-------------|----------|-----------|----------------|------------|
| 1 | {tên} | {layer/category} | {X/Y modules} | {module list} | High/Medium/Low |

---

## Phase 2: Incremental Confirmation (Batch-of-3)

### Quy tắc BẮT BUỘC

1. **Smart Grouping**: Nhóm patterns theo category (BE Handler, BE Error, FE Component...)
   → User focus 1 chủ đề per batch, không nhảy lung tung.
2. **Mỗi batch = 3 patterns**.
3. **Confidence Score**:
   - High (>80% modules dùng) → suggest "auto-confirm"
   - Medium (40-80%) → cần review kỹ
   - Low (<40%) → có thể là edge case hoặc legacy
4. **Max 7 batches** (~21 patterns). Nếu nhiều hơn → gom phần ít quan trọng
   vào "Minor Patterns" section (list nhưng không bắt confirm từng cái).
5. **KHÔNG gộp tất cả rồi hỏi 1 lần** — mỗi batch PHẢI CHỜ user confirm.
6. **Tier tagging**: Mỗi confirmed pattern phải được tag tier:
   - TIER-0: Core rule, luôn load
   - TIER-1 + [TAG]: Pattern detail, load theo task-feature

### Format mỗi batch

```markdown
---
**🔍 Batch {N}/? — {Category} Patterns**

| # | Pattern | Mô tả | Modules | Confidence | Tier | Variants? |
|---|---------|-------|---------|------------|------|-----------|
| 1 | `{name}` | {mô tả} | A, B, C | High ✅ | TIER-0 | {có/không} |
| 2 | `{name}` | {mô tả} | D, E | Medium ⚠️ | TIER-1 [TAG] | {có/không} |
| 3 | `{name}` | {mô tả} | F | Low ❓ | TIER-1 [TAG] | {có/không} |

**Code sample (trích dẫn thực tế):**
// Pattern 1 — từ Module A
{code thực tế trích xuất}

**❓ Câu hỏi:**
1. Giữ pattern nào? (chọn số: 1, 2, 3, "all", hoặc "skip")
2. Pattern nào đang sai/legacy cần loại?
3. Có variant nào cần ưu tiên?
---
```

### Running Summary (accumulator)

Sau mỗi batch, agent cập nhật summary:

```markdown
## Confirmed Patterns (Running)
- ✅ [TIER-0] [BE/Handler] Handler thin pattern — batch 1
- ✅ [TIER-1: error-handling] [BE/Error] NotFoundException taxonomy — batch 1
- ❌ REJECTED [BE/Error] InvalidOperationException — batch 1 (legacy)
- ✅ [TIER-1: component] [FE/Component] BaseService wrapper — batch 2
...
```

> Phase 3 đọc summary này, KHÔNG parse conversation history.

### Kết thúc loop khi:
- Hết patterns trong raw list
- HOẶC đạt max 7 batches
- HOẶC user nói "đủ rồi"

---

## Phase 3: Deep Extraction

Cho MỖI confirmed pattern:

### 3.1 — Best Implementation
- Đọc 2-3 module, chọn đoạn code tốt nhất.
- Ghi rõ: module nào, file nào, tại sao tốt.

### 3.2 — Anti-Pattern Mining
- Grep code smell liên quan đến pattern này.
- Nếu tìm thấy → ghi: module nào, code sai gì, cách fix.
- Nếu KHÔNG tìm thấy → ghi: "Clean — no violations found".
- **KHÔNG bịa vi phạm để đạt quota.**

### 3.3 — Sinh Pitfall Entry (nếu có vi phạm)

| P{n} | Mô tả | ❌ Sai (code trích dẫn) | ✅ Đúng (code trích dẫn) |
|------|-------|------------------------|-------------------------|

### 3.4 — Decision Tree Entry (nếu pattern có variants)

```
Q{n}: "Module có [đặc điểm X] không?"
├─ CÓ → dùng template/pattern A
└─ KHÔNG → dùng template/pattern B
```

---

## Phase 4: Generate + Validate

### 4.1 — Fill Output Scaffold

Agent fill context theo **scaffold files** trong thư mục `scaffold/` của skill này:

| Scaffold file | Output file | Sections bắt buộc |
|---------------|-------------|-------------------|
| `architecture.scaffold.md` | `.agents/context/architecture.md` | 8 sections (xem scaffold) |
| `feature.scaffold.md` | `.agents/context/templates/{scope}/feature.md.template` | Decision Qs + Code Patterns |
| `checklist.scaffold.md` | `.agents/context/checklist.md` | Global ref + project items |

### 4.2 — Self-Score bằng Quality Rubric

| Tiêu chí | 1 (Fail) | 3 (Pass) | 5 (Excellent) |
|----------|----------|----------|---------------|
| Specificity | Chung chung | Có rule + type cụ thể | Có ✅/❌ code + P{n} |
| Actionability | Không biết làm gì | Có rule follow được | Có decision tree Q{n} |
| Anti-patterns | Không có | Có list | Có evidence module |
| Code Examples | Không code | Có snippets | Cặp ✅/❌ mỗi pattern |
| Completeness | Thiếu layers | Cover hết layers | Layers + pitfalls |
| Tier Compliance | Không phân tier | Có TIER-0/1 | TIER-0 ≤200 lines + TAG markers |

**Ngưỡng:** Mỗi tiêu chí ≥ 3. Nếu fail → quay lại Phase 3 bổ sung.

### 4.3 — Final Review

- Trình toàn bộ context cho user.
- User approve → commit files vào `.agents/context/`.
- User reject → chỉnh sửa theo feedback.

---

## Output

Các file được tạo/cập nhật trong `.agents/context/`:
- `architecture.md` — Kiến trúc project (theo TIER format)
- `templates/{scope}/feature.md.template` — Code pattern templates
- `checklist.md` — Checklist riêng project
- `TEMPLATES-GUIDE.md` — Chỉ mục mô tả cách dùng từng template

## Guardrails

- **Không copy mù quáng**: Loại bỏ logic rác khỏi code template.
- **Tiêu cự**: Mô tả KIẾN TRÚC, không mô tả DATA DOMAIN.
- **Không ôm scope quá lớn**: Nếu codebase >50 modules → ưu tiên core modules trước.
- **Accelerator không bắt buộc**: Luôn có fallback (grep + scan).
- **Mỗi batch PHẢI chờ user**: Tuyệt đối không gộp tất cả patterns rồi trình 1 lần.
