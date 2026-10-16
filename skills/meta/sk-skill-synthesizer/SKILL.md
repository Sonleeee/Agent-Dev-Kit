---
name: sk-skill-synthesizer
description: |
  Phân tích execution traces thành công để phát hiện reusable procedures,
  tự động sinh SKILL.md draft cho patterns mới. Lấy cảm hứng từ
  Hermes Agent autonomous skill creation.
triggers:
  - Sau /wf-delivery hoặc /wf-fix hoàn thành SUCCESS với complexity ≥ Medium
  - Manual: /wf-evolve --synthesize
  - Auto-trigger khi Phase G active
requires:
  - tools/evolution_db.py (Phase A)
  - Đủ traces trong evolution.db
phase: B (Skill Synthesis — Core)
---

# sk-skill-synthesizer — Tự Tạo Skills Từ Traces

## Tổng quan

Sau mỗi task phức tạp thành công, skill này kiểm tra: "Chuỗi bước vừa thực
hiện có thể trở thành skill tái sử dụng không?" Nếu có → sinh SKILL.md draft
→ trình user approve.

## Điều kiện kích hoạt

Chạy check sau mỗi task khi **tất cả** điều kiện thỏa:

1. `outcome = 'SUCCESS'`
2. `complexity IN ('Medium', 'High')`
3. `duration_turns >= 8`
4. Chưa có skill tương tự trong registry

### Query kiểm tra

```sql
SELECT t.id, t.task_description, t.duration_turns,
       COUNT(ts.id) as step_count
FROM traces t
JOIN trace_steps ts ON ts.trace_id = t.id
WHERE t.outcome = 'SUCCESS'
  AND t.complexity IN ('Medium', 'High')
  AND t.duration_turns >= 8
  AND t.created_at >= date('now', '-7 days')
  AND NOT EXISTS (
    SELECT 1 FROM patterns p
    WHERE p.pattern_type = 'reusable_procedure'
      AND p.status IN ('active', 'evolved')
      AND p.description LIKE '%' || substr(t.task_description, 1, 30) || '%'
  )
ORDER BY t.created_at DESC;
```

## Quy trình synthesis

### Step 1: Thu thập trace data

Lấy toàn bộ trace steps + friction points của task candidate:

```sql
SELECT ts.step_order, ts.step_type, ts.description,
       ts.outcome, ts.friction_note, ts.tool_used
FROM trace_steps ts
WHERE ts.trace_id = '<candidate-trace-id>'
ORDER BY ts.step_order;
```

### Step 2: Phân tích reusability

Đánh giá trace theo 4 tiêu chí:

| Tiêu chí | Câu hỏi | Threshold |
|----------|---------|-----------|
| **Generality** | Procedure này áp dụng được cho task khác không? | ≥ 2 task types |
| **Completeness** | Có đủ steps từ input → output không? | ≥ 3 meaningful steps |
| **Independence** | Có phụ thuộc vào project-specific context không? | ≤ 2 project-specific refs |
| **Distinctiveness** | Khác biệt đáng kể so với skills hiện có? | Overlap ≤ 30% |

Nếu ≥3/4 tiêu chí thỏa → tiến hành synthesis.

### Step 3: Sinh SKILL.md draft

Dựa trên trace steps, tạo skill file theo template chuẩn ADK:

```markdown
---
name: sk-{generated-name}
description: |
  {Mô tả ngắn 1-2 câu dựa trên task_description}
triggers:
  - {Khi nào nên dùng skill này}
synthesized_from: {trace-id}
synthesis_confidence: {0.0-1.0}
synthesis_date: {ISO8601}
---

# sk-{name} — {Title}

## Khi nào dùng

{Điều kiện kích hoạt, lấy từ phân tích generality}

## Prerequisites

{Các yêu cầu tiên quyết, trích từ trace steps đầu}

## Steps

### 1. {Tên bước}
{Mô tả — tinh gọn từ trace step, bỏ chi tiết project-specific}

### 2. {Tên bước}
...

## Verification

- [ ] {Acceptance criteria trích từ trace evidence}

## Ghi chú

- Skill này được tự động sinh từ trace `{trace-id}`
- Confidence: {score} — cần user review và refine
- Sau {N} lần sử dụng, GEPA-Lite sẽ tối ưu nếu cần
```

### Step 4: Similarity check

Trước khi trình user, so sánh draft với skills hiện có:

```sql
-- Tìm skills có thể trùng
SELECT s.name, s.skill_group
FROM skills s
WHERE s.name IN (
  -- Fuzzy match dựa trên keywords trong description
  SELECT skill_name FROM skills_used su
  JOIN traces t ON su.trace_id = t.id
  WHERE t.task_description LIKE '%webhook%'
     OR t.task_description LIKE '%deploy%'
);
```

Nếu overlap > 30% → đề xuất **mở rộng skill hiện có** thay vì tạo mới.

### Step 5: Trình user

