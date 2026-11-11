import { test } from 'node:test';
import assert from 'node:assert/strict';
import { readFileSync } from 'node:fs';
import { PRICE_USDC } from '../build/buildcore.js';
import { orderBody } from '../guard/guardcore.js';

const read = (p) => readFileSync(new URL(p, import.meta.url), 'utf8');

test('build page: 99 USDC, scope before pay, no keys, honest', () => {
  assert.equal(PRICE_USDC, 99);
  const html = read('../build/index.html');
  assert.match(html, /99 USDC on Solana/);
  assert.match(html, /Scope is agreed before you pay/);
  assert.match(html, /No custody of your keys, ever/);
  assert.match(html, /never ask for a private key/);
  assert.match(html, /Nobody has bought this yet/);
  assert.match(html, /x\.com\/idlehandslabs/);
  assert.match(read('../build/build.js'), /99 USDC/);
});

test('build order uses the kind repo shape the Worker accepts', () => {
  const sig = '5'.repeat(88);
  assert.deepEqual(orderBody('https://github.com/a/b', sig).body, { kind: 'repo', chain: 'solana', target: 'a/b', tx: sig });
});

test('build page is linked from the founder and roast pages', () => {
  assert.match(read('../founder/index.html'), /href="\.\.\/build\/"/);
  assert.match(read('../roast/index.html'), /href="\.\.\/build\/"/);
});
