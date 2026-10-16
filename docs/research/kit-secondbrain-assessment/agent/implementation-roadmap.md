# Lộ trình hỗ trợ agent

← [Index](../../2026-10-04-kit-secondbrain-repo-assessment.md) · [Lộ trình developer](../developer/implementation-roadmap.md)

Phạm vi: context/memory, writeback, điều phối agent và công cụ thu thập nguồn. Các thay đổi cho UI, kiểm thử sản phẩm và media nằm ở [lộ trình developer](../developer/implementation-roadmap.md).

## Đợt 1 — Sửa contract và dữ liệu tra cứu

1. Registry cache dùng link file thật; xử lý `active/stale/superseded`, expiry và revision nguồn.
2. Thống nhất Kit Vault Steward với Brain receiver/payload template.
3. Cho consolidator tạo candidate từ execution ledger và đi qua `AUTO/ASK/SKIP`.
4. Thêm `writeback_id`, `supersedes`, receipt và audit file/ID/expiry/evidence.

**Đạt khi:** lookup mở đúng note, retry không tạo bản sao, payload được route đúng, insight thiếu evidence không tự vào Wiki. Chi tiết: [knowledge/memory](knowledge-memory-lifecycle.md).

## Đợt 2 — Cải thiện workflow có sẵn

1. Bổ sung checkpoint Ponytail cho abstraction, dependency và tái sử dụng.
2. Dùng cách trình bày i-have-adhd như preference output, không là rule cứng.
3. Log nguồn context đã nạp, scope và cấp độ nạp theo OpenViking.

Chi tiết: [thực thi agent](agent-execution-governance.md). Quality gate UI được tách sang [nhóm developer](../developer/implementation-roadmap.md).

## Đợt 3 — Chọn một PoC runtime hoặc addon

| Nhu cầu | Phương án | Điều kiện đạt |
|---|---|---|
| Memory coding xuyên phiên | Gentleman Engram | Resume/handoff đúng một project, output có thể kiểm bằng Markdown. |
| Search/tổng hợp vault curated | Hindsight | Tìm đúng source, provenance và freshness đúng. |
| Research thiếu kênh dữ liệu | Agent Reach | 1–2 backend cần thiết, không mất provenance. |
| Agent cần đọc nguồn bằng Chrome/Edge desktop | BrowserSkill | Profile/domain rõ, task bounded và provenance đầy đủ. |
| Cần pipeline browser agent Python | browser-use | Output schema, stop condition, step/cost limit và kết quả thực được kiểm. |

Chỉ thử **một** phương án cho mỗi vấn đề. Đo baseline trước/sau: tỷ lệ tìm đúng nguồn, khả năng tiếp tục task, thời gian, chi phí, lượng context, can thiệp thủ công và khả năng chạy lại.
