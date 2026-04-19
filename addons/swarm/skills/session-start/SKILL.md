---
name: session-start
description: |
  Khởi động session với pipeline cố định clarify -> plan -> impl -> review.
  Gọi 1 lần đầu session. AI tự quản lý stage và tự chuyển khi user chốt.
  Không bỏ qua stage nào, không code khi chưa qua Gate 1.
context-required: optional
output: session-pipeline
---

# Session Start — Pipeline Lock

<HARD-GATE>
Skill này bắt buộc được invoke TRƯỚC KHI làm bất kỳ điều gì trong session.
Sau khi invoke, AI phải duy trì pipeline state cho toàn bộ session — không reset, không bỏ stage.
</HARD-GATE>

## PIPELINE BẮT BUỘC

Khi skill này được activate, AI **PHẢI** commit vào pipeline sau cho **toàn bộ session**:

```
CLARIFY  →  PLAN  →  IMPL  →  REVIEW
```

**Không có ngoại lệ. Không bỏ stage. Không code khi chưa qua Gate 1.**

---

## Hiển thị trạng thái

Ở **đầu mỗi response** trong session, hiển thị dòng trạng thái:

```
[SESSION] Stage: <STAGE_HIỆN_TẠI> | Gate 1: ✅/⏳ | Gate 2: ✅/⏳ | Gate 3: ✅/⏳
```

Ví dụ:
```
[SESSION] Stage: CLARIFY | Gate 1: ⏳ | Gate 2: ⏳ | Gate 3: ⏳
[SESSION] Stage: PLAN    | Gate 1: ✅ | Gate 2: ⏳ | Gate 3: ⏳
[SESSION] Stage: IMPL    | Gate 1: ✅ | Gate 2: ⏳ | Gate 3: ⏳
[SESSION] Stage: REVIEW  | Gate 1: ✅ | Gate 2: ✅ | Gate 3: ⏳
```

---

## Tín hiệu chuyển stage

### AI tự chuyển khi user chốt

| User nói | AI làm |
|---|---|
| "chốt", "ok rồi", "đủ rồi", "sang plan" | CLARIFY → PLAN (nếu checklist CLARIFY pass) |
| "chốt plan", "ok impl", "code đi", "làm đi" | PLAN → IMPL (nếu Gate 1 pass) |
| "xong", "done", "review đi", "chốt impl" | IMPL → REVIEW (nếu Gate 2 pass) |

### User gọi lệnh thủ công

| Lệnh | Hành động |
|---|---|
| `/clarify` | Quay lại CLARIFY bất cứ lúc nào — không cần gate |
| `/plan` | Chuyển sang PLAN (kiểm tra Gate 1, báo nếu fail) |
| `/impl` | Chuyển sang IMPL (kiểm tra Gate 2, báo nếu fail) |
| `/review` | Chuyển sang REVIEW |
| `/status` | Hiển thị trạng thái stage và gate hiện tại |

---

## Rules từng stage

### Stage: CLARIFY

**Có thể lặp lại nhiều lần. Có thể quay lại bất cứ lúc nào.**

Mục tiêu: làm rõ bài toán — không thiết kế, không code.

Skill gọi bên trong: `core/business-discovery`

Checklist cần pass trước khi sang PLAN:
- [ ] Problem statement rõ
- [ ] Scope in/out xác định
- [ ] Risks và edge cases chính
- [ ] Open questions / assumptions đã note
- [ ] Root cause layer (nếu là Bugfix)
- [ ] `API contract changed: Yes / No / Unknown`

<HARD-GATE>
KHÔNG chốt design chi tiết trong stage này.
KHÔNG generate code hay task breakdown dài.
KHÔNG tự chuyển sang PLAN khi checklist chưa pass — hỏi thêm.
</HARD-GATE>

---

### Stage: PLAN

**Gate 1** — Không sang IMPL nếu thiếu bất kỳ item nào dưới đây.

Mục tiêu: chốt approach và ràng buộc implement.

Skill gọi bên trong: `core/solution-planning`, `core/api-contract-guard` (nếu API đổi)

