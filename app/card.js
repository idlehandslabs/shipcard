// Renders a Shipcard summary as a 1200x675 SVG string (X's 16:9 image size).
const W = 1200, H = 675;
const C = { bg: '#F4F1EA', ink: '#121212', soft: '#6B675F', faint: '#DCD6C9', accent: '#FF5A1F' };
const FONT = "Inter, 'Segoe UI', -apple-system, Helvetica, Arial, sans-serif";

const esc = (s) => String(s).replace(/[&<>"']/g, (c) => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c]));
const fmt = (d) => new Date(d + 'T00:00:00Z').toLocaleDateString('en-US', { month: 'short', day: 'numeric', timeZone: 'UTC' });
const dow = (d) => 'SMTWTFS'[new Date(d + 'T00:00:00Z').getUTCDay()];

export function renderCard(label, s, { watermark = true } = {}) {
  const max = Math.max(1, ...s.days.map((d) => d.count));
  const cell = 64, gap = 14, gx = W - 72 - (cell * 7 + gap * 6), gy = 92;

  const strip = s.days.map((d, i) => {
    const x = gx + i * (cell + gap);
    const h = d.count ? 14 + Math.round((cell - 14) * (d.count / max)) : 8;
    const fill = d.count ? C.accent : C.faint;
    return `<rect x="${x}" y="${gy + cell - h}" width="${cell}" height="${h}" rx="10" fill="${fill}"/>
      <text x="${x + cell / 2}" y="${gy + cell + 30}" text-anchor="middle" font-size="20" font-weight="600" fill="${C.soft}">${dow(d.date)}</text>`;
  }).join('');

  const hl = s.highlights.length
    ? s.highlights.map((h, i) => `<text x="72" y="${438 + i * 46}" font-size="30" font-weight="500" fill="${C.ink}"><tspan fill="${C.accent}" font-weight="800">→</tspan>  ${esc(h)}</text>`).join('')
    : `<text x="72" y="438" font-size="30" font-weight="500" fill="${C.soft}">A quiet week. Next one counts.</text>`;

  const stats = `${s.activeDays} active day${s.activeDays === 1 ? '' : 's'}` + (s.streak > 1 ? `  ·  ${s.streak}-day streak` : '');

  return `<svg xmlns="http://www.w3.org/2000/svg" width="${W}" height="${H}" viewBox="0 0 ${W} ${H}" font-family="${FONT}">
  <rect width="${W}" height="${H}" fill="${C.bg}"/>
  <text x="72" y="104" font-size="26" font-weight="700" fill="${C.soft}" letter-spacing="0.5">${esc(label)}</text>
  <text x="72" y="148" font-size="22" font-weight="500" fill="${C.soft}">${fmt(s.from)} – ${fmt(s.to)}</text>
  <text x="66" y="318" font-size="168" font-weight="900" fill="${C.ink}" letter-spacing="-8">${s.total}</text>
  <text x="${72 + String(s.total).length * 96 + 18}" y="268" font-size="40" font-weight="800" fill="${C.ink}" letter-spacing="-1">commit${s.total === 1 ? '' : 's'}</text>
  <text x="${72 + String(s.total).length * 96 + 18}" y="314" font-size="40" font-weight="800" fill="${C.ink}" letter-spacing="-1">shipped</text>
  <text x="${gx}" y="${gy + cell + 78}" font-size="22" font-weight="600" fill="${C.soft}">${esc(stats)}</text>
  ${strip}
  <line x1="72" y1="378" x2="${W - 72}" y2="378" stroke="${C.faint}" stroke-width="2"/>
  ${hl}
  ${watermark ? `<text x="${W - 72}" y="${H - 34}" text-anchor="end" font-size="20" font-weight="600" fill="${C.soft}">made with <tspan fill="${C.ink}" font-weight="800">shipcard</tspan></text>` : ''}
</svg>`;
}

/** Rasterise an SVG string to a PNG Blob (browser only). */
export function svgToPng(svg, scale = 2) {
  return new Promise((resolve, reject) => {
    const img = new Image();
    const url = URL.createObjectURL(new Blob([svg], { type: 'image/svg+xml' }));
    img.onload = () => {
      const c = document.createElement('canvas');
      c.width = W * scale; c.height = H * scale;
      const ctx = c.getContext('2d'); ctx.scale(scale, scale); ctx.drawImage(img, 0, 0);
      URL.revokeObjectURL(url);
      c.toBlob((b) => (b ? resolve(b) : reject(new Error('PNG export failed'))), 'image/png');
    };
    img.onerror = () => { URL.revokeObjectURL(url); reject(new Error('Could not render card')); };
    img.src = url;
  });
}
