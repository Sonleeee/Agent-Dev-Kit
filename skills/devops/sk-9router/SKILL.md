---
name: sk-9router
description: |
  Cấu hình, kiểm tra và troubleshoot 9Router cho AI coding tools và OpenAI-compatible clients.
  Dùng khi cần cài đặt 9router, cấu hình endpoint local http://localhost:20128/v1,
  kết nối provider, tạo API key, chọn model, thiết lập Codex/Claude Code/Cursor/Cline/Roo/Continue,
  hoặc debug lỗi routing, model, quota, API key, stream và fallback.
context-required: false
output: 9router-setup-report
---

# 9Router

## Mục tiêu

Giúp agent dùng 9Router như một AI gateway local OpenAI-compatible: cài đặt, chạy dashboard, kết nối provider, lấy API key, cấu hình tool, test request và xử lý lỗi.

## Nguồn chuẩn

- Website: `https://9router.com/`
- GitHub: `https://github.com/decolua/9router`
- Endpoint mặc định: `http://localhost:20128/v1`
- Dashboard mặc định: `http://localhost:20128/dashboard`
- Lệnh cài đặt nhanh: `npm install -g 9router`
- Lệnh chạy nhanh: `9router`

Nếu task yêu cầu thông tin mới nhất về version, provider, model, CLI integration, giá hoặc breaking change, phải tra cứu docs/GitHub hiện tại trước khi kết luận.

## Quy trình

### Bước 1: Xác định mục đích

Hỏi hoặc suy luận từ context:

- Tool cần cấu hình: Codex, Claude Code, Cursor, Cline, Roo, Continue, OpenAI SDK hay tool khác.
- Mục tiêu routing: dùng provider miễn phí, provider giá rẻ, subscription, custom OpenAI-compatible endpoint, hay fallback combo.
- Môi trường: Windows/macOS/Linux, chạy global package, source repo, Docker hay server riêng.
- Yêu cầu bảo mật: local-only hay expose ra LAN/internet.

### Bước 2: Kiểm tra cài đặt

Trên máy local, ưu tiên lệnh không phá hủy:

```bash
node --version
npm --version
9router --version
```

Nếu chưa có 9Router:

```bash
npm install -g 9router
9router
```

Nếu chạy từ source repo 9Router:

```bash
npm install
PORT=20128 NEXT_PUBLIC_BASE_URL=http://localhost:20128 npm run dev
```

Ghi rõ nếu cần quyền network, cài package, hoặc sửa cấu hình ngoài workspace.

### Bước 3: Kết nối provider

Mở dashboard `http://localhost:20128/dashboard`, sau đó:

- Thêm provider bằng OAuth, API key, cookie/browser flow, hoặc compatible node tùy provider.
- Ưu tiên setup theo tier: subscription -> cheap -> free.
- Nếu dùng custom endpoint, xác minh base URL, auth header, model ID và khả năng stream.
- Bật/tắt RTK token saver theo nhu cầu debug. Khi debug request raw, tạm tắt compression nếu nó làm khó đọc log.

Không bao giờ in token, cookie, API key, OAuth code hoặc full request có secret vào output.

### Bước 4: Lấy API key và endpoint

Cấu hình client như một OpenAI-compatible provider:

```text
Base URL: http://localhost:20128/v1
API key: key sinh trong dashboard 9Router
Model: model hoặc combo ID hiện có trong dashboard
```

Nếu tool yêu cầu URL không có `/v1`, đọc docs của tool đó. Mặc định với OpenAI SDK và phần lớn AI coding tools là dùng base URL có `/v1`.

### Bước 5: Test nhanh

Kiểm tra server:

```bash
curl http://localhost:20128/v1/models
```

Kiểm tra chat completion:

```bash
curl http://localhost:20128/v1/chat/completions \
  -H "Authorization: Bearer $NINE_ROUTER_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"model":"<model-id>","messages":[{"role":"user","content":"ping"}],"stream":false}'
```

Trên PowerShell, dùng biến môi trường:

```powershell
$env:NINE_ROUTER_API_KEY = "<api-key>"
curl.exe http://localhost:20128/v1/models -H "Authorization: Bearer $env:NINE_ROUTER_API_KEY"
```

Nếu `/v1/models` fail, sửa server/API key trước. Nếu `/v1/models` OK nhưng chat fail, kiểm tra model ID, provider credential, quota, compatible format và stream.

### Bước 6: Cấu hình tool

Với bất kỳ tool nào, tìm setting tương đương:

- `base_url`, `api_base`, `openai_api_base`, `OPENAI_BASE_URL` hoặc `OPENAI_API_BASE`
- `api_key`, `OPENAI_API_KEY`
- `model`

Mẫu cấu hình chung:

```text
OPENAI_BASE_URL=http://localhost:20128/v1
OPENAI_API_KEY=<9router-api-key>
MODEL=<model-id-or-combo-id>
```

Nếu tool có setup wizard trong dashboard 9Router, ưu tiên wizard vì nó có thể ghi đúng file cấu hình riêng của tool.

## Troubleshooting

### Không vào được dashboard

- Kiểm tra process 9Router có đang chạy không.
- Kiểm tra port `20128` có bị chiếm không.
- Nếu đổi port, đồng bộ lại endpoint tool thành `http://localhost:<port>/v1`.

### Lỗi API key

- Tạo key mới trong dashboard.
- Kiểm tra header `Authorization: Bearer <key>`.
- Nếu expose server, bật yêu cầu API key và dùng HTTPS/reverse proxy.

### Lỗi model không tồn tại

- Gọi `/v1/models` để lấy model ID thực tế.
- Kiểm tra prefix provider/model hoặc combo ID trong dashboard.
- Không suy diễn model ID từ docs cũ khi dashboard đang trả danh sách khác.

### Lỗi provider/quota/fallback

- Kiểm tra provider credential còn hợp lệ.
- Xem quota/reset/cost trong dashboard.
- Đặt combo fallback theo thứ tự: subscription -> cheap -> free.
- Nếu một provider lỗi format/stream, test riêng với `stream:false` trước.

### Lỗi stream/SSE

- Test `stream:false` để tách lỗi model với lỗi streaming.
- Kiểm tra client có hỗ trợ OpenAI-compatible streaming không.
- Nếu qua proxy/reverse proxy, đảm bảo proxy không buffer SSE.

## Output

Trả về ngắn gọn theo format:

```markdown
## 9Router Setup Report

- Status: Installed | Running | Needs install | Blocked
- Endpoint: http://localhost:20128/v1
- Dashboard: http://localhost:20128/dashboard
- Tool: [tên tool]
- Provider/model: [provider/model hoặc combo]
- Tests: /v1/models OK|Fail, chat OK|Fail
- Notes: [lỗi, cảnh báo secret, bước tiếp theo]
```

## Guardrails

- Không commit API key, OAuth token, cookie, `~/.9router/db.json`, `usage.json` hoặc log có secret.
- Không paste full secret vào chat/output. Nếu cần xác minh, chỉ hiện 4 ký tự đầu/cuối.
- Khi sửa config của tool ngoài workspace, xin phê duyệt nếu lệnh cần quyền ngoài sandbox.
- Khi thông tin có thể mới thay đổi như provider, model, version, endpoint phụ, docs setup tool, phải tra cứu nguồn chính thức trước.
