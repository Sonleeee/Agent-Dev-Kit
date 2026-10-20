---
id: security
type: utility
entry-command: /wf-security
description: Quét bảo mật cơ bản — OWASP top 10, secrets, auth issues
skills-suggested:
  - security/sk-owasp-scan
  - security/sk-secret-detection
modifiers:
  --owasp: Chỉ OWASP top 10 checks
  --secrets: Chỉ tìm hardcoded secrets
  --auth: Chỉ kiểm tra auth/authorization flow
---

# /wf-security

**Mục tiêu:** Quét bảo mật cơ bản cho codebase — phát hiện vulnerabilities phổ biến.

## Khi nào dùng

- Trước deploy lần đầu
- Sau khi thêm auth/authorization logic
- Khi handle user input, file upload, API calls
- Security audit định kỳ

## Quy trình

### Bước 1: Scan Dependencies

Agent kiểm tra:

- Package versions — có known CVEs không?
- Outdated packages — có bản vá bảo mật chưa cập nhật?
- Unused dependencies — giảm attack surface

### Bước 2: OWASP Top 10 Check

Agent kiểm tra theo OWASP Top 10:

| # | Vulnerability | Kiểm tra gì |
|---|---|---|
| A01 | Broken Access Control | Auth bypass, role check, IDOR |
| A02 | Cryptographic Failures | Hardcoded keys, weak hashing, no HTTPS |
| A03 | Injection | SQL injection, XSS, command injection |
| A04 | Insecure Design | Missing rate limit, no input validation |
| A05 | Security Misconfiguration | Debug mode on, default credentials, CORS |
| A06 | Vulnerable Components | Known CVEs in dependencies |
| A07 | Auth Failures | Weak password policy, no MFA, session issues |
| A08 | Data Integrity Failures | No input validation, unsigned data |
| A09 | Logging Failures | No security logging, logging sensitive data |
| A10 | SSRF | URL parsing, internal network access |

### Bước 3: Secrets Detection

Agent quét:

- API keys, tokens trong source code
- Passwords trong config files
- Connection strings với credentials
- Private keys / certificates
- `.env` files committed to git

### Bước 4: Auth Flow Review

Agent trace:

- Login flow: proper password hashing? Token generation secure?
- Authorization: role checks ở đúng layer? Missing checks?
- Session management: expiry, rotation, invalidation
- Password reset: secure token? Expiry?

### Bước 5: Report

Agent output:

| Severity | Mô tả |
|---|---|
| 🔴 Critical | Exploitable ngay — cần fix trước deploy |
| 🟠 High | Rủi ro cao trong production |
| 🟡 Medium | Cần fix nhưng không urgent |
| 🟢 Low | Best practice, nên sửa khi có thời gian |

## Output bắt buộc

- Security report phân loại theo severity
- Remediation guidance cho mỗi finding
- Summary: X Critical / Y High / Z Medium / W Low
- Go/No-go recommendation

## Guardrails

- Security scan KHÔNG sửa code — chỉ report
- KHÔNG log hoặc output sensitive data (keys, passwords) trong report
- False positives phải được ghi rõ — đừng gây panic
- Nếu có Critical finding → recommend KHÔNG deploy, chuyển `/wf-fix`

## Pre-completion Checklist (PHẢI verify trước khi report)

- [ ] Đã kiểm tra Delegation Policy ở đầu file?
- [ ] Nếu full audit → ĐÃ invoke parallel scanner subagents?
- [ ] Report KHÔNG chứa sensitive data (keys, passwords)?
- [ ] Mỗi finding có remediation guidance?
- [ ] Go/No-go recommendation rõ ràng?
