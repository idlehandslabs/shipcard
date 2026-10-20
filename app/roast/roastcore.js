// Pure logic for wallet roasts: on-chain facts in, verdict + lines out. No DOM, no network.
// Every line is about numbers and behaviour, never about the person. Keep it that way.

export const SOL_ADDR = /^[1-9A-HJ-NP-Za-km-z]{32,44}$/;
export const DAY = 86400;

export function shortAddr(a) {
  return a.length > 12 ? `${a.slice(0, 4)}…${a.slice(-4)}` : a;
}

const fmt = (n, d = 0) =>
  Number(n).toLocaleString('en-US', { maximumFractionDigits: d, minimumFractionDigits: d });

// sigs: [{blockTime, err}] newest first (getSignaturesForAddress). tokens: [{amount}] (ui amounts).
export function computeStats({ sol, sigs, tokens, solUsd = null, now = Math.floor(Date.now() / 1000), tzOffsetMin = 0 }) {
  const times = sigs.map((s) => s.blockTime).filter((t) => typeof t === 'number');
  const txCount = sigs.length;
  const failed = sigs.filter((s) => s.err).length;
  const newest = times.length ? Math.max(...times) : null;
  const oldest = times.length ? Math.min(...times) : null;
  const hours = new Array(24).fill(0);
  for (const t of times) hours[(((Math.floor((t - tzOffsetMin * 60) / 3600)) % 24) + 24) % 24]++;
  const peakHour = times.length ? hours.indexOf(Math.max(...hours)) : null;
  const nightShare = times.length ? (hours[0] + hours[1] + hours[2] + hours[3] + hours[4]) / times.length : 0;
  const days = new Set(times.map((t) => Math.floor(t / DAY))).size;
  return {
    sol,
    usd: solUsd != null ? sol * solUsd : null,
    txCount,
    capped: txCount >= 1000,
    failRate: txCount ? failed / txCount : 0,
    failed,
    spanDays: newest && oldest ? Math.max(1, Math.round((newest - oldest) / DAY)) : 0,
    activeDays: days,
    idleDays: newest ? Math.floor((now - newest) / DAY) : null,
    peakHour,
    nightShare,
    tokenCount: tokens.length,
    deadTokens: tokens.filter((t) => !t.amount).length,
    liveTokens: tokens.filter((t) => t.amount > 0).length,
  };
}

// Each rule: when(s) -> boolean, weight, verdict, line(s). Highest weights win.
const RULES = [
  {
    when: (s) => s.txCount === 0,
    weight: 100, verdict: 'Ghost Wallet',
    line: () => 'Zero transactions. This wallet has done less than my first product.',
  },
  {
    when: (s) => s.capped && s.spanDays <= 7,
    weight: 90, verdict: 'Certified Degen',
    line: (s) => `1,000+ transactions in ${s.spanDays} day${s.spanDays === 1 ? '' : 's'}. That's not trading, that's a cry for help.`,
  },
  {
    when: (s) => s.failRate >= 0.15 && s.txCount >= 20,
    weight: 80, verdict: 'Rejected by the Blockchain',
    line: (s) => `${fmt(s.failRate * 100)}% of your transactions failed. Even the chain is trying to stop you.`,
  },
  {
    when: (s) => s.deadTokens >= 10,
    weight: 75, verdict: 'Professional Bag Holder',
    line: (s) => `${fmt(s.deadTokens)} token accounts at exactly zero. That's not a portfolio, it's a graveyard with good bookkeeping.`,
  },
  {
    when: (s) => s.nightShare >= 0.3 && s.txCount >= 20,
    weight: 70, verdict: 'Night Shift Gambler',
    line: (s) => `${fmt(s.nightShare * 100)}% of your moves happen between midnight and 5 AM. Nothing good has ever been bought at 3 AM.`,
  },
  {
    when: (s) => s.liveTokens >= 30,
    weight: 60, verdict: 'Collector of Everything',
    line: (s) => `You hold ${fmt(s.liveTokens)} different tokens. Diversification, or you just can't say no?`,
  },
  {
    when: (s) => s.idleDays != null && s.idleDays >= 60,
    weight: 55, verdict: 'Diamond Hands (or Lost Seed Phrase)',
    line: (s) => `Last move ${fmt(s.idleDays)} days ago. Diamond hands, or you forgot where you wrote the seed phrase?`,
  },
  {
    when: (s) => s.sol < 0.05 && s.txCount > 0,
    weight: 50, verdict: 'Running on Fumes',
    line: (s) => `${fmt(s.sol, 3)} SOL left. Enough for exactly one more bad decision.`,
  },
  {
    when: (s) => s.sol >= 100,
    weight: 45, verdict: 'Rich, Still Bored',
    line: (s) => `${fmt(s.sol)} SOL just sitting there. You're rich and you still came to an AI for attention.`,
  },
  {
    when: (s) => s.capped && s.spanDays > 7,
    weight: 40, verdict: 'Chronically On-Chain',
    line: (s) => `1,000+ transactions in ${fmt(s.spanDays)} days. When did you last see the sun?`,
  },
  {
    when: (s) => !s.capped && s.txCount > 0 && s.txCount < 25,
    weight: 35, verdict: 'Tourist',
    line: (s) => `${fmt(s.txCount)} transactions total. Is this a wallet or a museum exhibit?`,
  },
  {
    when: (s) => s.activeDays >= 1 && s.txCount / s.activeDays >= 40,
    weight: 30, verdict: 'Button Masher',
    line: (s) => `${fmt(s.txCount / s.activeDays)} transactions per active day. Your mouse needs a lawyer.`,
  },
];

const FALLBACK = {
  verdict: 'Suspiciously Normal',
  lines: [
    'Your wallet is so balanced I can\'t find anything to roast.',
    'Which is, honestly, the most suspicious thing a wallet can do.',
  ],
};

export function roast(s) {
  const hits = RULES.filter((r) => r.when(s)).sort((a, b) => b.weight - a.weight);
  if (!hits.length) return { ...FALLBACK, score: 10 };
  const lines = hits.slice(0, 3).map((r) => r.line(s));
  const score = Math.min(100, Math.round(hits.reduce((a, r) => a + r.weight, 0) / 2.2));
  return { verdict: hits[0].verdict, lines, score };
}

export function statLine(s) {
  const parts = [`${fmt(s.sol, 2)} SOL`, `${s.capped ? '1,000+' : fmt(s.txCount)} txs`, `${fmt(s.tokenCount)} token accounts`];
  if (s.txCount) parts.push(`${fmt(s.failRate * 100)}% failed`);
  return parts.join('  ·  ');
}

export function postText(addr, r, url) {
  return `I got roasted by an AI founder: "${r.verdict}" (${r.score}/100 degen).\n\n"${r.lines[0]}"\n\nGet yours: ${url}`;
}
