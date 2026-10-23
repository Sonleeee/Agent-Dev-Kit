---
name: sk-owasp-scan
description: |
  Checklist OWASP Top 10 + 21 lỗ hổng đặc thù của mã do AI sinh (AI-Generated Code
  Vulnerabilities) cho codebase. Dùng khi: security review, trước deploy, sau khi
  thêm auth/input handling, hoặc sau khi AI agent sinh lượng code lớn.
  Trigger: "security scan", "OWASP check", "kiểm tra bảo mật", "vulnerability scan".
  Nguồn bổ sung: tanviet12/vbsec (https://github.com/tanviet12/vbsec)
---

# OWASP Scan + AI Code Security

## Mục tiêu
Kiểm tra codebase theo OWASP Top 10 (2021) kết hợp 21 lỗ hổng phổ biến nhất trong
mã nguồn do AI sinh — phát hiện cả vulnerabilities truyền thống lẫn các anti-patterns
đặc thù mà LLM hay mắc phải.

## Khi nào chạy
- Trước deploy production lần đầu
- Sau khi thêm auth/authorization modules
- Sau khi thêm user input handling
- Sau khi AI agent sinh lượng code lớn (scaffold, migration, API routes)
- Security audit định kỳ

---

## Phần A — Checklist OWASP Top 10 (2021)

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

---

## Phần B — 21 Lỗ Hổng Đặc Thù Của Mã Do AI Sinh

> Nguồn: [tanviet12/vbsec](https://github.com/tanviet12/vbsec) — Bộ 21 vulnerability
> types phổ biến nhất trong code do LLM tự sinh. Phân tích theo ngữ nghĩa (semantic
> analysis), truy vết luồng dữ liệu từ user input đến dangerous call thay vì chỉ
> matching chuỗi ký tự.

### Nhóm 1: Rò rỉ Bí mật & Cấu hình sai

- [ ] **`HARDCODED-SECRET`** — AI hay hardcode password, API key, JWT secret trực tiếp
  trong source code thay vì dùng biến môi trường. Kiểm tra: không có secret literal
  nào trong code; tất cả phải đọc từ `process.env`, `os.environ`, config vault.
- [ ] **`VERBOSE-ERROR-DEBUG-MODE`** — AI thường để `debug=True`, `app.use(errorHandler)`
  trả stack trace đầy đủ. Kiểm tra: production không lộ internal error, stack trace,
  hoặc đường dẫn file server.
- [ ] **`CORS-MISCONFIG`** — AI hay đặt `origin: '*'` hoặc reflect origin header
  không kiểm tra. Kiểm tra: CORS chỉ cho phép danh sách domain cụ thể trên production.

### Nhóm 2: Injection (Tiêm mã)

- [ ] **`SQL-INJECTION`** — AI thường nối chuỗi SQL trực tiếp từ `req.query`/`req.body`
  thay vì dùng parameterized queries. Kiểm tra: mọi query phải parameterized hoặc
  dùng ORM safe method (không phải `$queryRawUnsafe`, `sequelize.query` với template
  literal).
- [ ] **`COMMAND-INJECTION`** — AI hay gọi `exec()`, `subprocess.run()` với input từ
  user không sanitize. Kiểm tra: không exec user input; nếu cần, dùng allowlist
  commands và escapeshellarg.
- [ ] **`XSS`** — AI sinh HTML mà không escape output, đặc biệt khi dùng
  `dangerouslySetInnerHTML`, `v-html`, `bypassSecurityTrustHtml`. Kiểm tra: mọi user
  data phải escape trước khi render; cấm bypass XSS protection mà không có lý do.
- [ ] **`INSECURE-DESERIALIZATION`** — AI dùng `JSON.parse`, `pickle.loads`,
  `unserialize()` trên dữ liệu từ untrusted source mà không validate schema.
  Kiểm tra: deserialize chỉ sau khi validate schema/type.
- [ ] **`SSRF`** — AI tạo endpoint nhận URL từ user rồi fetch nội bộ. Kiểm tra:
  validate URL đầu vào, cấm truy cập internal network (169.254.x.x, localhost, 10.x).
- [ ] **`PATH-TRAVERSAL`** — AI dùng path từ user input để đọc/ghi file mà không
  normalize và restrict. Kiểm tra: `path.resolve` + kiểm tra prefix không thoát ra
  khỏi thư mục cho phép.

### Nhóm 3: Xác thực & Phân quyền

- [ ] **`BROKEN-ACCESS-CONTROL`** — AI tạo routes nhưng quên gắn middleware auth hoặc
  gắn sai thứ tự. Kiểm tra: mọi protected route có auth middleware; thứ tự middleware
  đúng (auth trước business logic).
- [ ] **`IDOR`** — AI dùng `req.params.id` để query DB mà không kiểm tra ownership.
  Kiểm tra: truy vấn phải có điều kiện `WHERE user_id = currentUser.id` hoặc
  tương đương.
- [ ] **`MASS-ASSIGNMENT`** — AI truyền thẳng `req.body` vào `Model.create()` hoặc
  `Model.update()` mà không whitelist fields. Kiểm tra: chỉ cho phép các field cụ thể
  (DTO/allowlist), không spread toàn bộ body.
- [ ] **`JWT-NONE-ALGORITHM`** — AI dùng `jwt.decode()` thay vì `jwt.verify()`, hoặc
  không chỉ định `algorithms` rõ ràng. Kiểm tra: luôn dùng `jwt.verify(token, secret,
  { algorithms: ['HS256'] })` hoặc tương đương.
- [ ] **`WEAK-PASSWORD-HASHING`** — AI dùng MD5/SHA1/SHA256 thuần để hash password.
  Kiểm tra: dùng bcrypt, scrypt, hoặc argon2 với salt.
- [ ] **`CSRF`** — AI tạo form POST mà không gắn CSRF token. Kiểm tra: mọi state-
  changing request (POST/PUT/DELETE) có CSRF protection hoặc dùng SameSite cookie.

### Nhóm 4: Lạm dụng & Race Condition

- [ ] **`BRUTE-FORCE`** — AI không thêm giới hạn số lần thử đăng nhập. Kiểm tra:
  có rate limiting hoặc account lockout sau N lần thất bại.
- [ ] **`MISSING-RATE-LIMIT`** — AI tạo API endpoint mà không áp rate limit. Kiểm tra:
  mọi public-facing endpoint có rate limiting (express-rate-limit, throttle decorator).
- [ ] **`RACE-CONDITION`** — AI không xử lý concurrent access (ví dụ: trừ số dư mà
  không lock). Kiểm tra: các thao tác tài chính/inventory dùng transaction +
  optimistic/pessimistic locking.
- [ ] **`UNRESTRICTED-FILE-UPLOAD`** — AI cho phép upload không kiểm tra file type,
  size, content. Kiểm tra: validate MIME type thực tế (magic bytes), giới hạn size,
  lưu ngoài webroot.

### Nhóm 5: Dependencies & Supply Chain

- [ ] **`OUTDATED-DEPENDENCY`** — AI import package phiên bản cũ có CVE đã biết.
  Kiểm tra: chạy `npm audit`, `pip-audit`, `govulncheck`, `composer audit` và xử lý
  các finding Critical/High.
- [ ] **`SLOPSQUATTING`** — AI bịa tên package không tồn tại (hallucinated package
  names), kẻ tấn công đăng ký trước tên đó trên npm/PyPI với mã độc. Kiểm tra: mọi
  dependency mới phải verify là package thật sự tồn tại, có maintainer rõ ràng,
  không phải tên do AI tự nghĩ ra.

---

## Phương Pháp Kiểm Tra Khuyến Nghị

Thay vì chỉ matching string, áp dụng **phân tích ngữ nghĩa 4 tầng tin cậy**:

| Tầng | Nguồn dữ liệu | Mức độ nguy hiểm |
|:---:|:---|:---|
| 1 | **Stranger-supplied:** Form input, URL params, headers, file uploads | 🔴 Nguy hiểm nhất |
| 2 | **Peer-supplied:** Database records, API responses từ service khác | 🟠 Cần validate |
| 3 | **System-produced:** Config files, environment variables | 🟡 Thường an toàn |
| 4 | **Constants:** Hardcoded literals trong code | 🟢 An toàn (trừ secrets) |

Chỉ flag khi dữ liệu tầng 1–2 đi thẳng vào dangerous call mà không qua sanitization.

---

## Output
- Scan report phân loại theo 2 phần: OWASP A01–A10 và AI-Vuln 21 types
- Mỗi finding: severity (CRITICAL/HIGH/MEDIUM/LOW), evidence (file:line), remediation
  kèm code snippet trước/sau fix
- Summary: Critical / High / Medium / Low counts
- Verdict: `PASS` / `CONDITIONAL PASS` / `FAIL`
- Go/No-go cho deploy

## Guardrails
- Scan KHÔNG sửa code — chỉ report
- KHÔNG output sensitive data trong report (keys, passwords)
- False positives ghi rõ — dont create panic
- Focus codebase đang review — không extrapolate
