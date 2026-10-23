# Obsidian Addon — Obsidian Vault

Addon này cung cấp các skill để đọc, chưng cất và lưu tri thức vào Obsidian Vault.

## Thiết lập

1. Cài Obsidian và tạo vault.
2. Có thể khởi đầu từ `vault-template/`.
3. Khai báo đường dẫn bằng `vault-path` trong `AGENTS.md` hoặc cấu hình dự án phù hợp.
4. Nếu có quy tắc `AI_INSTRUCTIONS.md` trong vault, agent cần tuân theo.

## Skills

- `sk-vault-steward`: lưu tri thức hoặc đồng bộ vào vault theo yêu cầu tường minh.
- `sk-context-cache`: cache kết quả phân tích có thể tái sử dụng.
- `sk-memory-consolidator`: chưng cất kiến thức theo yêu cầu; không tự ghi log hội thoại.

Các skill chỉ dùng được khi addon được cài vào đường dẫn được agent host discover.

## Alias tương thích

`/wf-vault-sync` được giữ như adapter deprecated chỉ khi được gọi trực tiếp. Nó route sang `sk-vault-steward`; không còn một procedure sync riêng trong workflow. Ghi vault luôn cần yêu cầu tường minh hoặc chính sách AUTO đã được người dùng thiết lập rõ.

## Cấu trúc vault gợi ý

```text
brain/
├── north-star.md
├── decisions/
├── knowledge/
├── projects/
└── daily/
```

Có thể dùng `vault-template/` làm điểm khởi đầu; không yêu cầu giữ nguyên cấu trúc này nếu vault hiện tại đã có quy ước riêng.
