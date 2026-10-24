---
name: adk-delegation-validator
description: Kiểm tra ranh giới, kết quả và bằng chứng của subtask khi task thực sự được delegate. Không kích hoạt hoặc yêu cầu delegate cho task chạy inline.
---

# Delegation Validator

## Activation Rule

Kích hoạt sau một subtask được delegate hoặc khi người dùng yêu cầu kiểm tra
quy trình delegation. Không kích hoạt chỉ vì task có nhiều bước hoặc nhiều file.

## Validation Checklist

Agent **PHẢI** tự kiểm tra các điều kiện sau trước khi tiếp tục:

### 1. Kiểm tra lý do delegate

```
Số subtasks trong plan: ___
Các subtasks có sửa CÙNG file không: Yes / No
→ Delegation chosen: Yes / No (số task không tự quyết định thay agent)
```

### 2. Nếu đã delegate

- [ ] Scope và output của subtask có rõ không?
- [ ] Kết quả có thay đổi nằm trong scope và evidence kiểm chứng phù hợp không?
- [ ] Các thay đổi có xung đột hoặc cần hợp nhất/review độc lập không?

Chỉ yêu cầu reviewer độc lập nếu user muốn hoặc rủi ro cần góc nhìn thứ hai.

### 3. Nếu task chạy inline

- Không yêu cầu tạo report delegation.
- Tiếp tục task bình thường và ghi evidence ở mức cần thiết.

## Output

Nếu task có execution contract, có thể ghi kết quả gọn:

```markdown
## Delegation Validation
- delegation_used: true/false
- subtasks_delegated: [list]
- verification: command/result hoặc chưa chạy
- violations: [list or "none"]
```

## Guardrails

- Skill này không thay thế review code.
- Không tạo handoff/review vòng lặp nếu lợi ích không vượt chi phí.
- Chỉ sửa finding có evidence và nằm trong scope; không chặn task vì thiếu nghi thức.
