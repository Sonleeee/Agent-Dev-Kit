---
id: retro
type: utility
entry-command: /sk-retro
description: Sprint retrospective — git metrics analysis → health scores → insights → action items
modifiers:
  --period: Chỉ định khoảng thời gian (mặc định 2 tuần). VD: --period 1w, --period 1m
  --team: Focus phân tích theo contributor (ai commit gì, phân bổ work)
  --churn: Focus files có thay đổi nhiều nhất — hot spots
  --full: Phân tích đầy đủ tất cả dimensions
---

# /sk-retro

**Mục tiêu:** Sprint retrospective dựa trên git metrics — phân tích health, tìm patterns, đề xuất action items.

## Khi nào dùng

- Cuối sprint/iteration — review team performance
- Sau release — đánh giá quality
- Muốn tìm hot spots (files thay đổi nhiều, code churn cao)
- Cần data-driven insights cho improvement

## Input

- (Optional) Khoảng thời gian: `--period 2w` (mặc định 2 tuần)
- (Optional) Branch: mặc định current branch
- Project có git history

## Quy trình

### Bước 1: Collect — Thu thập Git Metrics

Agent chạy commands thu thập data:

**Commit metrics:**

- Tổng số commits trong period
- Commit frequency (commits/ngày trung bình)
- Commit message quality (conventional commits %, message length)

**File metrics:**

- Files thay đổi nhiều nhất (top 10 hot spots)
- Files mới tạo vs files bị xóa
- Churn rate = (lines added + lines deleted) / total lines per file
- Largest commits (by diff size)

**Author metrics (nếu `--team`):**

- Commits per author
- Files touched per author
- Reviewer distribution (nếu có PR data)

### Bước 2: Analyze — Phân tích Patterns

Agent phân tích từ metrics:

**Health indicators:**

| Metric | 🟢 Healthy | 🟡 Warning | 🔴 Concern |
|---|---|---|---|
| Commit size | ≤200 lines | 201-500 lines | >500 lines |
| Commit frequency | Daily | 2-3 days gap | >1 week gap |
| File churn | <3 changes/file | 3-5 changes/file | >5 changes/file |
| New vs modified | Balanced | Skewed | Only new or only modify |
| Hotspot concentration | Distributed | 30% in top 3 files | >50% in top 3 files |

**Patterns detected:**

- 🔁 **Churn hotspots** — Files thay đổi >5 lần → candidate cho refactor
- 📦 **Large commits** — Commits >500 lines → cần split nhỏ hơn
- 🧩 **Coupled files** — Files luôn commit cùng nhau → possible tight coupling
- 🔙 **Fix-on-fix** — Fix commit ngay sau commit trước → quality concern
- 🗑️ **Dead code** — Files tạo rồi xóa trong cùng sprint → wasted effort

### Bước 3: Score — Health Scores

Agent tính health scores (1-10):

| Dimension | Score | Rationale |
|---|---|---|
| Commit hygiene | X/10 | Message quality, size, frequency |
| Code stability | X/10 | Churn rate, hotspot concentration |
| Velocity | X/10 | Throughput vs churn ratio |
| Architecture | X/10 | Coupling signals, new modules alignment |
| Overall | X/10 | Weighted average |

### Bước 4: Insights — Key Findings

Agent rút ra insights dạng:

```markdown
### 💡 Key Insights

1. **[Insight title]**
   - Evidence: [git data]
   - Impact: [positive/negative]
   - Recommendation: [action]
```

### Bước 5: Action Items

Agent đề xuất improvements:

**Chia theo category:**

- 🔧 **Technical debt** — Files cần refactor (churn cao)
- 📏 **Process** — Commit size limit, review cadence
- 🧪 **Quality** — Modules cần thêm tests (nhiều fix-on-fix)
- 📐 **Architecture** — Coupling cần giải quyết 

## Output bắt buộc

```markdown
## 📊 Retro Report

### Period
[date range] | [X commits] | [Y files changed] | [Z contributors]

### Health Scores
| Dimension | Score | Trend |
|---|---|---|
| Commit hygiene | X/10 | ⬆️/⬇️/➡️ |
| Code stability | X/10 | ⬆️/⬇️/➡️ |
| Velocity | X/10 | ⬆️/⬇️/➡️ |
| Architecture | X/10 | ⬆️/⬇️/➡️ |
| **Overall** | **X/10** | ⬆️/⬇️/➡️ |

### 🔥 Hot Spots (top 5 churn files)
| File | Changes | Churn | Note |
|---|---|---|---|
| [file] | [count] | [lines] | [concern?] |

### 💡 Key Insights
1. [insight with evidence]
2. [insight with evidence]
3. [insight with evidence]

### 🔧 Action Items
| Priority | Category | Action | Target |
|---|---|---|---|
| 🔴 High | [category] | [specific action] | [file/module] |
| 🟡 Medium | [category] | [specific action] | [file/module] |
| ℹ️ Low | [category] | [specific action] | [file/module] |

### 📈 Recommendations for Next Sprint
- [recommendation 1]
- [recommendation 2]
- [recommendation 3]
```

## Guardrails

- `/sk-retro` KHÔNG sửa code — chỉ analysis + recommendations
- Health scores phải dựa trên data — không subjective
- Insights phải có evidence (git data) — không speculation
- Action items phải specific + actionable — không generic advice
- `--team` mode: data-driven, KHÔNG blame individuals — focus improvement
- Nếu git history quá ngắn (<5 commits) → cảnh báo insufficient data
- Trend (⬆️/⬇️/➡️) chỉ hiện khi có data period trước để so sánh
