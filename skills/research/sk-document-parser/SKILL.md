---
name: sk-document-parser
description: |
  Kỹ năng tự động parse tài liệu nghiệp vụ (PDF, Word, Excel, PowerPoint, HTML) sang định dạng Markdown.
  Giúp Agent nạp tài liệu thiết kế thô trực tiếp vào context mà không bị ô nhiễm định dạng nhị phân.
inputs:
  - doc-path: Đường dẫn tuyệt đối đến file cần parse (.pdf, .docx, .xlsx, .pptx, .html)
output: markdown (Lưu tại .agents/context/temp_spec.md)
---

# 📄 Bộ Chuyển Đổi Tài Liệu Nghiệp Vụ — sk-document-parser

## 🎯 Mục tiêu

Giúp AI Agent tự động phân tích cấu trúc cấu tệp tin nghiệp vụ thô của khách hàng (hoặc tài liệu thiết kế hệ thống) và chuyển đổi chúng thành định dạng Markdown sạch sẽ để làm dữ liệu ngữ cảnh (ground truth context) phục vụ lập trình.

---

## 🛠️ Nguyên lý Phân tích cấu trúc (Parser Engine)

Để tránh phụ thuộc vào các framework bên thứ ba, Agent sẽ áp dụng các thuật toán parse cấu trúc tệp tin như sau:

### 1. Với tệp Word (.docx) & PowerPoint (.pptx)
*   **Bản chất:** Đây là các file nén dạng Zip chứa các cấu trúc XML bên trong.
*   **Thuật toán parse của Agent:**
    1.  Giải nén file `.docx` / `.pptx` tạm thời vào thư mục scratch.
    2.  Đọc file XML chứa nội dung chính (ví dụ `word/document.xml` đối với Word).
    3.  Ánh xạ (map) các thẻ XML của Word sang cú pháp Markdown:
        *   `<w:pStyle w:val="Heading1">` ➔ Map thành Heading `#`
        *   `<w:p>` ➔ Map thành đoạn văn (Paragraph)
        *   `<w:r>` ➔ Trích xuất text run bên trong
        *   `<w:tbl>` ➔ Map thành bảng Markdown (`|`)
        *   `<w:numPr>` ➔ Map thành danh sách có thứ tự/không thứ tự (`-` hoặc `1.`)

### 2. Với tệp Excel (.xlsx)
*   **Bản chất:** Bảng tính 2 chiều.
*   **Thuật toán parse của Agent:**
    1.  Đọc các ô (cells) dữ liệu của từng Sheet.
    2.  Trích xuất hàng đầu tiên làm tiêu đề cột (Headers).
    3.  Dựng lại toàn bộ grid dữ liệu dưới dạng bảng Markdown chuẩn, ngăn cách bởi ký tự `|`.
    4.  Bỏ qua các ô trống hoặc định dạng style màu sắc, chỉ giữ lại text/number và liên kết.

### 3. Với tệp PDF
*   **Bản chất:** Tài liệu hiển thị theo tọa độ tĩnh.
*   **Thuật toán parse của Agent:**
    1.  Sử dụng thư viện đọc PDF cục bộ để trích xuất text kèm theo tọa độ.
    2.  Nhóm các dòng text có khoảng cách dòng (line spacing) gần nhau thành các Paragraph blocks.
    3.  Nhận diện Heading dựa trên kích thước font chữ (font size) lớn hơn thông thường.
    4.  Nhận diện các cột dữ liệu thẳng hàng theo tọa độ X để dựng thành Table.

### 4. Với tệp HTML
*   **Bản chất:** Cấu trúc cây DOM.
*   **Thuật toán parse của Agent:**
    1.  Parse cây DOM, loại bỏ các thẻ script, style, head, nav, footer.
    2.  Ánh xạ trực tiếp các thẻ Semantic HTML sang Markdown:
        *   `<h1>` đến `<h6>` ➔ `#` đến `######`
        *   `<p>` ➔ Đoạn văn
        *   `<a>` ➔ Link `[text](url)`
        *   `<ul>`, `<li>` ➔ Danh sách `-`

---

## 🚀 Quy trình thực thi của Agent

1.  **Bước 1: Kiểm tra định dạng:** Agent nhận diện extension của file đầu vào tại `doc-path`.
2.  **Bước 2: Kích hoạt Parser tương ứng:**
    *   Sử dụng script Python hoặc Node.js cục bộ (nếu có sẵn) hoặc tự áp dụng thuật toán đọc file nhị phân/XML tương ứng để trích xuất văn bản thô.
3.  **Bước 3: Xuất file Markdown:** Lưu file Markdown kết quả tại `.agents/context/temp_spec.md`.
4.  **Bước 4: Summary Context:** Đọc lại file Markdown vừa tạo, tóm tắt 3 điểm cốt lõi (Mục tiêu, Yêu cầu chức năng, Cấu trúc dữ liệu) và trình bày cho User trước khi đưa vào context làm việc.
