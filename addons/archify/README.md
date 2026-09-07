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

## Quy trình chuẩn

```text
source/code evidence
  → typed JSON IR
  → Archify validate
  → self-contained architecture.html
  → review/share
```

Archify hỗ trợ các loại diagram: `architecture`, `workflow`, `sequence`,
`dataflow`, `lifecycle`. Với diagram phản ánh code thật, agent phải ghi source
evidence và git SHA; HTML chỉ là artifact giao tiếp, không thay thế code/test.

```bash
node bin/archify.mjs validate architecture snapshot.json --quality showcase --json
node bin/archify.mjs deliver architecture snapshot.json architecture.html --quality showcase --json
node bin/archify.mjs compare architecture base.json head.json architecture-delta.html --json
```

Template snapshot: `architecture-snapshot.md.template`.
