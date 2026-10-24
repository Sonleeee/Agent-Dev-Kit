# UI Design Craft Addon (`ui-design`)

Addon cung cấp kho **Design Archetypes**, **Token Compiler**, **Motion Physics Recipes (Emil Kowalski)**, **Component Blueprints kèm `break-ui` stress payloads**, bộ tính toán toán học **WCAG 2.2 Relative Luminance Contrast**, và trình kiểm toán **Anti-Slop UI Auditor** qua cả **MCP Server (Stdio)** lẫn **CLI** (Zero-Dependency Node.js ESM).

## Phạm vi

- **Tra cứu & khởi tạo Design Tokens:** Phối hợp cùng skill core `adk-ui-craft` để chọn đúng Archetype theo lĩnh vực, điều chỉnh 3 thông số Dials (`variance`, `motion`, `density`), và xuất `DESIGN.md` / `@theme` Tailwind v4 / CSS Variables / W3C DTCG JSON.
- **Kiểm chứng toán học & chống AI Slop:** Xác thực độ tương phản màu sắc chuẩn WCAG 2.2 AA/AAA và quét mã nguồn giao diện chấm điểm Impeccable 20/20.
- **Bảo vệ file an toàn:** `scaffold_design_contract` mặc định không ghi đè nếu `DESIGN.md` đã tồn tại (`overwrite=false`).

## Cài đặt

```powershell
adk addon add ui-design
# hoặc chạy trực tiếp:
node addons/ui-design/setup.js
# hoặc:
powershell -File addons/ui-design/setup.ps1
```

## Danh mục 7 MCP Tools

| Tool | Tác dụng |
|---|---|
| `search_design_archetypes` | Tìm kiếm & xếp hạng 8 Design Archetypes theo query, domain và khoảng cách Euclid với Dials (`variance`, `motion`, `density`) |
| `get_design_tokens` | Biên dịch token của Archetype ra `design-md`, `tailwind-v4`, `css-vars`, hoặc `dtcg-json` |
| `get_component_blueprint` | Lấy đặc tả Component Blueprint + công thức chuyển động vật lý + bộ test `break-ui` + code mẫu |
| `verify_color_contrast` | Tính toán chính xác độ tương phản màu theo WCAG 2.2 Relative Luminance và gợi ý mã màu đạt chuẩn nếu `FAIL` |
| `audit_ui_code` | Gọi `ui_slop_auditor.py` (kèm JS fallback) để chấm điểm Impeccable 20/20 |
| `fix_ui_slop` | Tự động sửa các lỗi UI Anti-Slop tĩnh (`transition-all`, `100vh`, `scale-0`, thiếu `focus-visible:ring`) |
| `scaffold_design_contract` | Sinh hợp đồng thiết kế `DESIGN.md` chuẩn vào `target_dir/DESIGN.md` |

## Chế độ CLI (Dual-Mode)

```bash
node addons/ui-design/mcp-server/index.js --help
node addons/ui-design/mcp-server/index.js search fintech
node addons/ui-design/mcp-server/index.js tokens linear-precision-dark tailwind-v4
node addons/ui-design/mcp-server/index.js component data-table
node addons/ui-design/mcp-server/index.js contrast "#A1A1AA" "#09090B" AA
node addons/ui-design/mcp-server/index.js audit ./src
node addons/ui-design/mcp-server/index.js fix ./src
node addons/ui-design/mcp-server/index.js scaffold stripe-fintech-clarity ./my-app
```
