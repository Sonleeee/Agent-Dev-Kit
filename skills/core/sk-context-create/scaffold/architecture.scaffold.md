# Architecture Scaffold

> Agent fill nội dung bên dưới dựa trên patterns đã confirmed ở Phase 2-3.
> Cấu trúc này là CỐ ĐỊNH (kit-level). Nội dung tùy thuộc dự án.

---

## TIER-0: Core (≤200 lines — LUÔN ĐỌC)

### 1. Architecture Pattern

<!-- Flow diagram dạng text hoặc mermaid -->
```
[Mô tả luồng chính của kiến trúc]
```

### 2. Layer Responsibilities

| Layer | Làm gì | KHÔNG làm gì |
|-------|--------|--------------|
| {layer1} | {responsibilities} | {restrictions} |
| {layer2} | {responsibilities} | {restrictions} |

### 3. Error/Exception Handling Strategy

- Exception base class: `{tên}`
- Taxonomy: {liệt kê exception types + khi nào dùng}

### 4. Naming Conventions

| Đối tượng | Convention | Ví dụ |
|-----------|-----------|-------|
| {entity} | {rule} | {example} |

### 5. Folder Structure

```
{project-root}/
├── {layer1}/
├── {layer2}/
└── ...
```

### 6. Known Anti-Patterns (Index)

> Chi tiết + code examples ở TIER-2.

| # | Anti-Pattern | Mô tả ngắn |
|---|-------------|-------------|
| AP-1 | {tên} | {1 dòng mô tả} |

---

## TIER-1: Pattern Details (đọc theo [TAG])

<!-- Agent CHỈ load section có TAG khớp với task-feature -->

### [TAG: {tag1}] {Pattern Name}

**Khi nào dùng:** {điều kiện}
**Code pattern:**
```{language}
{code mẫu chuẩn — ✅ Best implementation}
```

### [TAG: {tag2}] {Pattern Name}

**Khi nào dùng:** {điều kiện}
**Code pattern:**
```{language}
{code mẫu chuẩn}
```

<!-- Thêm sections [TAG: ...] cho mỗi confirmed pattern TIER-1 -->

---

## TIER-2: Deep Reference (đọc khi cần)

### Known Anti-Patterns (Full Examples)

| P{n} | Mô tả | ❌ Sai | ✅ Đúng | Evidence Module |
|------|-------|--------|---------|-----------------|
| P1 | {mô tả} | `{code sai}` | `{code đúng}` | {module} |

### Decision Tree

```
Q1: "{câu hỏi phân loại}"
├─ CÓ → {hướng A}
└─ KHÔNG → {hướng B}

Q2: "{câu hỏi tiếp theo}"
├─ CÓ → {hướng C}
└─ KHÔNG → {hướng D}
```

### Baseline Modules

| Module | Status | Ghi chú |
|--------|--------|---------|
| {module1} | ✅ Reference | Gold standard |
| {module2} | ⚠️ Legacy | Chưa migrate pattern X |
