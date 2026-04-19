# Project Checklist — TL BIOMASS

> Extend từ global `quality/master-checklist.md` (38 items) + `quality/feature-bug-gates.md`.
> File này chỉ chứa items BỔ SUNG hoặc OVERRIDE cho TLBIOMASS.

---

## Dùng Global (không thay đổi)

Checklist gốc: `[global]/.agents/quality/master-checklist.md` — dùng toàn bộ 38 items.
Quality gates: `[global]/.agents/quality/feature-bug-gates.md` — Feature/Bug gates.
Decision tree: `[global]/.agents/quality/mapping-rules.md`.

---

## Items Bổ Sung — TLBIOMASS Specific

| # | Nhóm | Item | Kết quả | Evidence |
|---|---|---|---|---|
| T1 | FE Pattern | Nút Save/Submit có `disabled={isSubmitting}` chống double submit | [ ] Pass / [ ] Fail / [ ] N/A | |
| T2 | FE Pattern | Error toast dùng `response.errors?.[0]` (KHÔNG dùng `response.message`) | [ ] Pass / [ ] Fail / [ ] N/A | |
| T3 | FE Pattern | Không có hardcoded text — tất cả qua locales keys | [ ] Pass / [ ] Fail / [ ] N/A | |
| T4 | FE Pattern | i18n keys thêm vào cả `vi.json` VÀ `en.json` | [ ] Pass / [ ] Fail / [ ] N/A | |
| T5 | FE Pattern | Tab count (nếu có) build từ `data.summary`, không hardcode | [ ] Pass / [ ] Fail / [ ] N/A | |
| T6 | BE Pattern | Handler không chứa query filter/sort/paging — nằm ở repository | [ ] Pass / [ ] Fail / [ ] N/A | |
| T7 | BE Pattern | Exception taxonomy đúng: not-found → `NotFoundException`, business error → `BusinessException` | [ ] Pass / [ ] Fail / [ ] N/A | |
| T8 | BE Pattern | Error message/code tập trung tại `Domain/Constants/ErrorMessages/` | [ ] Pass / [ ] Fail / [ ] N/A | |
| T9 | BE Pattern | Chỉ inject `ICurrentInternalUserResolver` khi module thực sự cần business field user id nội bộ | [ ] Pass / [ ] Fail / [ ] N/A | |
| T10 | BE Pattern | Nếu cần user id nội bộ cho business field: dùng luồng chung `ICurrentInternalUserResolver`, không duplicate private resolve method | [ ] Pass / [ ] Fail / [ ] N/A | |

| T11 | Template Sync | Nếu task thay đổi pattern FE/BE → đã cập nhật file template tương ứng trong `.agents/context/templates/` | [ ] Pass / [ ] Fail / [ ] N/A | |
| T12 | BE Pattern | DTOs (Create/Update) phải có default values cho các field cơ bản (Status="Active", Note="", v.v.) nếu chưa có | [ ] Pass / [ ] Fail / [ ] N/A | |
| T13 | FE Pattern | Frontend Update request payload KHÔNG chứa trường `id`, id chỉ truyền trên URL path | [ ] Pass / [ ] Fail / [ ] N/A | |
| T14 | BE Pattern | Xử lý File, Export Excel hoặc Delete Aggregate PHẢI dùng code từ các file `.cs.template` đặc thù, không tự implement | [ ] Pass / [ ] Fail / [ ] N/A | |

---

## Module-Specific Checklists

### Inventory / Warehouse / Config / Product

- [ ] Bộ lọc (reset/apply) hoạt động đúng, không cần reload trang
- [ ] Đặt lại bộ lọc → clear filter state VÀ gọi API ngay (không cần bấm thêm)
- [ ] Paging reset về trang 1 khi thay đổi filter

### Sale Contract

- [ ] File upload validate đúng loại file và size limit
- [ ] Status flow đúng theo nghiệp vụ (Active/Inactive/...)
- [ ] Liên kết Customer + Product validate tồn tại trước khi lưu

---

## Checklist Check Prompt

Khi cần check module theo checklist, dùng prompt:

```
Kiểm tra module [{tên module}] theo checklist:
1. Đối chiếu toàn bộ items trong `.agents/quality/checklists/master-standard.md`
2. Đối chiếu items bổ sung trong `.agents/context/checklist.md`
3. Đánh dấu từng mục: Pass / Fail / N/A
4. Nếu Fail, nêu rõ: vấn đề + file + fix tối thiểu
5. Kết luận: Pass / Pass có điều kiện / Blocked
```
