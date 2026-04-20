---
name: sk-docker-review
description: |
  Review Dockerfile và docker-compose — size, security, caching, best practices.
  Dùng khi: tạo Docker setup mới, optimize image size, debug container issues,
  review Docker config trước deploy.
  Trigger: "review Docker", "optimize Dockerfile", "docker-compose review".
context-required: false
output: docker-review-checklist
---

# Docker Review

## Mục tiêu
Review Docker configuration — đảm bảo images nhỏ, secure, build nhanh, production-ready.

## Khi nào chạy
- Tạo Dockerfile mới
- Image size quá lớn — cần optimize
- Container fail / unexpected behavior
- Trước deploy production

## Checklist

### Dockerfile
- [ ] Multi-stage build? (tách build stage vs runtime stage)
- [ ] Base image cụ thể version? (không dùng `latest`)
- [ ] Base image nhỏ nhất có thể? (alpine, slim, distroless)
- [ ] COPY trước RUN install? (tận dụng layer caching)
- [ ] `.dockerignore` có và đầy đủ? (node_modules, .git, tests...)
- [ ] Non-root user? (không chạy container as root)
- [ ] HEALTHCHECK defined?
- [ ] Không COPY secrets vào image?

### docker-compose
- [ ] Services có depends_on đúng? (start order)
- [ ] Environment variables tách riêng? (.env file)
- [ ] Volumes mount đúng? (data persistence)
- [ ] Network isolation? (không expose all services)
- [ ] Resource limits? (memory, CPU)
- [ ] Restart policy? (unless-stopped / on-failure)

### Security
- [ ] Base image scan — no known CVEs?
- [ ] Secrets qua environment, KHÔNG build args?
- [ ] Exposed ports tối thiểu?
- [ ] Read-only filesystem? (khi có thể)

### Performance
- [ ] Layer ordering tối ưu cho caching?
- [ ] Combined RUN commands? (giảm layers)
- [ ] Build args cho cache-busting?
- [ ] Final image size < target? (thường < 200MB cho app)

## Output
- Docker review checklist với PASS/FAIL
- Image size analysis (nếu build được)
- Recommendations kèm code fixes cụ thể

## Guardrails
- Không sửa Dockerfile trực tiếp — chỉ recommend
- Recommendations phải kèm Dockerfile snippet cụ thể
- Đo lường: image size trước vs sau (nếu có thể)
