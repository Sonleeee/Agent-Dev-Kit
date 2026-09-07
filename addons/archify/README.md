# Archify Addon — Architecture HTML

> Tùy chọn cho Dev/BA/PM/PO cần sơ đồ kiến trúc, workflow, sequence, data-flow
> hoặc lifecycle dạng HTML tự chứa.

## Khi nào dùng

- Cần giải thích kiến trúc cho người không đọc code.
- Cần review thay đổi architecture trước merge.
- Cần artifact HTML/SVG/PNG gắn với một git revision.

## Cài đặt

```bash
npx skills add tt-a1i/archify -g
```

Archify yêu cầu Node.js 18+. Kiểm tra skill sau khi cài:

```bash
node bin/archify.mjs doctor
```

Thông thường không cần tự chạy schema hoặc renderer. Chỉ cần yêu cầu agent
dùng Archify; các lệnh bên dưới dành cho integration, troubleshooting hoặc CI.

## Quy trình chuẩn

```text
question / source evidence
  → typed JSON IR
  → validate (`standard` hoặc `showcase`)
  → deliver atomic
  → self-contained HTML
  → visual-check (nếu cần browser evidence)
```

Archify hỗ trợ các loại diagram: `architecture`, `workflow`, `sequence`,
`dataflow`, `lifecycle`. Với diagram phản ánh code thật, agent phải ghi source
evidence và git SHA; HTML chỉ là artifact giao tiếp, không thay thế code/test.

### Prompt khuyến nghị

```text
Use Archify to map this repository's runtime architecture.
Show 8–12 core components, one primary path, external dependencies,
and trust boundaries. Put supporting detail in cards instead of adding
more edges. Use verified source evidence pinned to the current git commit
when possible. Deliver docs/architecture/<name>.html and the JSON source.
Return validation, artifact hash, and visual-review status separately.
```

### Lệnh thủ công / CI

Chạy từ thư mục cài Archify:

```bash
node bin/archify.mjs guide "Show an API request with a Redis cache miss" --json
node bin/archify.mjs validate architecture snapshot.json --quality showcase --json
node bin/archify.mjs deliver architecture snapshot.json architecture.html --quality showcase --json
node bin/archify.mjs visual-check architecture.html --json
node bin/archify.mjs compare architecture base.json head.json architecture-delta.html --quality showcase --json
```

`deliver` chỉ thay file đích sau khi các gate pass. `visual-check` là bằng chứng
browser tự động, không đồng nghĩa với đánh giá thẩm mỹ của con người. Không coi
HTML là ground truth thay cho code, test hoặc source evidence.

## Chọn đúng loại diagram

| Loại | Dùng khi | Ví dụ |
|---|---|---|
| `architecture` | Component, service, storage, boundary | Bản đồ runtime của repo |
| `workflow` | Quy trình, approval, branch, runbook | CI/CD và rollback |
| `sequence` | Call, return, timing, cache miss | Login/API request |
| `dataflow` | Pipeline, transformation, lineage, PII | ETL và luồng dữ liệu |
| `lifecycle` | State, retry, wait, terminal outcome | Vòng đời job hoặc agent run |

Nên bắt đầu bằng một câu chuyện bounded: khoảng 8–12 node chính, một primary
path và chỉ các nhánh giúp trả lời câu hỏi. Nếu chưa biết chọn loại nào, dùng
`guide --json` trước.

## Use case nhanh

### 1. Dev — onboarding repo cũ

```text
Analyze this repository and use Archify to create a high-level architecture map.
Focus on request entrypoints, core services, databases, queues, external systems,
and trust boundaries. Show only the main runtime path.
```

### 2. Dev/Reviewer — architecture delta trước merge

```text
Create validated Archify architecture snapshots for the base and current commit.
Compare them and show added, removed, changed, moved, and rerouted facts.
Do not infer risk or merge safety; report only authored topology changes.
```

### 3. BA/PO — mô tả luồng nghiệp vụ có technical handoff

```text
Use Archify workflow to map checkout: customer submits order, payment approval,
inventory reservation, fulfillment, notification, rejection, and retry paths.
Keep business labels readable and separate external actors from internal services.
```

### 4. Dev/BA — giải thích một API khó

```text
Use Archify sequence for login: browser, API gateway, auth service, JWT validation,
Redis session lookup, PostgreSQL fallback, and response. Show cache-hit and
cache-miss paths, timing order, and async calls if any.
```

### 5. Data/PM — lineage và PII boundary

```text
Use Archify dataflow to show event source, ingestion, transform, warehouse,
analytics model, dashboard, and export. Mark PII crossings and consumers.
Do not invent runtime guarantees that are not supported by the source.
```

### 6. DevOps — CI/CD và rollback

```text
Use Archify workflow to map commit, build, test, security scan, approval,
deploy, health check, rollback, and notification. Highlight the failure branch
without making the diagram a dense task list.
```

### 7. Agent platform — lifecycle của một task

```text
Use Archify lifecycle for an agent task: queued, context loaded, planning,
waiting for approval, implementing, verifying, failed/retry, completed, and
cancelled. Show retry and terminal paths explicitly.
```

Template snapshot: `architecture-snapshot.md.template`.
