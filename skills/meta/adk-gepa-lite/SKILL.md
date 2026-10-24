---
name: adk-gepa-lite
description: Đề xuất và đánh giá có kiểm soát thay đổi cho skill, workflow hoặc rule khi maintainer yêu cầu. Dựa trên trace có evidence; không tự sửa file hoặc chạy sau mỗi task.
---

# adk-gepa-lite — Evolutionary Optimization Engine

## Tổng quan

GEPA-Lite là bản lightweight của GEPA (Genetic-Pareto Prompt Evolution):
- **GEPA gốc:** Cần DSPy + Python runtime + benchmark suite
- **GEPA-Lite:** Chạy thuần bằng agent instructions + LLM judgment

Nguyên lý giống nhau: **tạo nhiều biến thể → đánh giá → chọn tốt nhất**.
Khác biệt: evaluation bằng LLM-as-judge thay vì automated benchmarks.

## 5 Bước Của GEPA-Lite

```
READ → DIAGNOSE → MUTATE → EVALUATE → SELECT
```

---

## Step 1: READ — Đọc target và thu thập evidence

Chỉ tính trace có invocation evidence cho target. Loại commit metadata-only,
outcome PARTIAL/unknown và dữ liệu suy ra từ commit prefix/file path; success rate
hoặc friction aggregate chỉ là tín hiệu tìm kiếm, phải đối chiếu trace gốc trước
khi đưa ra kết luận.

### Input cần thu thập

1. **Target file:** Nội dung hiện tại của SKILL.md / workflow.md / rule section
2. **Usage traces:** Tất cả traces nơi target được sử dụng
3. **Friction points:** Friction liên quan đến target
4. **Success cases:** Traces thành công (để không phá vỡ cái đang tốt)

### Queries

```sql
-- Lấy tất cả traces dùng target skill
SELECT t.id, t.task_description, t.outcome, t.duration_turns,
       GROUP_CONCAT(ts.description, ' → ') as step_flow
FROM traces t
JOIN skills_used su ON su.trace_id = t.id
JOIN trace_steps ts ON ts.trace_id = t.id
WHERE su.skill_name = '{target_skill}'
ORDER BY t.created_at DESC
LIMIT 20;

-- Lấy friction points của target
SELECT fp.description, fp.category, fp.severity,
       fp.suggested_fix, ts.description as at_step
FROM friction_points fp
LEFT JOIN trace_steps ts ON fp.step_id = ts.id
WHERE fp.related_skill = '{target_skill}'
ORDER BY fp.severity DESC;
```

---

## Step 2: DIAGNOSE — Phân tích nguyên nhân gốc

Đọc friction points và traces, xác định **tại sao** target gây vấn đề.

### Phân loại root causes

| Root cause type | Dấu hiệu | Ví dụ |
|----------------|----------|-------|
| **Ambiguous step** | `unclear_instruction` friction ≥ 3 lần ở cùng step | "Step 3 nói 'verify API' nhưng không nói verify cái gì" |
| **Missing step** | `skill_gap` friction + agent phải improvise | "Không có bước check backward compatibility" |
| **Redundant step** | Step bị `skip` > 50% thời gian | "Step 2 'list all endpoints' bị skip khi chỉ sửa 1 endpoint" |
| **Wrong order** | Step B `retry` nhưng pass khi chạy trước A | "Check imports trước khi implement sẽ tránh retry" |
| **Too verbose** | Skill dùng nhiều tokens, output quá dài | "Skill instruction 500 tokens nhưng chỉ cần 200" |
| **Too terse** | `user_correction` vì agent hiểu sai | "Bước quá ngắn, agent diễn giải sai ý" |

### Output

```markdown
## Diagnosis Report: {target_name}

### Performance Summary
- Used: {N} times | Success: {X}% | Friction: {M} points

### Root Causes (ranked by impact)
1. **[Ambiguous]** Step 3 "Detect breaking changes" — 5/8 friction 
   points ở bước này. Agent không biết breaking change là gì cụ thể.
   
2. **[Missing]** Không có bước check enum value changes — 2 friction
   vì agent miss enum additions affecting consumers.
   
3. **[Too verbose]** Step 1 "List all API endpoints" — 7/10 lần bị
   skip vì task chỉ liên quan 1-2 endpoints.
```

---

## Step 3: MUTATE — Tạo biến thể

Dựa trên root causes, tạo **3-5 biến thể** (variants) bằng các mutation operators:

