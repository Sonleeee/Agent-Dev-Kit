# Architecture — [Project Name]

> File này định nghĩa guardrails kiến trúc cụ thể của project.
> Domain skills (backend/frontend) đọc file này để biết pattern cần follow.
> Điền theo thực tế project. Xóa sections không liên quan.

---

## Architecture Pattern

> Mô tả flow chuẩn từ entry point đến data layer.

**Flow:** [ví dụ: Controller → MediatR Handler → Repository → Database]

**Layer Responsibilities:**
- **[Layer 1]:** [làm gì, không làm gì]
- **[Layer 2]:** [làm gì, không làm gì]
- **[Layer 3]:** [làm gì, không làm gì]

---

## Error / Exception Handling

> Taxonomy lỗi chuẩn của project — giúp AI throw đúng exception đúng chỗ.

| Tình huống | Exception / Error Type | HTTP Status |
|---|---|---|
| Input không hợp lệ | [ValidationException] | 400 |
| Resource không tồn tại | [NotFoundException] | 404 |
| Vi phạm business rule | [BusinessException] | 400 |
| Unauthorized | [UnauthorizedException] | 401/403 |

**Anti-patterns (không được làm):**
- [ví dụ: Không throw InvalidOperationException cho business errors]
- [ví dụ: Không hardcode error message trong handler/controller]

---

## Naming Conventions

- **BE entities:** [PascalCase / camelCase / snake_case]
- **BE files:** [convention]
- **FE components:** [PascalCase]
- **FE files:** [kebab-case / camelCase]
- **API routes:** [/api/v1/resource-name]
- **DB tables:** [snake_case]

---

## Folder Structure

**Backend:**
```
[điền cấu trúc folder thực tế]
src/
├── [module]/
│   ├── [layer]/
│   └── ...
```

**Frontend:**
```
[điền cấu trúc folder thực tế]
src/
├── pages/
├── services/
├── components/
└── ...
```

---

## Known Anti-Patterns

> Những gì KHÔNG được làm trong project này — học từ kinh nghiệm thực tế.

- [anti-pattern 1]: [mô tả + tại sao tránh]
- [anti-pattern 2]: [mô tả + tại sao tránh]

---

## Known Pitfalls

> Lỗi hay gặp lặp đi lặp lại — documented để AI không lặp lại.

- [pitfall 1]: [mô tả + cách tránh]
- [pitfall 2]: [mô tả + cách tránh]
