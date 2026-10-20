---
id: deploy
type: utility
entry-command: /wf-deploy
skills-suggested:
  - core/sk-execution-contract
  - devops/sk-ci-pipeline-check
---

> [!IMPORTANT]
> ## Delegation Policy � �?c TRU?C khi b?t d?u
>
> | �i?u ki?n | H�nh d?ng B?T BU?C |
> |:---|:---|
> | Deploy c� migration + rollback plan | **PH?I** `invoke_subagent(TypeName="research", Role="Deploy Checklist Verifier")` d? verify checklist |
> | Deploy don gi?n (no migration) | Ch?y inline, KH�NG c?n subagent |


# /wf-deploy

**Mục tiêu:** chuẩn bị release/deploy có kiểm soát.

## Checklist bắt buộc

- [ ] Scope/version/changelog rõ
- [ ] Build và test pass từ clean state
- [ ] Migration/rollback plan rõ
- [ ] Secrets/config không bị commit
- [ ] Health check, observability và rollback owner rõ
- [ ] Review artifact và user approval nếu có production side effect

Nếu thiếu một mục critical, status là `BLOCKED`; không tự deploy.

## Pre-completion Checklist (PH?I verify tru?c khi deploy)

- [ ] �� ki?m tra Delegation Policy ? d?u file?
- [ ] T?t c? checklist items PASS?
- [ ] User approval cho production side effects?
