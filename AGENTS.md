# Project: TL BIOMASS

> File này là "passport" của project. Agent đọc file này đầu tiên khi nhận bất kỳ task nào.

---

## Identity

- **project-type:** dotnet-clean-arch+react-vite
- **display-name:** TL BIOMASS
- **description:** Hệ thống quản lý thu mua và chế biến Biomass (hợp đồng bán hàng, kho, tồn kho, cấu hình, sản phẩm)
- **agent-system-version:** 1.0.0

## Tech Stack

- **Backend:** .NET 10, MediatR, EF Core, CQRS, Clean Architecture, DDD, FluentValidation
- **Frontend:** React 18, TypeScript, Vite, MUI (Material-UI), react-hook-form, Zod, Axios
- **Database:** PostgreSQL
- **Auth:** JWT
- **Infra:** Docker, docker-compose

## Context Files

> Agent đọc các file này theo thứ tự khi load project context.

- **architecture:** `.agents/context/architecture.md`
- **checklist:** `.agents/context/checklist.md`
  > Extend từ global master-checklist (38 items) + TLBIOMASS-specific items (T1–T8)
  > Checklist đầy đủ 38 items: `.agents/quality/checklists/master-standard.md` (project copy)

## Reference Modules

> **🛑 QUAN TRỌNG:** KHÔNG DÙNG 1 MODULE (như SalesContracts) ĐỂ COPY PASTE CHO MỌI TRƯỜNG HỢP.
> Các module thực tế rất đa dạng (có File, không File, có Export...). Do đó, thay vì copy từ module cũ, AI **BẮT BUỘC PHẢI DÙNG BỘ TEMPLATE CHUẨN MỰC** theo hướng dẫn sau:

- **BE Feature Template Guide (Ground Truth):** `.agents/context/templates/be/feature.md.template` -> Đọc file này đầu tiên để biết cách chọn file `.cs.template` phù hợp với nghiệp vụ.
- **BE Templates Folder:** `.agents/context/templates/be/templates/` -> Chứa các mã nguồn mẫu chuyên biệt cho CRUD cơ bản, xử lý FileStorage, Export Excel, và Delete Cascade.
- **FE pattern reference:** `TL_BIOMASS/src/pages/sale-contract/`
- **FE service reference:** `TL_BIOMASS/src/services/sale-contact/`

## Team Context

- **Team size:** 2–5
- **Code review:** optional
- **Deploy frequency:** on-demand

## Rule Overrides

Không có override — dùng global rules 100%.
