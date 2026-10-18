# Repo: Agent-Dev-Kit (Tầng 1 — Core Kit)

> File này là "passport" của **chính repo Agent-Dev-Kit**: bộ khung workflows, rules, skills và template dùng chung. Agent đọc file này khi làm việc **trong repo phát triển/maintain kit**.

---

## Identity

- **project-type:** agent-dev-kit (meta — không phải ứng dụng nghiệp vụ)
- **display-name:** Agent-Dev-Kit
- **description:** Bộ công cụ và quy ước giúp AI agent code đúng pattern, giữ quality gates, tích lũy tri thức — nhân bản vào dự án qua thư mục kit (thường mount dưới tên `.agents/`).
- **agent-system-version:** 0.6.1

## Phạm vi repo này (tránh nhầm với dự án app)

- Repo này **không** phải source một sản phẩm cụ thể (ví dụ TL BIOMASS hay web app bất kỳ).
- Danh tính và tech stack của **ứng dụng** nằm ở **Tầng 2**: file `AGENTS.md` ở **root của từng repo dự án**, và `.agents/context/` trong repo đó. Thông tin đó **chỉ** sửa/thêm trong repo của dự án đó, không ghi vào đây.

## Tech stack (bản thân kit)

- **Định dạng:** Markdown, cấu trúc thư mục theo convention (portable mọi IDE có AI).
- **Code runtime:** không có — kit là tài liệu + workflow + template.

## Context & điểm vào chính (đọc theo thứ tự khi onboard kit)

- **hành vi agent:** `SYSTEM.md`
- **tổng quan & cách dùng:** `README.md`
- **luồng end-to-end:** `HowItWorks.md`
- **quality gates:** `rules/global.md`
- **execution contract:** `skills/core/sk-execution-contract/SKILL.md` + `templates/execution-contract.md.template`
- **mẫu passport cho app (Tầng 2):** `templates/AGENTS.md.template` — copy ra root repo dự án rồi điền theo app

## Integrations

- **kit-path:** `C:\Sonlee\AI\Agent-Dev-Kit`

## Nội dung chính trong repo

| Khu vực | Vai trò |
|--------|---------|
| `workflows/` | Lệnh `/wf-clarify`, `/wf-plan`, `/wf-impl`, `/wf-review`, … |
| `skills/` | Skill theo domain (core, devops, security, …) |
| `agents/` | Persona hệ thống |
| `templates/` | Template output |
| `addons/` | Mở rộng tùy chọn (codegraph, archify, database, …) |

## Team Context (repo kit)

- **Team size:** nhỏ (maintainer + contributors)
- **Code review:** khuyến nghị khi đổi workflow/rules ảnh hưởng rộng
- **Release:** theo CHANGELOG / tag

## Rule Overrides

Không có override riêng cho repo kit — giữ `rules/global.md` làm nguồn chuẩn trừ khi tài liệu kit quy định khác.
