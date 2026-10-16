# Lộ trình hỗ trợ developer

← [Index](../../2026-10-04-kit-secondbrain-repo-assessment.md) · [Lộ trình agent](../agent/implementation-roadmap.md)

Phạm vi: thiết kế, triển khai, kiểm thử UI và tạo artifact giới thiệu sản phẩm. Các công cụ này chỉ được áp dụng ở project có workload tương ứng.

## Đợt 1 — Chuẩn hóa đầu vào và bằng chứng UI

1. Đưa các guideline phổ quát về keyboard/focus, form, responsive, state và accessibility vào `sk-ui-review` tùy chọn.
2. Yêu cầu `ui-brief`, route, viewport và ảnh render/test result cho thay đổi UI.
3. Nếu project đã có Storybook, đọc component/story hiện hữu rồi chạy interaction và accessibility test liên quan. Nếu chưa có, dùng browser hoặc Playwright MCP theo workflow project.

**Đạt khi:** review có thể đối chiếu UI thật với brief, các state chính và kết quả kiểm thử; không kết luận từ source code đơn lẻ. Chi tiết: [UI/design](ui-design-and-product-artifacts.md).

## Đợt 2 — PoC theo nhu cầu của project

| Nhu cầu | Phương án | Điều kiện đạt |
|---|---|---|
| Project có design system | design-systems-to-agent-skills | Token, icon, API và import được xác minh từ source/revision. |
| Thiết kế từ brief đến prototype | OpenDesign hoặc zero-to-design | `DESIGN.md` và artifact handoff thống nhất với passport Tầng 2. |
| Cải thiện visual quality | Impeccable hoặc frontend-design | Có direction rõ và evidence render, không chỉ đánh giá bằng prompt. |
| Demo/release video | HyperFrames hoặc Brag | Artifact xuất được, xem lại được và gắn với release cụ thể. |
| Học cách xây AI/CLI | AI Engineering from Scratch hoặc Yoinks | Chọn bài học/pattern gắn với task developer thực tế. |

**Đo baseline:** thời gian sửa UI, số vòng phản hồi, lỗi responsive/a11y, mức tái sử dụng component và khả năng handoff. PoC chỉ mở khi project có nhu cầu rõ; cùng một nhiệm vụ dùng cùng rubric để so sánh.
