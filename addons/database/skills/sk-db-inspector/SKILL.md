---
name: sk-db-inspector
description: |
  Sử dụng Gridex MCP (hoặc công cụ Database Inspector tương thích) để kết nối, tra cứu cấu trúc (schema) và truy vấn dữ liệu một cách an toàn.
  Hỗ trợ phân tích dữ liệu thực tế để đối chiếu nghiệp vụ, gỡ lỗi EF Core, viết migrations và tối ưu câu lệnh SQL.
accelerators: gridex
---

# Tra Cứu và Truy Vấn Cơ Sở Dữ Liệu An Toàn (Database Inspection)

## Mục tiêu

Cung cấp quy trình chuẩn để AI agent sử dụng các công cụ kết nối cơ sở dữ liệu (hiện tại là Gridex MCP) kết nối, đọc cấu trúc cơ sở dữ liệu (schema) và thực thi các câu lệnh SQL phục vụ cho việc phát triển phần mềm, gỡ lỗi LINQ/EF Core, hoặc đối chiếu dữ liệu nghiệp vụ một cách an toàn nhất, tránh ảnh hưởng đến hiệu năng hệ thống.

## Khi nào sử dụng?

- **Gỡ lỗi API/LINQ Translation**: Khi gặp lỗi truy vấn EF Core, cần chạy thử câu lệnh SQL thuần để cô lập lỗi.
- **Tìm hiểu cấu trúc nghiệp vụ**: Khi cần hiểu các bảng liên quan đến một tính năng (ví dụ: `InventoryPeriod`, `ShipPlan`).
- **Xác minh dữ liệu thực tế**: Khi cần kiểm tra xem dữ liệu trong database có đúng với mong đợi của API hay UI không.
- **Tạo Migrations/Entity**: Khi tạo mới hoặc chỉnh sửa Entity trong Backend, cần đối chiếu với kiểu dữ liệu của các cột trong bảng thật.

---

## Các công cụ hỗ trợ (Gridex MCP Tools)

Khi kết nối, Gridex cung cấp các công cụ chính sau để hỗ trợ kiểm tra dữ liệu:

1. **Khảo sát cấu trúc (Schema & Metadata):**
   - `list_connections`: Liệt kê các kết nối DB đang khả dụng.
   - `list_schemas`: Liệt kê các schema trong database.
   - `list_tables`: Liệt kê danh sách các bảng trong schema/connection cụ thể.
   - `describe_table`: Lấy chi tiết thông tin các cột, kiểu dữ liệu và ràng buộc của một bảng.
   - `list_relationships`: Liệt kê các quan hệ khóa ngoại (Foreign Keys) giữa các bảng.
   - `search_across_tables`: Tìm kiếm từ khóa trên các cột của nhiều bảng để định vị dữ liệu.

2. **Truy vấn & Thao tác dữ liệu (Data Queries):**
   - `get_sample_rows`: Xem nhanh một số dòng dữ liệu mẫu của bảng mà không cần viết lệnh SQL.
   - `query`: Thực thi câu lệnh SQL chỉ đọc (`SELECT`). Luôn ưu tiên dùng tool này để an toàn.
   - `execute_write_query`: Thực thi câu lệnh SQL thay đổi dữ liệu hoặc cấu trúc bảng (`INSERT`, `UPDATE`, `DELETE`, `DDL`). Chỉ dùng khi cần thiết và có sự phê duyệt của User.
   - `explain_query`: Giải thích (Explain Plan) của một câu query để tối ưu hiệu năng.

---

## Quy trình thực hiện

### Bước 1: Kiểm tra kết nối & Lựa chọn Connection
Trước khi chạy truy vấn, cần xác định kết nối DB đang hoạt động:
- Chạy `list_connections` để xem danh sách các DB có sẵn.
- Chọn connection phù hợp với môi trường đang làm việc (Dev, Staging).

### Bước 2: Tìm kiếm và Khảo sát cấu trúc bảng (Schema Inspection)
Tuyệt đối không đoán bừa tên bảng hoặc tên cột.
- Sử dụng `list_tables` hoặc `search_across_tables` để tìm đúng tên bảng liên quan đến nghiệp vụ (ví dụ: tìm bảng chứa từ khóa `ship`).
- Dùng `describe_table` trên bảng cần kiểm tra để biết chính xác kiểu dữ liệu của các cột.
- Dùng `list_relationships` để hiểu liên kết khóa ngoại giữa bảng hiện tại với các bảng khác, phục vụ việc viết câu lệnh `JOIN`.

### Bước 3: Xem dữ liệu mẫu và Viết SQL chỉ đọc
- Dùng `get_sample_rows` để xem nhanh cấu trúc dữ liệu thực tế trong bảng.
- Khi cần truy vấn phức tạp (JOIN, WHERE, GROUP BY), sử dụng công cụ `query`:
  - **Bắt buộc có giới hạn số dòng**: Luôn chỉ định `LIMIT` (ví dụ: `LIMIT 50`) để tránh quét dữ liệu quá lớn hoặc làm quá tải bộ nhớ IDE.
  - **Tối ưu hóa**: Tránh quét toàn bộ bảng lớn (Full Table Scan). Hãy tận dụng các cột có chỉ mục (Index) hoặc Khóa chính trong điều kiện `WHERE`.

### Bước 4: Thực hiện ghi dữ liệu hoặc sửa schema (chỉ khi được yêu cầu)
- Nếu cần thay đổi dữ liệu hoặc DDL, sử dụng `execute_write_query` trước đó hoặc các helper tool (`insert_rows`, `update_rows`, `delete_rows`).
- Luôn kiểm tra lại câu lệnh cẩn thận trước khi gửi thực thi để tránh mất mát dữ liệu ngoài ý muốn.

### Bước 5: Đối chiếu và Ánh xạ sang Code
Sau khi nhận được kết quả dữ liệu:
- **Ánh xạ Entity**: Đối chiếu kiểu dữ liệu SQL với kiểu dữ liệu của C# (Backend) hoặc TypeScript (Frontend).
- **Gỡ lỗi LINQ/EF Core**: So sánh SQL được dịch bởi EF Core với SQL thuần để tìm ra điểm tối ưu hoặc sửa lỗi cú pháp.

---

## Nguyên tắc an toàn & Guardrails

> [!IMPORTANT]
> **Quy tắc bảo mật và an toàn dữ liệu**
> 1. **Mặc định là Read-Only**: Ưu tiên sử dụng công cụ `query` thay vì `execute_write_query`.
> 2. **Tuyệt đối không tự ý thay đổi dữ liệu**: Không chạy lệnh thay đổi dữ liệu (`INSERT`, `UPDATE`, `DELETE`, `DROP`, `ALTER`) trực tiếp nếu không được User yêu cầu cụ thể.
> 3. **Che giấu thông tin nhạy cảm**: Khi xuất kết quả truy vấn vào tài liệu, logs hoặc artifacts, hãy che giấu (mask) các thông tin nhạy cảm như mật khẩu, tokens, thông tin cá nhân khách hàng.
> 4. **Giới hạn số dòng trả về**: Bắt buộc giới hạn số dòng dữ liệu (limit) trong mỗi câu query để tránh treo hệ thống hoặc làm nghẽn đường truyền.
