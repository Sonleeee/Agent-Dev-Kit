---
id: predict
type: utility
entry-command: /sk-predict
description: 5 expert personas tranh luận impact trước khi implement — Architect, Security, Performance, UX, Ops
modifiers:
  --fast: Mỗi persona chỉ 3 bullets, bỏ debate round
  --focus: Chỉ chạy 2-3 personas liên quan nhất (agent tự chọn)
  --deep: Mỗi persona phân tích kỹ + đưa evidence từ codebase hiện tại
---

# /sk-predict

**Mục tiêu:** 5 expert personas tranh luận impact của thay đổi trước khi implement — phát hiện risks, trade-offs, và blind spots.

## Khi nào dùng

- Thay đổi architecture lớn (thêm service, đổi database, refactor core module)
- Feature mới ảnh hưởng nhiều stakeholders
- Quyết định kỹ thuật quan trọng (tech stack, design pattern, scaling strategy)
- Trước khi `/sk-plan` cho task phức tạp — giúp plan toàn diện hơn

## Input

- Mô tả thay đổi dự kiến (1-5 câu)
- Context: codebase hiện tại, constraints, requirements
- (Optional) Câu hỏi cụ thể muốn debate

## 5 Expert Personas

### 🏗 Architect

**Mindset:** "Thiết kế này có scale không? Coupling có tăng? Extensibility ra sao?"

Phân tích:

- Modularity — tách biệt concerns đúng?
- Coupling — dependency mới giữa modules?
- Scalability — horizontal/vertical scaling impact?
- Extensibility — có block future changes?
- Pattern consistency — phù hợp với architecture hiện tại?

### 🔐 Security Expert

**Mindset:** "Attack surface thay đổi thế nào? Có tạo vulnerability mới?"

Phân tích:

- Attack surface — endpoint mới, data exposure mới?
- Auth model — permissions, roles affected?
- Data protection — sensitive data handling thay đổi?
- Third-party risk — new dependencies, external calls?
- Compliance — regulatory impact (GDPR, PCI...)?

### ⚡ Performance Engineer

**Mindset:** "Bottleneck ở đâu? N+1? Memory? Latency?"

Phân tích:

- Query patterns — N+1, missing indexes, full table scan?
- Memory — object allocation, caching strategy?
- Network — API call chains, payload sizes?
- Concurrency — lock contention, queue depth?
- Benchmarks — cần measure gì? Baseline hiện tại?

### 🎨 UX / Developer Experience

**Mindset:** "User/developer có hiểu không? Có confuse không?"

Phân tích:

- User impact — flow thay đổi? Learning curve?
- API ergonomics — intuitive? Consistent naming?
- Error messages — helpful? Actionable?
- Migration path — backward compatible? Breaking changes?
- Documentation — cần update gì?

### 🔧 Operations / SRE

**Mindset:** "Deploy thế nào? Monitor ra sao? Rollback được không?"

Phân tích:

- Deployment — blue/green? Rolling? Downtime?
- Monitoring — metrics mới cần track?
- Rollback — có rollback plan? Data migration reversible?
- Infrastructure — resource requirements thay đổi?
- Observability — logging, tracing, alerting?

## Quy trình

### Bước 1: Context Gathering

Agent tóm tắt:

- Thay đổi dự kiến
- Modules/files ảnh hưởng
- Constraints hiện tại

### Bước 2: Independent Analysis

Mỗi persona phân tích **độc lập**:

- Impact assessment (positive + negative)
- Risks identified
- Questions/concerns
- Recommendations

### Bước 3: Debate Round

Agent tổng hợp conflicts giữa personas:

- Architect muốn X nhưng Performance nói bottleneck
- Security muốn Y nhưng UX nói complexity
- Ops muốn Z nhưng Architect nói over-engineering

Mỗi conflict → trình bày cả 2 sides + trade-off.

### Bước 4: Consensus & Recommendations

Agent tổng hợp:

- **Consensus points** — tất cả đồng ý
- **Contested points** — cần user decide
- **Risks accepted** — acknowledged but proceed
- **Blockers** — phải resolve trước khi implement

## Output bắt buộc

```markdown
## 🔮 Predict Report

### Change Summary
[mô tả thay đổi]

### Expert Analyses

#### 🏗 Architect
- Impact: [...]
- Risks: [...]
- Recommendation: [...]

#### 🔐 Security
- Impact: [...]
- Risks: [...]
- Recommendation: [...]

#### ⚡ Performance
- Impact: [...]
- Risks: [...]
- Recommendation: [...]

#### 🎨 UX/DX
- Impact: [...]
- Risks: [...]
- Recommendation: [...]

#### 🔧 Ops
- Impact: [...]
- Risks: [...]
- Recommendation: [...]

### Debates
[conflicts giữa personas + trade-offs]

### Consensus
- ✅ Agree: [...]
- ⚠️ Contested: [user cần decide]
- ⚡ Risks Accepted: [...]
- 🚫 Blockers: [phải resolve]

### Final Recommendation
[proceed / proceed with conditions / reconsider]
```

## Guardrails

- `/sk-predict` KHÔNG thay thế `/sk-plan` — nó **bổ trợ** trước plan
- Mỗi persona phải argue từ **góc độ chuyên môn riêng** — không generic
- Recommendations phải actionable — không mơ hồ
- Nếu thay đổi đơn giản (≤2 files, no architecture change) → khuyên user dùng `/sk-plan` trực tiếp
- Debates phải present cả 2 sides — không bias
