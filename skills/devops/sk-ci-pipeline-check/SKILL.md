---
name: sk-ci-pipeline-check
description: |
  Kiểm tra CI/CD pipeline config — thiếu step nào, best practices, security.
  Dùng khi: review CI config (GitHub Actions, GitLab CI, Azure DevOps),
  thêm pipeline mới, hoặc debug CI fail.
  Trigger: "kiểm tra CI", "review pipeline", "CI fail", "thêm GitHub Actions".
context-required: false
output: ci-review-checklist
---

# CI Pipeline Check

## Mục tiêu
Review CI/CD config và đề xuất cải thiện — đảm bảo pipeline reliable, secure, efficient.

## Khi nào chạy
- Tạo CI/CD pipeline mới
- CI build fail — cần debug config
- Review pipeline hiện tại — tìm gaps
- Thêm steps mới vào pipeline

## Checklist

### Build Steps
- [ ] Build step có cache dependencies? (node_modules, .nuget, pip cache)
- [ ] Build step dùng lock file? (package-lock.json, yarn.lock)
- [ ] Multi-stage build? (tách build vs runtime)
- [ ] Build timeout hợp lý? (không quá ngắn/dài)

### Test Steps
- [ ] Có test step? (unit, integration, e2e)
- [ ] Test có run riêng, không gộp với build?
- [ ] Test failure → pipeline fail? (không swallow)
- [ ] Coverage threshold configured?

### Security
- [ ] Secrets dùng environment variables, KHÔNG hardcode?
- [ ] Dependency scanning step? (npm audit, dotnet audit)
- [ ] Image scanning? (nếu dùng Docker)
- [ ] Least privilege permissions cho CI runner?

### Deployment
- [ ] Environment separation? (dev, staging, prod)
- [ ] Manual approval cho production deploy?
- [ ] Rollback strategy documented?
- [ ] Health check sau deploy?

### Performance
- [ ] Parallel jobs cho independent stages?
- [ ] Caching strategy tối ưu?
- [ ] Pipeline runtime < 10 phút? (target)
- [ ] Conditional triggers? (chỉ build khi relevant files thay đổi)

## Output
- CI review checklist với PASS/FAIL cho mỗi item
- Recommendations cho FAIL items
- Estimated improvement (nếu áp dụng recommendations)

## Guardrails
- Không sửa CI config trực tiếp — chỉ recommend
- Recommendations phải cụ thể — có code snippet mẫu
- CI config syntax phải match platform (GitHub Actions YAML ≠ GitLab CI YAML)
