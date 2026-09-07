---
name: archify-architecture-map
description: |
  Tạo hoặc cập nhật sơ đồ architecture, workflow, sequence, dataflow hoặc lifecycle
  bằng Archify chính chủ khi user yêu cầu rõ. Có thể bắt đầu từ repository, plan,
  mô tả hệ thống, Mermaid hoặc JSON snapshot. Không tự chạy sau wf-plan và không
  thay thế renderer/schema của Archify.
metadata:
  short-description: Tạo diagram HTML bằng Archify khi được gọi
---

# Archify Architecture Map

Skill tùy chọn của Agent-Dev-Kit. Chỉ kích hoạt khi user nói rõ muốn dùng
Archify hoặc muốn tạo/cập nhật diagram kiến trúc/kỹ thuật. Không tự động chạy sau
`/wf-plan`, `/wf-impl`, `/wf-review` hay bất kỳ workflow nào khác.

## Nguyên tắc

- Dùng skill/repo Archify chính chủ làm renderer, schema và validator.
- Không tự viết renderer, không tự fork JSON schema và không chuyển Mermaid thành
  HTML bằng cách ghép template thủ công.
- Input có thể là source repository, plan, requirements, mô tả plain text, Mermaid
  hoặc JSON snapshot đã có.
- Nếu diagram phản ánh code thật, chỉ gắn source evidence khi repository, commit,
  file và line range xác minh được. Không bịa topology, runtime impact hoặc risk.
- Giữ diagram bounded: khoảng 8–12 node chính, một primary path và các nhánh có
  ích cho câu hỏi hiện tại.

## Router loại diagram

| Câu hỏi cần trả lời | Loại Archify |
|---|---|
| Component, service, storage, boundary | `architecture` |
| Quy trình, approval, branch, runbook | `workflow` |
| API call, return, timing, cache miss | `sequence` |
| Pipeline, transformation, lineage, PII | `dataflow` |
| State, retry, wait, terminal outcome | `lifecycle` |

Nếu chưa rõ loại, dùng scenario guide của Archify trước hoặc hỏi user một câu
ngắn về điều họ muốn người xem hiểu sau khi xem diagram.

## Quy trình thực hiện

1. Xác định input và câu hỏi của người xem. Không mặc định input phải là source
   code hay plan.
2. Xác định diagram type, phạm vi, primary path, các boundary và output path.
3. Nếu Archify chưa được cài, báo user cài skill chính chủ:

   ```bash
   npx skills add tt-a1i/archify -g
   ```

4. Gọi Archify để tạo typed JSON IR. Với repository-backed diagram, dùng commit
   và source evidence đã xác minh; với diagram từ plan/mô tả, ghi `source evidence: none`
   thay vì giả lập line code.
5. Validate candidate bằng Archify. Dùng `standard` khi khám phá, `showcase` khi
   handoff/review/commit.
6. Chỉ dùng `deliver` sau khi candidate pass. Với HTML cần kiểm tra browser, chạy
   `visual-check`; tách riêng artifact validation, browser evidence và perceptual
   visual review.
7. Trả về đường dẫn JSON/HTML, diagram type, validation summary, receipt/hash nếu
   có, source evidence status và những giới hạn còn lại.

## Output convention

Mặc định dùng thư mục do user chỉ định. Nếu user không chỉ định, đề xuất:

```text
docs/architecture/
├── <name>.json
├── <name>.html
├── <name>.receipt.json
└── architecture-snapshot.md
```

Không tự tạo hoặc commit output nếu user chỉ yêu cầu tư vấn/prompt. Khi user yêu
cầu artifact, giữ JSON nguồn cùng HTML để có thể refine và compare về sau.

## Prompt patterns

### Từ repository

```text
Use Archify to map this repository's runtime architecture.
Show 8–12 core components, one primary path, external dependencies,
and trust boundaries. Use verified source evidence pinned to the current commit.
```

### Từ plan hoặc mô tả

```text
Use Archify to draw the architecture described below.
Treat this as a proposed design, not as implemented source code.
Show the primary path, boundaries, dependencies, and one important failure path.
```

### So sánh snapshot

```text
Use Archify to compare the base and current architecture snapshots.
Report only authored added, removed, changed, moved, or rerouted facts.
Do not infer merge safety or runtime risk without separate evidence.
```

## Official commands

Chạy từ thư mục cài Archify; không tự thay thế các lệnh này bằng implementation
riêng của kit:

```bash
node bin/archify.mjs doctor
node bin/archify.mjs guide "Show an API request with a Redis cache miss" --json
node bin/archify.mjs validate <type> <input.json> --quality showcase --json
node bin/archify.mjs deliver <type> <input.json> <output.html> --quality showcase --json
node bin/archify.mjs visual-check <output.html> --json
node bin/archify.mjs compare architecture <base.json> <head.json> <delta.html> --json
```

Chi tiết integration và template nằm tại:

- [`README.md`](./README.md)
- [`architecture-snapshot.md.template`](./architecture-snapshot.md.template)
- [Archify Authoring Cookbook](https://github.com/tt-a1i/archify/blob/main/docs/authoring-cookbook.md)
- [Archify official skill contract](https://github.com/tt-a1i/archify/blob/main/archify/SKILL.md)
