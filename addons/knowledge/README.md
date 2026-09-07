# Knowledge Addon

> Gói tùy chọn cho Second Brain, cache tri thức và writeback vào Obsidian.

## Khi nào bật

- Project dùng Obsidian/Second Brain.
- Cần cache review, pattern, decision hoặc ghi knowledge sau workflow.

## Skills

- `sk-context-cache`: cache kết quả phân tích có TTL và provenance.
- `sk-memory-consolidator`: chưng cất tri thức thành entry có thể tái sử dụng.
- `sk-vault-steward`: writeback sang vault theo policy `AUTO/ASK/SKIP`.

Core workflows vẫn chạy được khi addon này không có; khi thiếu skill, agent chỉ báo
`SKIP` cho bước writeback và không tự tạo dữ liệu thay thế.
