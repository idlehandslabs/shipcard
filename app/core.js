// Shipcard core: pure functions, no DOM. Works in the browser and in Node tests.

export const DAY = 24 * 60 * 60 * 1000;

/** Accepts "owner/repo", "github.com/owner/repo", full URLs, ".git" suffixes. */
export function parseRepo(input) {
  if (!input) return null;
  let s = String(input).trim().replace(/\.git$/, '').replace(/\/+$/, '');
  s = s.replace(/^https?:\/\//, '').replace(/^www\./, '').replace(/^github\.com\//, '');
  const m = s.match(/^([A-Za-z0-9-]{1,39})\/([A-Za-z0-9._-]{1,100})(?:\/.*)?$/);
  return m ? { owner: m[1], repo: m[2] } : null;
}

const PREFIX = /^(feat|fix|perf|refactor|docs|test|tests|chore|build|ci|style|revert)(\([^)]*\))?!?:\s*/i;
const PRIORITY = { feat: 0, perf: 1, fix: 2, refactor: 3 };

export function isNoise(message) {
  const first = (message || '').split('\n')[0].trim();
  if (!first) return true;
  if (/^Merge (pull request|branch|remote-tracking branch)/i.test(first)) return true;
  if (/^(wip|tmp|temp|\.|-)$/i.test(first)) return true;
  if (/^(chore(\([^)]*\))?:\s*)?(run )?bookkeeping\b/i.test(first)) return true;
  return false;
}

export function cleanMessage(message, max = 64) {
  let s = (message || '').split('\n')[0].trim().replace(PREFIX, '');
  s = s.replace(/\s+/g, ' ');
  if (s) s = s[0].toUpperCase() + s.slice(1);
  s = s.replace(/[.\s]+$/, '');
  return s.length > max ? s.slice(0, max - 1).trimEnd() + '…' : s;
}

function kind(message) {
  const m = (message || '').match(PREFIX);
  return m ? m[1].toLowerCase() : 'other';
}

const iso = (d) => new Date(d).toISOString().slice(0, 10);

/**
 * Summarise GitHub commit objects over the `days` days ending at `now` (UTC days).
 * commits: [{ sha, commit: { message, author: { date } } }]
 */
export function summarize(commits, now = Date.now(), days = 7, tzOffsetMin = 0) {
  // Work in "shifted" time (UTC + offset, minutes east) so UTC day math yields local days.
  const off = tzOffsetMin * 60000;
  now += off;
  const end = new Date(iso(now) + 'T00:00:00Z').getTime() + DAY; // end of today
  const start = end - days * DAY;
  const buckets = [];
  for (let i = 0; i < days; i++) buckets.push({ date: iso(start + i * DAY), count: 0 });

  const kept = [];
  for (const c of commits || []) {
    const msg = c?.commit?.message ?? '';
    const t = Date.parse(c?.commit?.author?.date ?? c?.commit?.committer?.date ?? '') + off;
    if (!Number.isFinite(t) || t < start || t >= end) continue;
    if (isNoise(msg)) continue;
    const idx = Math.floor((t - start) / DAY);
    buckets[idx].count++;
    kept.push({ msg, t });
  }

  // highlights: unique cleaned messages, features first, then most recent
  const seen = new Set();
  const highlights = kept
    .map((k) => ({ ...k, text: cleanMessage(k.msg), pri: PRIORITY[kind(k.msg)] ?? 4 }))
    .filter((k) => k.text && !seen.has(k.text.toLowerCase()) && seen.add(k.text.toLowerCase()))
    .sort((a, b) => a.pri - b.pri || b.t - a.t)
    .slice(0, 4)
    .map((k) => k.text);

  // streak: consecutive active days ending today (or yesterday, if today is empty so far)
  let i = buckets.length - 1;
  if (buckets[i].count === 0) i--;
  let streak = 0;
  for (; i >= 0 && buckets[i].count > 0; i--) streak++;

  return {
    total: kept.length,
    activeDays: buckets.filter((b) => b.count > 0).length,
    streak,
    days: buckets,
    highlights,
    from: buckets[0].date,
    to: buckets[buckets.length - 1].date,
  };
}

export function postText(repoLabel, s) {
  if (!s.total) return `Quiet week on ${repoLabel}. Back at it next week. #buildinpublic`;
  const lines = [
    `This week on ${repoLabel}: ${s.total} commit${s.total === 1 ? '' : 's'} across ${s.activeDays} day${s.activeDays === 1 ? '' : 's'}.`,
  ];
  if (s.highlights.length) lines.push('', ...s.highlights.slice(0, 3).map((h) => `→ ${h}`));
  lines.push('', '#buildinpublic');
  return lines.join('\n');
}
