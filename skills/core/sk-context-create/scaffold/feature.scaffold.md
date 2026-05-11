# Feature Template Scaffold

> Agent fill nội dung bên dưới cho mỗi feature/module type.
> Tạo 1 file `.md.template` cho mỗi scope (be/, fe/).

---

## Decision Questions

Trước khi code, agent trả lời các câu hỏi sau:

```
Q1: "{câu hỏi phân loại feature type}"
├─ A → dùng template section {X}
└─ B → dùng template section {Y}

Q2: "{câu hỏi về dependencies}"
├─ Có dependency → {handling}
└─ Không dependency → {default}
```

## Naming Placeholders

| Placeholder | Convention | Ví dụ |
|-------------|-----------|-------|
| `{ModuleName}` | PascalCase, singular | `Warehouse` |
| `{moduleName}` | camelCase, singular | `warehouse` |
| `{module-name}` | kebab-case, singular | `warehouse` |
| `{TABLE_NAME}` | UPPER_SNAKE_CASE | `WAREHOUSE` |

## Code Pattern Sections

### Pattern 1: {tên pattern}

✅ **Đúng:**
```{language}
{code mẫu chuẩn với placeholders}
```

❌ **Sai (Anti-pattern):**
```{language}
{code vi phạm pattern}
```

### Pattern 2: {tên pattern}

✅ **Đúng:**
```{language}
{code mẫu chuẩn}
```

❌ **Sai:**
```{language}
{code vi phạm}
```

<!-- Thêm sections cho mỗi confirmed pattern -->

## Checklist cuối file

Trước khi submit code, verify:

- [ ] Naming đúng convention (xem bảng Naming Placeholders)
- [ ] Follow đúng code pattern (xem sections ✅/❌ ở trên)
- [ ] Không vi phạm Known Anti-Patterns trong `architecture.md`
- [ ] Decision Questions đã trả lời đúng
- [ ] Build pass
