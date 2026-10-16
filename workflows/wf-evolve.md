---
name: wf-evolve
description: |
  Workflow phân tích execution traces tích lũy, phát hiện friction patterns
  và đề xuất cải tiến cho skills, workflows, rules.
  Có thể chạy manual hoặc auto-trigger (Phase G).
modifiers:
  --focus: skills|workflows|rules|all (default: all)
  --period: 7d|30d|90d (default: 30d)
  --synthesize: Chỉ chạy skill synthesis (Phase B)
  --optimize: Chỉ chạy GEPA-Lite optimization (Phase D/E/F)
  --dry-run: Chỉ phân tích, không đề xuất changes
requires:
  - tools/evolution_db.py
  - Đủ traces trong evolution.db (recommend ≥10 traces)
phase: C (Evolution Workflow — Core)
---

# /wf-evolve — Evolution Analysis & Optimization

## Khi nào dùng

| Trigger | Mô tả |
|---------|-------|
| Manual | User gõ `/wf-evolve` hoặc `/wf-evolve --focus skills --period 30d` |
| Auto (Phase G) | Hệ thống tự kích hoạt khi đủ traces hoặc friction spike |
| Scheduled | Cron hàng tuần/tháng (cấu hình trong config/evolution.toml) |

## Step 1: Data Collection

### 1.1 Thống kê tổng quan

```sql
-- Tổng quan hoạt động trong period
SELECT
  COUNT(DISTINCT s.id) as total_sessions,
  COUNT(DISTINCT t.id) as total_traces,
  ROUND(AVG(t.duration_turns), 1) as avg_turns,
  ROUND(AVG(t.tokens_used)) as avg_tokens,
  ROUND(CAST(SUM(CASE WHEN t.outcome='SUCCESS' THEN 1 ELSE 0 END) AS REAL)
    / COUNT(*) * 100, 1) as success_rate_pct,
  COUNT(DISTINCT fp.id) as total_friction_points
FROM sessions s
JOIN traces t ON t.session_id = s.id
LEFT JOIN friction_points fp ON fp.trace_id = t.id
WHERE t.created_at >= date('now', '-{period}');
```

### 1.2 Friction breakdown

```sql
-- Top friction categories
SELECT
  fp.category,
  COUNT(*) as count,
  ROUND(CAST(COUNT(*) AS REAL) /
    (SELECT COUNT(*) FROM friction_points fp2
     JOIN traces t2 ON fp2.trace_id = t2.id
     WHERE t2.created_at >= date('now', '-{period}')) * 100, 1) as pct
FROM friction_points fp
JOIN traces t ON fp.trace_id = t.id
WHERE t.created_at >= date('now', '-{period}')
GROUP BY fp.category
ORDER BY count DESC;
```

### 1.3 Skill health

```sql
SELECT * FROM v_skill_health
WHERE times_used > 0
ORDER BY
  CASE health_status
    WHEN 'critical' THEN 1
    WHEN 'warning' THEN 2
    ELSE 3
  END,
  success_rate ASC;
```

## Step 2: Health Dashboard

Tổng hợp data thành dashboard markdown:

```markdown
## 📊 Evolution Health Dashboard
**Period:** {start_date} → {end_date} | **Traces:** {N}

### Overview
| Metric | Value | Trend | Status |
|--------|-------|-------|--------|
| Total tasks | {N} | {↑↓→} | {✅⚠️🔴} |
| Success rate | {X}% | {↑↓→} | {✅⚠️🔴} |
| Avg turns/task | {N} | {↑↓→} | {✅⚠️🔴} |
| Avg tokens/task | {N} | {↑↓→} | {✅⚠️🔴} |
| Total friction | {N} | {↑↓→} | {✅⚠️🔴} |

### Skill Health
| Skill | Used | Success | Friction | Health |
|-------|------|---------|----------|--------|
| {name} | {N}x | {X}% | {N} pts | {✅⚠️🔴} |

### Top Friction Categories
| # | Category | Count | % | Most Affected |
|---|----------|-------|---|---------------|
| 1 | {cat} | {N} | {X}% | {skill/rule} |
```

**Status thresholds:**
- ✅ Success ≥ 90%, Friction ≤ 2/task, Turns ≤ previous avg
- ⚠️ Success 70-90%, Friction 2-5/task
- 🔴 Success < 70%, Friction > 5/task

## Step 3: Deep Analysis

Cho mỗi item có status ⚠️ hoặc 🔴, drill down:

### 3.1 Skill analysis

```sql
-- Chi tiết friction cho skill yếu
SELECT fp.description, fp.severity, fp.suggested_fix,
       t.task_description, ts.step_type, ts.description as step_desc
FROM friction_points fp
JOIN traces t ON fp.trace_id = t.id
LEFT JOIN trace_steps ts ON fp.step_id = ts.id
WHERE fp.related_skill = '{weak_skill}'
  AND t.created_at >= date('now', '-{period}')
ORDER BY fp.severity DESC, t.created_at DESC;
```

### 3.2 Pattern detection

```sql
-- Tìm friction patterns lặp lại
SELECT fp.description,
       COUNT(*) as occurrences,
       GROUP_CONCAT(DISTINCT fp.related_skill) as affected_skills,
       MIN(t.created_at) as first_seen,
       MAX(t.created_at) as last_seen
FROM friction_points fp
JOIN traces t ON fp.trace_id = t.id
WHERE t.created_at >= date('now', '-{period}')
GROUP BY fp.description
HAVING COUNT(*) >= 3
ORDER BY occurrences DESC;
```

