import { verifyColorContrast } from '../services/wcag-engine.js';

export const tool = {
  name: 'verify_color_contrast',
  description:
    'Tính toán chính xác tỷ lệ tương phản màu sắc theo công thức toán học WCAG 2.2 Relative Luminance (L = 0.2126R + 0.7152G + 0.0722B), kiểm tra PASS/FAIL cho AA/AAA và tự động đề xuất mã màu foreground đạt chuẩn nếu FAIL.',
  inputSchema: {
    type: 'object',
    properties: {
      foreground_hex: {
        type: 'string',
        description: 'Mã màu chữ/icon (ví dụ: "#A1A1AA" hoặc "#0A2540")'
      },
      background_hex: {
        type: 'string',
        description: 'Mã màu nền (ví dụ: "#09090B" hoặc "#FFFFFF")'
      },
      level: {
        type: 'string',
        enum: ['AA', 'AAA'],
        description: 'Mức chuẩn WCAG cần kiểm tra (mặc định: "AA")'
      }
    },
    required: ['foreground_hex', 'background_hex']
  },
  execute(args) {
    const res = verifyColorContrast(args.foreground_hex, args.background_hex, args.level);
    if (res.isError) {
      return {
        isError: true,
        content: [{ type: 'text', text: res.error }]
      };
    }
    return {
      content: [{ type: 'text', text: JSON.stringify(res.data, null, 2) }]
    };
  }
};
