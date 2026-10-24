import { test } from 'node:test';
import assert from 'node:assert/strict';
import { parseRepo, cleanMessage, isNoise, summarize, postText } from '../core.js';

const NOW = Date.parse('2026-10-20T15:00:00Z');
const c = (date, message) => ({ sha: Math.random().toString(16).slice(2), commit: { message, author: { date } } });

test('isNoise skips dependency bumps and bare doc touch-ups but keeps real work', () => {
  assert.equal(isNoise('Bump lodash from 4.17.20 to 4.17.21'), true);
  assert.equal(isNoise('chore(deps): bump axios from 1.0.0 to 1.1.0'), true);
  assert.equal(isNoise('Update README.md'), true);
  assert.equal(isNoise('Update pricing page copy'), false);
  assert.equal(isNoise('feat: bump allocator for faster parsing'), false);
});

test('summarize can bucket by local day via tzOffsetMin', () => {
  // 23:30 UTC on the 19th is already the 20th at UTC+2
  const list = [c('2026-10-19T23:30:00Z', 'a')];
  assert.equal(summarize(list, NOW, 7, 0).days.at(-2).count, 1);
  const s = summarize(list, NOW, 7, 120);
  assert.equal(s.days.at(-1).date, '2026-10-20');
  assert.equal(s.days.at(-1).count, 1);
});

test('parseRepo accepts common forms', () => {
  for (const s of ['vercel/next.js', 'github.com/vercel/next.js', 'https://github.com/vercel/next.js',
                   'https://github.com/vercel/next.js.git', 'https://www.github.com/vercel/next.js/tree/canary/docs'])
    assert.deepEqual(parseRepo(s), { owner: 'vercel', repo: 'next.js' }, s);
  assert.equal(parseRepo('not a repo'), null);
  assert.equal(parseRepo(''), null);
  assert.equal(parseRepo('https://gitlab.com/a/b'), null);
});

test('cleanMessage strips prefixes, keeps first line, truncates', () => {
  assert.equal(cleanMessage('feat(ui): add PNG export\n\nlong body'), 'Add PNG export');
  assert.equal(cleanMessage('fix!: crash on empty repo.'), 'Crash on empty repo');
  assert.equal(cleanMessage('x'.repeat(100), 20).length, 20);
});

test('isNoise drops merges and junk', () => {
  assert.ok(isNoise('Merge pull request #12 from a/b'));
  assert.ok(isNoise('wip'));
  assert.ok(isNoise(''));
  assert.ok(isNoise('Run bookkeeping for cycle 4'));
  assert.ok(isNoise('chore: bookkeeping'));
  assert.ok(!isNoise('Add card renderer'));
});

test('summarize buckets the last 7 UTC days and ignores older/newer commits', () => {
  const s = summarize([
    c('2026-10-20T09:00:00Z', 'feat: card renderer'),
    c('2026-10-20T10:00:00Z', 'fix: rate limit message'),
    c('2026-10-19T23:59:00Z', 'docs: readme'),
    c('2026-10-14T00:00:00Z', 'chore: setup'),          // first day of window
    c('2026-10-13T23:59:59Z', 'too old'),
    c('2026-10-21T00:00:00Z', 'future'),
    c('2026-10-18T12:00:00Z', 'Merge branch main'),       // noise
  ], NOW);
  assert.equal(s.total, 4);
  assert.equal(s.days.length, 7);
  assert.equal(s.from, '2026-10-14');
  assert.equal(s.to, '2026-10-20');
  assert.deepEqual(s.days.map((d) => d.count), [1, 0, 0, 0, 0, 1, 2]);
  assert.equal(s.activeDays, 3);
  assert.equal(s.streak, 2);
  assert.equal(s.highlights[0], 'Card renderer');            // features first
});

test('highlights are unique and capped at 4', () => {
  const list = ['feat: a', 'feat: a', 'feat: b', 'fix: c', 'docs: d', 'chore: e', 'refactor: f']
    .map((m, i) => c(`2026-10-20T0${i}:00:00Z`, m));
  const s = summarize(list, NOW);
  assert.equal(s.highlights.length, 4);
  assert.equal(new Set(s.highlights).size, 4);
});

test('streak counts back from yesterday when today is empty', () => {
  const s = summarize([c('2026-10-19T10:00:00Z', 'a'), c('2026-10-18T10:00:00Z', 'b')], NOW);
  assert.equal(s.streak, 2);
});

test('empty week', () => {
  const s = summarize([], NOW);
  assert.equal(s.total, 0);
  assert.equal(s.streak, 0);
  assert.match(postText('a/b', s), /Quiet week/);
});

test('postText summarises', () => {
  const s = summarize([c('2026-10-20T09:00:00Z', 'feat: card renderer')], NOW);
  const t = postText('me/shipcard', s);
  assert.match(t, /1 commit across 1 day/);
  assert.match(t, /→ Card renderer/);
});