### 3.3 Workflow bottleneck analysis

```sql
-- Steps nào hay fail/retry nhất?
SELECT ts.step_type, ts.outcome,
       COUNT(*) as count,
       ROUND(AVG(ts.tokens)) as avg_tokens
FROM trace_steps ts
JOIN traces t ON ts.trace_id = t.id
WHERE t.workflow = '{workflow}'
  AND t.created_at >= date('now', '-{period}')
GROUP BY ts.step_type, ts.outcome
ORDER BY ts.step_type, count DESC;
```

## Step 4: Generate Proposals

Dựa trên analysis, tạo proposals chia theo loại:

### 4.1 Skill proposals

| Action | Khi nào | Ưu tiên |
|--------|---------|---------|
| **Refine** | success_rate < 90% AND times_used ≥ 10 | HIGH nếu < 70% |
| **Synthesize** | Phát hiện reusable procedure chưa có skill | MEDIUM |
| **Deprecate** | times_used = 0 trong 90 ngày | LOW |
| **Merge** | 2 skills overlap > 50% | MEDIUM |

### 4.2 Workflow proposals

| Action | Khi nào | Ưu tiên |
|--------|---------|---------|
| **Add step** | Friction pattern lặp ≥ 5 lần → thiếu bước | HIGH |
| **Remove step** | Step bị skip > 50% | MEDIUM |
| **Reorder** | Step B thường retry sau A nhưng pass khi B trước A | MEDIUM |
| **Add condition** | Step chỉ cần thiết cho certain task types | LOW |

### 4.3 Rule proposals

| Action | Khi nào | Ưu tiên |
|--------|---------|---------|
| **Clarify** | rule_violation friction > 5 AND tasks vẫn succeed | HIGH |
| **Strengthen** | rule_violation friction AND tasks often fail | MEDIUM |
| **Relax** | PROTECTED rule nhưng luôn bị violate, tasks still succeed | LOW (trình user) |

## Step 5: Proposal Presentation

```markdown
## 🧬 Evolution Proposals ({period} analysis)

### Priority: HIGH

#### Proposal 1: Refine sk-api-contract-guard
- **Problem:** Success rate 65% (threshold 90%)
- **Root cause:** {phân tích từ friction_points}
- **Evidence:** {N} friction points across {M} tasks
- **Proposed action:** Chạy GEPA-Lite optimization (Phase D)
- **Expected impact:** +{X}% success rate

#### Proposal 2: New skill sk-db-migration
- **Problem:** 4 tasks cần migration nhưng không có skill
- **Evidence:** trace-015, trace-028, trace-041, trace-055
- **Proposed action:** Synthesize skill từ traces
- **Expected impact:** Reduce avg turns by {N} for migration tasks

### Priority: MEDIUM
...

### Priority: LOW
...

---
**Actions:** [Apply All HIGH] [Review One-by-One] [Dry Run Only] [Skip]
```

## Step 6: Apply Proposals

Khi user approve:

### Cho Refine proposals → delegate sang `sk-gepa-lite` (Phase D)
### Cho Synthesize proposals → delegate sang `sk-skill-synthesizer` (Phase B)
### Cho Workflow/Rule proposals → apply trực tiếp:

1. Đọc file hiện tại
2. Apply thay đổi đề xuất
3. Chạy validate (lint markdown, check cross-refs)
4. Commit với message: `evolution: {description}`
5. Log vào evolution_runs

## Step 7: Log Evolution Run

```sql
INSERT INTO evolution_runs
  (target_type, target_name, trigger, strategy, outcome)
VALUES
  ('{type}', '{name}', '{manual|auto}', '{strategy}', '{outcome}');
```

## Tích hợp với workflows hiện có

| Workflow | Hook point |
|----------|-----------|
| `/wf-delivery` | Sau Gate 3 PASS → check synthesis triggers |
| `/wf-fix` | Sau verify → check friction patterns |
| `/wf-review` | Design Evolution Candidate → log vào patterns |
| `/wf-retro` | Kết hợp git metrics + evolution data |

## Ví dụ output

User chạy `/wf-evolve --focus skills --period 30d`:

```
📊 Evolution Health Dashboard
Period: 2026-09-15 → 2026-10-15 | Traces: 47

Overview:
  Tasks: 47 (↑12 vs previous)
  Success rate: 82% (↓5%) ⚠️
  Avg turns: 18.3 (↑2.1) ⚠️
  Total friction: 31 points

Skill Health:
  🔴 sk-api-contract-guard    | 20x used | 60% success | 8 friction
  ⚠️ sk-regression-checklist  | 15x used | 73% success | 5 friction
  ⚠️ sk-docs-seeker           | 12x used | 75% success | 4 friction
  ✅ sk-execution-contract    | 47x used | 95% success | 2 friction
  ✅ sk-solution-planning     | 35x used | 91% success | 1 friction

Top Friction:
  1. unclear_instruction (12, 39%) → mostly sk-api-contract-guard
  2. missing_context (8, 26%) → architecture.md gaps
  3. wrong_tool (5, 16%) → sk-docs-seeker tool routing

Proposals:
  [HIGH] Refine sk-api-contract-guard → GEPA-Lite Phase D
  [HIGH] Enrich architecture.md with missing patterns
  [MED]  Fix sk-docs-seeker tool routing
  [MED]  Synthesize sk-db-migration from 4 traces
  [LOW]  Archive sk-docker-review (unused 90 days)

Apply? [All HIGH] [Review] [Skip]
```
