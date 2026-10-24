/**
 * WCAG 2.2 Relative Luminance & Color Contrast Math Engine
 * Zero-dependency pure functions for color space transformations,
 * contrast ratio calculation and accessible color recommendation.
 */

export function normalizeHex(hexStr) {
  if (!hexStr || typeof hexStr !== 'string') return null;
  let clean = hexStr.trim().replace(/^#/, '');
  if (/^[0-9a-fA-F]{3}$/.test(clean)) {
    clean = clean.split('').map((c) => c + c).join('');
  }
  if (!/^[0-9a-fA-F]{6}$/.test(clean)) return null;
  return '#' + clean.toUpperCase();
}

export function hexToRgb(hex) {
  const norm = normalizeHex(hex);
  if (!norm) return null;
  const num = parseInt(norm.slice(1), 16);
  return {
    r: (num >> 16) & 255,
    g: (num >> 8) & 255,
    b: num & 255
  };
}

export function rgbToHex(r, g, b) {
  const clamp = (n) => Math.max(0, Math.min(255, Math.round(n)));
  return (
    '#' +
    [clamp(r), clamp(g), clamp(b)]
      .map((v) => v.toString(16).padStart(2, '0'))
      .join('')
      .toUpperCase()
  );
}

export function srgbChannelToLinear(channel8Bit) {
  const c = channel8Bit / 255;
  return c <= 0.04045 ? c / 12.92 : Math.pow((c + 0.055) / 1.055, 2.4);
}

export function getRelativeLuminance(hex) {
  const rgb = hexToRgb(hex);
  if (!rgb) return null;
  const R = srgbChannelToLinear(rgb.r);
  const G = srgbChannelToLinear(rgb.g);
  const B = srgbChannelToLinear(rgb.b);
  return 0.2126 * R + 0.7152 * G + 0.0722 * B;
}

export function getContrastRatio(fgHex, bgHex) {
  const l1 = getRelativeLuminance(fgHex);
  const l2 = getRelativeLuminance(bgHex);
  if (l1 === null || l2 === null) return null;
  const lighter = Math.max(l1, l2);
  const darker = Math.min(l1, l2);
  return (lighter + 0.05) / (darker + 0.05);
}

export function rgbToHsl(r, g, b) {
  r /= 255;
  g /= 255;
  b /= 255;
  const max = Math.max(r, g, b);
  const min = Math.min(r, g, b);
  let h = 0;
  let s = 0;
  const l = (max + min) / 2;
  if (max !== min) {
    const d = max - min;
    s = l > 0.5 ? d / (2 - max - min) : d / (max + min);
    switch (max) {
      case r:
        h = (g - b) / d + (g < b ? 6 : 0);
        break;
      case g:
        h = (b - r) / d + 2;
        break;
      case b:
        h = (r - g) / d + 4;
        break;
    }
    h /= 6;
  }
  return { h, s, l };
}

export function hslToRgb(h, s, l) {
  let r, g, b;
  if (s === 0) {
    r = g = b = l;
  } else {
    const hue2rgb = (p, q, t) => {
      if (t < 0) t += 1;
      if (t > 1) t -= 1;
      if (t < 1 / 6) return p + (q - p) * 6 * t;
      if (t < 1 / 2) return q;
      if (t < 2 / 3) return p + (q - p) * (2 / 3 - t) * 6;
      return p;
    };
    const q = l < 0.5 ? l * (1 + s) : l + s - l * s;
    const p = 2 * l - q;
    r = hue2rgb(p, q, h + 1 / 3);
    g = hue2rgb(p, q, h);
    b = hue2rgb(p, q, h - 1 / 3);
  }
  return { r: Math.round(r * 255), g: Math.round(g * 255), b: Math.round(b * 255) };
}

export function suggestAccessibleForeground(fgHex, bgHex, targetRatio) {
  const fgRgb = hexToRgb(fgHex);
  const bgLum = getRelativeLuminance(bgHex);
  if (!fgRgb || bgLum === null) return null;

  const { h, s } = rgbToHsl(fgRgb.r, fgRgb.g, fgRgb.b);
  const preferLighter = bgLum < 0.5;
  const directions = preferLighter ? ['lighter', 'darker'] : ['darker', 'lighter'];

  for (const dir of directions) {
    let bestHex = null;

    for (let step = 0; step <= 100; step++) {
      const l = dir === 'lighter' ? step / 100 : 1 - step / 100;
      const rgb = hslToRgb(h, s, l);
      const candidateHex = rgbToHex(rgb.r, rgb.g, rgb.b);
      const ratio = getContrastRatio(candidateHex, bgHex);
      if (ratio !== null && ratio >= targetRatio) {
        bestHex = candidateHex;
        break;
      }
    }
    if (bestHex) return bestHex;
  }

  return preferLighter ? '#FFFFFF' : '#000000';
}

export function verifyColorContrast(foregroundHex, backgroundHex, level = 'AA') {
  const fgNorm = normalizeHex(foregroundHex);
  const bgNorm = normalizeHex(backgroundHex);
  const targetLevel = (level || 'AA').toUpperCase() === 'AAA' ? 'AAA' : 'AA';

  if (!fgNorm || !bgNorm) {
    return {
      isError: true,
      error: `Lỗi: Mã màu Hex không hợp lệ (foreground="${foregroundHex}", background="${backgroundHex}"). Hãy truyền định dạng #RRGGBB hoặc #RGB.`
    };
  }

  const fgLum = getRelativeLuminance(fgNorm);
  const bgLum = getRelativeLuminance(bgNorm);
  const ratio = getContrastRatio(fgNorm, bgNorm);
  const ratioRounded = Number(ratio.toFixed(2));

  const normalTarget = targetLevel === 'AAA' ? 7.0 : 4.5;
  const largeTarget = targetLevel === 'AAA' ? 4.5 : 3.0;
  const uiTarget = 3.0;

  const normalPass = ratio >= normalTarget;
  const largePass = ratio >= largeTarget;
  const uiPass = ratio >= uiTarget;

  const suggestedFg = normalPass
    ? fgNorm
    : suggestAccessibleForeground(fgNorm, bgNorm, normalTarget);
  const suggestedRatio = suggestedFg
    ? Number(getContrastRatio(suggestedFg, bgNorm).toFixed(2))
    : null;

  return {
    isError: false,
    data: {
      foreground_hex: fgNorm,
      background_hex: bgNorm,
      foreground_luminance: Number(fgLum.toFixed(4)),
      background_luminance: Number(bgLum.toFixed(4)),
      contrast_ratio: `${ratioRounded.toFixed(2)}:1`,
      contrast_numeric: ratioRounded,
      target_level: targetLevel,
      evaluations: {
        normal_text: {
          required: `${normalTarget.toFixed(1)}:1`,
          status: normalPass ? 'PASS' : 'FAIL'
        },
        large_text: {
          required: `${largeTarget.toFixed(1)}:1`,
          status: largePass ? 'PASS' : 'FAIL'
        },
        ui_component: {
          required: `${uiTarget.toFixed(1)}:1`,
          status: uiPass ? 'PASS' : 'FAIL'
        }
      },
      ...(normalPass
        ? {}
        : {
            suggested_foreground_hex: suggestedFg,
            suggested_contrast_ratio: `${suggestedRatio.toFixed(2)}:1`
          })
    }
  };
}
