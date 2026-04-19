# Project Type Registry

Agent đọc file này sau khi có `project-type` từ `AGENTS.md` của project.

## Cách dùng

1. Agent đọc `AGENTS.md` ở project root → lấy `project-type`
2. Tìm `project-type` trong bảng dưới → biết `context-required` nào cần load
3. Load từ `[project-root]/.agents/context/` theo danh sách
4. Nếu không tìm thấy type → dùng `generic`, báo user

## Project Types

| Type ID | Tên | Tech Stack điển hình | Context Required | Templates |
|---|---|---|---|---|
| `dotnet-clean-arch` | .NET Clean Architecture | .NET 8, MediatR, EF Core, CQRS, DDD | architecture.md, checklist.md | templates/be/ |
| `dotnet-minimal-api` | .NET Minimal API | .NET 8, FastEndpoints, EF Core | architecture.md | templates/be/ |
| `node-express` | Node.js REST API | Node 20, Express, TypeScript, Prisma | architecture.md | templates/be/ |
| `node-nestjs` | NestJS | NestJS, TypeScript, TypeORM/Prisma | architecture.md | templates/be/ |
| `react-vite` | React SPA | React 18, TypeScript, Vite, Zustand | architecture.md, checklist.md | templates/fe/ |
| `react-nextjs` | Next.js | Next.js 14, TypeScript, App Router | architecture.md, checklist.md | templates/fe/ |
| `vue-vite` | Vue SPA | Vue 3, TypeScript, Pinia | architecture.md | templates/fe/ |
| `mobile-rn` | React Native | React Native, Expo, TypeScript | architecture.md | templates/fe/ |
| `fullstack-nextjs` | Full-stack Next.js | Next.js, Prisma, tRPC | architecture.md, checklist.md | templates/be/, templates/fe/ |
| `dotnet-clean-arch+react-vite` | .NET + React Full-stack | .NET 10, MediatR, EF Core, CQRS, DDD + React 18, Vite, MUI, react-hook-form, Zod | architecture.md, checklist.md | templates/be/, templates/fe/ |
| `python-fastapi` | Python FastAPI | Python 3.12, FastAPI, SQLAlchemy | architecture.md | templates/be/ |
| `generic` | Generic (fallback) | Bất kỳ | (none required) | (none) |

## Thêm Project Type Mới

Khi onboard project với tech stack chưa có trong bảng:
1. Copy `_project-template/` để có skeleton
2. Điền `architecture.md` với kiến trúc cụ thể của project
3. Tạo code templates trong `context/templates/` nếu cần
4. Thêm type mới vào bảng trên với đúng `context-required`
5. Đăng ký `project-type` trong `AGENTS.md` của project

> **Mở rộng:** Bảng trên là danh sách mẫu. Bạn có thể thêm bất kỳ
> project type nào. Chỉ cần đảm bảo `AGENTS.md` khai báo đúng type
> và `context/` folder có đủ files tương ứng.

## Context Load Order (theo project-type)

Khi agent load context cho project, thứ tự đọc:

```
1. [project-root]/AGENTS.md              ← identity, tech stack, pointers
2. [global]/.agents/rules/global.md      ← quality gates, guardrails chung
3. [project-root]/.agents/context/rule-overrides.approved.md  ← nếu có
4. [project-root]/.agents/context/architecture.md             ← kiến trúc project
5. [project-root]/.agents/context/checklist.md                ← nếu có custom
6. [global]/.agents/quality/master-checklist.md               ← nếu không có custom
7. [project-root]/.agents/context/templates/be/ hoặc fe/      ← code pattern ground truth
```

## Ghi chú

- `context-required` là minimum cần có. Project có thể thêm `rule-overrides.approved.md`, `checklist.md` tuỳ nhu cầu.
- Nhiều project cùng type → share template set, chỉ khác nhau ở `AGENTS.md` và `context/architecture.md`.
- Project dùng type `dotnet-clean-arch+react-vite` cần cả `templates/be/` VÀ `templates/fe/`.
