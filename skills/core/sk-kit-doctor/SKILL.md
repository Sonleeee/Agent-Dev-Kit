---
name: sk-kit-doctor
description: |
  Kỹ năng tự chẩn đoán (Health Check) và bảo trì hạ tầng hoạt động của Agent-Dev-Kit.
  Kiểm tra connectivity của các MCP, kiểm tra git config, kiểm tra cấu trúc thư mục core.
output: markdown (Bản báo cáo sức khỏe Health Report và danh sách các điểm tự động fix)
---

# 🏥 Trình Chẩn Đoán & Bảo Trì Hệ Thống — sk-kit-doctor

## 🎯 Mục tiêu

Đảm bảo môi trường làm việc của AI Agent (cổng kết nối MCP, các file rules cấu hình, file passport) luôn hoạt động hoàn hảo và đúng quy chuẩn, giúp phát hiện sớm các lỗi khiến Agent hoạt động sai hoặc mất kiểm soát.

> [!NOTE]
> **Phân biệt với [sk-context-update/SKILL.md](file:///c:/Sonlee/AI/Agent-Dev-Kit/skills/core/sk-context-update/SKILL.md):** 
> *   `sk-context-update` dùng để cập nhật tri thức nghiệp vụ và code templates của dự án.
> *   `sk-kit-doctor` dùng để kiểm tra lỗi hạ tầng và kết nối công cụ của Kit.

---

## 🔍 Quy trình Chẩn Đoán của Agent (SOP)

### Bước 1: Passport Audit (Kiểm tra Passport dự án)
*   Agent kiểm tra file `AGENTS.md` ở root thư mục dự án xem có tồn tại không.
*   Rà soát các trường bắt buộc trong file: `project-type`, `agent-system-version`, `kit-path`, `vault-path`.
*   *Nếu thiếu:* Cảnh báo cho user và chuẩn bị bổ sung.

### Bước 2: Structure & Rules Audit (Kiểm tra quy tắc)
*   Kiểm tra sự tồn tại của thư mục `.agents/context/` và các file tối thiểu: `architecture.md`, `checklist.md`.
*   Kiểm tra file cấu hình Git `.gitignore` xem đã bỏ qua các file log tạm, file nháp của agent chưa (như `.agents/scratch/`, `.env`).

### Bước 3: Connectivity & Tools Audit (Kiểm tra kết nối)
*   **MCP Connectivity:** Ping thử các MCP server đang chạy trên hệ thống (ví dụ: DBHub MCP, Chrome-devtools MCP, StitchMCP) để đảm bảo chúng phản hồi đúng quyền hạn và không bị tắt.
*   **Git connectivity:** Kiểm tra xem git credentials có hợp lệ để đẩy code/pull code không.

### Bước 4: Auto-Fix (Tự động khắc phục lỗi)
*   Nếu thiếu file template (ví dụ `checklist.md`), agent tự động copy từ thư mục `_project-template/` sang `.agents/context/`.
*   Tự động bổ sung các file nháp của agent vào `.gitignore` nếu chưa có.
*   Tạo lại thư mục `.agents/scratch/` nếu bị xóa.

---

## 📝 Health Report Template (Đầu ra bắt buộc)

Mỗi khi skill hoàn thành, Agent phải hiển thị báo cáo:

```markdown
### 🏥 Kit Health Report

#### 1. Trạng thái kiểm tra (Audit Status)
*   [ ] Passport `AGENTS.md` ➔ [OK / MISSING / INVALID]
*   [ ] Cấu trúc `.agents/context/` ➔ [OK / INCOMPLETE]
*   [ ] Kết nối MCP Servers ➔ [OK / FAILED]
*   [ ] Cấu hình `.gitignore` ➔ [OK / MISCONFIGURED]

#### 2. Các điểm đã tự động fix (Auto-fixed Items)
*   [Danh sách các lỗi đã được agent tự động sửa chữa]

#### 3. Khuyến nghị hành động (Recommendations)
*   [Các lỗi cần user can thiệp thủ công, ví dụ: Bật lại MCP server X]
```