### Mutation operators

| Operator | Mô tả | Khi dùng |
|----------|--------|---------|
| `clarify` | Viết lại step rõ ràng hơn, thêm chi tiết | Root cause: Ambiguous |
| `add_example` | Thêm ví dụ Before/After vào step | Root cause: Ambiguous |
| `add_guard` | Thêm checkpoint/checklist vào step | Root cause: Missing |
| `remove_step` | Bỏ step không cần thiết | Root cause: Redundant |
| `merge_steps` | Gộp 2+ steps liên quan | Root cause: Redundant |
| `split_step` | Tách 1 step phức tạp thành sub-steps | Root cause: Ambiguous |
| `reorder` | Đổi thứ tự steps | Root cause: Wrong order |
| `simplify` | Rút gọn instruction | Root cause: Too verbose |
| `conditional` | Thêm điều kiện khi nào chạy step | Root cause: Redundant |

### Chiến thuật tạo variants

```
Variant A: Áp dụng 1 mutation cho root cause #1 (top priority)
Variant B: Áp dụng mutation khác cho root cause #1
Variant C: Áp dụng mutation cho root cause #2
Variant D: Kết hợp A + C (fix top 2 root causes)
Variant E: Kết hợp B + C (alternative combo)
```

### Constraints cho mutations

- **Size limit:** Variant không được dài hơn 150% original
- **Coverage:** Variant phải giữ nguyên mọi step đang hoạt động tốt
- **Format:** Phải tuân thủ SKILL.md / workflow template chuẩn ADK
- **No regression:** Không sửa step có success rate > 95%

### Ví dụ mutation

**Original step (adk-api-contract-guard, step 3):**
```markdown
### 3. Detect breaking changes
Kiểm tra xem thay đổi có phá vỡ API contract hiện tại không.
```

**Variant A (clarify + add_guard):**
```markdown
### 3. Detect breaking changes
Kiểm tra từng thay đổi API theo checklist:

- [ ] Field bị xóa? → BREAKING
- [ ] Field type thay đổi? → BREAKING
- [ ] Field optional → required? → BREAKING
- [ ] Required → optional? → SAFE (backward compatible)
- [ ] Field mới (optional)? → SAFE
- [ ] Enum value thêm? → CHECK consumers trước
- [ ] Enum value xóa? → BREAKING
- [ ] Response status code thay đổi? → BREAKING
- [ ] URL path thay đổi? → BREAKING

Nếu có bất kỳ BREAKING → flag và trình user trước khi tiếp tục.
```

**Variant B (split_step):**
```markdown
### 3a. Liệt kê tất cả thay đổi API
So sánh API signatures trước/sau. Ghi danh sách:
- Fields added/removed/changed
- Types changed
- Required/optional changed

### 3b. Phân loại từng thay đổi
Với mỗi thay đổi ở 3a, phân loại:
- BREAKING: consumers hiện tại sẽ bị lỗi
- SAFE: backward compatible
- REVIEW: cần xác nhận với user

### 3c. Quyết định
- Nếu có BREAKING → dừng, trình user
- Nếu chỉ SAFE → tiếp tục
- Nếu có REVIEW → hỏi user từng item
```

---

## Step 4: EVALUATE — Chấm điểm

Mỗi variant được đánh giá trên **4 trục**:

### 4.1 Clarity Score (0-100)

LLM-as-judge: "Đọc instruction này, một AI agent có hiểu chính xác
phải làm gì ở mỗi bước không? Có mơ hồ ở đâu không?"

Rubric:
- 90-100: Mọi bước crystal clear, không thể hiểu sai
- 70-89: Hầu hết rõ, 1-2 chỗ có thể hiểu khác nhau
- 50-69: Nhiều chỗ mơ hồ, agent phải đoán
- <50: Confusing, likely to produce wrong behavior

### 4.2 Completeness Score (0-100)

"Variant này cover được bao nhiêu % use cases phát hiện trong traces?"

```
Completeness = (số traces mà variant xử lý đúng) / (tổng traces) × 100
```

### 4.3 Conciseness Score (0-100)

"Variant có đủ gọn để không lãng phí tokens không?"

```
Token ratio = tokens(variant) / tokens(original)
Conciseness = max(0, 100 - (token_ratio - 1) × 100)
Bonus: +10 nếu variant loại bỏ redundancy rõ ràng
```

### 4.4 Trace Replay Score (0-100) — QUAN TRỌNG NHẤT

