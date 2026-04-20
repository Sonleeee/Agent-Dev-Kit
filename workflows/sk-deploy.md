---
id: deploy
type: utility
entry-command: /sk-deploy
next: null
input-from: ship-ready-task
output-format: deploy-checklist
---

# /sk-deploy

**Mục tiêu:** Checklist pre-deploy để đảm bảo không có gì bị bỏ quên trước khi push production.

## Pre-conditions
- Gate 3 đã pass (không còn Critical finding)
- Task đã có ship decision: `Ready to ship`

## Checklist

### Environment & Config
- [ ] Environment variables đã được set đúng trên môi trường target
- [ ] Config khác nhau giữa environments đã được xem xét
- [ ] Secrets không bị hardcode hoặc commit

### Database
- [ ] Migration scripts đã được test trên staging
- [ ] Rollback migration script đã sẵn sàng (nếu có schema change)
- [ ] Data migration (nếu có) đã được verify

### Dependencies
- [ ] Dependency mới đã được install và lock version
- [ ] Breaking changes từ dependency upgrade đã được handle

### API & Integration
- [ ] API contract changes đã được thông báo tới consumers
- [ ] Backward compatibility hoặc versioning đã được xem xét
- [ ] Third-party integrations đã được test

### Build & Deploy
- [ ] Build pass trên CI
- [ ] Tests pass trên CI
- [ ] Deploy script / pipeline đã review

### Rollback Plan
- [ ] Rollback procedure được ghi rõ
- [ ] Thời gian rollback ước tính: [X phút]
- [ ] Ai có quyền trigger rollback?

### Monitoring
- [ ] Metrics / logs cần quan sát sau deploy được xác định
- [ ] Alert thresholds đã được set
- [ ] On-call person đã được thông báo

## Output
```markdown
## Deploy Checklist — [Task/Feature Name]

### Pre-deploy Status
- Environment: Ready / Pending
- Database: Ready / Pending
- Build/Test: Pass / Fail

### Deploy Window
- Planned: [datetime]
- Rollback window: [timeframe]

### Post-deploy Verification
- [ ] [verification step 1]
- [ ] [verification step 2]

### Sign-off
- Deployed by: [name]
- Verified by: [name]
```

## Guardrails
- Không deploy nếu rollback plan chưa rõ
- Không deploy nếu còn failing tests trên CI
- Ghi lại incident nếu có vấn đề xảy ra sau deploy
