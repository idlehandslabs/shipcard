import { test } from 'node:test';
import assert from 'node:assert/strict';
import { readFileSync } from 'node:fs';
import { parseRepo, orderBody, PRICE_USDC } from '../guard/guardcore.js';

const SIG = '5'.repeat(88);

test('repo input forms normalise to owner/name', () => {
  assert.equal(parseRepo('idlehandslabs/founder-kit'), 'idlehandslabs/founder-kit');
  assert.equal(parseRepo('https://github.com/idlehandslabs/founder-kit.git'), 'idlehandslabs/founder-kit');
  assert.equal(parseRepo('github.com/a/b/'), 'a/b');
  assert.equal(parseRepo('https://www.github.com/a/b?tab=readme'), 'a/b');
});

test('bad repo input is rejected', () => {
  for (const bad of ['', 'a', 'a/b/c', 'a/..', '../x', 'https://gitlab.com/a/b', 'a/b c']) assert.equal(parseRepo(bad), null, bad);
});

test('order body matches what orders.py accepts for kind repo', () => {
  assert.deepEqual(orderBody('a/b', ` ${SIG} `).body, { kind: 'repo', chain: 'solana', target: 'a/b', tx: SIG });
  assert.ok(orderBody('nope', SIG).error);
  assert.ok(orderBody('a/b', 'not-a-sig').error);
});

test('price matches orders.py and the page is honest', () => {
  assert.equal(PRICE_USDC, 49);
  const py = readFileSync(new URL('../../agent/orders.py', import.meta.url), 'utf8');
  assert.match(py, /"repo":\s*49\.0/);
  const html = readFileSync(new URL('../guard/index.html', import.meta.url), 'utf8');
  assert.match(html, /Nobody has bought this yet/);
  assert.doesNotMatch(html, /history/i);
});

test('guard page is linked from the founder page and the kit README', () => {
  const founder = readFileSync(new URL('../founder/index.html', import.meta.url), 'utf8');
  assert.match(founder, /href="\.\.\/guard\/"/);
  const readme = readFileSync(new URL('../../kit/README.md', import.meta.url), 'utf8');
  assert.match(readme, /idlehandslabs\.github\.io\/shipcard\/guard\//);
  assert.match(readme, /49 USDC/);
  assert.match(readme, /Nobody has\s+bought this yet/);
});

test('delivery template: workflow runs guard.py; hook matches the kit; no history scan', () => {
  const read = (p) => readFileSync(new URL('../../delivery/guard-install/' + p, import.meta.url), 'utf8');
  const wf = read('.github/workflows/guard.yml');
  assert.match(wf, /on: \[push, pull_request\]/);
  assert.match(wf, /fetch-depth: 0/);
  assert.match(wf, /contents: read/);
  assert.match(wf, /python3 agent\/guard\.py "\$BEFORE"/);
  const section = read('README-SECTION.md');
  const kit = readFileSync(new URL('../../kit/README.md', import.meta.url), 'utf8');
  const hook = 'exec python3 agent/guard.py "$(git rev-parse @{u} 2>/dev/null || echo HEAD~1)"';
  assert.ok(section.includes(hook) && kit.includes(hook), 'hook line must match the tested kit README');
  assert.match(section, /not caught/);
  for (const p of ['.github/workflows/guard.yml', 'README-SECTION.md', 'PR.md']) {
    assert.doesNotMatch(read(p), /--history/);
  }
  assert.match(read('PR.md'), /status "paid"/);
});
