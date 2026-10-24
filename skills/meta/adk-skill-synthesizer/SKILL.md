---
name: adk-skill-synthesizer
description: Phân tích execution trace có evidence để đề xuất quy trình tái sử dụng và tạo bản nháp skill khi maintainer yêu cầu. Không tự chạy sau task hoặc commit; cần người duyệt trước khi thêm skill.
---

# adk-skill-synthesizer — Tự Tạo Skills Từ Traces

## Tổng quan

Chỉ chạy khi maintainer yêu cầu phân tích trace hoặc đề xuất skill. Trace/commit
đơn lẻ không đủ để kết luận có quy trình tái sử dụng; candidate cần evidence từ
nhiều task độc lập và người dùng duyệt draft trước khi thêm vào kit.

## Điều kiện kích hoạt

Xét candidate khi **tất cả** điều kiện sau có evidence:

1. `outcome = 'SUCCESS'`
2. `complexity IN ('Medium', 'High')`
3. `duration_turns >= 8`
4. Chưa có skill tương tự trong registry

Không xem commit metadata-only, outcome `PARTIAL`, workflow/skill suy đoán từ commit
prefix hoặc file path là bằng chứng task thành công hay procedure đã được dùng.
Nếu trace không ghi được cách task hoàn thành và kiểm chứng, loại nó khỏi candidate.

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
  AND CASE
        WHEN json_valid(t.acceptance_evidence)
        THEN json_extract(t.acceptance_evidence, '$.task_outcome_observed') = 1
        ELSE 0
      END
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
description: {Mô tả ngắn về intent và khi nào dùng skill này}
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

- Nguồn đề xuất: trace `{trace-id}` (ghi provenance trong body, không thêm metadata host-specific)
- Confidence: {score} — cần user review và refine
- Maintainer có thể yêu cầu GEPA-Lite đánh giá sau khi có thêm evidence sử dụng
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

Đặt trong source: `skills/{group}/sk-{name}/SKILL.md`. Installer export skill vào
`.agents/skills/sk-{name}/` để Antigravity và Codex tìm thấy.

[Approve] [Edit trước] [Reject] [Reject + lý do]
```

### Step 6: Add the approved draft

Nếu user approve:

1. Chỉ sau khi user duyệt draft, ghi SKILL.md vào `skills/{group}/sk-{name}/SKILL.md`.
2. Register vào DB chỉ khi maintainer yêu cầu hoặc trace logging đã được bật:
   ```sql
   INSERT INTO skills (name, skill_group, current_version)
   VALUES ('sk-{name}', '{group}', '1.0');
   
   INSERT INTO skill_versions (skill_name, version, change_reason, change_description)
   VALUES ('sk-{name}', '1.0', 'synthesis',
           'Reviewed synthesis from trace set {trace-ids}');
   
   INSERT INTO patterns (pattern_type, description, status)
   VALUES ('reusable_procedure', '{task_description}', 'active');
   ```
3. Log synthesis event:
   ```sql
   INSERT INTO evolution_runs (target_type, target_name, trigger, strategy, outcome)
    VALUES ('skill', 'sk-{name}', 'manual', 'synthesize', 'upgraded');
   ```

### Step 7: Post-synthesis tracking

Sau khi skill được tạo, nếu maintainer bật trace capture, theo dõi qua `adk-trace-capture`:
- Đếm times_used, times_succeeded, times_failed
- Khi có đủ evidence sử dụng → đề xuất GEPA-Lite để maintainer cân nhắc; không tự kích hoạt.

## Ví dụ cụ thể

Ví dụ dưới đây chỉ minh họa hình dạng artifact. Một trace Stripe đơn lẻ **không đủ**
evidence để kết luận đây là procedure dùng lại được; cần các task độc lập khác cho
thấy cách tiếp cận tương tự trước khi đề xuất draft.

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

### Output: Draft `skills/devops/adk-webhook-resilient/SKILL.md`

```markdown
---
name: adk-webhook-resilient
description: Thiết lập webhook endpoint với signature verification, idempotency, retry và dead letter queue cho integration cần reliability cao.
---

Đề xuất từ trace-2026-10-15-003; maintainer đã review và chốt nội dung.

# adk-webhook-resilient — Resilient Webhook Setup

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
VALUES ('skill', 'sk-{proposed-name}', 'manual', 'synthesize', 'rejected');
```

Chỉ ghi rejection nếu maintainer yêu cầu lưu feedback này; không tự cập nhật threshold
hoặc synthesis strategy từ một lần từ chối.
