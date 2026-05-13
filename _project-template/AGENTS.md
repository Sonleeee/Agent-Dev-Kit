# Project: [Tên Project]

> File này là "passport" của project. Agent đọc file này đầu tiên khi nhận bất kỳ task nào.
> Điền đầy đủ các section dưới. Xóa comments (dòng bắt đầu bằng >) trước khi dùng.

---

## Identity

- **project-type:** [dotnet-clean-arch | react-vite | node-express | generic | ...]
  > Tra danh sách type trong `.agents/registry/index.md`
- **display-name:** [Tên hiển thị của project]
- **description:** [1 câu mô tả project làm gì]
- **agent-system-version:** 1.0.0

## Tech Stack

- **Backend:** [.NET 8 / Node 20 / Python 3.12 / N/A]
- **Frontend:** [React 18 / Vue 3 / Next.js 14 / N/A]
- **Database:** [PostgreSQL / MySQL / MongoDB / N/A]
- **Auth:** [JWT / OAuth2 / Session / N/A]
- **Infra:** [Docker / K8s / Serverless / N/A]

## Context Files

> Agent đọc các file này theo thứ tự khi load project context.

- **architecture:** `.agents/context/architecture.md`
- **checklist:** `.agents/context/checklist.md`
  > Xóa dòng này nếu dùng global master-checklist không có customization
- **rule-overrides:** `.agents/context/rule-overrides.approved.md`
  > Xóa dòng này nếu dùng global rules hoàn toàn

## Integrations

> Dùng để Agent-Dev-Kit ghi ngược tri thức có giá trị vào SecondBrain.

- **kit-path:** `.agents/`
- **vault-path:** `C:\Sonlee\AI\SecondBrain`
  > Sửa lại nếu SecondBrain vault nằm ở đường dẫn khác. Để trống nếu project không dùng writeback.

## Reference Modules

> Agent dùng các module này như "ground truth" khi sinh code.

- **BE pattern reference:** [src/path/to/reference-module/]
- **FE pattern reference:** [src/path/to/reference-module/]

## Team Context

- **Team size:** [solo / 2–5 / 5+]
- **Code review:** [required / optional]
- **Deploy frequency:** [daily / weekly / on-demand]

## Rule Overrides

> Nếu có override, tạo `.agents/context/rule-overrides.approved.md`
> và liệt kê ở đây để agent biết file đó tồn tại.

- rule-overrides: `.agents/context/rule-overrides.approved.md`
  > Xóa dòng này nếu không có override