"Nếu agent dùng variant này thay vì bản gốc, friction cũ có tránh được không?"

**Quy trình:**
1. Lấy tất cả traces có friction liên quan
2. Với mỗi trace, hỏi LLM:
   ```
   Context: Agent đang làm task "{task_description}".
   Đến bước gây friction: "{friction_description}".
   
   Original instruction: {original_step}
   New instruction: {variant_step}
   
   Với instruction mới, agent có tránh được friction point này không?
   Trả lời: AVOIDED (agent sẽ làm đúng) / UNCLEAR / WORSE (tệ hơn)
   ```
3. Tính score:
   ```
   replay_score = (AVOIDED × 1 + UNCLEAR × 0 + WORSE × -1) / total × 100
   Normalize to 0-100 range
   ```

### 4.5 Overall Score

```
overall = clarity × 0.25 + completeness × 0.25 + 
          conciseness × 0.15 + trace_replay × 0.35
```

Trace Replay có weight cao nhất vì nó đo **thực tế có tốt hơn không**.

### Evaluation Matrix

```markdown
## Evaluation Results: {target_name}

|              | Clarity | Complete | Concise | Replay | OVERALL |
|--------------|---------|----------|---------|--------|---------|
| **Current**  |   70    |    75    |   80    |   60   | **70**  |
| **Var-A**    |   85    |    80    |   70    |   82   | **80**  |
| **Var-B**    |   90    |    85    |   60    |   80   | **80**  |
| **Var-C**    |   75    |    90    |   75    |   70   | **77**  |
| **Var-D**    |   88    |    90    |   65    |   88   | **84**  |
| **Var-E**    |   92    |    88    |   68    |   90   | **86**  ← BEST

Winner: Variant E (overall 86 vs current 70)
Improvement: +16 points (+23%)
```

---

## Step 5: SELECT — Chọn và áp dụng

### Decision rules

```
IF best_variant.overall > current.overall + 5:    # Phải tốt hơn ≥5 điểm
    AND best_variant.trace_replay > current.trace_replay:  # Replay phải tốt hơn
    AND best_variant.completeness >= current.completeness - 5:  # Không mất coverage
    → PROPOSE UPGRADE
ELSE:
    → KEEP CURRENT (log insights cho lần sau)
```

### Presentation

```markdown
## 🧬 GEPA-Lite Upgrade Proposal

### Target: adk-api-contract-guard v1.0 → v1.1

**Winner:** Variant E (score 86 vs current 70, +23%)
**Strategy:** clarify + add_guard (step 3)

### Changes:
{diff showing before/after}

### Evidence:
- Trace replay: 7/8 old friction points would be avoided
- Clarity: +22 points (step 3 no longer ambiguous)
- Trade-off: +15% longer (+30 tokens), justified by checklist

### Risk:
- LOW: Changes scoped to 1 step, no structural change
- All existing success cases still covered

[Approve] [View Full Diff] [Edit Before Apply] [Reject]
```

### Khi user approve

1. Update file content
2. Log vào DB:
```sql
INSERT INTO evolution_runs (target_type, target_name, trigger, strategy, 
    candidates_generated, candidates_evaluated, best_candidate_id, outcome)
VALUES ('skill', '{name}', '{trigger}', 'optimize', 
    5, 5, {best_id}, 'upgraded');

UPDATE skills SET current_version = '{new_ver}', last_evolved_at = datetime('now')
WHERE name = '{name}';

INSERT INTO skill_versions (skill_name, version, change_reason, change_description,
    performance_before)
VALUES ('{name}', '{new_ver}', 'gepa_evolution', '{description}',
    '{"success_rate": {old_rate}, "friction": {old_friction}}');
```

---

## Áp dụng cho Multi-Skill Chains (Phase E)

Tương tự Phase D nhưng target là quy trình phối hợp giữa các skills.

### Mutation operators bổ sung cho skill chains

| Operator | Mô tả |
|----------|--------|
| `add_guard` | Thêm verification gate hoặc guardrail |
| `gate_adjustment` | Điều chỉnh gate criteria |
| `shortcut_path` | Thêm fast-path cho task type phổ biến |

### Ví dụ

