---
name: sk-delegation-validator
description: >
  Kiểm tra agent đã tuân thủ Delegation Policy chưa sau mỗi subtask trong /wf-impl.
  Tự động nhắc agent invoke subagent nếu phát hiện vi phạm.
trigger: model_decision
---

# Delegation Validator

## Activation Rule

Kích hoạt skill này khi:
- Agent đang trong `/wf-impl` và vừa hoàn thành một subtask
- Agent chuẩn bị báo Dev Done
- Cần kiểm tra delegation compliance

## Validation Checklist

Agent **PHẢI** tự kiểm tra các điều kiện sau trước khi tiếp tục:

### 1. Delegation Decision Check

```
Số subtasks trong plan: ___
Các subtasks có sửa CÙNG file không: Yes / No
→ Delegation required: Yes (≥2 độc lập) / No (1 task hoặc cùng file)
```

### 2. Nếu Delegation Required = Yes

- [ ] Đã gọi `invoke_subagent(TypeName="self", Workspace="branch")` cho mỗi subtask?
- [ ] Mỗi subagent chỉ nhận plan-lite + file scope (KHÔNG chat history)?
- [ ] Đã gọi reviewer subagent cho spec compliance review?
- [ ] Đã gọi reviewer subagent cho code quality review?

**Nếu BẤT KỲ checkbox nào = unchecked → DỪNG LẠI và thực hiện bước bị thiếu.**

### 3. Nếu Delegation Required = No

- [ ] Đã tự chạy spec compliance checklist?
- [ ] Đã tự chạy code quality checklist?
- [ ] Kết quả review được ghi vào ledger?

## Output

Ghi kết quả validation vào execution contract:

```markdown
## Delegation Validation
- delegation_required: true/false
- subtasks_delegated: [list]
- spec_review: PASS/FAIL
- quality_review: PASS/FAIL
- violations: [list or "none"]
```

## Guardrails

- Skill này KHÔNG thay thế review — chỉ kiểm tra quy trình delegation
- Nếu phát hiện violation, agent PHẢI sửa trước khi tiếp tục
- Không skip validation khi dùng modifier `--fast` (chỉ rút gọn, không bỏ)
