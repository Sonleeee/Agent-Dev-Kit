import path from 'node:path';
import { saveSessionState } from '../services/session-manager.js';

export const tool = {
  name: 'evaluate_interview',
  description:
    'Đánh giá input kiến trúc và ghi scratchpad chứa ADR draft vào project_dir/.agents/.cache/scaffold-session.json. Chỉ gọi khi người dùng yêu cầu rõ interview/chấm điểm và đồng ý side effect ghi file.',
  inputSchema: {
    type: 'object',
    properties: {
      answers: {
        type: 'object',
        description:
          'Các lựa chọn của dev: { scale: "A"|"B"|"C", consistency: "A"|"B", background_jobs: "A"|"B"|"C", protocols: ["1","2","3"] }'
      },
      project_dir: {
        type: 'string',
        description: 'Thư mục dự án mục tiêu (mặc định là thư mục hiện tại)'
      },
      project_name: {
        type: 'string',
        description: 'Tên dự án'
      }
    },
    required: ['answers']
  },
  execute(args) {
    const answers = args.answers || {};
    const scale = (answers.scale || 'B').toUpperCase();
    const consistency = (answers.consistency || 'A').toUpperCase();
    const jobs = (answers.background_jobs || 'B').toUpperCase();
    const protocols = Array.isArray(answers.protocols) ? answers.protocols : ['1'];
    const targetDir = args.project_dir ? path.resolve(args.project_dir) : process.cwd();
    const projName = args.project_name || path.basename(targetDir);

    // 1. Tính toán Complexity Score (/10)
    let score = 1.0;
    if (scale === 'A') score += 0.5;
    else if (scale === 'B') score += 1.0;
    else if (scale === 'C') score += 3.0;

    if (consistency === 'A') score += 1.5;
    else score += 0.5;

    if (jobs === 'A') score += 0.0;
    else if (jobs === 'B') score += 0.5;
    else if (jobs === 'C') score += 2.0;

    if (protocols.includes('3')) score += 1.0;
    if (protocols.includes('2')) score += 1.0;

    score = Math.min(10, Math.max(1, score));

    // 2. Feature Flags
    const features = {
      hasPessimisticLock: consistency === 'A',
      hasDbQueue: jobs === 'B',
      hasRedisQueue: jobs === 'C',
      hasHmacWebhook: protocols.includes('3'),
      hasWebSocket: protocols.includes('2'),
      hasIdempotency: consistency === 'A' || protocols.includes('3')
    };

    // 3. Khuyến nghị kiến trúc
    let archId = 'clean-arch-ts';
    let archName = 'Pragmatic Clean Monolith';
    if (scale === 'C' || jobs === 'C') {
      archName = 'High-Scale Event-Driven Service';
    }

    // 4. Tạo nội dung ADR-001 chi tiết cá nhân hóa
    const adrContent = `# ADR-001: Kiến Trúc Lựa Chọn Dựa Trên Khảo Sát Kỹ Thuật

- **Dự án**: ${projName}
- **Trạng thái**: Accepted
- **Ngày lập**: ${new Date().toISOString().split('T')[0]}
- **Độ phức tạp hệ thống**: ${score.toFixed(1)} / 10

## 1. Kết quả khảo sát đầu vào (Interview Inputs)
- **Quy mô người dùng (Scale)**: ${scale === 'A' ? 'Nội bộ / MVP (< 100 users)' : scale === 'B' ? 'Vừa / Khởi nghiệp (1.000 - 10.000 users/ngày)' : 'Lớn / Flash-sale (50.000 - 100.000+ users)'}
- **Tính nhất quán dữ liệu**: ${consistency === 'A' ? 'Chính xác tức thời (Strong Consistency - Tiền tệ / Tồn kho)' : 'Chấp nhận trễ vài giây (Eventual Consistency)'}
- **Tác vụ ngầm**: ${jobs === 'A' ? 'In-Memory (0 đồng hạ tầng)' : jobs === 'B' ? 'PostgreSQL DB-backed Queue (Bền vững, 0 đồng Redis)' : 'Distributed Redis/RabbitMQ'}
- **Giao thức kết nối**: ${protocols.map((p) => (p === '1' ? 'RESTful JSON' : p === '2' ? 'WebSocket Realtime' : p === '3' ? 'HMAC Webhook Receiver' : p)).join(', ')}

## 2. Quyết định kiến trúc cốt lõi
1. **Mô hình mã nguồn**: Áp dụng **Clean Architecture** (Domain -> Application -> Infrastructure -> Interfaces). Ranh giới nghiệp vụ được cô lập tuyệt đối khỏi Web Framework và DB Driver.
2. **Quản lý dữ liệu**: ${features.hasPessimisticLock ? 'Sử dụng PostgreSQL ACID Transactions + `SELECT ... FOR UPDATE` khi trừ tồn kho / số dư để triệt tiêu Race Condition.' : 'Áp dụng Optimistic Lock hoặc Eventual Consistency.'}
3. **Xử lý tác vụ ngầm**: ${features.hasDbQueue ? 'Tạo bảng `background_jobs` với `SELECT ... FOR UPDATE SKIP LOCKED` để worker xử lý ngầm mà không cần tốn tiền cài đặt cụm Redis riêng.' : features.hasRedisQueue ? 'Kết nối Redis Queue (BullMQ).' : 'Xử lý non-blocking trong memory event loop.'}
4. **Bảo mật Webhook & Giao tiếp**: ${features.hasHmacWebhook ? 'Bắt buộc xác thực chữ ký số HMAC SHA-256 bằng `crypto.timingSafeEqual` và kiểm tra `idempotency_key` trước khi cộng tiền / duyệt đơn.' : 'Chuẩn hóa REST API DTOs.'}

## 3. Ranh giới bất biến (Invariants)
- Tầng Domain tuyệt đối không import Express, FastAPI hay bất kỳ thư viện bên ngoài nào.
- Mọi thao tác thay đổi số dư hoặc trừ tồn kho phải nằm trong Transaction.
- Mọi Webhook từ cổng thanh toán phải được verify chữ ký trước khi chạm tới Use Case.
`;

    // 5. Lưu vào Ephemeral Scratchpad
    const sessionState = {
      session_id: `scaffold_${Date.now()}`,
      timestamp: new Date().toISOString(),
      answers,
      complexity_score: score,
      architecture_id: archId,
      features,
      adr_content: adrContent,
      status: 'READY_TO_SCAFFOLD'
    };

    const cachePath = saveSessionState(targetDir, sessionState);

    let summaryText = `### 📊 Đánh giá Kiến Trúc & Độ Phức Tạp: **${score.toFixed(1)} / 10**\n\n`;
    summaryText += `* **Kiến trúc khuyến nghị:** \`${archName}\` (\`${archId}\`)\n`;
    summaryText += `* **Độ phức tạp:** ${score <= 3 ? '🟢 Rất thấp (1 dev gánh mượt)' : score <= 6 ? '🟡 Vừa phải (Thực dụng, 1-2 dev tối ưu)' : '🔴 Cao (Cần team từ 3-5 dev)'}\n\n`;
    summaryText += `#### 🛠️ Các khối kỹ thuật sẽ được kích hoạt:\n`;
    if (features.hasPessimisticLock)
      summaryText += `- ✅ **Pessimistic Lock (\`SELECT FOR UPDATE\`):** Khóa dòng DB an toàn, chống bán trùng tồn kho.\n`;
    if (features.hasDbQueue)
      summaryText += `- ✅ **DB-Backed Job Queue:** Hàng đợi lưu trực tiếp trong PostgreSQL (0 đồng thêm server, server sập bật lại không mất job).\n`;
    if (features.hasHmacWebhook)
      summaryText += `- ✅ **HMAC Webhook Receiver:** Xác thực chữ ký số SHA-256 + Idempotency chống fake giao dịch Momo/Stripe.\n`;
    if (features.hasIdempotency)
      summaryText += `- ✅ **Idempotency Guard:** Chống double-charge khi người dùng bấm liên tục.\n`;
    summaryText += `\n💾 **Đã lưu trạng thái vào Ephemeral Scratchpad:** \`${cachePath}\`\n*(Context được bảo vệ chống trôi/ảo giác; file tạm này sẽ tự động xóa ngay sau khi scaffold hoàn tất)*\n\n`;
    summaryText += `👉 Bạn có thể gọi tool \`scaffold_project\` để bắt đầu sinh mã nguồn theo chuẩn này!`;

    return {
      content: [{ type: 'text', text: summaryText }]
    };
  }
};
