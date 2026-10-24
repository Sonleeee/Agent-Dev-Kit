export const tool = {
  name: 'list_architectures',
  description:
    'Liệt kê danh sách các bộ khung kiến trúc source base chuẩn (Blueprints) có sẵn để khởi tạo dự án mới.',
  inputSchema: {
    type: 'object',
    properties: {}
  },
  execute(args, ctx) {
    const { blueprintsDb } = ctx;
    const list = blueprintsDb
      .map(
        (b) =>
          `### 🏛️ \`${b.id}\` — ${b.name}\n- **Tech Stack**: ${b.techStack}\n- **Mô tả**: ${b.description}\n- **Phù hợp nhất**: ${b.idealFor}`
      )
      .join('\n\n');
    return {
      content: [
        {
          type: 'text',
          text: `## 📦 Danh sách các Source Base Blueprints có sẵn:\n\n${list}\n\nNếu người dùng yêu cầu tạo source base, dùng skill scaffold để xác nhận target_dir trước khi gọi tool ghi file.`
        }
      ]
    };
  }
};
