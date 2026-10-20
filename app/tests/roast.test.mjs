import { test } from 'node:test';
import assert from 'node:assert/strict';
import { computeStats, roast, statLine, shortAddr, SOL_ADDR, postText } from '../roast/roastcore.js';

const NOW = 1_800_000_000;
const sig = (t, err = null) => ({ blockTime: t, err });

test('address check', () => {
  assert.ok(SOL_ADDR.test('rQATX95gRcH6LRJj3mtsAv182gwsoJWvMqScSXzhvT9'));
  assert.ok(!SOL_ADDR.test('0x1234'));
  assert.ok(!SOL_ADDR.test('hello world'));
  assert.equal(shortAddr('rQATX95gRcH6LRJj3mtsAv182gwsoJWvMqScSXzhvT9'), 'rQAT…hvT9');
});

test('empty wallet is a ghost', () => {
  const s = computeStats({ sol: 0, sigs: [], tokens: [], now: NOW });
  const r = roast(s);
  assert.equal(r.verdict, 'Ghost Wallet');
  assert.equal(r.lines.length, 1);
});

test('degen: 1000 txs in 3 days, many failures, dead tokens', () => {
  const sigs = Array.from({ length: 1000 }, (_, i) => sig(NOW - i * 250, i % 4 === 0 ? { x: 1 } : null));
  const tokens = [...Array(25).fill({ amount: 0 }), ...Array(5).fill({ amount: 3 })];
  const s = computeStats({ sol: 0.01, sigs, tokens, now: NOW });
  assert.equal(s.capped, true);
  assert.equal(s.deadTokens, 25);
  assert.ok(s.failRate > 0.2);
  const r = roast(s);
  assert.equal(r.verdict, 'Certified Degen');
  assert.equal(r.lines.length, 3);
  assert.ok(r.score > 50 && r.score <= 100);
  assert.match(statLine(s), /1,000\+ txs/);
});

test('idle whale', () => {
  const s = computeStats({ sol: 250, sigs: [sig(NOW - 100 * 86400), sig(NOW - 101 * 86400)], tokens: [], now: NOW });
  const r = roast(s);
  assert.ok(r.lines.some((l) => /100 days ago/.test(l)));
  assert.ok(r.lines.some((l) => /250 SOL/.test(l)));
});

test('night owl uses local timezone offset', () => {
  // 30 txs at 02:00 UTC. In UTC+5:30 (offset -330) that is 07:30 local: not night.
  const base = Math.floor(NOW / 86400) * 86400 + 2 * 3600;
  const sigs = Array.from({ length: 30 }, (_, i) => sig(base - i * 86400));
  assert.ok(computeStats({ sol: 1, sigs, tokens: [], now: NOW, tzOffsetMin: 0 }).nightShare > 0.9);
  assert.equal(computeStats({ sol: 1, sigs, tokens: [], now: NOW, tzOffsetMin: -330 }).nightShare, 0);
});

test('lines never mention people, only numbers', () => {
  const sigs = Array.from({ length: 1000 }, (_, i) => sig(NOW - i * 60, i % 3 ? null : {}));
  const r = roast(computeStats({ sol: 0.001, sigs, tokens: Array(40).fill({ amount: 0 }), now: NOW }));
  for (const l of r.lines) assert.ok(!/scam|fraud|criminal|rug/i.test(l), l);
});

test('one-day wonder and dust collector rules', () => {
  const sigs = Array.from({ length: 30 }, (_, i) => sig(NOW - 3600 - i * 60));
  const s = computeStats({ sol: 1, sigs, tokens: [{ amount: 0 }, { amount: 0 }, { amount: 0 }, { amount: 5 }], now: NOW });
  assert.equal(s.activeDays, 1);
  const r = roast(s);
  assert.equal(r.verdict, 'One-Day Wonder');
  assert.ok(r.lines.some((l) => /3 token accounts at zero/.test(l)));
});

test('post text', () => {
  const r = { verdict: 'Tourist', score: 15, lines: ['x'] };
  assert.match(postText('a', r, 'https://u'), /Tourist.*15\/100[\s\S]*https:\/\/u/);
});
