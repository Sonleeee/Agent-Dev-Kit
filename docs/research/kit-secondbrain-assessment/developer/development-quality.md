# Công cụ học và chất lượng phát triển

**Người dùng chính:** developer muốn học, xây hoặc review sản phẩm. Coding agent có thể dùng các nguồn này để hỗ trợ developer, nhưng chúng không thuộc memory hay orchestration của agent.

← [Index](../../2026-10-04-kit-secondbrain-repo-assessment.md) · [Lộ trình developer](implementation-roadmap.md)

| Repo | Giá trị | Quyết định |
|---|---|---|
| [rohitg00/ai-engineering-from-scratch](https://github.com/rohitg00/ai-engineering-from-scratch) | Curriculum theo mục tiêu, mỗi lesson tạo artifact như prompt, skill, agent hoặc MCP. | Thư viện tham khảo cho developer; chỉ rút lesson cần thiết vào kế hoạch học, không nhập toàn bộ nội dung vào Kit. |
| [pablostanley/yoinks](https://github.com/pablostanley/yoinks) | CLI TUI nhỏ, tập trung một tác vụ và tái sử dụng công cụ có sẵn. | Tham khảo UX/độ tối giản khi developer xây CLI; không là dependency của Kit hay pipeline ingestion. |

Chất lượng code khi agent thực thi vẫn cần checkpoint minimality của [Ponytail](../agent/agent-execution-governance.md). Phần công cụ thiết kế và kiểm thử sản phẩm frontend nằm ở [UI/design](ui-design-and-product-artifacts.md).
