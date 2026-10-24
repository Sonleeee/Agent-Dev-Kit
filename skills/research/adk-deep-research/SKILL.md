---
name: adk-deep-research
description: Nghiên cứu chuyên sâu đa nguồn (Web, GitHub Reference Repos, Papers, SecondBrain, NotebookLM) khi người dùng yêu cầu deep research, khảo sát hệ sinh thái hoặc đánh giá toàn diện một công nghệ/kiến trúc lớn. Không dùng cho tra cứu API/docs nhanh khi đang code (dùng adk-docs-seeker).
---

# Deep Research & Multi-Source Synthesis — adk-deep-research

## 🎯 Phân biệt ranh giới với Research thường

| Tiêu chí | Research Nhanh (`adk-docs-seeker` / `adk-pattern-researcher`) | Deep Research (`adk-deep-research`) |
| :--- | :--- | :--- |
| **Mục đích** | Giải quyết câu hỏi kỹ thuật tức thời khi đang code (cú pháp API, chọn 1 trong 2 pattern). | Khảo sát hệ sinh thái, thẩm định công nghệ mới, mổ xẻ kiến trúc nhiều repo/bài báo để lập chiến lược. |
| **Nguồn dữ liệu** | 1–2 nguồn (Official Docs, Context7, System Design MCP). | Đa tầng: GitHub Reference Repos, Papers/ArXiv, Web/Community, SecondBrain Vault, NotebookLM. |
| **Đầu ra** | Câu trả lời gọn + Code snippet ngay trong chat. | Báo cáo tổng hợp có **Ma trận đối soát**, **Provenance/Citation** và **Bản đồ tích hợp (Adoption Plan)**. |

---

## 🚀 Quy Trình Thực Thi 5 Bước (Multi-Source Synthesis)

### Bước 1: Định khung câu hỏi nghiên cứu (Research Framing)
Trước khi tìm kiếm, chốt rõ 3 trục:
1. **Core Question:** Cần trả lời quyết định kỹ thuật/sản phẩm nào?
2. **Inclusion / Exclusion Criteria:** Loại bỏ các nguồn rác (blog SEO, bài viết thiếu căn cứ kỹ thuật, repo bỏ hoang) và xác định phạm vi (ví dụ: chỉ lấy giải pháp zero-dependency, local-first, hoặc production-ready).
3. **Evaluation Axes:** Các trục đem ra cân đo (Kiến trúc cốt lõi, Chi phí token/hạ tầng, Độ phức tạp tích hợp, Rủi ro bảo mật/lock-in).

### Bước 2: Thu thập đa nguồn theo phân tầng (Tiered Source Gathering)
Khai thác nguồn theo thứ tự độ tin cậy giảm dần:
1. **Tầng 1 — Mã nguồn & Đặc tả gốc (Reference Coding — kế thừa `xerj`):**
   - Đọc trực tiếp cấu trúc repo, schema, file cấu hình hoặc mã nguồn thực thi của các dự án chuẩn mực thay vì chỉ đọc README quảng cáo.
2. **Tầng 2 — Kho tri thức nội bộ (SecondBrain / NotebookLM nếu khả dụng):**
   - Kiểm tra xem chủ đề đã có ghi chú trong Obsidian Vault (`01_Wiki/`, `00_Raw/`) hoặc NotebookLM (`adk-notebooklm-research` trong addon) chưa để kế thừa tri thức sẵn có.
3. **Tầng 3 — Web, Bài báo học thuật & Thảo luận thực chiến:**
   - Tìm kiếm các báo cáo kỹ thuật, arXiv papers, GitHub Issues/Discussions hoặc post-mortem thực tế từ kỹ sư đi trước.
   - Nếu cần bóc tách trang web/tài liệu dài, gọi các skill trong addon (`adk-web-cleaner`, `adk-document-parser` thuộc `addons/obsidian`).

### Bước 3: Đối chiếu chéo & Giải phẫu cơ chế (Mechanism Deconstruction)
Với mỗi nguồn/repo được chọn, tuyệt đối **không tóm tắt bề mặt**; phải bóc tách:
- **Bản chất cơ chế (How it actually works):** Nó giải quyết bài toán bằng cấu trúc dữ liệu, giao thức hay thuật toán gì?
- **Điểm đột phá thật vs Quảng cáo (Signal vs Hype):** Phần nào là kỹ thuật thực chất, phần nào chỉ là wrapper/marketing?
- **Giới hạn & Cái giá phải trả (Hidden Costs):** Đánh đổi về latency, memory, dependency hay độ khó bảo trì là gì?

### Bước 4: Lập Ma Trận Đối Soát & Phân Tầng Áp Dụng
Tổng hợp thành bảng so sánh trực diện và phân loại rõ:
- **Adopt (Hấp thụ cơ chế ngay):** Lấy nguyên lý/thuật toán đưa vào dự án hiện tại.
- **Trial / Addon (Thử nghiệm tách biệt):** Đóng gói làm addon/PoC tùy chọn, không làm phình Core.
- **Hold / Reject (Loại bỏ):** Không phù hợp ngữ cảnh hoặc gây bloatware.

### Bước 5: Kiểm định Provenance & Bàn giao
- Mọi nhận định kỹ thuật quan trọng phải gắn kèm link nguồn (URL hoặc đường dẫn file cục bộ).
- Phân biệt rõ **Fact từ nguồn** và **Đánh giá/Đề xuất của Agent**.
- Không tự ý ghi đè vào Obsidian Vault hay sửa code dự án nếu người dùng chỉ yêu cầu nghiên cứu.

---

## 🛡️ Guardrails

- **Chống "Bịa Nguồn" (Zero Hallucinated Citations):** Tuyệt đối không tự chế URL, số sao GitHub hay kết quả benchmark nếu chưa đọc từ nguồn thật.
- **Cấm Bơm Phồng (Anti-Bloat):** Khi đề xuất tích hợp kết quả nghiên cứu vào dự án, luôn ưu tiên học **cơ chế/giao thức nhẹ nhất** thay vì kéo cả thư viện/runtime nặng vào hệ thống.
