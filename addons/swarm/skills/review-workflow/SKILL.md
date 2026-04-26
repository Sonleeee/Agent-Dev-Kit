---
name: review-workflow
description: |
  Dieu phoi review sau implement: architecture review + regression check +
  api contract guard, voi gemini-cli dong vai tro reviewer chinh.
context-required: optional
output: review-summary
---

# Review Workflow

## Muc tieu

Tong hop review sau implement trong 1 lan goi, giu role ro rang:

- Antigravity = route va tong hop (qua Terminal run_command)
- gemini-cli / codex-cli = reviewer fresh-eyes (qua Terminal)

## Inputs toi thieu

- Scope review: `BE`, `FE`, hoac `BE+FE`
- Danh sach files/modules vua thay doi
- API contract changed: `Yes / No`
- Self-check output tu implementer

## Workflow dieu phoi

### Buoc 1 - Architecture Review

Neu scope co BE:

- chay `domain/backend/architecture-review`

Neu scope co FE:

- chay `domain/frontend/architecture-review`

### Buoc 2 - Regression Check

- chay `core/regression-checklist`

### Buoc 3 - API Contract Guard

- neu API contract changed = Yes -> chay `core/api-contract-guard`
- neu No -> ghi `Contract: OK (unchanged)`

### Buoc 4 - Tong hop findings

Sap xep:

- Critical
- Major
- Minor

Moi finding can co:

- mo ta van de
- layer/file anh huong
- muc do
- fix toi thieu de nghi

## Guardrails

- Reviewer khong implement code
- Khong ket luan `Ready` khi con Critical
- Luon uu tien fix toi thieu, khong mo rong thanh refactor lon

## Output

Dung template `../../../templates/sk-review-summary.md.template`.
