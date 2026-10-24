---
name: adk-notebooklm-research
description: Nghiên cứu và tổng hợp tài liệu bằng NotebookLM MCP khi người dùng yêu cầu dùng NotebookLM hoặc làm việc với notebook đã chọn. Không tự tạo, đồng bộ, ghi wiki hay xóa notebook nếu chưa được yêu cầu.
---

# Nghiên cứu bằng NotebookLM — adk-notebooklm-research

## 🎯 Mục tiêu
Giúp lập trình viên truy vấn và tổng hợp tri thức từ nguồn đã có trong NotebookLM.
NotebookLM là phương tiện research được yêu cầu, không phải bước mặc định của mọi
task nghiệp vụ.

---

## ⚙️ Quy Trình Thực Thi Của Agent

### Bước 1: Chọn nguồn
Nếu user chỉ định notebook, dùng notebook đó. Nếu chưa chỉ định nhưng yêu cầu rõ
NotebookLM, tra cứu danh sách notebook và hỏi/chọn theo chủ đề phù hợp:
*   **Tool:** `notebooklm.notebook_list`
*   *Hành động:* Quét danh sách để tìm xem đã có notebook nào về chủ đề này chưa.

### Bước 2: Tạo notebook khi được yêu cầu
Chỉ tạo notebook mới nếu user yêu cầu tạo hoặc xác nhận việc tạo là cần thiết.
Tuân theo naming convention từ `AGENTS.md` hoặc quy ước của người dùng; không áp
dụng tiền tố riêng của một project trong skill dùng chung.

### Bước 3: Nạp nguồn khi được yêu cầu
Chỉ thêm hoặc đồng bộ source theo yêu cầu rõ; thao tác này ghi dữ liệu ngoài chat:
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

### Bước 5: Trình bày kết quả
Tổng hợp kết quả bằng tiếng Việt, phân biệt thông tin có dẫn chứng từ nguồn với suy
luận. Ghi thành wiki/file chỉ khi user yêu cầu và đã xác định đúng đích ghi.

### Dọn dẹp
Không xóa notebook/source và không tự suy ra notebook nào đã hết hạn. Chỉ thực hiện
xóa khi user yêu cầu rõ và xác nhận đúng tài nguyên.

---

## 🛡️ Guardrails

* Không xem câu trả lời của NotebookLM là nguồn sự thật nếu không trích được tài liệu hỗ trợ.
* Đối chiếu công thức, quy định pháp lý và thông tin có hệ quả cao với source gốc.
* Không tạo, đồng bộ, ghi file hoặc xóa nếu intent của user không bao gồm thao tác đó.
