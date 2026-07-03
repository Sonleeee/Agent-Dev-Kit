---
name: sk-domain-research
description: |
  Kịch bản nghiên cứu domain nghiệp vụ mới sử dụng các MCP tools của NotebookLM.
  Tạo, truy vấn và dọn dẹp các notebooks nghiên cứu chuyên ngành.
inputs:
  - domain-topic: Chủ đề hoặc tài liệu nghiệp vụ cần nghiên cứu (ví dụ: Quy trình kiểm tra tạp chất Biomass)
output:
  - summary: Báo cáo tóm tắt quy tắc nghiệp vụ cốt lõi cho Dev
---

# Domain Research via NotebookLM — sk-domain-research

## 🎯 Mục tiêu
Giúp lập trình viên nhanh chóng tiếp cận và làm chủ các kiến thức nghiệp vụ ngoài ngành (như quy trình Logistics, chuỗi cung ứng sinh khối Biomass, đối soát tài chính...) bằng cách tự động hóa quy trình phân tích tài liệu thông qua hệ thống **NotebookLM**.

---

## ⚙️ Quy Trình Thực Thi Của Agent

### Bước 1: Tra cứu Notebook hiện có
Agent sử dụng công cụ MCP `notebooklm` để kiểm tra danh sách notebook hiện có nhằm tránh tạo trùng lặp:
*   **Tool:** `notebooklm.notebook_list`
*   *Hành động:* Quét danh sách để tìm xem đã có notebook nào về chủ đề này chưa.

### Bước 2: Tạo Notebook Nghiên cứu Mới
Nếu chưa có notebook phù hợp, Agent tạo mới một cái theo quy ước đặt tên thống nhất:
*   **Format tên:** `[TLBIOMASS] <Tên nghiệp vụ nghiên cứu>` (ví dụ: `[TLBIOMASS] Quy trình cân xe và đo ẩm`)
*   **Tool:** `notebooklm.notebook_create`

### Bước 3: Nạp tài liệu nguồn (Sources)
Agent thêm các tài liệu thô, giáo trình, hoặc thông tư quy định nghiệp vụ vào Notebook:
*   **Tool:** `notebooklm.source_add` hoặc `notebooklm.source_sync_drive` (nếu tài liệu nằm trên Google Drive).
*   *Tham số:* Truyền đường dẫn file hoặc drive link tương ứng.

### Bước 4: Truy vấn chưng cất Nghiệp vụ (Domain Extraction)
Agent gửi các truy vấn thông minh đến NotebookLM để trích xuất các quy tắc cốt lõi:
*   **Tool:** `notebooklm.notebook_query`
*   **Các câu hỏi truy vấn mẫu:**
    1.  *Khái niệm cốt lõi:* "Các định nghĩa, thuật ngữ và chỉ số đo lường quan trọng nhất trong tài liệu này là gì?"
    2.  *Quy trình/Luồng nghiệp vụ:* "Quy trình từng bước hoạt động của nghiệp vụ này diễn ra thế nào? Ai tham gia?"
    3.  *Ràng buộc kỹ thuật tiềm ẩn:* "Có các quy tắc validation dữ liệu, công thức toán học hoặc ràng buộc kiểm toán nào cần lưu ý?"
    4.  *Edge cases:* "Có các trường hợp đặc biệt, ngoại lệ hoặc rủi ro sai sót nào được đề cập trong tài liệu không?"

### Bước 5: Chưng cất kết quả thành Cẩm nang Dev (Wiki Entry)
*   Agent tổng hợp câu trả lời từ NotebookLM thành một cẩm nang kỹ thuật bằng Tiếng Việt.
*   Ghi nhận cẩm nang này vào `01_Wiki/02_Brain/` hoặc thư mục wiki tương ứng của dự án để đội ngũ Dev cùng tham khảo.

### Bước 6: Dọn dẹp tài nguyên (Notebook Lifecycle Cleanup)
Để tránh rác tài nguyên lưu trữ đám mây, các notebook phục vụ nghiên cứu ngắn hạn cần được dọn dẹp sau khi đã chưng cất xong tri thức:
*   **Tool:** `notebooklm.notebook_delete`
*   *Lưu ý:* Luôn báo cáo và xin xác nhận của User trước khi chạy lệnh delete.

---

## 🛡️ Guardrails

*   **Không giữ notebook rác:** Xóa bỏ các notebook hết hạn sử dụng (không truy cập > 30 ngày).
*   **Đặt tên đúng chuẩn:** TUYỆT ĐỐI tuân thủ tiền tố `[TLBIOMASS]` để phân biệt với các notebook cá nhân khác.
*   **Verify thông tin:** Dù NotebookLM trả về kết quả tốt, luôn đối chiếu các công thức toán học hoặc quy chuẩn pháp lý với tài liệu gốc trước khi đưa vào spec.
