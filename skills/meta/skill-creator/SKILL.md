---
name: skill-creator
description: |
  Meta-skill để tạo mới skill hoặc onboard project vào global agent system.
  Dùng khi: tạo SKILL.md mới từ ý tưởng, onboard project mới vào registry,
  hoặc extract pattern từ codebase có sẵn thành context files.
  Trigger: "tạo skill", "onboard project", "tạo AGENTS.md", "extract pattern từ code".
context-required: false
output: new-skill-package | project-context-files
---

# Skill Creator (Meta)

## Mục Tiêu

Rút domain knowledge → tạo SKILL.md chuẩn + project context files.

---

## Bước 0 — Chọn Mode

Hỏi user ngay khi kích hoạt:

> **Bạn đang muốn:**
> **[1] Tạo skill mới từ ý tưởng** — chưa có codebase mẫu nào
> **[2] Onboard project có source** — đã có codebase, muốn extract pattern tự động

---

## MODE 1 — Tạo Skill Mới Từ Ý Tưởng

> Dùng khi: user có ý tưởng tự động hóa nhưng chưa có code mẫu nào.
> Inspired by: skill-generator pipeline (interview → detect → generate → dry-run).

### Phase 1 — Quick Check

Nếu user mô tả đủ rõ **(trigger + steps + rules + output format)** → nhảy thẳng Phase 3.
Nếu chưa rõ → bắt đầu phỏng vấn.

> **Ví dụ đủ rõ:** "Tạo skill review PR: đọc diff, check convention, liệt kê issues theo Critical/Major/Minor, trả markdown."
> **Ví dụ chưa rõ:** "Tạo skill kiểm tra code" → cần phỏng vấn.

### Phase 2 — Interview (tối đa 8 câu)

Hỏi tuần tự, dừng khi đã đủ thông tin:

1. Skill này dùng khi nào? (trigger / điều kiện kích hoạt)
2. Input là gì? (file, text, params...)
3. Output là gì? (format, structure, destination)
4. Các bước thực hiện theo thứ tự?
5. Rules / constraints quan trọng (không được làm gì, giới hạn gì)?
6. Edge cases cần xử lý?
7. Ví dụ thực tế 1 lần dùng? (input → output mẫu)
8. Platform nào? (Cursor / Claude / All) — Global hay project-specific?

### Phase 3 — Complexity Detection

Tính điểm để chọn output structure:

| Yếu tố | Điểm |
|---|---|
| Nhiều steps (>5) | +2 |
| Nhiều edge cases (>3) | +2 |
| Cần project context | +3 |
| Cần templates/examples | +2 |
| Multi-platform | +1 |
| Orchestration nhiều skill | +3 |

| Score | Output |
|---|---|
| 1–5 | Chỉ `SKILL.md` |
| 6–12 | `SKILL.md` + `templates/` |
| 13–20 | `SKILL.md` + `phases/` + `templates/` |
| 21+ | Full package: SKILL.md + phases/ + templates/ + examples/ |

### Phase 4 — Generate

**SKILL.md bắt buộc có:**

```yaml
---
name: [kebab-case]
description: |
  [Trigger rõ — viết "pushy", cover nhiều cách user hỏi]
  [Mô tả mục đích + khi nào dùng]
context-required: true/false/optional
output: [loại output]
---
```

**Sections bắt buộc:** Mục Tiêu, Quy trình (steps), Guardrails
**Sections tùy chọn:** Known Pitfalls, Examples, References

**7 Nguyên Tắc SKILL.md Tốt:**
1. **Atomic**: 1 skill = 1 việc. Tên có "và" → tách
2. **Trigger rõ**: description đủ để AI tự kích hoạt đúng lúc
3. **Steps cụ thể**: đủ để execute không cần hỏi thêm
4. **Examples > Rules**: 2–3 ví dụ tốt hơn 50 dòng quy tắc
5. **Guardrails thực tế**: từ pitfalls đã gặp, không lý thuyết
6. **Ngắn gọn**: SKILL.md < 150 dòng, dài hơn → tách phases/
7. **Context-aware**: khai báo rõ `context-required`

**15 Anti-Patterns cần tránh:**
- 🐙 **Octopus**: skill làm quá nhiều việc → tách
- 👻 **Ghost**: trigger quá mơ hồ → AI không tự kích hoạt được
- 🎪 **Circus**: quá nhiều options/branches → khó predict output
- 📜 **Scroll**: SKILL.md quá dài, AI đọc không hết → tách phases/
- 🔓 **Unlocked**: không có guardrails → AI làm sai ngoài scope

### Phase 5 — Dry Run

Mô phỏng 1–2 tình huống thực tế với skill vừa tạo.
Kiểm tra output có đúng mong muốn không. Điều chỉnh nếu cần.

### Phase 6 — Register

- Đặt vào folder đúng: `core/` / `orchestration/` / `domain/` / `meta/`
- Nếu project-specific: đặt vào `[project]/.agents/skills/`
- Ghi vào `CHANGELOG.md` global

