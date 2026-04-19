# Master Checklist

38 items unified — dùng được cho mọi web/mobile project.
Project có thể subset hoặc extend trong `.agents/context/checklist.md`.

## Cách Dùng
- Tick từng item: `Pass / Fail / N/A`
- Ghi evidence cho items quan trọng
- Items có `*` = bắt buộc cho mọi task web

## Checklist

| # | Nhóm | Item | Kết quả | Evidence |
|---|---|---|---|---|
| 1 | UI/UX | Layout, font, màu sắc, spacing nhất quán với design | [ ] Pass / [ ] Fail / [ ] N/A | |
| 2 | UI/UX | Responsive không vỡ trên mobile/tablet/desktop | [ ] Pass / [ ] Fail / [ ] N/A | |
| 3 | UI/UX | Empty state hiển thị đúng khi không có dữ liệu | [ ] Pass / [ ] Fail / [ ] N/A | |
| 4 | UI/UX | Button/interactive control có hover, active, loading phù hợp | [ ] Pass / [ ] Fail / [ ] N/A | |
| 5 | UI/UX | Không có lỗi chính tả trên label, header, button | [ ] Pass / [ ] Fail / [ ] N/A | |
| 6 | Navigation | Breadcrumb / tiêu đề trang / link điều hướng đúng luồng | [ ] Pass / [ ] Fail / [ ] N/A | |
| 7 | Filter/Search | Filter tabs (nếu có): default state, highlight, badge count đúng | [ ] Pass / [ ] Fail / [ ] N/A | |
| 8 | Filter/Search | Popup tìm nâng cao (nếu có) hiển thị đầy đủ và hoạt động đúng | [ ] Pass / [ ] Fail / [ ] N/A | |
| 9 | Filter/Search | Search: exact/partial/invalid/clear hoạt động đúng | [ ] Pass / [ ] Fail / [ ] N/A | |
| 10 | Validation * | Field required có đánh dấu và thông báo lỗi rõ ràng | [ ] Pass / [ ] Fail / [ ] N/A | |
| 11 | Validation | Chặn nhập sai kiểu dữ liệu, format, min/max length | [ ] Pass / [ ] Fail / [ ] N/A | |
| 12 | Validation | Bấm Save khi để trống field được xử lý đúng | [ ] Pass / [ ] Fail / [ ] N/A | |
| 13 | Create * | Chống duplicate submit khi bấm Save liên tục | [ ] Pass / [ ] Fail / [ ] N/A | |
| 14 | Create | Default values được gán đúng theo nghiệp vụ | [ ] Pass / [ ] Fail / [ ] N/A | |
| 15 | Create | Tạo thành công có toast/message và điều hướng đúng | [ ] Pass / [ ] Fail / [ ] N/A | |
| 16 | Read/List | Loading/skeleton hiển thị khi dữ liệu chưa tải xong | [ ] Pass / [ ] Fail / [ ] N/A | |
| 17 | Read/List | Filter/search không có kết quả hiển thị thông báo đúng | [ ] Pass / [ ] Fail / [ ] N/A | |
| 18 | Read/List | Sắp xếp (nếu có) tăng/giảm đúng, cột không sort thì đúng hành vi | [ ] Pass / [ ] Fail / [ ] N/A | |
| 19 | Read/List | Dữ liệu map đúng cột và đúng format (tiền/ngày/số) | [ ] Pass / [ ] Fail / [ ] N/A | |
| 20 | Read/List | Hover row/icon (nếu có) hiển thị đúng state/tooltip | [ ] Pass / [ ] Fail / [ ] N/A | |
| 21 | Update | Mở form edit có dữ liệu cũ đầy đủ và chính xác | [ ] Pass / [ ] Fail / [ ] N/A | |
| 22 | Update | Bấm Save khi không đổi dữ liệu được xử lý hợp lý | [ ] Pass / [ ] Fail / [ ] N/A | |
| 23 | Update | Concurrent update không gây ghi đè vô lý | [ ] Pass / [ ] Fail / [ ] N/A | |
| 24 | Delete/Approve | Có popup xác nhận cho thao tác nguy hiểm | [ ] Pass / [ ] Fail / [ ] N/A | |
| 25 | Delete/Approve | Hủy bỏ thao tác thì không thay đổi dữ liệu | [ ] Pass / [ ] Fail / [ ] N/A | |
| 26 | Delete/Approve | Xác nhận thao tác thì cập nhật UI + trạng thái dữ liệu đúng | [ ] Pass / [ ] Fail / [ ] N/A | |
| 27 | Delete/Approve | Business rule khi xóa được chặn/cảnh báo đúng | [ ] Pass / [ ] Fail / [ ] N/A | |
| 28 | Paging | Đổi page size, next/prev/first/last, go-to page đúng hành vi | [ ] Pass / [ ] Fail / [ ] N/A | |
| 29 | Paging | Boundary case: 1 trang hoặc page không hợp lệ được xử lý đúng | [ ] Pass / [ ] Fail / [ ] N/A | |
| 30 | Error Handling * | Hành vi bất thường (double click, mất mạng) không làm crash | [ ] Pass / [ ] Fail / [ ] N/A | |
| 31 | Error Handling * | Lỗi hiển thị thân thiện, không lộ raw error từ server | [ ] Pass / [ ] Fail / [ ] N/A | |
| 32 | Code Hygiene | Không còn debug logs thừa | [ ] Pass / [ ] Fail / [ ] N/A | |
| 33 | Performance | Tải trang, search/filter, paging response đạt mức chấp nhận | [ ] Pass / [ ] Fail / [ ] N/A | |
| 34 | Compatibility | Chạy đúng trên Chrome/Firefox/Safari/Edge | [ ] Pass / [ ] Fail / [ ] N/A | |
| 35 | Keyboard UX | Thứ tự di chuyển bằng phím Tab hợp lý (nếu có form/grid) | [ ] Pass / [ ] Fail / [ ] N/A | |
| 36 | Security | Không lộ sensitive data trong UI hoặc console | [ ] Pass / [ ] Fail / [ ] N/A | |
| 37 | Permission | Unauthorized user không thể access protected routes/actions | [ ] Pass / [ ] Fail / [ ] N/A | |
| 38 | i18n | Không có text hardcode trong component (nếu project dùng i18n) | [ ] Pass / [ ] Fail / [ ] N/A | |

## Case Tối Thiểu Theo Loại Task

**Feature:**
- [ ] 2 happy path
- [ ] 2 edge case
- [ ] 1 error handling / user message

**Bugfix:**
- [ ] 1 case tái hiện bug gốc (trước/sau fix)
- [ ] 1 anti-regression case cho luồng liên quan

## Pass / Fail Rules (Ship Decision)

| Tình trạng | Kết luận | Hành động |
|---|---|---|
| Có finding `Critical` | **Blocked** | Phải fix trước khi ship |
| Không có `Critical`, có `Major` | **Pass có điều kiện** | Ship được + ghi rõ residual risks |
| Chỉ có `Minor` hoặc sạch | **Pass** | Ship |

> Quality gates chi tiết (before implement / before ship) → xem `quality/feature-bug-gates.md`

## Kết Quả Tổng Kết
- Overall: Pass / Pass with risks / Fail
- Findings: Critical / Major / Minor / None
- Evidence: [link/screenshot]
- Residual risks: [nếu có]
