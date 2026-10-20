---
name: sk-system-architect
description: |
  Kỹ năng kiến trúc hệ thống và dựng source base dự án chuẩn.
  Tích hợp trực tiếp với MCP Server 'system-design' để tra cứu các pattern phân tán
  (outbox, idempotency, circuit breaker, caching) và tự động sinh source base (Clean Architecture)
  mà không cần tìm kiếm bừa bãi ra ngoài internet.
context-required: optional
output: architecture-decision-or-scaffold
---

# System Architect & Scaffolding Skill

## Mục tiêu

Cung cấp tư duy kiến trúc hệ thống chuẩn mực, giải pháp độ tin cậy cao (High Reliability & Consistency) và năng lực tự động dựng khung source base chuẩn (Scaffolding Engine) cho các dự án mới.

## Nguyên tắc cốt lõi (Core Invariants)

1. **Ground-Truth First — Không Lan Man Internet**:
   Khi đối mặt với các bài toán kiến trúc phân tán (tránh trùng đơn hàng, ghi DB kèm gửi message, chống sập cache khi flash sale, ngắt mạch khi service chậm):
   **BẮT BUỘC gọi MCP Server `system-design`** qua các tool:
   - `search_patterns(query, category)`: Tìm pattern chuẩn đã được thẩm định.
   - `get_pattern_details(pattern_id)`: Lấy chi tiết bài toán, sơ đồ luồng Mermaid, invariants và code mẫu.

2. **Chống Over-Engineering**:
   Không vội vàng chia Microservices khi dự án dưới 10.000 users và team dưới 5 người. Hãy ưu tiên **Modular Monolith** hoặc **Clean Architecture Monolith**. Dùng tool `evaluate_interview` để có đánh giá khách quan.

3. **Chống Trôi Context Qua Ephemeral Scratchpad**:
   Trong quá trình phỏng vấn kiến trúc, bắt buộc gọi `evaluate_interview(answers)` để đóng băng trạng thái vào file `.agents/.cache/scaffold-session.json`. Không dựa vào bộ nhớ hội thoại tự do để tránh hallucination khi sinh code.

4. **Scaffolding Chuẩn Xác 100%**:
   Khi khởi tạo dự án mới:
   - Kích hoạt tool `scaffold_project(architecture_id, target_dir, project_name)` để bung trọn vẹn toàn bộ cây thư mục, Dockerfile, configs và cá nhân hóa `ADR-001.md` từ Ephemeral Scratchpad.
   - MCP Server sẽ tự động xóa sạch file Scratchpad sau khi hoàn tất để bảo vệ context window sạch sẽ.

## Các Công Cụ Khả Dụng (MCP Server: `system-design`)

| Tool Name | Khi Nào Sử Dụng? |
| :--- | :--- |
| `evaluate_interview` | Khi nhận được câu trả lời phỏng vấn (12 trụ cột), tính Complexity Score và lưu Ephemeral Scratchpad. |
| `search_patterns` | Khi cần tìm pattern giải quyết một vấn đề (ví dụ: "outbox", "trùng đơn", "idempotency"). |
| `get_pattern_details` | Khi cần xem sơ đồ Mermaid, quy tắc bất biến và code boilerplate của 1 pattern cụ thể. |
| `list_architectures` | Khi bắt đầu dự án mới, cần xem các kiến trúc source base có sẵn. |
| `scaffold_project` | Khi người dùng yêu cầu dựng source base mới theo Clean Architecture. |
| `inject_pattern` | Khi cần nhúng trực tiếp code mẫu của một pattern vào dự án đang phát triển. |
| `recommend_architecture` | Khi cần tư vấn chọn mô hình kiến trúc phù hợp với quy mô tải và quy mô team. |

## Quy trình làm việc chuẩn

### Kịch bản 1: Khởi tạo Source Base cho dự án mới
1. Đặt câu hỏi khảo sát: Mục tiêu dự án, tech stack (TypeScript/Python/Go), quy mô dự kiến.
2. Gọi `recommend_architecture` hoặc `list_architectures`.
3. Xác nhận thư mục đích với người dùng.
4. Gọi `scaffold_project` để tạo mã nguồn chuẩn.
5. Hướng dẫn người dùng các bước tiếp theo (cài dependencies, chạy docker-compose, cấu trúc các tầng).

### Kịch bản 2: Giải quyết vấn đề kiến trúc khi coding
1. Người dùng hỏi: *"Làm sao để vừa lưu đơn hàng vừa gửi notification mà không bị mất event nếu sập server?"*
2. Gọi `search_patterns(query: "outbox")`.
3. Gọi `get_pattern_details(pattern_id: "transactional-outbox")`.
4. Trích xuất giải pháp, sơ đồ Mermaid và code snippet chuẩn từ kết quả trả về để giải thích cho người dùng hoặc tích hợp vào code.
