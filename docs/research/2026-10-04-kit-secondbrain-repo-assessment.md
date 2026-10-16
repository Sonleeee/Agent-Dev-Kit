# Đánh giá repo cho Agent-Dev-Kit và SecondBrain

- **Ngày đối chiếu:** 04–05/10/2026.
- **Mục tiêu:** xác định cơ chế đáng học, addon/PoC đáng thử và thứ tự nâng cấp cho Agent-Dev-Kit và SecondBrain.
- **Trạng thái:** nghiên cứu và đề xuất; chưa cài runtime, benchmark hay thay đổi cấu hình agent.
- **Phương pháp:** đọc tài liệu chính chủ, đối chiếu cấu trúc local và giữ số liệu xu hướng như snapshot theo thời điểm.

Báo cáo được chia theo **người dùng chính**: năng lực/vận hành của agent và công cụ/quy trình phục vụ developer. Mỗi repo có một nơi phân tích chính; các trường hợp giao thoa dùng liên kết chéo. File này giữ vai trò index cho liên kết cũ.

## Kết luận điều hành

1. Sửa contract Kit ↔ SecondBrain, registry cache, freshness và dedup trước khi thêm memory/runtime mới.
2. Giữ Kit portable bằng Markdown; học pattern từ runtime bên ngoài thay vì đưa chúng vào core.
3. Nhánh agent tập trung context, memory, writeback, điều phối và truy cập nguồn ngoài.
4. Nhánh developer tập trung design system, kiểm thử UI, học/làm code và artifact giao sản phẩm.

## Tài liệu hỗ trợ agent

| Chủ đề | Câu hỏi trả lời | Repo/chủ đề chính |
|---|---|---|
| [Tri thức, context và memory](kit-secondbrain-assessment/agent/knowledge-memory-lifecycle.md) | Agent lưu, truy xuất và cập nhật tri thức ra sao? | OpenViking, Hindsight, hai Engram, VoiceStudio, cache/writeback |
| [Thực thi và governance](kit-secondbrain-assessment/agent/agent-execution-governance.md) | Agent có ownership, review và quyền hạn thế nào? | Ponytail, i-have-adhd, Paperclip, OpenRig, OpenShell |
| [Research và browser](kit-secondbrain-assessment/agent/research-ingestion-browser.md) | Agent đọc nguồn ngoài với provenance/evidence ra sao? | Agent Reach, BrowserSkill, browser-use |
| [Lộ trình agent](kit-secondbrain-assessment/agent/implementation-roadmap.md) | Sửa gì trước, PoC agent nào sau đó? | Writeback/cache → workflow → runtime |

## Tài liệu hỗ trợ developer

| Chủ đề | Câu hỏi trả lời | Repo/chủ đề chính |
|---|---|---|
| [Công cụ học và chất lượng phát triển](kit-secondbrain-assessment/developer/development-quality.md) | Developer học và xây sản phẩm hiệu quả thế nào? | AI Engineering from Scratch, Yoinks |
| [UI/design và product artifact](kit-secondbrain-assessment/developer/ui-design-and-product-artifacts.md) | Thiết kế, kiểm UI thật và handoff artifact ra sao? | Impeccable, OpenDesign, Vercel, Storybook, Playwright MCP, HyperFrames, Brag |
| [Lộ trình developer](kit-secondbrain-assessment/developer/implementation-roadmap.md) | Triển khai quality gate UI và PoC theo thứ tự nào? | Brief/render/test → design system → artifact |

## Dữ liệu chung và điểm giao

[Snapshot GitHub Trending ngày 05/10/2026](kit-secondbrain-assessment/trending-snapshot-2026-10-05.md) giữ xếp hạng sao theo thời điểm. VoiceStudio phục vụ capture đầu vào cho agent; Playwright MCP giúp coding agent kiểm sản phẩm của developer. Chúng có **một nơi phân tích chính** và liên kết chéo ở nhóm còn lại.

## Xác định repo được người dùng nêu

| Tên ban đầu | Repo được đánh giá |
|---|---|
| openviking | [volcengine/OpenViking](https://github.com/volcengine/OpenViking) |
| hindsigh | [vectorize-io/hindsight](https://github.com/vectorize-io/hindsight) |
| poneytail | [DietrichGebert/ponytail](https://github.com/DietrichGebert/ponytail) |
| i-adhd | [ayghri/i-have-adhd](https://github.com/ayghri/i-have-adhd) — giả định theo ngữ cảnh |
| brag | [latent-spaces/brag](https://github.com/latent-spaces/brag) |
| Engram coding agent | [Gentleman-Programming/engram](https://github.com/Gentleman-Programming/engram) |
| Engram architecture | [deepseek-ai/Engram](https://github.com/deepseek-ai/Engram) |
| agentReach | [Panniantong/Agent-Reach](https://github.com/Panniantong/Agent-Reach) |
| browserSkill | [Tencent/BrowserSkill](https://github.com/Tencent/BrowserSkill) |
| browser-use | [browser-use/browser-use](https://github.com/browser-use/browser-use) |

## Phạm vi bàn giao

- **Đầu ra:** index này, bốn file hỗ trợ agent, ba file hỗ trợ developer và một snapshot Trending trong `docs/research/kit-secondbrain-assessment/`.
- **Ngoài phạm vi:** cài runtime, sửa Kit/SecondBrain, thay cấu hình agent hoặc ghi kết quả vào vault.
- **Rủi ro:** capability, license và mức độ trưởng thành upstream có thể thay đổi; pin phiên bản và kiểm tra lại trước khi triển khai.
