# Tri thức, context và vòng đời memory

**Mindset:** tri thức chỉ hữu ích khi truy xuất đúng, còn hạn, có nguồn và có quy tắc cập nhật. File này trả lời cách Agent-Dev-Kit và SecondBrain quản lý context/memory; không đánh giá browser automation hay thiết kế UI.

← [Index](../../2026-10-04-kit-secondbrain-repo-assessment.md) · [Lộ trình agent](implementation-roadmap.md)

## Nền tảng và điểm nghẽn hiện tại

Kit đã có workflow, quality gate, execution contract, progress ledger và context manifest. SecondBrain dùng Markdown/Obsidian, phân lớp Raw, Wiki, Brain, Cache và có receiver cho writeback.

Năm vấn đề cần giải quyết trước khi thêm runtime memory:

1. Registry suy tên file từ ID nhưng 11/13 path kiểm tra tại ngày 04/10/2026 không tồn tại.
2. 11/13 cache entry đang `active` đã quá hạn.
3. Kit Vault Steward và Brain receiver mô tả hai đường ghi khác nhau.
4. Memory consolidator ghi toàn chat mà chưa đi qua policy `AUTO/ASK/SKIP` chung.
5. Retry/dedup chưa có `writeback_id` ổn định hay quan hệ `supersedes`.

**Quyết định nền tảng:** Kit quyết định khi nào cần ghi và phát payload; Brain quyết định nơi ghi, evidence và điều kiện đưa vào Wiki/Cache. Registry phải chứa link file thật, `active/stale/superseded`, `verified_at` và revision nguồn khi phù hợp.

## Các repo và phần đáng học

| Repo | Giá trị | Áp dụng có điều kiện |
|---|---|---|
| [volcengine/OpenViking](https://github.com/volcengine/OpenViking) | Context filesystem `viking://`, ba mức L0/L1/L2, SDK/CLI/API/MCP. | Kit đã tiếp thu nguyên tắc nạp context theo tầng và manifest. Chỉ thử runtime khi lookup hiện tại không đủ, không thay Markdown chuẩn. |
| [vectorize-io/hindsight](https://github.com/vectorize-io/hindsight) | Memory học dần, tìm kiếm/tổng hợp có nguồn. | PoC trên một thư mục Wiki đã biên tập, sau khi provenance và freshness được sửa. Không import toàn vault. |
| [Gentleman-Programming/engram](https://github.com/Gentleman-Programming/engram) | Memory cho coding agent: resume, handoff và quyết định xuyên phiên. | PoC một project có vài task nối tiếp; output phải có đường xuất/đối chiếu Markdown. |
| [deepseek-ai/Engram](https://github.com/deepseek-ai/Engram) | Kiến trúc memory bên trong model. | Chỉ là nguồn nghiên cứu kiến trúc, không phải integration workflow/MCP. |
| [debpalash/VoiceStudio](https://github.com/debpalash/VoiceStudio) | Dictation/transcription local, API/MCP. | Addon voice → transcript → Raw note khi có nhu cầu capture bằng giọng nói. Không đưa runtime AGPL-3.0 vào core. |

## Contract writeback tối thiểu

Mỗi candidate cần `writeback_id`, nguồn/evidence, scope, confidence, `workflow`, `created_at` và nếu thay thế insight cũ thì `supersedes`. Receiver trả receipt để consolidator chỉ dọn staging sau khi ghi thành công.

Cache không phải Wiki: cache được phép hết hạn và phải kiểm freshness trước khi dùng; Wiki chỉ nhận insight có evidence đủ. Lưu transcript hoặc screenshot thô ở Raw khi cần, không tự động nâng thành tri thức chuẩn.

## Bằng chứng local đã đối chiếu

| Repo | File |
|---|---|
| Agent-Dev-Kit | `docs/research/external-agent-patterns.md` |
| Agent-Dev-Kit | `addons/knowledge/skills/sk-context-cache/SKILL.md` |
| Agent-Dev-Kit | `addons/knowledge/skills/sk-vault-steward/SKILL.md` |
| Agent-Dev-Kit | `addons/knowledge/skills/sk-memory-consolidator/SKILL.md` |
| SecondBrain | `AI_INSTRUCTIONS.md`, `03_Cache/_REGISTRY.md` |
| SecondBrain | `.agent/skills/sk-agent-writeback-receiver/SKILL.md` và các template writeback/cache |

**Tiêu chí PoC memory:** tìm đúng nguồn bằng diễn đạt khác; phân biệt project; tiếp tục sau phiên mới; xử lý nguồn đổi/xóa; retry không tạo bản sao; hỗ trợ truy vấn tiếng Việt.