---

## MODE 2 — Onboard Project Có Source

> Dùng khi: đã có codebase, muốn AI tự extract pattern → tạo context files.
> Output: `AGENTS.md` + `.agents/context/architecture.md` + templates.

### Phase 1 — Quick Scan

Hỏi user 5 câu để định hướng scan:

1. Project tên gì? Làm gì (1 câu)?
2. BE tech stack? (ngôn ngữ, framework, ORM...)
3. FE tech stack? (framework, UI lib, form lib...)
4. Module "chuẩn nhất" trong project? (dùng làm ground truth)
5. Có rule đặc thù nào AI cần biết không? (convention, pattern riêng)

### Phase 2 — Auto Extract (đọc codebase)

Đọc các file sau theo thứ tự:

**BE — đọc để extract:**
```
[module-chuẩn]/
├── Commands/[Create]/[Entity]Command.cs        ← command structure
├── Commands/[Create]/[Entity]CommandHandler.cs ← handler pattern
├── Commands/[Create]/[Entity]Validator.cs      ← validation pattern
├── Queries/[GetPaged]/[Entity]QueryHandler.cs  ← query/paged pattern
└── [Entity]Controller.cs                       ← controller pattern
```

Extract từ code thực tế:
- Flow layers (Controller → ? → Repository)
- Exception taxonomy đang dùng (NotFoundException, BusinessException...)
- Naming conventions (namespace, file, class)
- Error message pattern (centralized vs rải rác)
- Folder structure thực tế

**FE — đọc để extract:**
```
[module-chuẩn]/
├── list/index.tsx        ← list page pattern
├── manage/index.tsx      ← form/manage pattern
├── manage/schema.ts      ← validation schema pattern
└── [service].ts          ← API call pattern
```

Extract từ code thực tế:
- Component pattern (MainCard, DataTable, form components...)
- Service layer pattern (BaseService, endpoints...)
- Error handling pattern (response.errors vs response.message)
- i18n pattern (locales keys, useTranslate usage)
- Known pitfalls đang có trong code

### Phase 3 — Propose & Confirm

Trình bày những gì đã extract cho user xác nhận:

```
Tôi đã đọc [module-chuẩn] và extract được:

**BE Flow:** Controller → MediatR → Handler → Repository
**Error taxonomy:**
  - NotFoundException → 404 (tìm thấy X lần)
  - BusinessException → 400 (tìm thấy X lần)
  - [!] InvalidOperationException cho not-found (tìm thấy X lần — cần ghi chú)

**FE Pattern:**
  - Service: extends BaseService, trả response.errors (không phải .message)
  - Form: useFormResolver + Zod, isSubmitting sau form declaration
  - i18n: locales key, các component tự dịch không cần t()

**Cần xác nhận:**
- Module chuẩn BE là SalesContracts đúng không?
- Có rule nào chưa capture không?
```

User xác nhận → tiến hành Phase 4.

### Phase 4 — Generate Context Files

Tạo đầy đủ các file sau:

```
[project-root]/
├── AGENTS.md                               ← điền từ interview + scan
└── .agents/context/
    ├── architecture.md                     ← guardrails từ extracted patterns
    ├── checklist.md                        ← nếu project có checklist riêng
    ├── rule-overrides.approved.md          ← nếu có deviation từ global rules
    └── templates/
        ├── be/feature.md.template          ← code example thực từ module chuẩn
        └── fe/page.md.template             ← code example thực từ module chuẩn
```

**Yêu cầu chất lượng template:**
- `be/feature.md.template`: dùng code thực từ module chuẩn, không pseudo-code
- `fe/page.md.template`: bao gồm service, list page, manage page, schema, i18n
- Ghi rõ known pitfalls đã phát hiện trong Phase 2
- Anti-patterns (code sai đang có trong codebase) phải được documented

### Phase 5 — Register

- Thêm `project-type` vào `[global]/.agents/registry/index.md` nếu type mới
- Xác nhận `AGENTS.md` pointer đến đúng `context-required` theo registry

---

## Output Tổng Hợp

| Mode | Output tối thiểu | Output đầy đủ |
|---|---|---|
| **Mode 1** | `SKILL.md` | `SKILL.md` + `templates/` + `examples/` |
| **Mode 2** | `AGENTS.md` + `architecture.md` | Full context: architecture + templates + checklist + registry entry |

---

## Guardrails

- Không tạo skill quá generic ("làm tất cả mọi thứ") — tách nhỏ
- Không tự điền context mà user chưa cung cấp hoặc code chưa có
- SKILL.md > 150 dòng → refactor ra `phases/` hoặc `templates/`
- Mode 2: luôn dry-run propose trước khi ghi file — không ghi thẳng
- Mode 2: documented rõ deviations (code vi phạm pattern) để user quyết định fix hay ghi exception
