---
name: sk-solution-planning
description: |
  Lap implementation plan ngan tu clarify record va project context.
  Dung de chot approach, impacted files, template selection, test obligations,
  va done criteria truoc khi code.
context-required: optional
output: implementation-plan-lite
---

# Solution Planning

## Muc tieu

Tao plan gon, de implement dung va khong over-formal.

## Context Loading

Neu project co:

- `AGENTS.md`
- `.agents/context/architecture.md`
- `.agents/context/templates/*`

thi phai doc de chot:

- impacted layers
- pattern constraints
- template selection

## Quy trinh

### Buoc 1 - Chot Approach

Chon 1 huong lam ngan gon.

### Buoc 2 - Impacted Files / Modules

Chi liet ke nhung file/module that su lien quan.

### Buoc 3 - Template Selection

Neu project co templates:

- phai chi ro template nao duoc dung o `/wf-impl`

### Buoc 4 - Test Obligations

Chi giu subset can thiet theo task-features.

### Buoc 5 - Done Criteria

Gom:

- implement xong
- self-check xong
- API contract status ro
- san sang review

## Output

Dung template `templates/implementation-plan-lite.md.template`.

## Guardrails

- Khong om scope qua lon trong 1 plan
- Khong bien `/wf-plan` thanh `/solution` + `/solution-plan` cu
- Neu task lon -> tach work items nho
