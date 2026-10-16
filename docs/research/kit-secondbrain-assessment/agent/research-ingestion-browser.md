# Ingestion, browser và evidence từ thế giới bên ngoài

**Mindset:** nguồn ngoài phải đi qua provenance, evidence và scope permission trước khi thành tri thức hoặc hành động. File này không thay thế memory lifecycle.

← [Index](../../2026-10-04-kit-secondbrain-repo-assessment.md) · [Lộ trình agent](implementation-roadmap.md)

## Thu thập nguồn

[Panniantong/Agent-Reach](https://github.com/Panniantong/Agent-Reach) tập hợp backend/CLI để đọc các nền tảng khác nhau. Giá trị với Kit là lấp kênh research mà công cụ host chưa đọc được; giá trị với SecondBrain là tạo đầu vào cho Raw trước khi web cleaner và receiver xử lý.

**Quyết định:** chỉ thử 1–2 kênh công khai có nhu cầu cụ thể. So sánh cùng URL/task với công cụ sẵn có theo nội dung thiếu, provenance, lỗi backend và ghi trùng. Không cài tất cả backend, không đưa vào core.

## Browser desktop và browser agent

| Repo | Phù hợp khi | Điều kiện bảo vệ |
|---|---|---|
| [Tencent/BrowserSkill](https://github.com/Tencent/BrowserSkill) | Agent cần thao tác/debug Chrome/Edge desktop đang đăng nhập, giữ browser/session rõ ràng. | Giới hạn profile, domain, thao tác và evidence; không xem session đang đăng nhập là quyền ngầm định. |
| [browser-use/browser-use](https://github.com/browser-use/browser-use) | Cần pipeline Python, custom tool, output schema hoặc automation chạy thành dịch vụ. | Task bounded, điều kiện dừng, step/cost limit; output schema không tự chứng minh hành động nghiệp vụ đúng. |

[Playwright MCP](../developer/ui-design-and-product-artifacts.md) được đánh giá chính ở nhóm developer vì use case trong báo cáo là kiểm UI trên staging. Agent vẫn có thể gọi công cụ này khi thực hiện test theo workflow developer.

## Chọn công cụ theo workload

| Nhu cầu | Hướng thử trước |
|---|---|
| RSS, transcript hoặc backend chuyên biệt từng nền tảng | Công cụ hiện có; thêm Agent Reach nếu thiếu kênh |
| Chrome/Edge desktop và profile đã xác định | Browser tooling host; BrowserSkill khi thiếu capability |
| Điều tra lỗi UI có console/request/response | BrowserSkill nếu capability bản cài đáp ứng; xem thêm [kiểm thử UI cho developer](../developer/ui-design-and-product-artifacts.md) |
| Browser agent bằng Python/schema/custom tool | browser-use |

## PoC chung

Dùng một tập tình huống: đọc trang động; nguồn cần đăng nhập; hết phiên/thiếu quyền; trang đổi sau thao tác; dừng task và giải phóng session. Chấm theo provenance/evidence, số lần cần người can thiệp, thời gian, chi phí và khả năng chạy lại.

Nối với Kit qua `sk-web-cleaner`; nối với SecondBrain qua payload có nguồn, thời điểm, URL, scope và receipt. Browser evidence không được tự biến thành Wiki note. Luồng `/wf-fix` và `/wf-test` cho sản phẩm UI nằm ở [nhóm developer](../developer/ui-design-and-product-artifacts.md).
