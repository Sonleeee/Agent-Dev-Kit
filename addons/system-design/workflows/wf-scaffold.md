# Workflow: Khởi tạo Source Base Dự Án Chuẩn Kiến Trúc (`/wf-scaffold`)

> **Mục tiêu:** Thực hiện phỏng vấn kiến trúc thực chiến (12 trụ cột), tính điểm độ phức tạp, lưu vết chống trôi context qua **Ephemeral Session Scratchpad** và tự động sinh source base chuẩn (Clean Architecture + ADR-001) ra đĩa qua MCP Server `system-design`.

---

## Khi nào sử dụng?
- Bắt đầu một dự án mới (Greenfield Project) hoặc setup lại source base chuẩn.
- Cần tư vấn kiến trúc có phản biện kỹ thuật, tránh over-engineering hoặc under-engineering.
- Muốn tự động hóa việc sinh code chuẩn kiến trúc kèm tài liệu quyết định (`ADR-001`).

---

## Quy trình 5 bước thực hiện

### Bước 1: Khảo Sát Kiến Trúc (2 Nhánh Tùy Chọn)
Khi người dùng gõ `/wf-scaffold`, AI chào đón và đưa ra **2 cách tiếp cận**:

#### 🚀 Cách 1: Nút Chọn Nhanh (Dành cho Dev bận rộn)
* **[1] Profile: Lean Solo / MVP (Tối giản, 1 dev ship siêu tốc)**
  * *Tech stack:* Clean Monolith + Postgres/SQLite + Background task RAM + REST API + JWT.
  * *Độ phức tạp:* **2/10** (0 đồng phát sinh, kéo về là code nghiệp vụ ngay).
* **[2] Profile: Enterprise SaaS / E-Commerce (Chuẩn doanh nghiệp thực chiến)**
  * *Tech stack:* Modular Monolith + Postgres (Pessimistic Lock) + DB Queue + REST + Webhook.
  * *Độ phức tạp:* **5.5/10** (Cân bằng hoàn hảo giữa tính bền vững và tốc độ code, chịu tải vài chục nghìn đơn/ngày).
* **[3] Profile: High-Scale Event-Driven (Tải lớn, phân tán)**
  * *Tech stack:* Clean Architecture + Redis BullMQ + Transactional Outbox + Circuit Breaker + WebSocket.
  * *Độ phức tạp:* **8.5/10** (Dành cho app triệu người, nghiệp vụ tài chính khắt khe, cần team từ 3-5 dev).

#### 🎯 Cách 2: Đo Ni Đóng Giày (4 Câu Hỏi Trọng Tâm Thực Chiến)
AI đưa ra bộ 4 câu hỏi trắc nghiệm (đầy đủ 4 tiêu chí: Tên kỹ thuật, Góc nhìn Dev, Góc nhìn End-user, Hạ tầng đi kèm):
1. **Quy mô người dùng thực tế:**
   * **A:** Dưới 100 người dùng (Nội bộ / MVP).
   * **B:** 1.000 đến 10.000 người dùng hoạt động mỗi ngày.
   * **C:** 50.000 - 100.000+ người, có khung giờ cao điểm săn flash sale.
2. **Tính chất dữ liệu:**
   * **A:** Chính xác tức thời (Strong Consistency - Tiền tệ, tài khoản, vé xe/vé phim, tồn kho số lượng có hạn, cấm bán trùng).
   * **B:** Chấp nhận trễ vài giây (Eventual Consistency - Mạng xã hội, đăng bài, thả tim, bình luận, đọc báo).
3. **Tác vụ ngầm (Gửi mail, tạo PDF, xuất báo cáo):**
   * **A:** Chạy ngầm trong RAM (`BackgroundTasks` / `setImmediate`), không tốn thêm server hay Redis.
   * **B:** DB-backed Queue lưu bảng `background_jobs` trong PostgreSQL (bền vững 100%, server crash bật lại không mất).
   * **C:** Hàng đợi chuyên dụng Redis BullMQ / RabbitMQ (tải hàng nghìn email/phút).
4. **Tổ hợp giao thức API cần dùng [Multi-select]:**
   * **[1] RESTful JSON API:** Cho Web & Mobile app gọi CRUD thông thường.
   * **[2] WebSocket Realtime:** Cho chat hoặc chuông thông báo nhảy lập tức.
   * **[3] Webhook Receiver:** Nhận callback tự động từ bên ngoài (Momo, VNPay, ZaloPay, Stripe) có verify chữ ký HMAC.

---

### Bước 2: Đánh Giá & Ghi Nhận Ephemeral Scratchpad
Sau khi nhận được đáp án từ người dùng (Ví dụ: `1B, 2A, 3B, 4[1,3]`):
1. AI kích hoạt MCP tool `evaluate_interview` với các tham số:
   * `answers`: `{ scale, consistency, background_jobs, protocols }`
   * `project_dir`, `project_name`
2. **Cơ chế chống trôi Context (Anti-Drift):** 
   * MCP Server tự động ghi trạng thái chuẩn hóa vào `.agents/.cache/scaffold-session.json`.
   * Tính toán **Complexity Score** (Thước đo độ phức tạp / 10).
   * Sinh sẵn dự thảo tài liệu quyết định `ADR-001.md`.
3. AI trình bày kết quả đánh giá cho dev:
   * Thước đo độ phức tạp: Điểm số + khuyến cáo quy mô team.
   * Các khối kỹ thuật sẽ được kích hoạt (Pessimistic lock, DB Queue, Webhook HMAC,...).
   * Hỏi dev xác nhận: *"Bạn có đồng ý với kiến trúc này để bắt đầu sinh mã nguồn không?"*

---

### Bước 3: Phê Duyệt & Sinh Mã Nguồn Tự Động (Scaffolding Engine)
Khi người dùng bấm "Chốt" hoặc đồng ý:
1. AI gọi tool `scaffold_project`.
2. **Quy trình thực thi của MCP Server:**
   * Đọc cấu hình từ file Ephemeral Scratchpad `.agents/.cache/scaffold-session.json`.
   * Bung toàn bộ cây thư mục Clean Architecture sạch sẽ ra đĩa.
   * Ghi đè file `docs/ADR-001-Architecture-Choice.md` với đúng các quyết định và invariants đã chốt.
   * Nhúng các module điều kiện (ví dụ: `hmac-verify.middleware.ts`, `db-queue.worker.ts`).
   * **Tự động hủy file Scratchpad (Auto-Eviction)** để bảo vệ context window cho các phiên làm việc tiếp theo.

---

### Bước 4: Kiểm Tra Invariants & Ranh Giới Kiến Trúc
AI xác nhận cấu trúc vừa tạo với người dùng:
- `src/domain/`: Thực thể nghiệp vụ thuần túy, zero-dependency.
- `src/application/`: Use cases & DTO validation.
- `src/infrastructure/`: Repositories, Database pool, Job workers.
- `src/interfaces/`: HTTP routes, controllers, middlewares.
- `docs/ADR-001-Architecture-Choice.md`: Bản hợp đồng kiến trúc lưu vết quyết định.

---

### Bước 5: Bàn Giao & Sẵn Sàng Triển Khai
AI hướng dẫn lệnh khởi động:
```bash
cd <project_name>
npm install
npm run dev
```
Gợi ý bước kế tiếp: Gõ `/wf-plan <tính năng>` để bắt đầu lập kế hoạch triển khai tính năng đầu tiên!
