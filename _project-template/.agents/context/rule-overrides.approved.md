# Rule Overrides — Approved

> File này khai báo tất cả override từ global rules.
> CHỈ ĐƯỢC override rules có nhãn [OVERRIDABLE] trong `rules/global.md`.
> Rules có nhãn [PROTECTED] KHÔNG THỂ override — AI sẽ bỏ qua override đó.
>
> Format:
>   - rule-id: [id của rule trong global.md]
>     value: [giá trị mới]
>     reason: [lý do override — bắt buộc]
>     approved-by: [tên người approve]
>     expires: [ngày hết hạn hoặc "never"]
>
> Xóa file này hoàn toàn nếu project dùng global rules 100%.

---

## Overrides

# Ví dụ — xóa hoặc thay thế bằng override thực tế:

# - rule-id: architecture-pattern
#   value: FastEndpoints (minimal API, không có MediatR)
#   reason: Project bắt đầu trước khi team adopt MediatR, không có migration plan
#   approved-by: [tên]
#   expires: never

# - rule-id: i18n-required
#   value: false
#   reason: Internal admin tool, chỉ 1 ngôn ngữ, không có i18n plan
#   approved-by: [tên]
#   expires: 2026-12-31

# - rule-id: gate3-major-threshold
#   value: Ship với Major nếu có risk acceptance từ tech lead
#   reason: Release cycle 2 tuần, Major được track trong backlog sprint kế tiếp
#   approved-by: [tên]
#   expires: never
