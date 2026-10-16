---
name: sk-trace-capture
description: |
  Ghi lại structured execution traces vào SQLite (evolution.db) sau mỗi bước
  trong workflow. Là nền tảng cho toàn bộ self-evolution pipeline.
  Tích hợp vào sk-execution-contract như một protocol bổ sung.
triggers:
  - Tự động khi evolution system được kích hoạt
  - Chạy ngầm song song với mọi workflow
requires:
  - tools/evolution_db.py
  - SQLite 3.35+ với FTS5
phase: A (Trace Infrastructure — Core)
---

# sk-trace-capture — Ghi Execution Traces

## Tổng quan

Skill này **bổ sung** (không thay thế) vào `sk-execution-contract`. Khi được
kích hoạt, mọi task thay đổi đều ghi trace có cấu trúc vào `evolution.db`.

## Protocol — Khi nào ghi gì

### 1. Bắt đầu task → Tạo session + trace

```
python evolution_db.py log_session '{
  "id": "<session-id>",
  "project": "<tên project từ AGENTS.md>",
  "user_intent": "<nguyên văn yêu cầu user>",
  "workflow_used": "<wf-delivery|wf-fix|...>"
}'
```

**Quy tắc tạo ID:**
- session-id: `sess-YYYY-MM-DD-NNN` (NNN tăng dần trong ngày)
- trace-id: `trace-YYYY-MM-DD-NNN`

### 2. Sau mỗi phase → Ghi trace step

```
python evolution_db.py log_step '{
  "trace_id": "<trace-id>",
  "step_order": 1,
  "step_type": "clarify|plan|impl|review|fix|test|deploy|research|other",
  "description": "<mô tả ngắn bước vừa làm>",
  "tool_used": "<tool chính đã dùng>",
  "output_summary": "<kết quả tóm tắt>",
  "outcome": "pass|fail|skip|retry",
  "tokens": 1500
}'
```

**Ghi gọn, không ghi raw output.** Chỉ ghi 1-2 câu mô tả và kết quả.

### 3. Khi gặp friction → Ghi friction point

Friction = bất kỳ lúc nào agent:
- Phải retry một bước
- Nhận user correction
- Không tìm được context cần thiết
- Chọn sai tool
- Gặp instruction mơ hồ trong skill/workflow
- Vi phạm rule rồi phải sửa

```
python evolution_db.py log_friction '{
  "trace_id": "<trace-id>",
  "step_id": 3,
  "category": "skill_gap|unclear_instruction|wrong_tool|missing_context|user_correction|rule_violation|tool_error",
  "description": "<mô tả ngắn vấn đề gặp phải>",
  "severity": "low|medium|high",
  "related_skill": "<tên skill liên quan, nếu có>",
  "related_rule": "<tên rule liên quan, nếu có>",
  "suggested_fix": "<agent tự đề xuất cách fix>"
}'
```

**Phân loại category:**

| Category | Khi nào | Ví dụ |
|----------|---------|-------|
| `skill_gap` | Không có skill phù hợp | Cần deploy nhưng không có sk-deploy |
| `unclear_instruction` | Đọc SKILL.md nhưng không rõ bước | "Bước 3 nói 'verify API' nhưng không nói verify cái gì" |
| `wrong_tool` | Chọn sai tool | Dùng web search thay vì đọc local docs |
| `missing_context` | Thiếu info trong architecture.md | "PageInfo type không được document" |
| `user_correction` | User sửa agent | "Không, dùng cursor-based, không dùng offset" |
| `rule_violation` | Vi phạm rule rồi tự phát hiện hoặc bị sửa | "Quên chạy build verification" |
| `tool_error` | Tool lỗi (không phải agent sai) | "MCP server timeout" |

### 4. Khi dùng skill → Ghi skill usage

```
python evolution_db.py log_skill_use '{
  "trace_id": "<trace-id>",
  "skill_name": "sk-execution-contract",
  "outcome": "success|partial|failed"
}'
```

### 5. Kết thúc task → Cập nhật outcome

```
python evolution_db.py update_outcome '{
  "trace_id": "<trace-id>",
  "session_id": "<session-id>",
  "outcome": "SUCCESS|PARTIAL|FAILED",
  "summary": "<tóm tắt 1-2 câu task đã làm>",
  "total_turns": 23,
  "total_tokens": 15400
}'
```

## Nguyên tắc ghi trace

1. **Gọn gàng:** Mỗi step description ≤2 câu. Không dump raw output.
2. **Trung thực:** Ghi friction thật, không bỏ qua lỗi mình gây ra.
3. **Nhất quán:** Luôn dùng đúng category và severity.
4. **Không blocking:** Nếu DB không available, ghi warning và tiếp tục task.
   Trace capture là best-effort, không được block delivery flow.

## Kiểm tra database

```bash
# Xem health tổng thể
python evolution_db.py health

# Search traces liên quan
python evolution_db.py search '{"table": "traces", "query": "pagination API"}'

# Query tùy ý
python evolution_db.py query '{"sql": "SELECT * FROM v_skill_health"}'
```

## Tích hợp với Execution Contract

Skill này **bổ sung** vào `sk-execution-contract`, không thay thế.
Khi evolution system active:

1. Contract bootstrap → thêm bước `log_session`
2. Mỗi phase update ledger → thêm bước `log_step`
3. Mỗi retry/error → thêm bước `log_friction`
4. Task kết thúc → thêm bước `update_outcome`

Nếu evolution system không active, `sk-execution-contract` chạy bình thường
mà không ghi trace.
