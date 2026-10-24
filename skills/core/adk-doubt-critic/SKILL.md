---
name: adk-doubt-critic
description: Phản biện một yêu cầu, thiết kế hoặc đoạn code khi người dùng yêu cầu ý kiến đối kháng, hoặc khi rủi ro đáng kể cần kiểm tra giả định độc lập. Không chạy mặc định sau mỗi phase.
---

# 🕵️ Kỹ Năng Tự Phản Biện Đối Kháng — adk-doubt-critic

## 🎯 Mục tiêu

Giúp AI Coding Agent (Antigravity, Claude Code, Codex, Cursor...) tự động đóng vai trò là một **kẻ phản biện đối kháng (Adversarial Critic)** để rà soát, nghi ngờ và tối ưu hóa các quyết định của chính mình ở mọi giai đoạn phát triển phần mềm, thay vì chấp nhận các phương án dễ dàng.

---

## 🤖 Hướng dẫn cho Agent (Core Instructions)

Chỉ kích hoạt khi người dùng yêu cầu phản biện, hoặc một quyết định rủi ro cao cần
kiểm tra giả định độc lập. Chọn góc nhìn theo đối tượng đang xét; không chạy đủ các
phase chỉ vì task có brainstorm, plan hoặc implement.

*   Nếu có tham số `--clarify` hoặc nhắc đến "yêu cầu / brainstorm / làm rõ": Chạy **Chế độ Phản biện Yêu cầu**.
*   Nếu có tham số `--plan` hoặc nhắc đến "kế hoạch / thiết kế / kiến trúc / giải pháp": Chạy **Chế độ Phản biện Thiết kế**.
*   Nếu có tham số `--impl` hoặc đưa ra đoạn code cụ thể: Chạy **Chế độ Phản biện Code** (Mặc định).

---

## 🔍 Chi tiết các Chế độ Thực thi

### 1. Chế độ Phản biện Yêu cầu (`--clarify`)

Áp dụng trong giai đoạn brainstorm, thu thập yêu cầu từ User.

#### Quy trình thực hiện (SOP):
*   **Bước 1: Ingestion (Đọc yêu cầu thô):** Quét toàn bộ mô tả tính năng của User.
*   **Bước 2: Claim Extraction (Trích xuất giả định nghiệp vụ):** Liệt kê các giả định ngầm trong yêu cầu.
    *   *Ví dụ:* "Yêu cầu ghi nhận là lưu thông tin đơn hàng, giả định rằng hệ thống thanh toán luôn thành công."
*   **Bước 3: Adversarial Doubt (Đặt câu hỏi đối kháng):** Đặt ra các kịch bản ngoại lệ mà yêu cầu chưa định nghĩa:
    *   *Mâu thuẫn logic:* "Nếu luồng thanh toán lỗi nhưng trừ tiền rồi thì xử lý thế nào?"
    *   *Trải nghiệm người dùng:* "Trạng thái hiển thị cho người dùng lúc chờ phản hồi từ cổng thanh toán là gì?"
    *   *Thiếu sót dữ liệu:* "Có cần lưu lại ID giao dịch của bên thứ ba không?"
*   **Bước 4: Report:** Trình bày danh sách các câu hỏi làm rõ (Elicitation Questions) dưới dạng **Doubt Report - Clarify** cho User để thống nhất spec.

---

### 2. Chế độ Phản biện Thiết kế (`--plan`)

Áp dụng sau khi đã có Spec rõ ràng và trước khi bắt tay viết code.

#### Quy trình thực hiện (SOP):
*   **Bước 1: Read Plan:** Đọc kỹ bản kế hoạch cài đặt (Plan) và kiến trúc hệ thống đề xuất.
*   **Bước 2: Design Criticism (Phản biện thiết kế):** Rà soát bản thiết kế theo 4 khía cạnh bảo mật, hiệu năng, sự đồng bộ và độ phức tạp:
    *   *Bảo mật:* "Thiết kế này có nguy cơ bị SQL Injection, IDOR hay lộ dữ liệu nhạy cảm không?"
    *   *Hiệu năng:* "Truy vấn DB trong vòng lặp này có gây lỗi N+1 không? Có cần cache không?"
    *   *Độ phức tạp:* "Giải pháp này có quá phức tạp không? Có thể đơn giản hóa bằng các thư viện/helper có sẵn không?"
    *   *Anti-patterns:* "Thiết kế này có vi phạm nguyên lý SOLID hay quy ước kiến trúc của dự án không?"
*   **Bước 3: Reconcile Plan (Cải tiến thiết kế):** Điều chỉnh bản kế hoạch thiết kế, bổ sung các phương án fallback, tối ưu hóa DB schema hoặc cấu trúc class.
*   **Bước 4: Report:** Trình bày bản kế hoạch đã được tối ưu hóa kèm theo ghi chú giải thích lý do thay đổi.

---

### 3. Chế độ Phản biện Code (`--impl` - Mặc định)

Áp dụng sau khi viết code xong hoặc trong lúc review code hiện tại.

#### Quy trình thực hiện (SOP):
Áp dụng quy trình **Doubt-driven Development (DDD)** theo chuỗi:

$$\text{CLAIM} \rightarrow \text{EXTRACT} \rightarrow \text{DOUBT} \rightarrow \text{RECONCILE} \rightarrow \text{STOP}$$

*   **Bước 1: CLAIM (Giả định của Code):** Đọc code và trích xuất các giả định của lập trình viên.
    *   *Ví dụ:* "Code giả định biến `data` truyền từ API luôn có giá trị."
*   **Bước 2: EXTRACT (Trích xuất điểm yếu):** Tìm các vị trí nhạy cảm dễ gây crash hoặc lỗi bảo mật.
*   **Bước 3: DOUBT (Nghi ngờ lỗi):** Tự đặt câu hỏi phá vỡ code:
    *   *Null pointer:* "Nếu `data` bị null hoặc undefined thì dòng X có gây crash không?"
    *   *Bảo mật:* "Dữ liệu đầu vào ở dòng Z đã được validate chống XSS chưa?"
    *   *Tài nguyên:* "Kết nối DB ở dòng Z đã được giải phóng (dispose) trong block `finally` chưa?"
*   **Bước 4: RECONCILE (Tái cấu trúc bảo vệ):** Sửa lại code, thêm các kiểm tra an toàn (Guard clauses), try-catch, validate input.
*   **Bước 5: STOP (Nghiệm thu):** Tự chạy thử test case để chắc chắn code sửa đổi hoạt động hoàn hảo.

---

## 📝 Doubt Report Template (Đầu ra bắt buộc)

Mỗi khi skill hoàn thành, Agent phải xuất ra báo cáo theo cấu trúc:

```markdown
### 🕵️ Doubt Report [--clarify / --plan / --impl]

#### 1. Các điểm nghi vấn phát hiện (Detected Doubts)
*   **[Độ nghiêm trọng: 🔴 Critical / 🟠 High / 🟡 Medium]** — [Vị trí/Yêu cầu]
    *   *Nghi vấn:* [Mô tả chi tiết nghi vấn/rủi ro]
    *   *Hệ quả tiềm ẩn:* [Nếu xảy ra thì hệ thống sẽ thế nào]

#### 2. Giải pháp điều chỉnh (Reconciliation Actions)
*   [ ] [Mô tả giải pháp gia cố cho từng điểm nghi vấn ở trên]

#### 3. Kết luận an toàn (Verdict)
*   [PASS / CONDITIONAL PASS / FAIL]
```
