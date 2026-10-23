---
name: sk-skill-creator
description: |
  Tạo hoặc cập nhật Agent Skill theo chuẩn portable, hoặc onboard project khi được yêu cầu.
  Dùng khi: tạo SKILL.md mới từ ý tưởng, onboard project mới vào registry,
  hoặc extract pattern từ codebase thành context files.
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
8. Host nào cần hỗ trợ? (Antigravity, Codex hoặc cả hai) — global hay project-specific?

Chỉ hỏi những điều chưa thể suy ra an toàn từ yêu cầu hoặc repo; không bắt buộc đi
hết danh sách nếu đã đủ thông tin để tạo artifact đúng scope.

### Phase 3 — Chọn kích thước nhỏ nhất

Mặc định chỉ tạo SKILL.md. Thêm references, scripts, examples hoặc assets khi
chúng giúp dùng lại quy trình hoặc tránh nạp nội dung lớn vào mỗi lần kích hoạt.
Không tạo phases/package nhiều tầng chỉ vì skill có nhiều bước.

### Phase 4 — Generate

**SKILL.md dùng portable Agent Skills frontmatter:**

```yaml
---
name: [kebab-case]
description: [Mục đích và intent đủ rõ để agent biết khi nào nạp skill]
---
```

Không thêm top-level metadata riêng như triggers, context-required, inputs, output
hoặc phase. Đưa input, output và điều kiện dùng vào description hoặc body.

**Sections nên có:** Khi nào dùng, Quy trình (steps), Guardrails
**Sections tùy chọn:** Known Pitfalls, Examples, References

**7 Nguyên Tắc SKILL.md Tốt:**
1. **Atomic**: 1 skill = 1 việc. Tên có "và" → tách
2. **Trigger rõ**: description phân biệt skill này với các skill gần intent
3. **Steps cụ thể**: đủ để execute không cần hỏi thêm
4. **Examples > Rules**: 2–3 ví dụ tốt hơn 50 dòng quy tắc
5. **Guardrails thực tế**: từ pitfalls đã gặp, không lý thuyết
6. **Ngắn gọn**: chỉ tách reference/template/script khi chúng giúp giảm context nạp thường xuyên
7. **Context-aware**: nêu context cần đọc trong body, không dựa vào custom metadata

**15 Anti-Patterns cần tránh:**
- 🐙 **Octopus**: skill làm quá nhiều việc → tách
- 👻 **Ghost**: trigger quá mơ hồ → AI không tự kích hoạt được
- 🎪 **Circus**: quá nhiều options/branches → khó predict output
- 📜 **Scroll**: SKILL.md quá dài, AI đọc không hết → tách phases/
- 🔓 **Unlocked**: không có guardrails → AI làm sai ngoài scope

### Phase 5 — Dry Run

Rà lại trigger với một yêu cầu thuộc phạm vi và một yêu cầu gần giống nhưng
không thuộc phạm vi khi user yêu cầu eval hoặc skill ảnh hưởng rộng. Không bắt
buộc dựng benchmark cho mọi skill mới.

### Phase 6 — Register

- Đặt source vào category phù hợp: `core/`, `devops/`, `meta/`, `research/`, `security/`, `testing/` hoặc addon owner.
- Khi cài kit, export skill vào `.agents/skills/<skill-name>/`.
- Nếu project-specific: đặt vào `[project]/.agents/skills/`
- Ghi vào `CHANGELOG.md` global

---

## MODE 2 — Onboard Project Có Source

> Dùng khi: đã có codebase, muốn AI tự extract pattern → tạo context files.
> Output: `AGENTS.md` + `.agents/context/architecture.md` + templates.

### Phase 1 — Quick Scan

Đọc passport và các entrypoint của repo trước. Chỉ hỏi các thông tin quan trọng
mà không thể suy ra từ code/config; các chủ đề sau là gợi ý, không phải bộ câu hỏi bắt buộc:

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
- Giữ phần hướng dẫn thường dùng gọn; chuyển tài liệu dài sang references khi điều đó giảm context nạp mỗi lần.
- Mode 2: luôn dry-run propose trước khi ghi file — không ghi thẳng
- Mode 2: documented rõ deviations (code vi phạm pattern) để user quyết định fix hay ghi exception
