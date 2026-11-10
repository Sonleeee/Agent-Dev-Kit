---
name: adk-web-harvest
description: |
  Thu thập và bóc tách dữ liệu web chuyên sâu phục vụ tổng hợp, phân tích và nghiên cứu tri thức.
  Dùng khi: cào tài liệu/báo cáo web, trích xuất Markdown sạch, bóc tách JSON theo schema.
  Mặc định chạy ngầm độc lập (Headless), không can thiệp vào trình duyệt người dùng.
  Trigger: "cào dữ liệu", "crawl web", "thu thập tài liệu", "lấy data để research", "scrape [url]".
---

# Web Harvest (Deep Research Data Extractor)

## Mục tiêu
Thu thập, bóc tách và tinh chế nội dung web từ một hoặc nhiều URL thành văn bản Markdown sạch (loại bỏ quảng cáo, điều hướng, script) hoặc cấu trúc JSON chuẩn xác, phục vụ nghiên cứu chuyên sâu mà không làm phiền người dùng.

## Ranh Giới An Toàn (Zero-Disruption Invariants)
1. **Chạy ngầm mặc định (Headless-First):** 100% tác vụ cào dữ liệu chạy ngầm trong nền. Tuyệt đối không mở cửa sổ trình duyệt đè lên màn hình, không làm phiền trải nghiệm lướt web của người dùng.
2. **Không can thiệp Chrome cá nhân:** Chỉ kết nối vào phiên Chrome thật khi có chỉ định rõ ràng (`--session` hoặc `--cdp-url`). Nếu là link công khai, luôn dùng trình duyệt độc lập.
3. **Phát hiện Login Wall minh bạch:** Nếu một trang yêu cầu đăng nhập (bị chuyển hướng sang `/login`), script sẽ thông báo rõ ràng thay vì cố tình hook trái phép vào session người dùng.

## 3 Chế Độ Thu Thập (Harvest Modes)

### 1. Headless Standalone (Mặc định - Khuyên dùng)
Dùng cho 95% các trường hợp (bài báo, tài liệu, video, trang tin tức, bài viết public):
```powershell
python skills/research/adk-web-harvest/scripts/harvest.py --url "<TARGET_URL>" --out ".agents/runtime/output.md"
```
- Tốc độ cao (2–4s).
- Không mở cửa sổ, không popup, 0 ma sát.

### 2. Isolated Profile (Tài khoản riêng cho AI)
Dùng khi cần cào dữ liệu định kỳ trên các trang sau đăng nhập mà không muốn đụng vào Chrome cá nhân:
```powershell
python skills/research/adk-web-harvest/scripts/harvest.py --url "<TARGET_URL>" --profile "$env:LOCALAPPDATA\Google\Chrome\AI_Session" --out ".agents/runtime/output.md"
```

### 3. Session-Attached (Chỉ dùng khi người dùng yêu cầu)
Dùng khi người dùng muốn đọc ngay một tab đang mở trên Chrome của họ:
```powershell
python skills/research/adk-web-harvest/scripts/harvest.py --session --url "<TARGET_URL>" --out ".agents/runtime/output.md"
```

## Quy Trình Thực Hiện

1. **Xác định mục tiêu:** Nhận URL từ người dùng.
2. **Chạy cào ngầm:** Gọi `harvest.py` ở chế độ standalone mặc định.
3. **Kiểm tra kết quả:**
   - Nếu cào thành công: Bóc tách Markdown, tóm tắt luận điểm cốt lõi.
   - Nếu gặp trang bắt đăng nhập: Báo cho người dùng và đề xuất phương án (tìm nguồn mở thay thế hoặc dùng session).
