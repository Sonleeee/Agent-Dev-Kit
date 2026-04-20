---
name: sk-owasp-scan
description: |
  Checklist OWASP Top 10 cho codebase — kiểm tra vulnerabilities phổ biến.
  Dùng khi: security review, trước deploy, sau khi thêm auth/input handling.
  Trigger: "security scan", "OWASP check", "kiểm tra bảo mật", "vulnerability scan".
context-required: false
output: owasp-scan-report
---

# OWASP Scan

## Mục tiêu
Kiểm tra codebase theo OWASP Top 10 (2021) — phát hiện vulnerabilities phổ biến nhất.

## Khi nào chạy
- Trước deploy production lần đầu
- Sau khi thêm auth/authorization modules
- Sau khi thêm user input handling
- Security audit định kỳ

## Checklist — OWASP Top 10 (2021)

### A01: Broken Access Control
- [ ] Mọi endpoint có auth check? (không có public endpoint ngoài ý muốn)
- [ ] Role-based access đúng? (admin-only routes locked)
- [ ] IDOR protection? (user A không access data user B)
- [ ] CORS config đúng? (không wildcard `*` trên production)
- [ ] Directory traversal blocked? (path params sanitized)

### A02: Cryptographic Failures
- [ ] Passwords hashed (bcrypt/argon2), KHÔNG plain text?
- [ ] Sensitive data encrypted at rest?
- [ ] HTTPS enforced? (no HTTP fallback)
- [ ] Không hardcode encryption keys?

### A03: Injection
- [ ] SQL queries parameterized? (không string concatenation)
- [ ] Input sanitized/escaped cho HTML output? (XSS prevention)
- [ ] OS command injection blocked? (không exec user input)
- [ ] LDAP, XML injection considered?

### A04: Insecure Design
- [ ] Rate limiting trên auth endpoints?
- [ ] Input validation ở server side? (không chỉ client)
- [ ] Business logic abuse protection?

### A05: Security Misconfiguration
- [ ] Debug mode OFF trên production?
- [ ] Default credentials changed?
- [ ] Error messages không lộ internal info?
- [ ] Security headers configured? (CSP, X-Frame-Options, etc.)

### A06: Vulnerable Components
- [ ] Package versions up-to-date?
- [ ] No known CVEs in dependencies?
- [ ] Unused packages removed?

### A07: Authentication Failures
- [ ] Strong password policy enforced?
- [ ] Account lockout after failed attempts?
- [ ] Session tokens secure? (HttpOnly, Secure, SameSite)
- [ ] Proper logout — session invalidation?

### A08: Data Integrity Failures
- [ ] Input validation comprehensive?
- [ ] File upload restrictions? (type, size, content check)
- [ ] Deserialization từ untrusted source safe?

### A09: Logging & Monitoring Failures
- [ ] Security events logged? (login, failed auth, access denied)
- [ ] Logs không chứa sensitive data? (passwords, tokens)
- [ ] Monitoring/alerting cho suspicious activity?

### A10: Server-Side Request Forgery (SSRF)
- [ ] URL input validated? (không cho phép internal network access)
- [ ] Whitelist domains cho external calls?

## Output
- OWASP scan report phân loại theo A01-A10
- Mỗi finding: severity, evidence (file:line), remediation
- Summary: Critical / High / Medium / Low counts
- Go/No-go cho deploy

## Guardrails
- Scan KHÔNG sửa code — chỉ report
- KHÔNG output sensitive data trong report (keys, passwords)
- False positives ghi rõ — dont create panic
- Focus codebase đang review — không extrapolate
