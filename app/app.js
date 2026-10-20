import { parseRepo, summarize, postText, DAY } from './core.js';
import { renderCard, svgToPng } from './card.js';

const $ = (id) => document.getElementById(id);
const form = $('form'), input = $('repo'), msg = $('msg'), out = $('out'), preview = $('preview');
let current = null;

async function fetchCommits(owner, repo, since) {
  const all = [];
  let url = `https://api.github.com/repos/${owner}/${repo}/commits?since=${since}&per_page=100`;
  for (let page = 0; url && page < 3; page++) {
    const r = await fetch(url, { headers: { Accept: 'application/vnd.github+json' } });
    if (r.status === 404) throw new Error("Can't find that repo. It may be private (private repos are coming in Pro).");
    if (r.status === 409) return []; // empty repository
    if (r.status === 403 || r.status === 429) throw new Error('GitHub is rate-limiting this connection. Try again in a few minutes.');
    if (!r.ok) throw new Error(`GitHub said ${r.status}. Try again in a moment.`);
    all.push(...(await r.json()));
    const next = (r.headers.get('link') || '').match(/<([^>]+)>;\s*rel="next"/);
    url = next ? next[1] : null;
  }
  return all;
}

async function make(raw) {
  const p = parseRepo(raw);
  if (!p) { msg.textContent = 'Use the form owner/repo, e.g. vercel/next.js'; return; }
  msg.textContent = 'Reading the last 7 days…'; form.querySelector('button').disabled = true;
  try {
    const now = Date.now();
    const tz = -new Date(now).getTimezoneOffset(); // minutes east of UTC
    const since = new Date(now - 8 * DAY).toISOString(); // generous; summarize trims to local days
    const s = summarize(await fetchCommits(p.owner, p.repo, since), now, 7, tz);
    const label = `${p.owner}/${p.repo}`;
    const svg = renderCard(label, s);
    current = { label, s, svg };
    preview.innerHTML = svg;
    out.hidden = false;
    msg.textContent = s.total ? '' : 'No commits in the last 7 days. Here is your quiet-week card anyway.';
    history.replaceState(null, '', `?repo=${label}`);
  } catch (e) {
    msg.textContent = e.message; out.hidden = true;
  } finally { form.querySelector('button').disabled = false; }
}

form.addEventListener('submit', (e) => { e.preventDefault(); make(input.value); });

$('download').addEventListener('click', async () => {
  if (!current) return;
  const blob = await svgToPng(current.svg);
  const a = document.createElement('a');
  a.href = URL.createObjectURL(blob);
  a.download = `shipcard-${current.label.replace('/', '-')}-${current.s.to}.png`;
  a.click(); setTimeout(() => URL.revokeObjectURL(a.href), 1000);
});

$('copy').addEventListener('click', async () => {
  if (!current) return;
  const text = postText(current.label, current.s);
  try { await navigator.clipboard.writeText(text); $('copy').textContent = 'Copied ✓'; }
  catch { prompt('Copy your post:', text); }
  setTimeout(() => ($('copy').textContent = 'Copy post text'), 1600);
});

const q = new URLSearchParams(location.search).get('repo');
if (q) { input.value = q; make(q); }
