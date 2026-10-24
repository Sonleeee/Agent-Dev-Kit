export const tool = {
  name: 'recommend_architecture',
  description:
    'Tư vấn lựa chọn kiến trúc tối ưu dựa trên quy mô người dùng, số lượng kỹ sư và yêu cầu nghiệp vụ để chống over-engineering.',
  inputSchema: {
    type: 'object',
    properties: {
      estimated_ccu: {
        type: 'number',
        description: 'Lượng người dùng đồng thời ước tính'
      },
      team_size: {
        type: 'number',
        description: 'Số lượng dev tham gia dự án'
      },
      business_type: {
        type: 'string',
        description: 'Loại hình dự án: "ecommerce", "ai-platform", "fintech", "crud-saas"'
      }
    },
    required: ['estimated_ccu', 'team_size']
  },
  execute(args) {
    const ccu = args.estimated_ccu || 100;
    const team = args.team_size || 2;
    const type = (args.business_type || '').toLowerCase();

    let recommendation = '';
    if (team <= 3 && ccu < 5000) {
      recommendation = `### 🎯 Kiến nghị: **Modular Monolith (hoặc Clean Architecture Monolith)**\n- **Lý do**: Đội ngũ nhỏ (${team} người), tải chưa quá lớn (< 5k CCU). Tránh lãng phí 80% thời gian cho network latency và devops.\n- **Blueprint đề xuất**: \`clean-arch-ts\` hoặc \`clean-arch-fastapi\`.`;
    } else if (team > 5 || ccu >= 10000 || type === 'fintech') {
      recommendation = `### 🎯 Kiến nghị: **Event-Driven Architecture / Microservices với Transactional Outbox**\n- **Patterns bắt buộc**: \`transactional-outbox\`, \`idempotency-key\`, \`circuit-breaker\`.`;
    } else {
      recommendation = `### 🎯 Kiến nghị: **Clean Architecture Service**\n- **Blueprint đề xuất**: \`clean-arch-ts\`.`;
    }

    return {
      content: [{ type: 'text', text: recommendation }]
    };
  }
};
