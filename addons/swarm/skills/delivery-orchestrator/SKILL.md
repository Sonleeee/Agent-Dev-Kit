---
name: delivery-orchestrator
description: |
  Dieu phoi quy trinh delivery gon theo flow clarify -> plan -> implement -> review.
  Dung khi can 1 lan goi de chay toan bo pipeline voi quality gates va phan vai
  ro Antigravity / codex-cli / gemini-cli.
context-required: optional
output: delivery-report
---

# Delivery Orchestrator

## Muc tieu

Dam bao moi task di qua dung flow ngan, khong quay lai mo hinh 6 buoc qua dai.

## Inputs toi thieu

- Task context
- Task type: `Feature` hoac `Bugfix`
- Scope: `BE`, `FE`, hoac `BE+FE`
- API contract changed: `Yes / No / Unknown`

## Pipeline dieu phoi

```text
Stage 1: /clarify -> core/business-discovery
Stage 2: /plan    -> core/solution-planning + api-contract-guard neu can
         [GATE 1 CHECK]
Stage 3: /impl    -> codex-cli implement voi domain skills
         [GATE 2 CHECK]
Stage 4: /review  -> gemini-cli review + review-workflow
         [GATE 3 CHECK]
```

## Agent routing

- `Antigravity` = orchestrator
- `codex-cli` = implementer
- `gemini-cli` = reviewer

## Gate checks

### Gate 1 - Ready

Dung pipeline neu thieu:

- [ ] Problem statement ro
- [ ] Scope in/out xac dinh
- [ ] Quality card ngan
- [ ] Plan theo thu tu

### Gate 2 - Dev Done

Dung truoc review neu:

- [ ] Self-check chua pass
- [ ] API contract status chua ro

### Gate 3 - Ship Ready

Blocked neu con finding Critical.

## Dieu kien dac biet

Neu `API contract changed = Yes` hoac `Unknown`:

- bat buoc chay `core/api-contract-guard`

Neu `task type = Bugfix`:

- bat buoc co root cause layer
- bat buoc co anti-regression case

## Output bat buoc

Dung template `../../templates/delivery-report.md.template`.
