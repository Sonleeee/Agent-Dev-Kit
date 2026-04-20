# Feature / Bug Quality Gates

Áp dụng cho mọi project. Định nghĩa điều kiện bắt buộc trước khi implement và trước khi ship.
Dùng bởi: `delivery-orchestrator`, `solution-planning`, `regression-checklist`, `review-workflow`.

---

## Gate: Before Implement (Feature)

Không được bắt đầu code khi chưa có:

- [ ] Problem statement rõ ràng (user biết mình đang fix/build cái gì)
- [ ] Scope in/out rõ ràng
- [ ] UI/UX constraints đã được mô tả trong quality card
- [ ] Validation + error handling constraints đã được mô tả
- [ ] Permission/sk-security constraints đã được mô tả
- [ ] Performance expectation đã được xác định
- [ ] API contract impact đã được đánh dấu (`Yes / No / Unknown`)
- [ ] Implementation plan + task order đã có
- [ ] Nếu API contract changed = `Yes/Unknown` → phải chạy `api-contract-guard` trước

## Gate: Before Ship (Feature)

Không được đóng task khi chưa có:

- [ ] Happy paths (tối thiểu 2) đã pass
- [ ] Edge cases trong scope (tối thiểu 2) đã pass
- [ ] Error handling / user message (tối thiểu 1) đã pass
- [ ] Regression checks cho luồng liên quan đã pass
- [ ] Evidence (screenshot/log) cho các checks quan trọng
- [ ] Không còn finding `Critical`
- [ ] Nếu có `Major`: ghi rõ điều kiện ship + residual risks

---

## Gate: Before Implement (Bugfix)

Không được bắt đầu fix khi chưa có:

- [ ] Root cause đã được chốt rõ (không fix symptom)
- [ ] Có anti-regression test case gắn với bug
- [ ] Đánh giá impact lan tỏa sang FE/BE/API

## Gate: Before Ship (Bugfix)

Không được đóng task khi chưa có:

- [ ] Bug gốc không còn tái hiện (chạy case before/after)
- [ ] Anti-regression case đã pass
- [ ] Luồng liên quan không bị regression
- [ ] Residual risks đã ghi nếu chưa test hết

---

## Pass / Fail Rules

| Tình trạng | Kết luận | Hành động |
|---|---|---|
| Có finding `Critical` | **Blocked** | Phải fix trước khi ship |
| Không có `Critical`, có `Major` | **Pass có điều kiện** | Ship được, ghi rõ điều kiện + residual risks |
| Chỉ có `Minor` hoặc không có finding | **Pass** | Ship |

---

## Mapping Hướng Dẫn Nhanh (để đưa vào quality card)

| Nếu task có... | Bắt buộc map checklist items... |
|---|---|
| UI + table | filter/search/sort/paging + empty state/loading (xem `mapping-rules.md` → `data-table`) |
| Thao tác ghi dữ liệu | validation + duplicate submit + toast/error message (`form-submit`) |
| Delete / Approve | confirmation + permission + data state after action (`delete-action`, `approve-action`) |
| API impact | route/status/request/response contract checks (`api-change` → chạy `api-contract-guard`) |
| Text hiển thị | i18n keys check (`i18n`) |

> Chi tiết decision tree → xem `quality/mapping-rules.md`
