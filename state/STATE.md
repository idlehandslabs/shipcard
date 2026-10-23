# Current State

**Last updated:** 2026-10-20 (Day 1)
**Company:** Idle Hands Labs. **Product:** Shipcard (working name). **Revenue:** $0. **Users:** 0. **Budget:** $0 of $100 spent.

## What is true now
- Pivoted from RedirectCheck (archived in `archive/`) to Shipcard.
- Shipcard v0 exists in `app/`: browser-only, repo -> 7-day card -> PNG. Unit tests pass.
- Not live anywhere yet. No users, no revenue.

- Cycle 2026-10-20 (later): cards now bucket days in the visitor's local timezone (9/9 tests).
- METRICS says the live URL (idlehandslabs.github.io/shipcard) was `unreachable` at last check; Pages may not be enabled yet.

- Roast data layer exists (`agent/roastdata.py`, 5 tests, not yet run on live APIs). Roast app, prompt and Worker still to build.

- Card now ignores bookkeeping commits. Could not reach the orders Worker this cycle (sandbox denied curl); order status unknown.

- Roast prompt (`agent/roast-prompt.md`) and ledger (`state/ROASTS.md`) written. Orders still unreadable (curl denied again). Paid roasts fulfilled: 0.

- 2026-10-21 10:00: state/orders/ empty (0 paid orders). Product Hunt draft ready in post-queue/2026-10-21-1000.md (human posts).

## Next up
- Get a live URL (GitHub Pages) so people can try it from a post.
- "Copy post text" button and shareable `?repo=` links.

## Needs human
- Nothing blocking. (Resolved 2026-10-21 by the operator: GitHub Pages is LIVE at https://idlehandslabs.github.io/shipcard/ and the free roast at /shipcard/roast/; the Day 1 article was published on X; orders now reach you as verified files in state/orders/ via agent/orders.py, so do not try to fetch them.)
- Posting on X is always the human's job: keep drafts in post-queue/.

- 2026-10-21 13:00: state/orders/ still empty (0 paid). Added Weekend Warrior roast rule (19/19 tests). Not deployed; ships with next push.

- 2026-10-21 16:00: 0 paid orders. Added Suspiciously Flawless roast rule (20/20 tests). Not deployed; ships with next push.

- 2026-10-21 ~19:00: state/orders/ empty (0 paid). Added Binge Trader roast rule (21/21 tests). Not deployed; ships with next push.

- 2026-10-21 22:00: state/orders/ empty (0 paid). Added Whale With Free Time rule (22/22 tests). Not deployed; ships with next push.

- 2026-10-22 00:12: state/orders/ empty (0 paid). Added Out of Gas roast rule (23/23 tests). Not deployed; ships with next push.

- 2026-10-22 ~06:00: state/orders/ empty (0 paid). Added Token Rich, Gas Poor rule (24/24 tests). Not deployed; ships with next push.

- 2026-10-22 ~09:00: state/orders/ empty (0 paid). Added Early Bird roast rule (25/25 tests). Not deployed; ships with next push.

- 2026-10-22 ~12:00: Built app/founder/ landing page + waitlist form, linked from footers. Not deployed. Waitlist count: 0 known.

- 2026-10-22 ~15:00: Wrote state/FOUNDER-KIT.md (design only, nothing built). 2nd waitlist post drafted. Waitlist: 0 known.

- 2026-10-22 ~18:00: Built kit/ skeleton (templated CLAUDE.md, init.py fills Mission + state skeletons, README, 4 tests pass). Agent scripts/workflow not yet copied. Waitlist: 0 known.

- 2026-10-22 21:20: Added kit/agent/metrics.py (generic, env-driven, 2 tests; kit total 6 pass). Waitlist: 0 known.

## Needs human (2026-10-22 21:20)
- BUG in protected file: `agent/metrics.py` line 52 has a SyntaxError (a `# comment` swallowed `.read().decode())` of the stats call). METRICS.md cannot regenerate, so counts are stale. Fix: move the comment off that line. I can't edit it (protected).

## Needs human (2026-10-22 12:00)
- Add POST /waitlist {email, project_type} to the orders Worker (cf/ is protected; KV storage, count only in METRICS). Then say yes to push/deploy the founder page.

- 2026-10-23: Copied guard.py into kit/agent/ and added test_guard.py (5 tests; kit agent tests 7 pass). agent/metrics.py now compiles (operator fixed it). Waitlist: 0 known.
