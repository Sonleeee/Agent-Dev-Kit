---
name: adk-web-tester
description: |
  Tự động hóa kiểm thử UI và luồng chức năng E2E trên trình duyệt thật bằng AI.
  Mặc định chạy ngầm (Headless), tự động chụp ảnh bằng chứng (Evidence Screenshots) và xuất báo cáo pass/fail.
  Trigger: "test web", "kiểm thử luồng [x]", "chạy test E2E giao diện", "tự động hóa thao tác web".
---

# Web Tester (AI E2E & UI Automation)

## Mục tiêu
Thực thi kiểm thử chức năng, xác thực giao diện (UI) và tự động hóa thao tác trình duyệt theo kịch bản xác định, xuất bằng chứng kiểm thử (Evidence Screenshots + Test Report) hoàn toàn chạy ngầm, không làm phiền người dùng.

## Ranh Giới An Toàn (Zero-Disruption Invariants)
1. **Chạy ngầm mặc định (Headless-First):** Quá trình test, click, nhập form chạy ngầm 100%. Không mở cửa sổ trình duyệt chèn vào màn hình làm việc của người dùng trừ khi có cờ `--headed`.
2. **Không cướp quyền điều khiển tab:** Tuyệt đối không can thiệp hoặc điều hướng tab người dùng đang lướt.
3. **Bằng chứng độc lập (Evidence-First):** Mọi kết quả pass/fail đều phải có ảnh chụp màn hình bằng chứng lưu vào file trên đĩa.

## Các Chế Độ Kiểm Thử

### 1. Headless Standalone (Mặc định)
Khởi chạy phiên trình duyệt ngầm sạch sẽ, thao tác kịch bản và chụp ảnh bằng chứng:
```powershell
python skills/testing/adk-web-tester/scripts/tester.py --url "<TARGET_URL>" --steps "type:input[name='q']:AI,click:button[type='submit'],wait:2" --screenshot "evidence.png"
```

### 2. Headed Mode (Xem trực tiếp khi cần debug)
Chỉ kích hoạt khi người dùng muốn quan sát trực tiếp AI thao tác bằng mắt thường:
```powershell
python skills/testing/adk-web-tester/scripts/tester.py --url "<TARGET_URL>" --headed --steps "..."
```

### 3. Session Test (Chỉ khi người dùng chỉ định)
Kết nối vào session có sẵn để test các luồng nghiệp vụ sau đăng nhập:
```powershell
python skills/testing/adk-web-tester/scripts/tester.py --session --steps "..."
```
