---
name: sk-dbhub-inspector
description: |
  Sử dụng DBHub MCP để kết nối, tra cứu cấu trúc (schema) và truy vấn dữ liệu một cách an toàn.
  Hỗ trợ phân tích dữ liệu thực tế để đối chiếu nghiệp vụ, gỡ lỗi EF Core, viết migrations và tối ưu câu lệnh SQL.
context-required: required
output: SQL queries, schema reports, data validation results
accelerators: dbhub
---

# Tra Cứu và Truy Vấn Cơ Sở Dữ Liệu An Toàn (Database Inspection via DBHub)

## Mục tiêu

Cung cấp quy trình chuẩn để AI agent sử dụng công cụ DBHub MCP kết nối, đọc cấu trúc cơ sở dữ liệu (schema) và thực thi các câu lệnh SQL phục vụ cho việc phát triển phần mềm, gỡ lỗi LINQ/EF Core, hoặc đối chiếu dữ liệu nghiệp vụ một cách an toàn nhất, tránh ảnh hưởng đến hiệu năng hệ thống.

## Khi nào sử dụng?

- **Gỡ lỗi API/LINQ Translation**: Khi gặp lỗi truy vấn EF Core, cần chạy thử câu lệnh SQL thuần để cô lập lỗi.
- **Tìm hiểu cấu trúc nghiệp vụ**: Khi cần hiểu các bảng liên quan đến một tính năng (ví dụ: `InventoryPeriod`, `ShipPlan`).
- **Xác minh dữ liệu thực tế**: Khi cần kiểm tra xem dữ liệu trong database có đúng với mong đợi của API hay UI không.
- **Tạo Migrations/Entity**: Khi tạo mới hoặc chỉnh sửa Entity trong Backend, cần đối chiếu với kiểu dữ liệu của các cột trong bảng thật.

---

## Các công cụ hỗ trợ (DBHub MCP Tools)

Khi kết nối thành công, DBHub cung cấp các công cụ chính:
1. `execute_sql`: Thực thi câu lệnh SQL (chỉ đọc - Readonly mặc định).
2. `search_objects`: Tìm kiếm các đối tượng trong database (table, view, column).

---

## Quy trình thực hiện

### Bước 1: Kiểm tra kết nối & Database Source
Trước khi chạy truy vấn, cần xác định xem DBHub đang kết nối tới nguồn dữ liệu (Source) nào để đảm bảo truy vấn đúng database.
- Đọc file cấu hình [dbhub.toml](file:///C:/Sonlee/AI/MCP/dbhub-runtime/dbhub.toml) để biết ID của database source (ví dụ: `main`).
- Kiểm tra danh sách bảng hiện có để xác nhận kết nối hoạt động tốt.

### Bước 2: Tìm kiếm cấu trúc bảng (Schema Inspection)
Trước khi viết câu lệnh `SELECT`, tuyệt đối không đoán tên bảng/cột.
- Sử dụng `search_objects` với từ khóa tên bảng hoặc cột liên quan để tìm chính xác tên.
- Nếu cần xem định nghĩa của một bảng (DDL), hãy chạy truy vấn lấy cấu trúc bảng:
  - **MySQL**: `SHOW CREATE TABLE <table_name>;` hoặc `DESCRIBE <table_name>;`
  - **PostgreSQL**: Truy vấn hệ thống `information_schema.columns`.

### Bước 3: Viết và Chạy SQL An Toàn
Khi thực thi câu lệnh SQL bằng `execute_sql`:
1. **Chỉ chạy câu lệnh READ-ONLY (`SELECT`)**: DBHub được cấu hình mặc định là `readonly = true` trong `dbhub.toml` để bảo vệ dữ liệu.
2. **Bắt buộc có giới hạn số dòng (`LIMIT` hoặc `TOP`)**:
   - Mặc dù DBHub có giới hạn `max_rows = 200`, bạn vẫn nên viết `LIMIT 50` hoặc tương đương trong câu lệnh SQL để tối ưu hóa thời gian chạy và lưu lượng mạng.
3. **Tránh quét toàn bộ bảng lớn (Full Table Scan)**:
   - Sử dụng điều kiện `WHERE` trên các cột có chỉ mục (Index) hoặc khóa chính.
   - Hạn chế các câu lệnh `LIKE '%keyword%'` trên các bảng có hàng triệu bản ghi nếu không cần thiết.

### Bước 4: Đối chiếu và Ánh xạ sang Code
Sau khi nhận được kết quả dữ liệu:
- **Ánh xạ Entity**: Đối chiếu kiểu dữ liệu (VARCHAR, INT, DATETIME,...) với kiểu dữ liệu của C# (string, int, DateTime,...) hoặc TypeScript.
- **Fix LINQ**: Chuyển đổi logic SQL chạy thành công về định dạng LINQ tương đương trong EF Core.
- **Giải quyết Bug dữ liệu**: Báo cáo sự sai lệch giữa dữ liệu thực tế trong DB và kết quả trả về của API/UI (ví dụ: cột bị `NULL`, sai định dạng múi giờ, v.v.).

---

## Nguyên tắc an toàn & Guardrails

> [!IMPORTANT]
> **Quy tắc bảo mật và an toàn dữ liệu**
> 1. **Tuyệt đối không chạy lệnh thay đổi dữ liệu** (`INSERT`, `UPDATE`, `DELETE`, `DROP`, `ALTER`) trực tiếp trên môi trường production nếu không được user yêu cầu và phê duyệt cụ thể.
> 2. **Che giấu thông tin nhạy cảm**: Khi xuất kết quả truy vấn hoặc viết tài liệu/artifacts, hãy che giấu (mask) hoặc ẩn các thông tin cá nhân nhạy cảm như mật khẩu mã hóa, token, hoặc thông tin cá nhân của khách hàng thực tế.
> 3. **Không chạy câu lệnh khóa bảng**: Tránh sử dụng các câu lệnh lock bảng hoặc giao dịch kéo dài gây nghẽn kết nối database phát triển.
