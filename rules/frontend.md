---
trigger: glob
paths:
  - "**/src/frontend/**/*"
  - "**/*.{css,scss,html,jsx,tsx,vue,svelte}"
---

# Frontend Rules

Các quy tắc áp dụng riêng cho UI/Frontend và thiết kế giao diện.

## Nhóm 1 — UI/UX Aesthetics [OVERRIDABLE]

### Modern Design [OVERRIDABLE]
- Luôn ưu tiên giao diện hiện đại: dark mode, glassmorphism, và vibrant colors.
- Sử dụng typography từ Google Fonts (Inter, Roboto, Outfit).
- Tránh màu sắc cơ bản (pure blue/red), dùng bảng màu HSL hài hòa.

### Micro-animations [OVERRIDABLE]
- Thêm các transition/hover effect nhẹ nhàng cho các thành phần tương tác.
- Đảm bảo giao diện cảm giác "alive" và phản hồi nhanh.

## Nhóm 2 — Code Style [OVERRIDABLE]

### Naming Convention [OVERRIDABLE]
- Các component files dùng PascalCase (ví dụ: `HeaderNav.tsx`).
- Variables/Functions dùng camelCase.
- CSS classes dùng BEM hoặc camelCase tùy project context.

### Semantic HTML [PROTECTED]
- Luôn dùng thẻ HTML5 ngữ nghĩa (header, footer, main, section, nav).
- Đảm bảo cấu trúc heading H1-H6 phân cấp đúng.

## Nhóm 3 — Components [OVERRIDABLE]

### Clean Components [OVERRIDABLE]
- Giữ component nhỏ, tập trung (Single Responsibility).
- Tách logic ra khỏi view (hợp tác với hooks nếu dùng React).
