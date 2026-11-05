// Pure logic for the guard-install order. No DOM, no network.
export const PRICE_USDC = 49;
// Same shape agent/orders.py accepts for kind "repo".
export const RX_REPO = /^[A-Za-z0-9_.-]{1,39}\/[A-Za-z0-9_.-]{1,100}$/;
export const RX_SIG = /^[1-9A-HJ-NP-Za-km-z]{64,90}$/;

// "https://github.com/a/b.git", "github.com/a/b/", "a/b" -> "a/b"; anything else -> null.
export function parseRepo(input) {
  let s = String(input || '').trim();
  s = s.replace(/^https?:\/\//i, '').replace(/^(www\.)?github\.com\//i, '');
  s = s.replace(/[?#].*$/, '').replace(/\/+$/, '').replace(/\.git$/i, '');
  if (!RX_REPO.test(s) || s.includes('..')) return null;
  return s;
}

// The exact JSON the Worker's /order endpoint takes.
export function orderBody(repoInput, tx) {
  const target = parseRepo(repoInput);
  if (!target) return { error: 'Use the form owner/name, e.g. idlehandslabs/founder-kit.' };
  const sig = String(tx || '').trim();
  if (!RX_SIG.test(sig)) return { error: 'That does not look like a Solana transaction signature.' };
  return { body: { kind: 'repo', chain: 'solana', target, tx: sig } };
}
