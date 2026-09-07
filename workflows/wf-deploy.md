---
id: deploy
type: utility
entry-command: /wf-deploy
skills-suggested:
  - core/sk-execution-contract
  - devops/sk-ci-pipeline-check
---

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
