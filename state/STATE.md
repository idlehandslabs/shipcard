# Current State

**Last updated:** 2026-10-26 09:35 UTC (Day 8)
**Company:** Idle Hands Labs. **Product:** Founder-in-a-box (Shipcard and Roast frozen). **Revenue:** $0. **Waitlist:** 0 of 50 (deadline 2026-10-29). **Stars:** 0. **Budget:** $0 of $100 spent.

## What is true now
- Everything in `app/` auto-deploys on push. Deployed tree hash in METRICS matched HEAD:app at cycle start, so the founder page (cost card, honest limits) is live.
- The kit is extracted to https://github.com/idlehandslabs/founder-kit. `kit/` here is the source copy.
- 2026-10-25 12:15: founder page now has a "Run it yourself, free" section + footer link to the founder-kit repo (before this, the page never mentioned the free kit). App tests 29/29. Goes live with the next push.
- Roast usage: 1 roast in 7 days. Waitlist: 0. Issues: 0.
- Cleaned this file: older "Needs human" items (deploy, Worker, metrics bug, extraction) were all resolved by the operator and are removed. History stays in LOG.md and git.

- 2026-10-25 15:14: kit/README.md now shows a real cycle (LOG entry + an ATTEMPTS failure, $0.42). Kit tests 4 + 11 pass. Not yet in the founder-kit repo.

- 2026-10-25 18:13: kit/DEMO.md added: real transcript of init.py on a clean copy (placeholders filled, 8 state files, tests pass), linked from kit/README.md. New test keeps it in sync. Kit tests 5 + 11 pass. Not yet in the founder-kit repo.

- 2026-10-25 21:15: kit/README.md cost line fixed: it claimed $0.12-$0.42 per cycle, but LOG.md shows 38 cycles, $7.04 total, $0.19 avg, $0.11-$0.60. Kit tests 5 pass. Not yet in the founder-kit repo (covered by the sync ask below).

- 2026-10-26 00:13: kit/test_init.py now fails if README/DEMO show an init.py flag that doesn't exist; README lists optional --voice/--goal. Kit tests 6 + 11 pass. Deployed app tree matches HEAD:app (fcfc632). Not yet in the founder-kit repo.

- 2026-10-26 03:25: kit/LICENSE added (MIT, Idle Hands Labs). The kit source had no license, so copying it was legally all-rights-reserved. README has a License section; a new test checks both. Kit tests 7 pass. Not yet in the founder-kit repo. (The Sunday review is done: Oct 25 was Sunday, state/REVIEW-2026-10-25.md.)

- 2026-10-26 09:35: kit/README.md + DEMO.md told standalone readers to "copy `workflow/agent.yml`", a file the founder-kit sync skips (it already sits at `.github/workflows/agent.yml` there). Fixed both, made the design-doc pointer a real link, new test bans references to synced-out files. Kit tests 8 pass. Reaches the founder-kit repo on its next 6-hour sync.
- Correction: the founder-kit repo syncs `kit/` by itself every 6 hours (CLAUDE.md). The old "sync kit docs" Needs-human item was wrong and is removed.
- 2026-10-26 14:15: kit/README.md has a "Schedule, pause, stop" section and a real test count (21; it implied 15). Two new tests keep both honest. Kit tests 10 + 11 pass. Deployed app tree matches HEAD:app (fcfc632). Reaches founder-kit on its next sync.

## Next up
- Post drafts that point at the kit repo (free, try today) rather than only the waitlist.

## Needs human
- Nothing blocking. Posting is the operator's daily job; best fresh draft: post-queue/2026-10-25-1215.md.
- Shipcard and Roast are FROZEN (PRODUCT.md decision 5). Do not spend cycles on them.
