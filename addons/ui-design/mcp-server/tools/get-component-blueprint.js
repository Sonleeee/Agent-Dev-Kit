export const tool = {
  name: 'get_component_blueprint',
  description:
    'Lấy đặc tả Component Blueprint kết hợp với công thức chuyển động vật lý (Motion Recipe), quy tắc Mobile Native, bộ dữ liệu phá thử giao diện (break-ui payloads) và code mẫu sạch 100% anti-slop.',
  inputSchema: {
    type: 'object',
    properties: {
      component_id: {
        type: 'string',
        description:
          'ID của component: "data-table", "modal-dialog", "drawer-sheet", "command-palette", "form-control", "status-badge", "bento-grid"'
      }
    },
    required: ['component_id']
  },
  execute(args, ctx) {
    const { componentBlueprintsDb, motionRecipesDb } = ctx;
    const id = (args.component_id || '').toLowerCase().trim();
    const bp = componentBlueprintsDb.find((b) => b.id.toLowerCase() === id);
    if (!bp) {
      return {
        isError: true,
        content: [
          {
            type: 'text',
            text: `Lỗi: Không tìm thấy component blueprint "${args.component_id}". Danh sách khả dụng: ${componentBlueprintsDb.map((b) => b.id).join(', ')}`
          }
        ]
      };
    }
    const recipe = motionRecipesDb.find((r) => r.id === bp.motion_recipe_id);

    let out = `# 🧩 Component Blueprint: ${bp.name} (\`${bp.id}\`)\n\n`;
    out += `## 1. Bất biến kỹ thuật & Trạng thái (Invariants)\n${bp.invariants.map((i) => `- ✅ ${i}`).join('\n')}\n\n`;
    out += `## 2. Quy tắc Mobile Native & Touch Ergonomics\n${bp.mobile_native_rules.map((m) => `- 📱 ${m}`).join('\n')}\n\n`;

    if (recipe) {
      out += `## 3. Công thức chuyển động vật lý (${recipe.name} — \`${recipe.id}\`)\n`;
      out += `- **Khi sử dụng**: ${recipe.when_to_use}\n`;
      out += `- **Easing**: \`${recipe.physics.easing}\` | **Duration**: \`${recipe.physics.duration_ms}ms\`\n`;
      out += `- **Tailwind Classes**: \`${recipe.tailwind_classes}\`\n`;
      out += `- **Nghiêm cấm (Forbidden Slop)**: ${recipe.forbidden_slop.join('; ')}\n\n`;
    }

    out += `## 4. Bộ dữ liệu cực đoan phá thử giao diện (\`break-ui\` Stress Payloads)\n\`\`\`json\n${JSON.stringify(bp.break_ui_payloads, null, 2)}\n\`\`\`\n\n`;
    out += `## 5. Mẫu code chuẩn Anti-Slop (React + Tailwind)\n\`\`\`tsx\n${bp.tailwind_react_snippet}\n\`\`\``;

    return {
      content: [{ type: 'text', text: out }]
    };
  }
};
