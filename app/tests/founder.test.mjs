import { test } from 'node:test';
import assert from 'node:assert/strict';
import { readFileSync } from 'node:fs';

const html = readFileSync(new URL('../founder/index.html', import.meta.url), 'utf8');

test('founder page links to the open-source kit repo', () => {
  assert.match(html, /href="https:\/\/github\.com\/idlehandslabs\/founder-kit"/);
});

test('founder page still has the waitlist form', () => {
  assert.match(html, /<form id="form">/);
});
