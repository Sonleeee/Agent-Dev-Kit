---
name: adk-paper-researcher
description: Thẩm định bài báo khoa học (arXiv, PDF, thuật toán AI/CS) theo phương pháp 3-Pass của Keshav, kiểm tra Ablation Study, truy vết Forward Citations chống lỗi thời và chuyển đổi công thức toán học sang mã nguồn thực thi (Karpathy Code-Bridge).
---

# Scientific Paper Researcher & Code-Bridge — adk-paper-researcher

## 🎯 Mục tiêu & Khi nào dùng

- **Mục tiêu:** Đọc, thẩm định phản biện và trích xuất giá trị thực thi từ các bài báo khoa học (`arXiv`, hội nghị NeurIPS/ICLR/ICML/ACL/OSDI, hoặc file PDF học thuật), biến công thức lý thuyết thành kiến trúc/code chạy được.
- **Khi nào dùng:**
  - Người dùng gửi link `arxiv.org`, DOI, tên bài báo khoa học hoặc file PDF nghiên cứu.
  - Cần kiểm chứng một thuật toán/kiến trúc từ paper trước khi áp dụng vào dự án.
  - Cần dịch công thức toán học (LaTeX equations) hoặc giả mã (pseudocode) trong paper sang code Python/TypeScript/Rust.
- **Không dùng khi:**
  - Tra cứu tài liệu API thư viện thông thường (dùng `adk-docs-seeker`).
  - Khảo sát repo mã nguồn mở thông thường không gắn với bài báo học thuật (dùng `adk-xia` hoặc `adk-deep-research`).

---

## 🔄 Quy Trình Thẩm Định 4 Bước (Academic Deconstruction Loop)

### Bước 1: 3-Pass Reading Protocol (Phương pháp S. Keshav)
Không đọc tuyến tính từ đầu đến cuối gây tràn context; đọc theo 3 lượt có chọn lọc:
1. **Pass 1 — Bird's-Eye Scan (5–10% nội dung):**
   - Đọc *Title, Abstract, Introduction, Section Headings* và *Conclusion*.
   - Xác định 5 chữ C: **Category** (loại bài báo), **Context** (nền tảng), **Correctness** (giả định có hợp lý không), **Contributions** (đóng góp mới thực sự là gì), **Clarity**.
2. **Pass 2 — Evidence & Figures Audit (Đọc biểu đồ & bảng số liệu):**
   - Kiểm tra các sơ đồ kiến trúc, bảng kết quả benchmark và đặc biệt là **Ablation Study (Bảng cắt bỏ từng thành phần)**.
3. **Pass 3 — Deep Mechanism Reconstruction (Tái tạo cơ chế lõi):**
   - Chỉ đào sâu vào đúng mục mô tả thuật toán/công thức toán học cần thiết để trả lời câu hỏi của người dùng hoặc để viết code.

### Bước 2: Adversarial Ablation & Citation Audit (Chống "Bẫy Quảng Cáo Học Thuật")
Trước khi khuyên người dùng áp dụng một paper, bắt buộc kiểm tra 3 câu hỏi phản biện:
1. **Ablation Truth Check:** Trong bảng *Ablation Study*, thành phần nào khi bỏ đi làm giảm hiệu năng nhiều nhất? (Chỉ giữ lại thành phần mang lại 80% giá trị thực; loại bỏ các module trang trí làm phức tạp hóa bài báo).
2. **Forward Citations & SOTA Check (Chống lỗi thời):** Dùng tìm kiếm web kiểm tra xem bài báo này từ khi xuất bản đến nay đã có bài báo mới nào chỉ ra điểm yếu, phản bác hoặc vượt qua (supersede) với chi phí thấp hơn chưa.
3. **Official Code vs. Paper Drift:** Kiểm tra xem tác giả có công bố repo mã nguồn chính thức (GitHub / PapersWithCode) không. Nếu có, ưu tiên đối chiếu code thực tế của tác giả với công thức trong bài báo (vì nhiều trick quan trọng chỉ nằm trong code chứ không viết trong paper).

### Bước 3: Karpathy Code-Bridge (Dịch Công Thức Toán Sang Code Tối Giản)
Khi người dùng cần hiểu sâu hoặc áp dụng thuật toán trong bài báo:
- Ánh xạ từng ký hiệu toán học trong công thức (ví dụ: $\alpha, \gamma, \mathcal{L}, W_q, K, V$) sang **tên biến có ý nghĩa trong lập trình** kèm chú thích kích thước/kiểu dữ liệu (`shape` / `type`).
- Viết một đoạn mã thực thi tối giản, tự chứa (Minimal Executable Reference — ưu tiên Python stdlib/NumPy/PyTorch hoặc ngôn ngữ của dự án) dưới 60 dòng để minh họa chính xác luồng chạy của công thức đó.

### Bước 4: Đánh giá Khả thi cho Dự Án (Production Viability Verdict)
Chốt rõ một trong 3 kết luận:
- **Adopt Core Mechanism:** Chỉ lấy công thức/thuật toán lõi (đã lược bỏ phần rườm rà qua Ablation Study) đưa vào code dự án.
- **Experimental PoC Only:** Cần chạy thử nghiệm trên tập dữ liệu nhỏ trước vì độ phức tạp tính toán/bộ nhớ cao.
- **Reject (Academic Hype):** Kết quả chỉ đẹp trên benchmark nhân tạo hoặc chi phí hạ tầng không xứng đáng với độ cải thiện nhỏ.

---

## 📋 Hợp Đồng Đầu Ra (`📄 Paper Deconstruction Report`)

```markdown
## 📄 Paper Audit: <Tên Bài Báo & Năm / Link arXiv>
- **verdict:** ADOPT_MECHANISM | EXPERIMENTAL_POC | REJECT_HYPE
- **official_code:** `<Link GitHub chính thức hoặc 'None'>`

### 1. Đóng góp cốt lõi & Kiểm toán Ablation (80/20 Signal)
- **Bài toán giải quyết:** <1-2 câu trực diện>
- **Thành phần quyết định hiệu năng (từ Ablation Study):** <Thành phần thực sự tạo ra khác biệt>
- **Thành phần có thể lược bỏ (Over-engineering trong paper):** <Phần rườm rà không cần mang vào code>

### 2. Karpathy Code-Bridge (Ánh xạ Toán học -> Code)
| Ký hiệu trong Paper | Tên biến trong Code | Ý nghĩa & Kiểu dữ liệu / Shape |
|---|---|---|
| `<Ký hiệu>` | `<variable_name>` | `<Giải thích ngắn gọn>` |

### 3. Rủi ro thực tế & Forward Citations
- **Giới hạn ẩn (Hidden Bottlenecks):** <Chi phí RAM/Latency/Edge cases mà tác giả ít nhấn mạnh>
- **Cập nhật mới hơn (nếu có):** <Các cải tiến hoặc phản biện sau khi bài báo ra đời>
```

---

## 🛡️ Guardrails

- **Zero Hallucinated Metrics:** Không tự suy diễn con số phần trăm cải thiện nếu không có trong bảng số liệu của bài báo.
- **Simplicity First (`R-MINIMAL-CODE`):** Không bê nguyên toàn bộ pipeline cồng kềnh của bài báo vào dự án sản xuất nếu chỉ cần 1 hàm tính điểm hoặc 1 cấu trúc dữ liệu lõi là đủ.
