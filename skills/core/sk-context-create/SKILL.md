---
name: sk-context-create
description: |
  Khởi tạo, định nghĩa và tổng hợp Context chuẩn cho dự án.
  Dùng khi dự án mới bắt đầu, hoặc khi phát hiện một Feature/Domain hoàn toàn mới
  chưa có kiến trúc/mẫu chuẩn trong `.agents/context/`.
context-required: optional
output: markdown (tạo các file trong `.agents/context/`)
---

# Khởi Tạo Context (Context Creation)

## Mục tiêu

Xây dựng kho tàng kiến thức (Architecture, Code Templates, Rules) để toàn bộ các Agents khác có thể follow theo khi implement code.

## Khi nào sử dụng?

- Khi onboard một project hoàn toàn mới vào Agent-Dev-Kit.
- Khi một Module/Domain hoàn toàn mới ra đời, mang theo các setup kiến trúc chưa từng có (Pattern mới, Thư viện mới).

## Quy trình khởi tạo (Global Scan & Indexing Workflow)

Thay vì chỉ định 1 module mẫu duy nhất có rủi ro sai sót, Agent sẽ quét trên quy mô toàn bộ Source Code của dự án và xây dựng hệ thống Template dựa trên dữ liệu thực tế (Data-driven):

### Bước 1 - Quét Toàn Bộ Source Code (Global Scanning)

- Agent thực hiện quét, phân tích cấu trúc luồng dữ liệu (Flow) và pattern code của toàn bộ các module hiện có trong source code.

### Bước 2 - Phân Nhóm Thống Kê Pattern (Clustering)

- **Nhóm 1 - Tần suất cao (Core Patterns):** List ra các template, đoạn cấu trúc xuất hiện thường xuyên ở phần lớn các module. Phải liệt kê minh chứng cụ thể (ví dụ: đang nằm ở những module nào).
- **Nhóm 2 - Tần suất thấp (Edge Cases / Exceptions):** List ra các template code ít gặp hơn, xử lý nghiệp vụ dị biệt, rẽ nhánh. Cũng phải liệt kê rõ module nào đang chứa nó.

### Bước 3 - Chờ Xác Nhận (User Confirmation)

- Agent trình bày cho user 2 list pattern ở Bước 2.
- **Review sự chuẩn xác của code (Pattern Review):** Trước khi chốt template, Agent và User cần review đoạn code mẫu (pattern) đó xử lý có chuẩn xác không, có bị vi phạm anti-pattern hay kiến trúc không.
- User sẽ rà soát và **confirm** sẽ chọn bốc các template mẫu nào trong đó để làm kim chỉ nam tạo template của dự án. Giai đoạn này chưa tạo file thực tế.

### Bước 4 - Sinh Template & Xây Dựng Chỉ Mục (Index File)

Dựa trên các pattern user đã duyệt:
- Tạo các file code gốc `*.template` (đã clear nghiệp vụ tĩnh, gắn `[Placeholder]`) vào `.agents/context/templates/`.
- **ĐẶC BIỆT DẤU NHẤN:** Bắt buộc sinh một file **Mục Lục / Chỉ Mục** (ví dụ: `.agents/context/TEMPLATES-GUIDE.md`). File này chứa tiêu đề của các template và **Description mô tả rất rõ ràng cách sử dụng**. Mục tiêu là để AI sau này khi code có thể đọc file Guideline này và chọn đúng template cho phù hợp hoàn cảnh.

## Output

Báo cáo tóm tắt dưới dạng Markdown các thay đổi/file được thêm mới trong hệ thống File System (chủ yếu nằm ở thư mục `.agents/context/`).

## Guardrails (Nguyên tắc)

- **Không copy mù quáng**: Đảm bảo loại bỏ logic rác khỏi code template.
- **Tiêu cự**: Tập trung mô tả KIẾN TRÚC chứ không mô tả DATA DOMAIN (không mô tả bảng user có cột gì, mà mô tả cách query bảng ra sao).
