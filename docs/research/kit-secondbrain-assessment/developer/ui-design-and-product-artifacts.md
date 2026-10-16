# UI/design và product artifact

**Mindset:** giao diện tốt cần nguồn sự thật về design system, render thật, review có evidence và artifact có thể handoff. Đây là addon cho project có UI, không là policy bắt buộc của mọi repo.

← [Index](../../2026-10-04-kit-secondbrain-repo-assessment.md) · [Lộ trình developer](implementation-roadmap.md)

## Quality và design system

| Repo | Giá trị | Hướng áp dụng |
|---|---|---|
| [pbakaus/impeccable](https://github.com/pbakaus/impeccable) | Design direction, `PRODUCT.md`, command workflow và detector rule. | Addon frontend; đối chiếu `PRODUCT.md` với passport Tầng 2 để tránh hai nguồn sự thật. |
| [vercel-labs/web-interface-guidelines](https://github.com/vercel-labs/web-interface-guidelines) | Checklist keyboard/focus, responsive, form, state, motion và accessibility. | `sk-ui-review` chứa phần phổ quát, bỏ các quy ước thương hiệu Vercel. |
| [vercel-labs/design-systems-to-agent-skills](https://github.com/vercel-labs/design-systems-to-agent-skills) | Trích token/icon/API/import đã xác minh từ source thành skill có artifact qua phiên. | `design-system-to-skill` với provenance `repo + revision + generated_at`; thử trên một design system thật. |
| [storybookjs/storybook](https://github.com/storybookjs/storybook) | Component cô lập, docs, story, interaction/a11y test. | Chỉ dùng với project đã có Storybook: đọc component thực, thêm story/test và lưu result làm evidence. |
| [anthropics/skills — frontend-design](https://github.com/anthropics/skills/tree/main/skills/frontend-design) | Visual direction và anti-default aesthetic. | Tham khảo cấu trúc skill, không coi là metric chất lượng. |
| [rithvikx/design-loop](https://github.com/rithvikx/design-loop) | Build → render evidence → critique → fix → regression. | Giữ rule tối giản: UI chưa hoàn thành nếu thiếu render evidence. Không mang toàn bộ state framework vào Kit. |
| [microsoft/playwright-mcp](https://github.com/microsoft/playwright-mcp) | Browser MCP để agent thao tác qua accessibility tree, chụp ảnh và kiểm thử flow UI. | Dùng trong `/wf-impl`, `/wf-fix` và `/wf-test` cho project UI: route, viewport, screenshot/visual diff và assertion. Snapshot accessibility chưa đủ để đánh giá thẩm mỹ. |

## Workspace và human-in-the-loop

[nexu-io/open-design](https://github.com/nexu-io/open-design) là workspace local-first từ brief → direction → `DESIGN.md` → prototype/artifact → handoff → memory, hỗ trợ Windows và Codex qua MCP/skill, đồng thời tích hợp HyperFrames. Đây là **P1 cho PoC workspace thiết kế**: thử một brief, dùng `DESIGN.md` làm contract, handoff HTML/CSS về repo dự án. Không để workspace thay passport hay receiver; đọc privacy/config trước PoC vì telemetry an toàn/độ tin cậy được nêu trong README.

[mitaraifail/zero-to-design](https://github.com/mitaraifail/zero-to-design) là mẫu workflow nhẹ để đi từ product discovery, references, nhiều direction cho người dùng chọn đến `DESIGN.md`. [onlook-dev/onlook](https://github.com/onlook-dev/onlook) và [open-pencil/open-pencil](https://github.com/open-pencil/open-pencil) phù hợp khi designer/PM cần phản hồi bằng selector, state và screenshot. Chúng là P2 vì cần desktop/MCP riêng và giới hạn filesystem.

## Artifact delivery

[latent-spaces/brag](https://github.com/latent-spaces/brag) và [heygen-com/hyperframes](https://github.com/heygen-com/hyperframes) phục vụ demo/release: HyperFrames có vòng lặp HTML/CSS/media → lint → preview → MP4 xác định. Chỉ dùng khi output cần video onboarding, walkthrough hay launch; không làm thay nhiệm vụ memory của SecondBrain.

Mỗi UI task nên có: `ui-brief`; design-system source/revision; component/token đã dùng; route + viewport; screenshot hoặc visual diff; a11y/interaction result; ngoại lệ đã chấp nhận. SecondBrain chỉ lưu quyết định/rubric/evidence có truy vết, không tự lưu CSS tạm hoặc toàn bộ screenshot vào Wiki.

Các công cụ browser phục vụ thu thập nguồn cho agent nằm ở [research/ingestion](../agent/research-ingestion-browser.md). Playwright MCP ở đây vì mục tiêu chính là xác minh sản phẩm của developer, dù agent là người thao tác browser.
