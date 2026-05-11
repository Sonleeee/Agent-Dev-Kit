---
id: predict
type: analysis
entry-command: /wf-predict
description: Expert Debate — 5 personas tranh luận impact trước khi implement
modifiers:
  --focus: Chỉ chạy personas liên quan nhất (2-3 thay vì 5)
---

# /wf-predict — Expert Debate

**Mục tiêu:** Trước khi implement thay đổi lớn, để 5 expert personas tranh luận impact từ nhiều góc nhìn — giảm rủi ro bất ngờ.

## Khi nào dùng

- Thay đổi architecture (thêm layer, đổi pattern, thêm dependency)
- Migration lớn (database, framework, API version)
- Feature ảnh hưởng nhiều modules (>5 files, cross-cutting)

## Input

- Mô tả thay đổi dự kiến
- Context: `AGENTS.md` + `architecture.md` (nếu có)

## 5 Expert Personas

| # | Persona | Góc nhìn | Câu hỏi chính |
|---|---------|----------|---------------|
| 1 | 🏗️ **Architect** | Kiến trúc & patterns | "Có phá vỡ separation of concerns không? Có tạo god class không?" |
| 2 | 🔒 **Security** | Bảo mật & compliance | "Có mở attack surface mới không? Data exposure risk?" |
| 3 | ⚡ **Performance** | Hiệu năng & scalability | "Có N+1 queries? Memory leak? Bottleneck mới?" |
| 4 | 🎨 **UX** | User experience & API ergonomics | "API có consistent không? Breaking change cho consumers?" |
| 5 | 🔧 **Ops** | Deployment & observability | "Có cần migration script? Rollback plan? Monitoring mới?" |

## Flow

```
Bước 1: Context Loading
  ├─ Đọc AGENTS.md + architecture.md
  └─ Hiểu current state

Bước 2: Persona Analysis (tuần tự hoặc song song)
  ├─ Mỗi persona phân tích thay đổi từ góc nhìn riêng
  ├─ Output: Findings list (severity: Critical/Major/Minor/Info)
  └─ Modifier --focus: chỉ chạy personas liên quan

Bước 3: Deduplication
  ├─ Gom findings trùng lặp
  └─ Rank theo severity

Bước 4: Debate Summary
  ├─ Trình bảng findings cho user
  ├─ Highlight conflicts giữa personas (nếu có)
  └─ Verdict: PROCEED / PROCEED WITH CAUTION / BLOCK

Bước 5: Knowledge Checkpoint
  Agent hỏi: "📝 Lưu kết quả debate vào SecondBrain không?"
  └─ Có → chạy sk-vault-steward (type: research)
```

## Output

```markdown
## 🔮 Predict Report: {tên thay đổi}

### Persona Findings

| # | Persona | Finding | Severity | Recommendation |
|---|---------|---------|----------|---------------|
| 1 | 🏗️ Architect | {finding} | Major | {recommendation} |
| 2 | 🔒 Security | {finding} | Minor | {recommendation} |
| ... | ... | ... | ... | ... |

### Conflicts
- {Persona A} vs {Persona B}: {mô tả xung đột}

### Verdict: {PROCEED / PROCEED WITH CAUTION / BLOCK}

### Mitigation Plan (nếu PROCEED WITH CAUTION)
1. {action item}
2. {action item}
```

## Verdict Rules

| Điều kiện | Verdict |
|-----------|---------|
| 0 Critical, ≤2 Major | ✅ PROCEED |
| 0 Critical, >2 Major | ⚠️ PROCEED WITH CAUTION |
| ≥1 Critical | ❌ BLOCK — phải resolve trước |

## Guardrails

- Mỗi persona phân tích **độc lập** — không bias bởi persona khác.
- Findings phải có **evidence** hoặc **reasoning** cụ thể, không nói chung chung.
- Không bịa findings để đạt quota — nếu persona không tìm thấy issue → ghi "No concerns".
- `--focus` modifier: Agent tự chọn 2-3 personas phù hợp nhất với loại thay đổi.