```sql
-- Steps hay bị skip trong một intent/quy trình
SELECT ts.step_type, 
       SUM(CASE WHEN ts.outcome='skip' THEN 1 ELSE 0 END) as skip_count,
       COUNT(*) as total,
       ROUND(CAST(SUM(CASE WHEN ts.outcome='skip' THEN 1 ELSE 0 END) AS REAL) 
         / COUNT(*) * 100) as skip_rate
FROM trace_steps ts
JOIN traces t ON ts.trace_id = t.id
WHERE t.task_description LIKE '%delivery%'
GROUP BY ts.step_type
HAVING skip_rate > 30;
```

**Kết quả:** `clarify` bị skip 40% → đề xuất thêm `--auto-clarify` modifier.

---

## Áp dụng cho Rules (Phase F)

Target: `rules/global.md`, `rules/backend.md`, `rules/frontend.md`.

### Đặc biệt: Tôn trọng [PROTECTED] rules

- Rules `[PROTECTED]` → **CHỈ `clarify` mutation** (viết rõ hơn, KHÔNG relax)
- Rules `[OVERRIDABLE]` → Mọi mutation đều cho phép

### Ví dụ

```sql
-- Rules hay bị violate
SELECT fp.related_rule, COUNT(*) as violations,
       AVG(CASE WHEN t.outcome='SUCCESS' THEN 1.0 ELSE 0.0 END) as success_with_violation
FROM friction_points fp
JOIN traces t ON fp.trace_id = t.id
WHERE fp.category = 'rule_violation'
GROUP BY fp.related_rule
HAVING violations >= 3;
```

**Kết quả:**
| Rule | Violations | Task Success |
|------|-----------|-------------|
| Minimal Change [PROTECTED] | 12 | 90% |
| Error Taxonomy [OVERRIDABLE] | 5 | 70% |

- Minimal Change: 12 violations nhưng 90% success → clarify rule (giải thích khi nào exempt)
- Error Taxonomy: 5 violations, 70% success → strengthen enforcement

---

## Gợi ý candidate khi được yêu cầu

Không cấu hình auto-trigger, cron hoặc check sau mỗi task. Khi maintainer yêu cầu
phân tích evolution, dùng các truy vấn dưới đây để tìm candidate; chỉ trình bày
đề xuất dựa trên trace có evidence và không tự sửa target.

```toml
[evolution.triggers]
# Ngưỡng lọc gợi ý; không tự kích hoạt action
trace_threshold = 20

# Chạy GEPA-Lite khi skill success rate drop dưới threshold
skill_degradation_threshold = 0.70

# Chạy khi có spike friction trong N ngày gần
friction_spike_window = "7d"
friction_spike_threshold = 5

# Không synthesize tự động
auto_synthesize = false
```

### Check candidate (chỉ khi maintainer yêu cầu)

```sql
-- Check 1: Đủ traces mới?
SELECT COUNT(*) FROM traces 
WHERE created_at > (SELECT MAX(created_at) FROM evolution_runs);

-- Check 2: Skill degraded?
SELECT name FROM skills 
WHERE success_rate < 0.70 AND times_used >= 10
  AND (last_evolved_at IS NULL OR last_evolved_at < date('now', '-14 days'));

-- Check 3: Friction spike?
SELECT COUNT(*) FROM friction_points fp
JOIN traces t ON fp.trace_id = t.id
WHERE t.created_at >= date('now', '-7 days') AND fp.severity = 'high';

-- Check 4: Synthesis candidate?
SELECT id FROM traces
WHERE outcome = 'SUCCESS' AND complexity IN ('Medium','High')
  AND duration_turns >= 8 AND created_at >= date('now', '-7 days');
```

---

## Phase H: Review evolution evidence

Phân tích hiệu quả của các thay đổi evolution chỉ khi maintainer yêu cầu. Kết quả
là đề xuất; không tự điều chỉnh strategy hoặc ghi config:

```sql
-- Evolution nào hiệu quả?
SELECT * FROM v_evolution_effectiveness;

-- Mutation types nào hay thành công?
SELECT ec.mutation_type,
       COUNT(*) as tried,
       SUM(CASE WHEN er.outcome = 'upgraded' THEN 1 ELSE 0 END) as succeeded
FROM evolution_candidates ec
JOIN evolution_runs er ON ec.run_id = er.id
WHERE ec.id = er.best_candidate_id OR er.best_candidate_id IS NULL
GROUP BY ec.mutation_type
ORDER BY succeeded DESC;
```

**Output:** Đề xuất thay đổi `preferred_mutations` hoặc `avoid_mutations` trong
config/evolution.toml, kèm evidence. Chỉ cập nhật file khi maintainer chọn rõ đề xuất.
