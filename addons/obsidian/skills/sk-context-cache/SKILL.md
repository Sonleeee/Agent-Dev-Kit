---
name: sk-context-cache
description: Tìm hoặc lưu cache tri thức kỹ thuật đã chưng cất trong Obsidian khi người dùng yêu cầu tra cứu, cache hoặc cập nhật rõ ràng. Không tự ghi cache theo kích thước phân tích hay tần suất lặp.
---

# Context Cache

Cache chỉ là bản tóm tắt có nguồn để giảm việc đọc lại phân tích; không phải ground truth. Không lưu toàn bộ conversation hoặc raw command output.

## Tra cứu

1. Xác định vault theo `vault-path` trong `AGENTS.md` hoặc dùng [`sk-vault-steward`](../sk-vault-steward/SKILL.md) để áp dụng quy tắc vault.
2. Đọc `03_Cache/_REGISTRY.md` nếu tồn tại; tìm entry phù hợp trong `patterns/`, `reviews/`, `decisions/`.
3. Kiểm tra `expires` và `confidence`; nếu cache hết hạn hoặc độ tin cậy thấp, verify lại với source/code hiện tại trước khi dùng.

## Tạo hoặc cập nhật cache

Chỉ ghi khi người dùng yêu cầu cache/update hoặc đã có policy AUTO bền vững được họ thiết lập rõ. Nếu chưa rõ là muốn lưu hay chỉ muốn xem, trả candidate trước.

- Dùng `03_Cache/{category}/{project}_{topic_snake_case}.md` nếu cấu trúc đó đã tồn tại.
- Giữ entry trong khoảng 50 dòng; gồm summary, key findings, evidence, references, tags, confidence và TTL/expiry.
- Kiểm tra entry trùng trước khi tạo; không overwrite nội dung hiện có. Bổ sung phần mới có nguồn hoặc hỏi nếu hai kết luận mâu thuẫn.
- Chỉ cập nhật `_REGISTRY.md` sau khi đã ghi entry; không tự cập nhật `AI_INDEX.md` nếu người dùng chưa yêu cầu.
- Mọi finding phải liên kết tới raw source, wiki entry hoặc code/file có thể kiểm tra.

Entry có thể dùng cấu trúc ngắn sau:

```markdown
---
type: cache_entry
project: "{project}"
topic: "{topic}"
tags: ["tag1", "tag2"]
created: "YYYY-MM-DD"
ttl: "3mo"
expires: "YYYY-MM-DD"
confidence: "medium"
---

# {topic}
## Summary
## Key Findings
## Evidence
## References
```

## Hạn chế

- `High` cần nhiều nguồn độc lập hoặc được xác nhận; một source đơn lẻ không đủ để gọi là stable rule.
- TTL là nhắc nhở để kiểm tra lại, không chứng minh nội dung đúng hay sai.
- Nếu không tìm thấy vault hoặc category folder, không tự tạo; báo đường dẫn/cấu trúc còn thiếu.
