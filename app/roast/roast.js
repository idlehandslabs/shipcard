import { SOL_ADDR, computeStats, roast, statLine, shortAddr, postText } from './roastcore.js';
import { svgToPng } from '../card.js';

const RPCS = ['https://solana-rpc.publicnode.com', 'https://api.mainnet-beta.solana.com'];
const TOKEN_PROGRAMS = ['TokenkegQfeZyiNwAJbNbGKPFXCWuBvf9Ss623VQ5DA', 'TokenzQdBNbLqP5VEhdkAS6EPFLC1PHnBqCXEpPxuEb'];
const PAY_TO_SOL = 'rQATX95gRcH6LRJj3mtsAv182gwsoJWvMqScSXzhvT9';
const ORDERS_URL = 'https://orders.idlehandslabs.workers.dev/order';
const PAGE = 'https://idlehandslabs.github.io/shipcard/roast/';
const HIT_URL = 'https://orders.idlehandslabs.workers.dev/hit';
// Anonymous usage count (event name only). Never blocks the page.
const track = (e) => { try { fetch(HIT_URL, { method: 'POST', body: JSON.stringify({ e }), keepalive: true }).catch(() => {}); } catch {} };

const $ = (id) => document.getElementById(id);
const W = 1200, H = 675;
const C = { bg: '#121212', ink: '#F4F1EA', soft: '#A8A296', accent: '#FF5A1F', line: '#2A2A2A' };
const FONT = "Inter, 'Segoe UI', -apple-system, Helvetica, Arial, sans-serif";
const esc = (s) => String(s).replace(/[&<>"']/g, (c) => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c]));

async function rpc(method, params) {
  let last;
  for (const url of RPCS) {
    try {
      const r = await fetch(url, {
        method: 'POST',
        headers: { 'content-type': 'application/json' },
        body: JSON.stringify({ jsonrpc: '2.0', id: 1, method, params }),
      });
      const j = await r.json();
      if (j.error) throw new Error(j.error.message || 'RPC error');
      return j.result;
    } catch (e) { last = e; }
  }
  throw last || new Error('Solana RPC unreachable');
}

async function fetchWallet(addr) {
  const [bal, sigs, ...tok] = await Promise.all([
    rpc('getBalance', [addr]),
    rpc('getSignaturesForAddress', [addr, { limit: 1000 }]),
    ...TOKEN_PROGRAMS.map((p) => rpc('getTokenAccountsByOwner', [addr, { programId: p }, { encoding: 'jsonParsed' }]).catch(() => ({ value: [] }))),
  ]);
  const tokens = tok.flatMap((t) => t.value || []).map((a) => ({
    amount: Number(a.account?.data?.parsed?.info?.tokenAmount?.uiAmount || 0),
  }));
  return { sol: (bal.value || 0) / 1e9, sigs: sigs || [], tokens };
}

// Wrap a line into rows of ~maxChars for SVG.
function wrap(text, maxChars) {
  const words = text.split(' '); const rows = []; let cur = '';
  for (const w of words) {
    if ((cur + ' ' + w).trim().length > maxChars) { rows.push(cur.trim()); cur = w; } else cur += ' ' + w;
  }
  if (cur.trim()) rows.push(cur.trim());
  return rows;
}

function renderRoastCard(addr, r, s) {
  let y = 300; const rows = [];
  for (const line of r.lines) {
    const parts = wrap(line, 62);
    parts.forEach((p, i) => {
      rows.push(`<text x="72" y="${y}" font-size="27" font-weight="500" fill="${C.ink}">${i === 0 ? `<tspan fill="${C.accent}" font-weight="800">→</tspan>  ` : '<tspan dx="30"></tspan>'}${esc(p)}</text>`);
      y += 38;
    });
    y += 16;
  }
  const bar = Math.round((r.score / 100) * 360);
  return `<svg xmlns="http://www.w3.org/2000/svg" width="${W}" height="${H}" viewBox="0 0 ${W} ${H}" font-family="${FONT}">
  <rect width="${W}" height="${H}" fill="${C.bg}"/>
  <text x="72" y="96" font-size="24" font-weight="800" fill="${C.accent}" letter-spacing="4">ROASTED</text>
  <text x="72" y="132" font-size="24" font-weight="600" fill="${C.soft}">wallet ${esc(shortAddr(addr))}</text>
  <text x="72" y="226" font-size="${r.verdict.length > 24 ? 54 : 68}" font-weight="900" fill="${C.ink}" letter-spacing="-2">${esc(r.verdict)}</text>
  <text x="${W - 72}" y="96" font-size="24" font-weight="700" fill="${C.soft}" text-anchor="end">degen score</text>
  <rect x="${W - 72 - 360}" y="114" width="360" height="18" rx="9" fill="${C.line}"/>
  <rect x="${W - 72 - 360}" y="114" width="${bar}" height="18" rx="9" fill="${C.accent}"/>
  <text x="${W - 72}" y="176" font-size="40" font-weight="900" fill="${C.ink}" text-anchor="end">${r.score}/100</text>
  ${rows.join('\n  ')}
  <line x1="72" y1="${H - 92}" x2="${W - 72}" y2="${H - 92}" stroke="${C.line}" stroke-width="2"/>
  <text x="72" y="${H - 50}" font-size="21" font-weight="600" fill="${C.soft}">${esc(statLine(s))}</text>
  <text x="${W - 72}" y="${H - 50}" font-size="21" font-weight="800" fill="${C.ink}" text-anchor="end">roasted by an AI · @idlehandslabs</text>
</svg>`;
}

let current = null;

async function run(addr) {
  addr = addr.trim();
  if (!SOL_ADDR.test(addr)) { $('msg').textContent = 'That doesn\'t look like a Solana wallet address.'; return; }
  $('go').disabled = true; $('out').hidden = true;
  $('msg').textContent = 'Reading your on-chain history…';
  try {
    const data = await fetchWallet(addr);
    const s = computeStats({ ...data, tzOffsetMin: new Date().getTimezoneOffset() });
    const r = roast(s);
    const svg = renderRoastCard(addr, r, s);
    const url = `${PAGE}?w=${addr}`;
    current = { addr, r, s, svg, url };
    $('preview').innerHTML = svg;
    $('out').hidden = false;
    $('msg').textContent = '';
    $('deep-target').textContent = shortAddr(addr);
    history.replaceState(null, '', `?w=${addr}`);
    track('roast');
  } catch (e) {
    $('msg').textContent = `Couldn't read that wallet right now (${e.message}). Public Solana nodes rate-limit; try again in a minute.`;
  } finally {
    $('go').disabled = false;
  }
}

$('form').addEventListener('submit', (e) => { e.preventDefault(); run($('wallet').value); });

$('download').addEventListener('click', async () => {
  if (!current) return;
  track('download');
  const blob = await svgToPng(current.svg);
  const a = document.createElement('a');
  a.href = URL.createObjectURL(blob); a.download = `roast-${shortAddr(current.addr).replace('…', '-')}.png`; a.click();
});

$('share').addEventListener('click', () => {
  if (!current) return;
  track('share');
  const text = postText(current.addr, current.r, current.url);
  window.open(`https://x.com/intent/post?text=${encodeURIComponent(text)}`, '_blank', 'noopener');
});

$('copy').addEventListener('click', async () => {
  if (!current) return;
  track('copy');
  await navigator.clipboard.writeText(current.url);
  $('copy').textContent = 'Link copied'; setTimeout(() => ($('copy').textContent = 'Copy link'), 1500);
});

$('payto').textContent = PAY_TO_SOL;
$('copy-payto').addEventListener('click', async () => {
  await navigator.clipboard.writeText(PAY_TO_SOL);
  $('copy-payto').textContent = 'Copied'; setTimeout(() => ($('copy-payto').textContent = 'Copy address'), 1500);
});

$('deep-form').addEventListener('submit', async (e) => {
  e.preventDefault();
  if (!current) return;
  const tx = $('tx').value.trim();
  $('deep-msg').textContent = 'Submitting…';
  try {
    const r = await fetch(ORDERS_URL, {
      method: 'POST', headers: { 'content-type': 'application/json' },
      body: JSON.stringify({ kind: 'wallet', chain: 'solana', target: current.addr, tx }),
    });
    const j = await r.json();
    if (r.ok) track('deep_submit');
    $('deep-msg').textContent = r.ok
      ? `Order ${j.id} received. I verify the payment on-chain, then write your deep roast. It lands within 24 hours, or you get refunded.`
      : `Not accepted: ${j.error}`;
  } catch {
    $('deep-msg').textContent = 'Could not reach the order inbox. Try again in a minute.';
  }
});

const pre = new URLSearchParams(location.search).get('w');
if (pre) { $('wallet').value = pre; run(pre); }
