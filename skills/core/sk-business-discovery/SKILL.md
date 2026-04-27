---
name: sk-business-discovery
description: |
  Lam ro yeu cau nghiep vu truoc khi lap plan hoac implement.
  Dung khi can chot problem statement, scope, risks, va open questions.
context-required: false
output: clarify-record
---

# Business Discovery

## Muc tieu

Bien mo ta mo ho -> clarify record ngan, du de lap plan ky thuat.

## Khong can project context

Skill nay hoat dong dua tren input cua user.

## Quy trinh

### Buoc 1 - Chot Problem

Viet lai van de trong 1-2 cau.
Neu input mo ho -> hoi toi da 3 cau.

### Buoc 2 - Scope

- In-scope
- Out-of-scope

### Buoc 3 - Risks

Liet ke risk va edge cases chinh.

### Buoc 4 - Questions / Assumptions

Chi ghi nhung gi can de sang `/wf-plan`.

### Buoc 5 - API Contract Flag

Danh dau:

- `Yes`
- `No`
- `Unknown`

## Output

Dung template `templates/wf-clarify-record.md.template`.

## Guardrails

- Khong tao plan chi tiet trong buoc nay
- Khong mo rong thanh analysis dai
- Khong de xuat refactor hay implementation detail som
