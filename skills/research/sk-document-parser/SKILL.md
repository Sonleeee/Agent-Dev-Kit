---
name: sk-document-parser
description: |
  Kỹ năng tự động parse tài liệu nghiệp vụ (PDF, Word, Excel, PowerPoint, HTML) sang định dạng Markdown.
  Hoạt động theo cơ chế Lai (Hybrid): Ưu tiên parse native zero-dependency, nâng cấp thông qua Microsoft MarkItDown.
inputs:
  - doc-path: Đường dẫn tuyệt đối đến file cần parse (.pdf, .docx, .xlsx, .pptx, .html)
output: markdown (Lưu tại .agents/context/temp_spec.md)
---

# 📄 Bộ Chuyển Đổi Tài Liệu Nghiệp Vụ Lai — sk-document-parser

## 🎯 Mục tiêu

Giúp AI Agent tự động phân tích cấu trúc tệp tin nghiệp vụ thô của khách hàng (hoặc tài liệu thiết kế hệ thống) và chuyển đổi chúng thành định dạng Markdown sạch sẽ để làm ngữ cảnh (ground truth context) phục vụ lập trình.

---

## 🏗️ Thiết Kế Lai (Hybrid Architecture)

Kỹ năng này hoạt động thông qua một file script chạy chung đặt tại **[parser.py](file:///c:/Sonlee/AI/Agent-Dev-Kit/skills/research/sk-document-parser/parser.py)** với cơ chế thông minh:

### 1. Phân Tích Native (Zero-Dependency)
*   **Định dạng hỗ trợ:** Word (`.docx`), HTML (`.html`, `.htm`).
*   **Nguyên lý:** Giải nén XML cấu trúc (đối với Word) hoặc parse cấu trúc cây DOM (đối với HTML) trực tiếp thông qua thư viện chuẩn có sẵn của Python (`zipfile`, `xml.etree`, `html.parser`).
*   **Đặc điểm:** Không yêu cầu cài đặt thêm thư viện ngoài, chạy được ở mọi nơi, bảo đảm tính di động tuyệt đối.

### 2. Phân Tích Nâng Cao (Microsoft MarkItDown Integration)
*   **Định dạng hỗ trợ:** PDF (`.pdf`), Excel (`.xlsx`), PowerPoint (`.pptx`), Zip (`.zip`), v.v.
*   **Nguyên lý:** Script sẽ tự động kiểm tra sự tồn tại của thư viện `markitdown` trong môi trường:
    *   *Nếu có:* Gọi thư viện `MarkItDown` để trích xuất dữ liệu với độ chính xác cao nhất.
    *   *Nếu chưa có:* Xuất cảnh báo hướng dẫn User cài đặt bằng lệnh `pip install markitdown` hoặc đề xuất chuyển đổi file sang định dạng Word/HTML để chạy ở chế độ Native.

---

## 🚀 Quy Trình Thực Thi Của Agent

1.  **Bước 1: Gọi script thực thi:** Agent chạy lệnh command line để kích hoạt script lai:
    ```bash
    python c:/Sonlee/AI/Agent-Dev-Kit/skills/research/sk-document-parser/parser.py <doc-path> c:/Sonlee/AI/Agent-Dev-Kit/context/temp_spec.md
    ```
2.  **Bước 2: Xử lý phản hồi:**
    *   *Trường hợp thành công:* Agent đọc file `.agents/context/temp_spec.md` vừa được tạo ra.
    *   *Trường hợp lỗi thiếu thư viện:* Agent hiển thị hướng dẫn cài đặt `markitdown` của script cho User và chờ User cài đặt, hoặc đề xuất đổi định dạng file.
3.  **Bước 3: Tóm tắt ngữ cảnh:** Agent phân tích file Markdown kết quả, tóm tắt các thông tin quan trọng nhất (Yêu cầu chức năng, Cấu trúc DB, Giao diện) để nạp vào bộ nhớ làm việc.
