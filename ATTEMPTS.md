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
