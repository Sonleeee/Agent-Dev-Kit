---
name: sk-secret-detection
description: |
  Tìm hardcoded secrets, API keys, passwords trong code và config files.
  Dùng khi: security audit, pre-commit check, review config files.
  Trigger: "tìm secrets", "hardcoded keys", "secret detection", "leak check".
---

# Secret Detection

## Mục tiêu
Phát hiện hardcoded secrets trong codebase — API keys, passwords, tokens, connection strings.

## Khi nào chạy
- Trước khi push code lên remote
- Security audit
- Onboard project mới — check existing codebase
- Sau khi thêm external service integration

## Patterns Cần Tìm

### API Keys & Tokens
- AWS: `AKIA[0-9A-Z]{16}`
- Google: `AIza[0-9A-Za-z_-]{35}`
- GitHub: `ghp_[0-9a-zA-Z]{36}`, `gho_`, `ghu_`, `ghs_`, `ghr_`
- Stripe: `sk_live_[0-9a-zA-Z]{24}`, `pk_live_`
- Slack: `xoxb-`, `xoxp-`, `xoxs-`
- JWT: `eyJ[A-Za-z0-9_-]*\.eyJ[A-Za-z0-9_-]*\.[A-Za-z0-9_-]*`

### Passwords & Credentials
- Connection strings: `password=`, `pwd=`, `passwd=`
- Database URLs: `postgres://user:pass@`, `mongodb://user:pass@`
- Config files: `apiKey:`, `secret:`, `token:` với giá trị thật

### Private Keys & Certificates
- `-----BEGIN RSA PRIVATE KEY-----`
- `-----BEGIN OPENSSH PRIVATE KEY-----`
- `-----BEGIN CERTIFICATE-----`
- `.pem`, `.key`, `.p12` files trong repo

### Quy Trình Quét

1. **Scan source code** — tất cả files text (*.cs, *.ts, *.json, *.yaml, *.env)
2. **Scan config** — appsettings*.json, .env*, docker-compose*, CI configs
3. **Scan git history** — (nếu được yêu cầu) `git log -p | grep pattern`
4. **Check .gitignore** — .env và config sensitive files có trong .gitignore?

### Phân Loại

| Level | Mô tả | Action |
|---|---|---|
| 🔴 Critical | Key/password live, public accessible | Revoke ngay + fix |
| 🟠 High | Key/password trong code, chưa public | Rotate + move to env |
| 🟡 Medium | Test/dev credentials hardcoded | Move to env, block prod |
| ℹ️ Info | Pattern trông giống secret nhưng là placeholder | Ghi chú, cần verify |

## Output
- Danh sách secrets phát hiện (MASKED — không hiện full value)
- File location cho mỗi finding
- Severity level
- Remediation steps
- .gitignore recommendations

## Guardrails
- KHÔNG hiện full secret value trong output — mask: `sk_live_****...5678`
- KHÔNG copy secrets ra ngoài codebase
- Nếu tìm thấy live key → recommend revoke NGAY, không chỉ fix code
- .env file findings → recommend `.gitignore` entry
