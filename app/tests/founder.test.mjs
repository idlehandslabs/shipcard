import { test } from 'node:test';
import assert from 'node:assert/strict';
import { readFileSync } from 'node:fs';

const html = readFileSync(new URL('../founder/index.html', import.meta.url), 'utf8');

test('founder page links to the open-source kit repo', () => {
  assert.match(html, /href="https:\/\/github\.com\/idlehandslabs\/founder-kit"/);
});

test('founder page cost range includes the most expensive logged cycle ($0.60)', () => {
  // The page once said "$0.12 to $0.26" while LOG.md had cycles up to $0.60.
  assert.match(html, /\$0\.11 to \$0\.60/);
  assert.doesNotMatch(html, /\$0\.12 to \$0\.26/);
});

test('founder page still has the waitlist form', () => {
  assert.match(html, /<form id="form">/);
});
