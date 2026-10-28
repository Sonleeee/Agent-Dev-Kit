# Repo: Agent-Dev-Kit (Tầng 1 — Core Kit)

> File này là "passport" của **chính repo Agent-Dev-Kit**: bộ khung rules, skills, agent personas và template dùng chung. Agent đọc file này khi làm việc **trong repo phát triển/maintain kit**.

---

## Identity

- **project-type:** agent-dev-kit (meta — không phải ứng dụng nghiệp vụ)
- **display-name:** Agent-Dev-Kit
- **description:** Bộ công cụ và quy ước giúp AI agent code đúng pattern, giữ quality gates, tích lũy tri thức — nhân bản vào dự án qua thư mục kit (thường mount dưới tên `.agents/`).
- **agent-system-version:** 0.9.0

## Phạm vi repo này (tránh nhầm với dự án app)

- Danh tính và tech stack của **ứng dụng** nằm ở **Tầng 2**: file `AGENTS.md` ở **root của từng repo dự án**, và `.agents/context/` trong repo đó. Thông tin đó **chỉ** sửa/thêm trong repo của dự án đó, không ghi vào đây.

## Tech stack (bản thân kit)

- **Tri thức & Giao thức:** Markdown theo chuẩn Agent Skills & Directory Conventions (portable 100% mọi IDE/host có AI).
- **Runtime & Tooling hỗ trợ:** Python, Shell/PowerShell, Lifecycle Hooks (`hooks.json`), MCP Servers và executable scripts trong skills (đảm bảo tính tự động hóa và kiểm soát xác định — deterministic execution).

## Context & điểm vào chính (đọc theo thứ tự khi onboard kit)

- **hành vi agent:** `SYSTEM.md`
- **tổng quan & cách dùng:** `README.md`
- **quality gates:** `rules/global.md`
- **execution contract:** `skills/core/adk-execution-contract/SKILL.md` + `templates/execution-contract.md.template`
- **mẫu passport cho app (Tầng 2):** `templates/AGENTS.md.template` — copy ra root repo dự án rồi điền theo app
- **mẫu hợp đồng UI & design token:** `templates/DESIGN.md.template` — đặc tả thẩm mỹ, token và anti-slop rules cho frontend

## Integrations

- **kit-path:** `C:\Sonlee\AI\Agent-Dev-Kit`

## Nội dung chính trong repo

| Khu vực | Vai trò |
|--------|---------|
| `skills/` | Kho Agent Skills theo domain (core, devops, testing, research, security, meta) |
| `rules/` | Guardrails và invariants luôn kích hoạt (`global.md`) |
| `agents/` | Persona hệ thống (inline hoặc delegate theo host) |
| `templates/` | Template output (design tokens, contracts, checklists) |
| `addons/` | Mở rộng tùy chọn (codegraph, database, system-design, obsidian, notebooklm...) |

## Team Context (repo kit)

- **Team size:** nhỏ (maintainer + contributors)
- **Code review:** khuyến nghị khi đổi workflow/rules ảnh hưởng rộng
- **Release:** theo CHANGELOG / tag

## Ranh Giới An Toàn (Invariants)

- **Always (Ground-Truth First):** Bắt buộc chạy `read_file` kiểm tra mã nguồn và CLI hiện tại TRƯỚC KHI đề xuất giải pháp, thêm cờ (flag), hoặc sửa code. Tuyệt đối không phán đoán dựa trên giả định.
- **Never (Ponytail Rule — R-MINIMAL-CODE):** Tuyệt đối không tự ý thêm cờ CLI, wrapper, helper hoặc abstraction mới khi chưa có ít nhất 3 ca sử dụng thực tế hoặc chưa có yêu cầu rõ ràng từ người dùng. Đoạn code tốt nhất là đoạn code không phải viết.
- **Ask First:** Hỏi người dùng trước khi thực hiện hành vi có side effect lớn (commit/push, xóa file hàng loạt, thay đổi kiến trúc cốt lõi).

## Rule Overrides

Không có override riêng cho repo kit — giữ `rules/global.md` làm nguồn chuẩn trừ khi tài liệu kit quy định khác.