Output bắt buộc:
- [ ] Chosen approach
- [ ] Impacted modules / files
- [ ] Template nào sẽ dùng (từ `.agents/context/templates/`)
- [ ] Test obligations
- [ ] Pre-Implementation Quality Card ngắn
- [ ] `API contract: No change / Change with guard`

<HARD-GATE>
KHÔNG code trong stage này.
KHÔNG sang IMPL khi Gate 1 chưa pass — giải thích item còn thiếu và yêu cầu bổ sung.
Nếu Gate 1 fail → ở lại PLAN hoặc đề nghị quay lại CLARIFY.
</HARD-GATE>

---

### Stage: IMPL

**Gate 2** — Không sang REVIEW nếu:

Mục tiêu: code đúng kiến trúc, đúng pattern, đúng template của project.

Skill gọi bên trong: `domain/backend/new-feature`, `domain/backend/fixbug`, `domain/frontend/new-feature`, `domain/frontend/fixbug` (tuỳ scope)

Quy trình:
1. Đọc `AGENTS.md`, `architecture.md`, và `context/templates/` trước khi code
2. Code theo pattern chuẩn của project
3. Self-check theo quality card từ PLAN
4. Output impl-summary

Output bắt buộc:
- [ ] Danh sách thay đổi đã implement
- [ ] Self-check pass theo quality card
- [ ] `API contract: OK / Risk`

<HARD-GATE>
KHÔNG review trong stage này — review là stage tiếp theo.
KHÔNG sang REVIEW khi Gate 2 chưa pass.
KHÔNG để 2 agent cùng sửa cùng một bounded task.
</HARD-GATE>

---

### Stage: REVIEW

**Gate 3** — Không kết luận Ready nếu còn finding Critical.

Mục tiêu: fresh-eyes review sau implement.

Skill gọi bên trong: `orchestration/review-workflow`

Quy trình bên trong review:
1. Architecture review (BE và/hoặc FE tuỳ scope)
2. Regression checklist
3. API contract guard (nếu API đổi)
4. Tổng hợp findings: Critical → Major → Minor

<HARD-GATE>
KHÔNG implement code trong stage này.
KHÔNG kết luận Ship Ready khi còn Critical.
Nếu có Critical → yêu cầu quay lại IMPL để fix.
</HARD-GATE>

---

## Khởi động

Khi skill được invoke lần đầu, AI thực hiện ngay:

1. **Xác nhận pipeline đã lock** — hiển thị dòng trạng thái đầu tiên:
   ```
   [SESSION] Stage: CLARIFY | Gate 1: ⏳ | Gate 2: ⏳ | Gate 3: ⏳
   ```

2. **Thu thập thông tin khởi động** — hỏi tuần tự từng câu:
   - Task summary: bạn muốn làm gì?
   - Task type: `Feature` / `Bugfix` / `Enhancement`?
   - Scope: `BE` / `FE` / `BE+FE`?

3. **Bắt đầu CLARIFY** — dẫn dắt user qua checklist clarify bằng cách hỏi từng câu một, không hỏi nhiều câu cùng lúc.

---

## Guardrails toàn session

- **KHÔNG** bỏ qua stage dù task nhỏ hay rõ ràng
- **KHÔNG** code ở stage CLARIFY hoặc PLAN
- **KHÔNG** để user skip IMPL khi Gate 1 chưa pass — giải thích lý do
- **KHÔNG** review trong IMPL
- Nếu user hỏi câu hỏi ngoài pipeline → trả lời bình thường, nhưng nhắc lại stage hiện tại ở đầu response
- Nếu user muốn quay lại stage cũ → cho phép, không cần gate

---

## Red Flags — dừng ngay khi thấy

| Nghĩ | Thực tế |
|---|---|
| "Task này nhỏ, skip clarify được" | Không bỏ stage dù task nhỏ |
| "Plan đã rõ, code luôn" | Gate 1 phải pass trước |
| "Tôi biết cách làm rồi" | Vẫn phải qua đủ checklist |
| "User đã hiểu, không cần clarify nữa" | User chốt mới chuyển, không AI tự quyết |
