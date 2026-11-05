import { orderBody, PRICE_USDC } from './guardcore.js';

const PAY_TO_SOL = 'rQATX95gRcH6LRJj3mtsAv182gwsoJWvMqScSXzhvT9';
const ORDERS_URL = 'https://orders.idlehandslabs.workers.dev/order';
const HIT_URL = 'https://orders.idlehandslabs.workers.dev/hit';
const track = (e) => { try { fetch(HIT_URL, { method: 'POST', body: JSON.stringify({ e }), keepalive: true }).catch(() => {}); } catch {} };
const $ = (id) => document.getElementById(id);

track('guard_view');
$('price').textContent = PRICE_USDC;
$('payto').textContent = PAY_TO_SOL;
$('copy-payto').addEventListener('click', async () => {
  await navigator.clipboard.writeText(PAY_TO_SOL);
  $('copy-payto').textContent = 'Copied'; setTimeout(() => ($('copy-payto').textContent = 'Copy address'), 1500);
});

$('order-form').addEventListener('submit', async (e) => {
  e.preventDefault();
  const o = orderBody($('repo').value, $('tx').value);
  if (o.error) { $('order-msg').textContent = o.error; return; }
  $('order-msg').textContent = 'Submitting…';
  try {
    const r = await fetch(ORDERS_URL, {
      method: 'POST', headers: { 'content-type': 'application/json' }, body: JSON.stringify(o.body),
    });
    const j = await r.json();
    if (r.ok) track('guard_submit');
    $('order-msg').textContent = r.ok
      ? `Order ${j.id} received for ${o.body.target}. I verify the 49 USDC on-chain, then a pull request adding guard.py opens on that repo within 48 hours. You decide whether to merge. No PR, full refund.`
      : `Not accepted: ${j.error}`;
  } catch {
    $('order-msg').textContent = 'Could not reach the order inbox. Try again in a minute.';
  }
});
