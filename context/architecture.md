# Architecture — TL BIOMASS

> File này định nghĩa guardrails kiến trúc cụ thể của project.
> Domain skills (backend/frontend) đọc file này để biết pattern cần follow.

---

## Architecture Pattern

**Flow BE:** Controller → MediatR → Handler → Repository → Database

**Layer Responsibilities:**

| Layer | Làm gì | Không làm gì |
|---|---|---|
| **Controller** | Nhận request, gọi MediatR, trả response qua `ApiControllerBase` helper | Không chứa business logic |
| **Handler** | Orchestration: validate entity liên quan, gọi repository, map DTO | Không ôm query filter/sort/paging phức tạp |
| **Validator** | Validate input contract (required, format, range, enum) qua FluentValidation | Không check tồn tại entity |
| **Domain / Entity** | Invariant nghiệp vụ qua `IBusinessRule` + `CheckRule(...)` | Không dependency infrastructure |
| **Repository** | Query, filter, sort, pagination, summary | Không chứa quyết định business error |

**Flow FE:** Page → Service → API (BaseService wrapper) → BE

**Layer Responsibilities FE:**

| Layer | Làm gì | Không làm gì |
|---|---|---|
| **pages/** | Render UI, gọi service, handle state | Không gọi API trực tiếp, không chứa business rule nặng |
| **services/** | Gọi API qua `BaseService`, định nghĩa request/response types | Không xử lý UI state |
| **routes/** | Định nghĩa routing, grouping routes | Không chứa logic |
| **locales/** | i18n keys cho vi/en | Không hardcode text trong component |

---

## Error / Exception Handling

### BE — Taxonomy Exception (bắt buộc)

| Tình huống | Exception Type | HTTP Status |
|---|---|---|
| Input không hợp lệ | `ValidationException` (FluentValidation) | 400 |
| Resource không tồn tại | `NotFoundException` | 404 |
| Vi phạm business rule | `BusinessException` / `BusinessRuleValidationException` | 400 |
| Unauthorized | `UnauthorizedException` | 401/403 |

**Anti-patterns (KHÔNG được làm):**
- KHÔNG dùng `InvalidOperationException` cho business/not-found trong Application layer
- KHÔNG hardcode error message literal trong handler/controller
- KHÔNG throw generic `Exception` cho business errors

**Error message/code chuẩn:**
- Tập trung theo module tại `Domain/Constants/ErrorMessages/*`
- Format ErrorCode: `{Module}.{Scenario}` — ví dụ: `SalesContract.InvalidFileType`
- BE trả message tiếng Anh để dev hiểu; FE dịch sang tiếng Việt qua locales

### FE — Error Handling

- Service layer trả `response.errors` (string array), KHÔNG có `response.message`
- Lấy error message: `response.errors?.[0]`
- Dịch message BE sang tiếng Việt: key pattern `` `namespace.${serverMessage}` ``; fallback nếu không có key

---

## Naming Conventions

- **BE entities:** PascalCase
- **BE files:** PascalCase (`CreateSalesContractCommand.cs`)
- **BE namespace:** `TLBIOMASS.{Layer}.Features.{Module}.{Operation}.{ClassName}`
- **FE components:** PascalCase
- **FE files:** kebab-case (`sale-contract.tsx`, `form-section.tsx`)
- **FE service class:** PascalCase, camelCase methods
- **API routes:** `/api/v1/{resource-name}` (kebab-case, plural)
- **DB tables:** snake_case

---

## Folder Structure

**Backend:**
```
code-base/src/Services/TLBIOMASS/
├── TLBIOMASS.API/
│   └── Controllers/              ← ApiControllerBase helpers: HandleCreate/Update/Delete/GetPaged
├── TLBIOMASS.Application/
│   └── Features/
│       └── {Module}/
│           ├── Commands/
│           │   └── {Operation}/  ← Command.cs + Handler.cs + Validator.cs
│           └── Queries/
│               └── {Operation}/  ← Query.cs + Handler.cs + Validator.cs
├── TLBIOMASS.Domain/
│   └── {Module}/
│       ├── {Entity}.cs           ← Entity + static Create() factory + CheckRule()
│       ├── Interfaces/           ← IRepository interface
│       └── Constants/ErrorMessages/  ← *Error.cs theo module
└── TLBIOMASS.Infrastructure/
    └── Repositories/
        └── {Module}Repository.cs ← Query/filter/sort/paged logic tại đây
```

**Frontend:**
```
TL_BIOMASS/src/
├── pages/
│   └── {page-folder}/
│       ├── list/index.tsx        ← MainCard + DataTable + slots
│       └── manage/
│           ├── index.tsx         ← mode: create | edit | detail
│           ├── schema.ts         ← Zod schema + FormProps type
│           └── sections/         ← Accordion sections
├── services/
│   └── {service-folder}/
│       ├── service.ts            ← extends BaseService
│       ├── request.ts            ← query/request types
│       ├── response.ts           ← response types
│       └── index.ts
├── routes/
│   ├── routing.ts                ← route objects (list/create/edit/detail functions)
│   └── children/
│       └── {feature}-routes.tsx  ← route group
└── locales/languages/
    ├── vi.json
    └── en.json
```

---

## Known Anti-Patterns

- **Handler ôm query phức tạp**: `Where/OrderBy/Skip/Take` phức tạp trong handler thay vì repository → Di chuyển xuống repository
- **Hardcode error message**: `throw new Exception("message")` trong handler → Dùng `NotFoundException`/`BusinessException` + ErrorMessages
- **`InvalidOperationException` cho not-found**: Legacy code trong SalesContracts handler, không lặp lại cho module mới
- **Hardcode text FE**: Text tiếng Việt/Anh trực tiếp trong component → Phải qua locales
- **Dùng `response.message` thay `response.errors`**: Service layer trả `errors` array, không phải `message`
- **Hardcode tab options**: Tab count phải build từ `data.summary`, không hardcode
- **Lạm dụng current-user resolver**: Feature/bug không cần business user id nhưng vẫn inject `ICurrentInternalUserResolver` → Chỉ dùng khi domain field bắt buộc cần internal user id (vd `AssessorUserId`, `ApprovedBy`)
- **Sai kiểu Status cho DTO Update**: Trong UpdateDto/UpdateCommand, trường Status phải là `Optional<EntityStatus>`, KHÔNG dùng `Optional<string>`.
- **Dùng Enum.Parse thừa thãi trong Mapster**: Status là `EntityStatus` thì map trực tiếp `src => src.Status.Value`, không bọc thêm `Enum.Parse`.
- **Frontend đính kèm ID thừa trong payload Update**: Hàm cập nhật FE (`service.update(id, payload)`) chỉ nhận data trong payload, KHÔNG nhét thêm `id: id` vào payload.

---

## Known Pitfalls

- **`isSubmitting` trước `useFormResolver`**: Khai báo `isSubmitting` PHẢI đặt SAU `form = useFormResolver(...)`, đặt trước sẽ lỗi "used before declaration"
- **`useTranslate` không cần thiết**: Các component `Button.Base`, `FormField.*`, `Text.Label`, `MainCard`, `DataTable` column header tự dịch — chỉ cần truyền locales key, KHÔNG bọc `t()`
- **Legacy SalesContracts handler**: `InvalidOperationException` cho not-found — đây là legacy, KHÔNG làm theo cho module mới
- **Zod import chuẩn**: `import zod from 'zod'` (default import, không phải named import)
- **Naming mismatch service/page**: `sale-contract` (page) ≠ `sale-contact` (service folder) — kiểm tra trước khi tham chiếu
- **Current user mapping cho business field**: Luôn ưu tiên luồng chung `ICurrentInternalUserResolver` (claim -> USER.USER_ID -> USER.ID), không copy private method resolve trong từng handler
- **Lỗi pattern matching khi xử lý Optional List trong Handler**: Tránh dùng `request.Items.Value is { } items` dễ gây lỗi null reference/warning; nên dùng `request.Items.Value ?? new List<T>()` cho rõ ràng, clean.

---

## Baseline Modules (cập nhật)

| Module | Trạng thái |
|---|---|
| `SalesContracts` | Module chuẩn BE cho CRUD cơ bản (chỉ tham khảo). Tuyệt đối **KHÔNG dùng để copy** khi làm các tính năng có Upload File, Export Excel hay Delete kéo theo con (Cascade). Phải đọc `.agents/context/templates/be/feature.md.template` để lấy template ghép đúng. |
| `StockEntries`, `StockBalances`, `Warehouses` | Đã về format chuẩn repository-centric |
| Dashboard / Statistics | Query đặc thù có thể xử lý trong handler theo nghiệp vụ — không phải anti-pattern |
