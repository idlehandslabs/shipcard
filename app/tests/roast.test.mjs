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

test('zero SOL with history is Out of Gas', () => {
  const s = computeStats({ sol: 0, sigs: [sig(NOW - 86400), sig(NOW - 2 * 86400)], tokens: [], now: NOW });
  assert.equal(roast(s).verdict, 'Out of Gas');
});

test('many tokens, little SOL is Token Rich, Gas Poor', () => {
  const tokens = Array(20).fill({ amount: 5 });
  const s = computeStats({ sol: 0.2, sigs: [sig(NOW - 86400), sig(NOW - 2 * 86400)], tokens, now: NOW });
  assert.ok(roast(s).lines.some((l) => /20 different tokens/.test(l)));
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

test('slow burner rule', () => {
  const sigs = Array.from({ length: 10 }, (_, i) => sig(NOW - 3600 - i * 50 * 86400));
  const r = roast(computeStats({ sol: 1, sigs, tokens: [], now: NOW }));
  assert.equal(r.verdict, 'Slow Burner');
  assert.match(r.lines[0], /10 transactions over/);
});

test('weekend warrior rule', () => {
  // 1970-01-03 is a Saturday: day index 2.
  const sat = (k) => 2 * 86400 + 3600 + k * 7 * 86400;
  const sigs = Array.from({ length: 25 }, (_, i) => sig(sat(i) + 60 * (i % 5)));
  const s = computeStats({ sol: 1, sigs, tokens: [], now: sat(30) });
  assert.equal(s.weekendShare, 1);
  assert.ok(roast(s).lines.some((l) => /Saturday or Sunday/.test(l)));
});

test('flawless record rule', () => {
  const sigs = Array.from({ length: 150 }, (_, i) => sig(NOW - 3600 - i * 20000));
  const s = computeStats({ sol: 5, sigs, tokens: [], now: NOW });
  assert.equal(s.failed, 0);
  assert.ok(roast(s).lines.some((l) => /zero failures/.test(l)));
});

test('binge trader rule', () => {
  const sigs = Array.from({ length: 60 }, (_, i) => sig(NOW - 3600 - i * 600));
  const s = computeStats({ sol: 2, sigs, tokens: [], now: NOW });
  assert.ok(s.activeDays <= 3);
  assert.ok(roast(s).lines.some((l) => /active day/.test(l)));
});

test('whale rule', () => {
  const s = computeStats({ sol: 2500, sigs: [sig(NOW - 100)], tokens: [], now: NOW });
  assert.ok(roast(s).lines.some((l) => /small island/.test(l)));
});

test('early bird rule', () => {
  const base = 5 * 3600 + 120;
  const sigs = Array.from({ length: 40 }, (_, i) => sig(base + i * 86400 + 60 * (i % 10)));
  const s = computeStats({ sol: 3, sigs, tokens: [], now: NOW });
  assert.equal(s.peakHour, 5);
  assert.ok(roast(s).lines.some((l) => /Up before the sun/.test(l)));
});

test('post text', () => {
  const r = { verdict: 'Tourist', score: 15, lines: ['x'] };
  assert.match(postText('a', r, 'https://u'), /Tourist.*15\/100[\s\S]*https:\/\/u/);
});
