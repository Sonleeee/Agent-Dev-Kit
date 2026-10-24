---
name: adk-trace-capture
description: Ghi structured execution traces khi người dùng hoặc cấu hình ADK bật trace capture. Ghi sự kiện và skill thực sự đã dùng; không chạy ngầm sau mọi bước hoặc suy diễn từ commit.
---

# adk-trace-capture — Ghi execution traces có evidence

## Tổng quan

Chỉ ghi trace khi người dùng hoặc cấu hình ADK đã bật cơ chế này. Capture là
best-effort: không tạo record cho từng hành động nhỏ và không làm chậm task.
Task ngắn có thể chỉ cần metadata commit; chỉ ghi workflow/skill khi thực sự được
dùng trong phiên.

## Protocol — Khi nào ghi gì

### 1. Bắt đầu trace khi capture đã bật

```
python evolution_db.py log_session '{
  "id": "<session-id>",
  "project": "<tên project từ AGENTS.md>",
  "user_intent": "<nguyên văn yêu cầu user>",
  "workflow_used": "<command thực sự được gọi, hoặc null nếu không dùng workflow>"
}'
```

**Quy tắc tạo ID:**
- session-id: `sess-YYYY-MM-DD-NNN` (NNN tăng dần trong ngày)
- trace-id: `trace-YYYY-MM-DD-NNN`

### 2. Ghi bước có ý nghĩa

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

Chỉ ghi bước lớn có ý nghĩa, retry, user correction hoặc handoff. Không tạo phase
giả nếu task đi thẳng từ yêu cầu sang implement. Ghi gọn, không ghi raw output.

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
| `skill_gap` | Không có skill phù hợp | Cần deploy nhưng không có adk-deploy |
| `unclear_instruction` | Đọc SKILL.md nhưng không rõ bước | "Bước 3 nói 'verify API' nhưng không nói verify cái gì" |
| `wrong_tool` | Chọn sai tool | Dùng web search thay vì đọc local docs |
| `missing_context` | Thiếu info trong architecture.md | "PageInfo type không được document" |
| `user_correction` | User sửa agent | "Không, dùng cursor-based, không dùng offset" |
| `rule_violation` | Vi phạm rule rồi tự phát hiện hoặc bị sửa | "Quên chạy build verification" |
| `tool_error` | Tool lỗi (không phải agent sai) | "MCP server timeout" |

### 4. Khi skill thực sự được dùng → ghi skill usage

```
python evolution_db.py log_skill_use '{
  "trace_id": "<trace-id>",
  "skill_name": "adk-execution-contract",
  "outcome": "success|partial|failed"
}'
```

Không suy ra skill usage từ tên folder/file trong diff hoặc từ commit prefix.

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
4. **Không blocking:** Nếu DB không available, tiếp tục task bình thường.
   Trace capture là best-effort, không được block delivery flow.
5. **Không bịa metrics:** Không ghi `SUCCESS`, turns, tokens, workflow, skills hoặc
   friction như dữ liệu quan sát nếu chỉ có metadata commit. Với commit-only record,
   dùng outcome không khẳng định task đã xong, để turns/tokens bằng 0, workflow null
   và không thêm skill usage.

## Kiểm tra database

```bash
# Xem health tổng thể
python evolution_db.py health

# Search traces liên quan
python evolution_db.py search '{"table": "traces", "query": "pagination API"}'

# Query tùy ý
python evolution_db.py query '{"sql": "SELECT * FROM v_skill_health"}'
```

## Quan hệ với Execution Contract

Trace capture độc lập với `adk-execution-contract`. Khi được bật, ghi session, bước
lớn, friction có thật và outcome có evidence. Không bắt buộc contract/ledger và
không ghi trace tự động chỉ vì skill đã được nạp.