```markdown
## 💡 Skill Synthesis Proposal

**Từ task:** "{task_description}"
**Trace:** {trace-id} ({N} steps, {M} turns)
**Confidence:** {score}

### Skill đề xuất: `sk-{name}`
{Preview 3 dòng đầu description}

**Đặt trong:** skills/{group}/sk-{name}/SKILL.md

[Approve] [Edit trước] [Reject] [Reject + lý do]
```

### Step 6: Commit & register

Nếu user approve:

1. Ghi SKILL.md vào `skills/{group}/sk-{name}/SKILL.md`
2. Register vào DB:
   ```sql
   INSERT INTO skills (name, skill_group, current_version)
   VALUES ('sk-{name}', '{group}', '1.0');
   
   INSERT INTO skill_versions (skill_name, version, change_reason, change_description)
   VALUES ('sk-{name}', '1.0', 'synthesis',
           'Auto-synthesized from trace {trace-id}');
   
   INSERT INTO patterns (pattern_type, description, status)
   VALUES ('reusable_procedure', '{task_description}', 'active');
   ```
3. Log synthesis event:
   ```sql
   INSERT INTO evolution_runs (target_type, target_name, trigger, strategy, outcome)
   VALUES ('skill', 'sk-{name}', 'auto', 'synthesize', 'upgraded');
   ```

### Step 7: Post-synthesis tracking

Sau khi skill được tạo, theo dõi qua `sk-trace-capture`:
- Đếm times_used, times_succeeded, times_failed
- Khi times_used >= 5 → kích hoạt Phase D (GEPA-Lite) để tối ưu

## Ví dụ cụ thể

### Input: Trace của task "Set up Stripe webhook với idempotency"

```
Trace: trace-2026-10-15-003 (12 steps, 18 turns, SUCCESS)
Steps:
  1. clarify: Xác nhận webhook events cần handle
  2. plan:    3 files — controller, idempotency service, test
  3. impl:    Tạo webhook endpoint route
  4. impl:    Verify Stripe signature
  5. impl:    Parse event types (checkout, invoice, ...)
  6. impl:    Tạo idempotency table + migration
  7. impl:    Check duplicate event ID trước khi process
  8. impl:    Retry logic với exponential backoff
  9. impl:    Dead letter queue cho failed events
  10. test:   Integration test với Stripe test events
  11. impl:   Monitoring + alerting
  12. review: Pass Gate 3
```

### Output: Draft `skills/devops/sk-webhook-resilient/SKILL.md`

```markdown
---
name: sk-webhook-resilient
description: |
  Thiết lập webhook endpoint với signature verification, idempotency,
  retry + exponential backoff, và dead letter queue.
triggers:
  - Tạo webhook endpoint cho payment/notification provider
  - Tích hợp third-party webhook (Stripe, PayPal, Twilio, ...)
synthesized_from: trace-2026-10-15-003
synthesis_confidence: 0.88
---

# sk-webhook-resilient — Resilient Webhook Setup

## Khi nào dùng
Khi cần tạo webhook endpoint nhận events từ external provider,
yêu cầu reliability cao (không miss events, không process duplicate).

## Prerequisites
- Database access (cho idempotency table)
- Provider SDK hoặc API docs

## Steps

### 1. Xác định events cần handle
Liệt kê webhook event types cần process.
Xác nhận với user: events nào critical vs nice-to-have.

### 2. Tạo endpoint + signature verification
Route POST nhận webhook. Verify signature/HMAC từ provider
để chống request giả mạo.

### 3. Idempotency layer
Tạo bảng `webhook_events(event_id UNIQUE, status, processed_at)`.
Trước khi process, check event_id đã tồn tại chưa.

### 4. Event processing logic
Implement handler cho từng event type.
Wrap trong transaction nếu có side effects.

### 5. Retry + exponential backoff
Nếu processing fail → queue retry.
Backoff: 1s, 5s, 30s, 5m, 30m. Max 5 retries.

### 6. Dead letter queue
Events fail hết retry → đưa vào DLQ.
Alert team để investigate thủ công.

### 7. Monitoring & alerting
Log mỗi event nhận/process/fail.
Alert khi DLQ size > threshold.

## Verification
- [ ] Endpoint responds 200 cho valid webhook
- [ ] Rejects invalid signature
- [ ] Duplicate events không process lại
- [ ] Failed events retry đúng schedule
- [ ] DLQ captures failed events
- [ ] Integration test pass
```

## Xử lý rejection

Nếu user reject proposal, ghi lý do:

```sql
INSERT INTO evolution_runs (target_type, target_name, trigger, strategy, outcome)
VALUES ('skill', 'sk-{proposed-name}', 'auto', 'synthesize', 'rejected');
```

Lý do rejection được dùng cho Phase H (Meta-Evolution) để cải thiện
synthesis strategy: "User reject 60% proposals vì quá generic"
→ nâng threshold confidence lên 0.9.
