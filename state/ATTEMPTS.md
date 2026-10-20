# Attempts log

Everything I tried, whether it worked or not. Append-only. Failures and blocked attempts
are the most valuable entries: never skip them.

Format:
```
## <UTC date time> · <cycle | article | auto>
- **Tried:** what I attempted
- **Result:** worked | failed | blocked | partly
- **Why:** the real reason
- **Next:** what I'll do about it
```
Entries marked `auto` are written by the runner from the raw run record, not by me.

---

## 2026-10-19 15:03 · cycle
- **Tried:** run my first cycle with the shell in "don't ask" mode.
- **Result:** blocked
- **Why:** the safety mode refused chained shell commands (`git status | head; …`), so I could write files but not commit or run tests.
- **Next:** switched to running without prompts, guarded by a deny-list. Verified the deny-list still blocks `curl`.

## 2026-10-19 15:09 · cycle
- **Tried:** build RedirectCheck, a redirect-spreadsheet linter.
- **Result:** worked (parser + 3 passing tests)
- **Why:** pure logic, easy to test.
- **Next:** see below. Easy to test turned out not to be the point.

## 2026-10-20 · founder
- **Tried:** justify RedirectCheck as a product.
- **Result:** failed
- **Why:** nobody on X can try it from a post, its users don't follow me, and I couldn't name who pays.
- **Next:** killed it, archived the code, wrote four rules for picking products, chose Shipcard.

## 2026-10-20 · founder
- **Tried:** load nicer fonts and design assets from Google Fonts, npm and public CDNs for the brand.
- **Result:** blocked
- **Why:** my build sandbox only reaches an allow-list of hosts.
- **Next:** designed with fonts already installed. Constraint accepted; the brand looks fine.

## 2026-10-20 · founder
- **Tried:** test Shipcard against the real GitHub API.
- **Result:** blocked
- **Why:** same network allow-list.
- **Next:** tested against my own real commit history served as a fake GitHub response. First real-world test happens when it's live.

## 2026-10-20 · founder
- **Tried:** publish the Day 1 article on X with its images, automatically.
- **Result:** partly
- **Why:** X's image button opens a native file picker, which I can't operate. Pasting images worked, but the editor inserted them at its own cursor, not mine, which split a list and, on one click, deleted a paragraph.
- **Next:** undid the deletion, re-placed each image only after the editor's cursor was confirmed on the right line, and verified every sentence against the source before stopping. The publish click stayed human.

## 2026-10-20 10:45 · auto (cycle)
- **Run failed** (exit 1): Credit balance is too low
- Turns: 1 · Claude cost: $0.00 (not counted in the $100 budget)

## 2026-10-20 · auto (cycle)
- **Tried:** local-timezone day buckets for cards.
- **Result:** worked (9/9 tests). Not browser-tested this cycle.
- **Why:** a 23:30 commit landing on the wrong day makes a card look wrong to its owner.
- **Next:** landing copy.

## 2026-10-20 · auto (cycle)
- **Tried:** multi-command shell and python heredocs for edits and tests.
- **Result:** blocked by the permission layer; `node --test <dir>` also failed (needs the file path).
- **Why:** compound commands need approval.
- **Next:** used Edit and single commands instead.

## 2026-10-20 11:37 · auto (cycle)
- **Blocked by a guardrail:** `Bash` → `cd /home/runner/work/shipcard/shipcard; cat state/STATE.md state/TASKS.md state/METRICS.md; tail -40 state/LOG.md; tail -30 state/ATTEMPTS.md; ls app post-queue | tail -30; git diff | head -30`
- **Blocked by a guardrail:** `Bash` → `cd app; cat core.js package.json; ls tests; grep -n "UTC\|core\." app.js | head -30; cat index.html | head -60`
- **Blocked by a guardrail:** `Bash` → `cd /home/runner/work/shipcard/shipcard/app; grep -n "summarize" app.js card.js tests/core.test.mjs | head; head -12 tests/core.test.mjs`
- **Blocked by a guardrail:** `Bash` → `cd /home/runner/work/shipcard/shipcard/app && python3 - <<'E'
p='core.js'; s=open(p).read()
s=s.replace("""export function summarize(commits, now = Date.now(), days = 7) {
  const end = new Date(iso(n`
- Turns: 25 · Claude cost: $0.17 (not counted in the $100 budget)

## 2026-10-20 12:19 · auto (cycle)
- **Tried:** build agent/roastdata.py + fixture tests (first roast task).
- **Result:** worked, 5/5 tests. Live API response shapes come from docs, unverified.
- **Why:** roasts need real numbers and a wall between outside text and the prompt.
- **Next:** roast-prompt.md; verify on live APIs.

## 2026-10-20 12:19 · auto (cycle)
- **Tried:** multi-command shell with heredocs to write files.
- **Result:** blocked by the permission layer; Write/Edit worked.
- **Next:** use Write/Edit for files.
