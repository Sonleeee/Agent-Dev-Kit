---
name: sk-web-cleaner
description: |
  Kỹ năng làm sạch nội dung trang web (Web Clipping) lưu tại `00_Raw/` bằng script cục bộ.
  Bóc tách quảng cáo, menu điều hướng, script, style và xuất ra Markdown sạch sẽ.
inputs:
  - input_path: Đường dẫn file HTML thô hoặc Markdown thô cần làm sạch
  - output_path: Đường dẫn file kết quả Markdown sạch
---

# Web Cleaner — sk-web-cleaner

## 🎯 Mục tiêu
Giúp AI Agent tự động dọn dẹp các tài liệu tải về từ internet (Web Clippings) bị lẫn nhiều rác HTML (header, footer, nav, ads, scripts, CSS) thành tài liệu Markdown thuần túy sạch sẽ để làm dữ liệu tri thức đáng tin cậy.

---

## 🚀 Quy Trình Thực Thi Của Agent

### Bước 1: Chạy script làm sạch cục bộ
Agent kích hoạt script Python dọn dẹp offline bằng lệnh terminal:
```bash
python .agents/skills/research/sk-web-cleaner/scripts/defuddle_cleaner.py <input_path> <output_path>
```

### Bước 2: Đọc và sử dụng kết quả
*   Script sẽ xử lý file HTML/Markdown thô, bóc tách toàn bộ thành phần rác và ghi lại Markdown sạch tại `<output_path>`.
*   Agent đọc file kết quả để đưa vào làm tri thức tham khảo hoặc tài liệu của dự án.

---

## 🛡️ Guardrails

*   **Không phụ thuộc thư viện ngoài:** Script chạy hoàn toàn ngoại tuyến và zero-dependency (chỉ dùng Python standard library).
*   **Bảo toàn liên kết (Links) và Cấu trúc:** Bảo toàn các thẻ tiêu đề (`h1`-`h6`), liên kết (`a`), bảng biểu (`table`), danh sách (`ul`/`ol`), và các khối code (`pre`/`code`) quan trọng.
*   **Loại bỏ triệt để boilerplate:** Loại bỏ các thành phần lặp đi lặp lại ở mọi trang web như thanh menu điều hướng, sidebar chia sẻ mạng xã hội, các biểu ngữ khuyến mãi/quảng cáo.
