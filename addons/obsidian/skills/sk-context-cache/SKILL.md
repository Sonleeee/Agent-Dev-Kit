---
name: sk-context-cache
description: |
  Cache phân tích context để tránh lặp lại công việc.
  Khi agent phân tích xong pattern/review/decision → lưu kết quả vào cache.
  Lần sau cần thông tin tương tự → đọc cache thay vì re-analyze.
context-required: optional
output: Cache entries trong Obsidian Vault 03_Cache/
---

# Context Cache — Tránh Phân Tích Lặp

## Mục tiêu

Tiết kiệm token và thời gian bằng cách cache kết quả phân tích. Thay vì đọc 5,800 tokens context mỗi lần → đọc 350 tokens cache entry (tiết kiệm ~94%).

## Khi nào kích hoạt?

| Trigger | Ví dụ |
|---------|-------|
| Phân tích >2,000 tokens | Review findings lớn, architecture scan |
| Kết quả có thể tái sử dụng | Pattern analysis, decision rationale |
| Bug lặp ≥2 lần | Root cause giống nhau ở nhiều module |

## Cache Structure

### Vault Location

```
Obsidian Vault/
├── 03_Cache/
│   ├── _REGISTRY.md          ← Index tất cả cache entries
│   ├── patterns/              ← Cached pattern analysis
│   ├── reviews/               ← Cached review findings
│   └── decisions/             ← Cached architecture decisions
```

### Naming Convention

```
{project}_{topic_snake_case}.md
```

Ví dụ:
- `wms_handler_thin_pattern.md`
- `emart_error_taxonomy.md`
- `biomass_date_handling_decision.md`

---

## Cache Write Flow

```
Bước 1: Trigger Detection
  ├─ Agent phát hiện analysis kết quả >2,000 tokens
  └─ HOẶC agent nhận lệnh cache từ workflow

Bước 2: Format Cache Entry
  ├─ Dùng Cache Entry Template (xem bên dưới)
  ├─ Content ceiling: ≤50 lines
  └─ Bắt buộc: tags, confidence, TTL

Bước 3: Write
  ├─ Tạo file trong 03_Cache/{category}/
  └─ Update _REGISTRY.md

Bước 4: Confirm
  └─ Report: "✅ Cached: {entry_name} (TTL: {ttl})"
```

### Cache Entry Template

```markdown
---
type: cache_entry
cache_id: {category}_{seq}
project: {project_name}
topic: {topic}
tags: [{tag1}, {tag2}]
created: {YYYY-MM-DD}
ttl: {1mo|3mo|6mo|long-term}
expires: {YYYY-MM-DD}
confidence: {high|medium|low}
source_count: {number}
---

# {Topic Title}

## Summary
{Tóm tắt ≤5 câu — tiếng Việt}

## Key Findings
- {finding 1}
- {finding 2}

## Evidence
- Module: {module_name} — {mô tả}

## References
- [[{raw_source_link}]]
- [[{wiki_article_link}]]
```

---

## Cache Lookup Flow

```
Bước 1: Check _REGISTRY.md
  ├─ Tìm entry có tags khớp với task context
  └─ Check TTL: expired? → skip, re-analyze

Bước 2: Hit / Miss
  ├─ HIT → đọc cache entry (≤50 lines) → dùng
  └─ MISS → analyze bình thường → trigger Write Flow

Bước 3: Confidence Check
  ├─ High confidence → dùng trực tiếp
  └─ Low confidence → dùng nhưng verify thêm
```

---

## TTL Management

| TTL | Khi nào dùng | Ví dụ |
|-----|-------------|-------|
| **1mo** | Findings dễ thay đổi | Bug patterns, performance metrics |
| **3mo** | Patterns ổn định trung bình | Review findings, feature patterns |
| **6mo** | Architecture decisions | Tech stack choices, layer design |
| **long-term** | Kiến thức nền tảng | Naming conventions, folder structure |

### Confidence Levels

| Level | Điều kiện | Hành vi |
|-------|-----------|---------|
| **High** | ≥3 sources từ modules khác nhau | Stable rule — dùng trực tiếp |
| **Medium** | 2 sources | Dùng nhưng monitor |
| **Low** | 1 source | Re-review sau 3 tháng |

---

## Integration Points

| Workflow/Skill | Cách dùng cache |
|----------------|----------------|
| `wf-review` | Cache review findings pattern → tái sử dụng cho review tương tự |
| `wf-review` + context manifest | Cache analysis results → không re-scan cùng codebase |
| execution contract | Cache change history → track evolution có approval |
| `wf-fix` | Cache root cause analysis → detect recurring bugs |

---

## Auto-Generation

### _REGISTRY.md Auto-Update

Khi thêm/xóa cache entry → skill tự động update `_REGISTRY.md`:
- Thêm row mới vào bảng index
- Đánh dấu entries expired
- Giữ _REGISTRY ≤50 lines (archive entries cũ)

### AI_INDEX Integration

Khi cache entry được tạo → check `01_Wiki/AI_INDEX.md`:
- Nếu topic chưa có trong AI_INDEX → thêm reference
- Giữ AI_INDEX ≤50 lines

---

## 3 Golden Rules

1. **≤50 lines**: Mỗi cache entry KHÔNG vượt 50 lines (ceiling cứng).
2. **Tags bắt buộc**: Mọi entry PHẢI có lookup tags trong frontmatter.
3. **Traceability**: Mọi entry PHẢI link về source (raw/wiki/code).

## Guardrails

- Cache là **heuristic** — không phải ground truth. Luôn verify khi confidence thấp.
- Không cache **toàn bộ conversation** — chỉ cache kết quả đã chưng cất.
- TTL expired → xóa hoặc re-analyze, không để entry stale.
