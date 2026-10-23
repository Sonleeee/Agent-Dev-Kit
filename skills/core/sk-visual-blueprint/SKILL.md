---
name: sk-visual-blueprint
description: |
  Kỹ năng trực quan hóa kiến trúc hệ thống kết hợp luồng dữ liệu (Architecture + Data Flow + Entity State)
  chuẩn Business Analyst (BA) dạng SVG/HTML tự chứa, siêu nhẹ. Thay thế hoàn toàn các công cụ vẽ cồng kềnh,
  chạy tức thì (0 dependency, 0 build step), giúp lập trình viên và stakeholder nhìn thấy rõ ràng cả
  thành phần dịch vụ lẫn dữ liệu truyền qua lại.
inputs:
  - system_flow: Yêu cầu tính năng, kiến trúc module, luồng xử lý hoặc thay đổi CSDL
output:
  - visual_artifact: File SVG hoặc HTML tự chứa tại `docs/architecture/<name>.svg` hoặc `.html`
---

# Visual Blueprint & Data Architecture — sk-visual-blueprint

## 🎯 Mục tiêu

Giải quyết triệt để sự "mù dữ liệu" của các sơ đồ kiến trúc truyền thống (chỉ vẽ các khối dịch vụ vô hồn). `sk-visual-blueprint` áp dụng phương pháp luận của **Business Analyst (BA)** và **Solution Architect** để đồng thời trực quan hóa:
1. **Kiến trúc hệ thống (Ai nói chuyện với ai)**.
2. **Luồng dữ liệu chuyển dịch (Data in Transit - API Endpoint, Payload JSON, DTO)**.
3. **Trạng thái thực thể lưu trữ (Data at Rest - Bảng CSDL, Entity State Transition)**.

Tất cả được xuất thành định dạng **SVG/HTML tự chứa (Self-contained)** trực tiếp bởi Agent mà **không cần cài đặt Node.js runtime, không cần npx hay scripts biên dịch cồng kềnh**.

---

## 📐 4 Dạng Sơ Đồ Cốt Lõi Theo Chuẩn BA

Agent lựa chọn dạng sơ đồ phù hợp nhất với mục tiêu truyền đạt:

```text
┌────────────────────────────────────────────────────────────────────────────────┐
│ 1. 4-Layer Service Blueprint  : Toàn cảnh luồng từ UI -> Logic -> API -> DB   │
│ 2. Data-rich Sequence         : Trình tự gọi tuần tự kèm Payload chi tiết     │
│ 3. Entity State Machine       : Vòng đời và sự biến đổi trạng thái dữ liệu     │
│ 4. ERD Data Model             : Cấu trúc bảng, kiểu dữ liệu và khoá quan hệ    │
└────────────────────────────────────────────────────────────────────────────────┘
```

---

### Dạng 1: 4-Layer Service Blueprint (Khuyên dùng cho tính năng mới)
Phân rã một nghiệp vụ thành 4 tầng rõ rệt:

1. **User Action / Touchpoint Layer:** Người dùng thao tác màn hình nào, nhập vào những form field gì.
2. **Business Rules & Validation Layer:** Điều kiện logic cần thỏa mãn trước khi xử lý (Validation, Authorization).
3. **Service & API Layer (Data in Transit):** Endpoint được gọi (`POST /api/v1/...`), kèm mẫu Payload JSON rút gọn.
4. **Data Persistence Layer (Data at Rest):** Bảng CSDL bị ảnh hưởng (`INSERT`/`UPDATE`) và trạng thái (`status = PENDING_PAYMENT`).

---

### Dạng 2: Data-rich Sequence (Khuyên dùng cho tích hợp API/Microservices)
Sơ đồ tương tác tuần tự giữa các bên (Client $\leftrightarrow$ Gateway $\leftrightarrow$ Service $\leftrightarrow$ Database $\leftrightarrow$ 3rd Party), nhưng tại mỗi mũi tên **bắt buộc ghi chú Schema hoặc Payload**:

```text
Client ────────── POST /orders { items, voucherCode } ──────────> OrderService
OrderService ──── SELECT balance FROM wallets WHERE user_id ───> Database
OrderService <─── Result: { balance: 500000 } ────────────────── Database
OrderService ──── Publish Event: OrderCreatedEvent(id, items) ─> Kafka/Broker
```

---

### Dạng 3: Entity State Machine (Khuyên dùng cho Quản lý Vòng đời Dữ liệu)
Trực quan hóa sự biến đổi trạng thái của các thực thể cốt lõi trong hệ thống:
$$\text{DRAFT (Nháp)} \xrightarrow[\text{User Submit}]{\text{Validate OK}} \text{PENDING (Chờ duyệt)} \xrightarrow[\text{Admin Approve}]{\text{Ghi sổ kế toán}} \text{ACTIVE (Hiệu lực)} \xrightarrow[\text{User Cancel}]{\text{Hoàn tiền}} \text{VOID (Hủy)}$$

---

### Dạng 4: ERD Data Model (Khuyên dùng khi thay đổi Schema Database)
Mô tả các thực thể dữ liệu với định dạng bảng rõ ràng:
- Tên bảng (Entity Name).
- Danh sách cột: Tên trường, Kiểu dữ liệu (`UUID`, `VARCHAR`, `DECIMAL`, `BOOLEAN`), Ràng buộc (`PK`, `FK`, `NOT NULL`).
- Mũi tên liên kết quan hệ ($1-1$, $1-N$, $N-N$).

---

## 🎨 Quy Chuẩn Thẩm Mỹ & Kỹ Thuật SVG / HTML

Mọi sơ đồ do Agent sinh ra phải tuân thủ chuẩn thẩm mỹ **Editorial Design** (không bóng mờ mờ mịt, không màu sắc lòe loẹt):

1. **Bảng màu chuẩn mực:**
   - Nền: Sáng (`#FFFFFF`) hoặc Tối nhẹ (`#0F172A`).
   - Khối dịch vụ: Viền mảnh (`stroke="#E2E8F0"` hoặc `stroke="#334155"`), bo góc `rx="6"`.
   - Màu nhấn (Accent): Chỉ dùng màu nổi bật (Xanh dương, Hổ phách, Ngọc lục bảo) cho 1–2 điểm trọng tâm người đọc cần chú ý trước tiên.
2. **Typography SVG:**
   - Font: `font-family="system-ui, -apple-system, sans-serif"`.
   - Phân cấp: Tiêu đề node `font-size="13" font-weight="600"`, nhãn dữ liệu/payload `font-size="11" font-family="monospace"`.
3. **Tính độc lập & Nhẹ nhàng:**
   - Toàn bộ sơ đồ gói gọn trong một file `.svg` hoặc `.html` thuần (Inline SVG + CSS tối giản).
   - Tự động co giãn theo khung nhìn (`viewBox="0 0 1000 600"` và `width="100%"`).
   - Không nạp bất kỳ thư viện JS bên ngoài nào (Zero CDNs, Zero bundle size).

---

## 📂 Quy Ước Lưu Trữ

- Lưu sơ đồ vào thư mục:
  ```
  docs/architecture/<tên-nghiệp-vụ>-blueprint.svg
  ```
  *(hoặc `.html` nếu cần tương tác cuộn/tooltip nhẹ)*.
- Liên kết đường dẫn file sơ đồ trực tiếp vào:
  - Bản kế hoạch (`docs/plans/...` hoặc `/wf-plan`).
  - Hợp đồng thực thi (`execution-contract.md`).
  - Pull Request / Review Summary (`/wf-review`).
