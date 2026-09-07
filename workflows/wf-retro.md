---
id: retro
type: analysis
entry-command: /wf-retro
description: Sprint Retrospective — git metrics → health scores → insights → action items
modifiers:
  --period: Chỉ định khoảng thời gian phân tích (vd. "7d", "2w", "1m")
  --team: Focus phân tích theo contributor
  --churn: Focus files thay đổi nhiều nhất
  --full: Phân tích đầy đủ tất cả dimensions
---

# /wf-retro — Sprint Retrospective

**Mục tiêu:** Phân tích sức khỏe codebase dựa trên git history — rút ra insights và action items cải thiện.

## Khi nào dùng

- Cuối sprint/iteration
- Khi cảm thấy codebase "xấu đi" nhưng chưa rõ ở đâu
- Trước khi lên kế hoạch refactoring
- Review sức khỏe dự án định kỳ

## Input

- Git repository (phải có git history)
- Period: mặc định 2 tuần, override bằng `--period`
- Project context: `AGENTS.md` (nếu có)

## Flow

```
Bước 1: Git Metrics Collection
  ├─ Collect: commits, files changed, insertions/deletions
  ├─ Period: --period hoặc default 2 tuần
  └─ Output: Raw metrics data

Bước 2: Multi-Dimension Analysis
  ├─ Churn Analysis: files thay đổi nhiều nhất
  ├─ Complexity Trends: files phình to vs thu gọn
  ├─ Contributor Patterns: ai làm gì, ở đâu
  ├─ Hotspot Detection: files vừa churn cao vừa phức tạp
  └─ Modifier --churn/--team/--full: focus dimension

Bước 3: Health Scoring
  ├─ Score 5 dimensions (1-5 scale)
  └─ Overall health: trung bình có trọng số

Bước 4: Insights & Action Items
  ├─ Rút ra insights từ metrics
  ├─ Đề xuất action items cụ thể
  └─ Prioritize: Quick Win / Medium / Long-term

Bước 5: Knowledge Checkpoint
  Áp dụng `SYSTEM.md` → Brain Writeback Policy.
  ├─ AUTO nếu có health insight, hotspot, recurring issue, hoặc action item đáng theo dõi
  │  └─ nếu Knowledge addon bật thì chạy sk-vault-steward (type: retro, target: cache:reviews hoặc log-only)
  └─ SKIP nếu không có insight mới ngoài số liệu tạm thời
```

## Bước 1: Git Metrics Collection

Các lệnh git cần chạy:

```bash
# Commits in period
git log --oneline --after="{start_date}" --before="{end_date}"

# Files changed with stats
git log --numstat --after="{start_date}" --before="{end_date}"

# Contributors
git shortlog -sn --after="{start_date}" --before="{end_date}"

# File churn (most changed files)
git log --name-only --after="{start_date}" --format="" | sort | uniq -c | sort -rn | head -20
```

## Bước 2: Multi-Dimension Analysis

### 2.1 — Churn Analysis
- Top 10 files thay đổi nhiều nhất
- Flag: file >5 lần thay đổi trong period = "hotspot"

### 2.2 — Complexity Trends
- Files tăng >50 lines = "growing"
- Files giảm >20 lines = "refactored"
- Tỷ lệ additions/deletions tổng thể

### 2.3 — Contributor Patterns (--team)
- Ai commit nhiều nhất ở module nào
- Bus factor: module chỉ 1 người touch = risk

### 2.4 — Hotspot Detection
- Files vừa churn cao VÀ kích thước lớn = priority refactor target

## Bước 3: Health Scoring

| Dimension | 1 (Nguy) | 3 (Ổn) | 5 (Tốt) |
|-----------|----------|---------|----------|
| Churn Distribution | >50% changes ở 3 files | Top 10 files < 40% | Phân bố đều |
| Code Growth | Net +500 lines | Net +100 lines | Net ≤0 (stable/shrink) |
| Contributor Spread | Bus factor 1 ở >3 modules | Bus factor 1 ở 1 module | Không có bus factor 1 |
| Refactoring Ratio | 0% deletions | 20-30% deletions | >30% deletions |
| Commit Frequency | <5 commits/week | 10-20/week | Steady rhythm |

### Overall Health

```
Overall = (Churn×2 + Growth×1.5 + Contributors×1.5 + Refactoring×2 + Frequency×1) / 8
```

| Score | Label | Action |
|-------|-------|--------|
| ≥4.0 | 🟢 Healthy | Duy trì |
| 3.0-3.9 | 🟡 Attention | Monitor + quick fixes |
| <3.0 | 🔴 At Risk | Cần refactoring sprint |

## Output

```markdown
## 📊 Retro Report: {project} — {period}

### Health Dashboard

| Dimension | Score | Trend |
|-----------|-------|-------|
| Churn Distribution | {score}/5 | {↑↓→} |
| Code Growth | {score}/5 | {↑↓→} |
| Contributor Spread | {score}/5 | {↑↓→} |
| Refactoring Ratio | {score}/5 | {↑↓→} |
| Commit Frequency | {score}/5 | {↑↓→} |
| **Overall** | **{overall}/5** | **{label}** |

### Hotspots (cần chú ý)

| # | File | Churn | Size | Action |
|---|------|-------|------|--------|
| 1 | {file} | {count} changes | {lines} lines | Refactor / Split |

### Insights
1. {insight 1}
2. {insight 2}

### Action Items

| # | Action | Priority | Effort |
|---|--------|----------|--------|
| 1 | {action} | Quick Win | Small |
| 2 | {action} | Medium | Medium |
```

## Guardrails

- Metrics phải từ **git history thực tế** — không ước lượng.
- Health scores là **heuristic** — phục vụ nhận biết nhanh, không phải KPI cứng.
- Action items phải **actionable** — không nói "cải thiện code quality" mà nói "split file X thành Y và Z".
- `--period` mặc định 2 tuần. Nếu project mới (<2 tuần history) → dùng toàn bộ history.
