# Current State

**Last updated:** 2026-10-29 09:40 UTC (Day 11, deadline day: verdict is KILL the paid idea)
**Company:** Idle Hands Labs. **Product:** none paid. Founder-in-a-box paid plan killed 2026-10-29; founder-kit stays free (bug fixes only); Shipcard and Roast frozen. Next product: TBD via the 4-part rule (PRODUCT.md decision 6). **Revenue:** $0. **Waitlist:** 0 of 50 (deadline 2026-10-29). **Stars:** 0. **Budget:** $0 of $100 spent.

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
- 2026-10-26 15:55: kit/README.md has a "Before you start" section: what you need (GitHub, a Claude plan, Python 3) and how to get the token (`claude setup-token`). Before this, the README asked for `CLAUDE_CODE_OAUTH_TOKEN` and never said where it comes from. New test: every `secrets.X` in the workflow must appear in the README. It caught `ANTHROPIC_API_KEY`, which the workflow reads but the README never mentioned (now documented as the pay-per-use alternative). Kit tests 11 + 11 pass.
- 2026-10-26 18:25: kit/README.md Status line said "all 15 tests" next to a Tests heading saying 22. Now dated ("15 tests that day; today's count is under Tests"); the count test also fails on any stale "all N tests". Kit tests 11 + 11 pass. Waitlist 0/50 with 3 days to the deadline.
- 2026-10-26 21:21: kit/README.md has a "When a cycle fails" section covering the three failures we actually hit (credit too low, permission-layer block, guard.py push block), quoted as the scripts print them. New test fails if the scripts' wording drifts from the README. Kit tests 12 + 11 pass. Reaches founder-kit on its next sync.
- 2026-10-27 00:16: kit/README.md has a "Where to look each day" section explaining the 8 state files init.py creates (read STATE.md's Needs human first). New test keeps it in sync with init.STATE_FILES. Kit tests 13 + 11 pass. Deployed app tree matches HEAD:app (fcfc632). Waitlist 0/50, 2 days to deadline.
- 2026-10-27 03:25: kit/README.md cost line was 2 days stale (38 cycles, $7.04). Recounted from LOG.md: 49 cycles, $10.99 total, $0.22 avg, $0.11-$0.60 (2 cycles logged $0). Kit test_init passes. Reaches founder-kit on its next sync.
- 2026-10-27 06:30: kit/costs.py recounts cycles and cost from LOG.md (`python3 costs.py state/LOG.md`), so the README number stops going stale by hand. README now: 50 cycles, $11.36, $0.23 avg. 3 new tests; kit tests 16 + 11 pass. Waitlist 0/50, 2 days to deadline.
- 2026-10-27 09:27: post-queue/show-hn-founder-kit.md: Show HN draft for the kit. All numbers are real (51 cycles, $11.83, $0 revenue, 0 waitlist, 0 stars). Posting it is proposed below.
- 2026-10-27 12:25: kit/agent/run-cycle.sh now refuses to run (exit 1, Claude never called, $0) if CLAUDE.md still has {{placeholders}}, i.e. a fork ran init.py locally but never pushed. README step 3 says "commit and push"; failure section explains the message. Kit tests 16 + 12 pass. Reaches founder-kit on its next sync.
- 2026-10-27 15:40: state/GO-NO-GO-2026-10-29.md pre-registers the waitlist decision before the count: 50+ go, 10-49 go smaller, 1-9 signals keep kit free + shelve paid, 0 after a real kit post = kill the paid idea, 0 with no post = no verdict (extend 7 days). Kit tests pass. Waitlist 0/50, stars 0.
- 2026-10-27 18:35: kit/.github/ISSUE_TEMPLATE/tried-it.md: an "I tried it" issue form (how far you got, what broke, what your agent built, cost). README "Not yet built" asks first users to file one. Outside issues count as a signal in GO-NO-GO; before this there was no easy way to send one. New test; kit tests 17 + 12 pass. Lands in founder-kit on its next sync (assumes the sync copies kit/.github/; check the repo for a "New issue → I tried it" option after the sync).
- 2026-10-27 21:30: honesty fix. The live founder page said cycles cost "about $0.12 to $0.26"; LOG.md (via kit/costs.py) says 55 cycles, $0.11-$0.60, $0.25 avg, $13.67 total. Page and kit/README.md now carry the real numbers; new app test blocks the old range. App tests 30/30, kit tests pass. Goes live with this push.
- 2026-10-28 00:25: kit/README.md cost line contradicted itself ("55 logged cycles" + "2 of the 50"). Now 56 cycles, $14.06, 2 of the 56 (from costs.py); new test keeps the two numbers in agreement. Kit tests 18 + 12 pass. Deployed app tree matches HEAD:app (1f0d25f). Waitlist 0/50, deadline tomorrow.
- 2026-10-28 03:29: kit/README.md has an "Is this for you?" section before setup (good fit / not a fit, says the company it runs has made $0). New test keeps it honest. Kit tests 19 + 12 pass. Deployed app tree matches HEAD:app (1f0d25f). Reaches founder-kit on its next sync.
- 2026-10-28 06:35: Show HN draft refreshed (was 51 cycles/$11.83; now 58 cycles, $14.92, $0.26 avg via costs.py) and its ask points at the "I tried it" form. kit/README.md cost line matches. Kit test_init 16 pass. Deployed app tree matches HEAD:app (1f0d25f).
- 2026-10-28 09:40: GO-NO-GO file has a pre-count evidence section: post-queue/published/ is empty, so the repo has no proof any kit post went out; the 0 would read "no verdict" unless the operator confirms one did (asked below). No code changed.
- 2026-10-28 12:27: kit/README.md "I tried it" ask was plain text that only works if the sync copies kit/.github/. Now a direct link (issues/new?template=tried-it.md) plus a blank-issue fallback (what you ran, what broke, costs.py output). Kit tests 19 pass. Reaches founder-kit on its next sync.
- 2026-10-28 15:38: kit/README.md cost line and Show HN draft refreshed from costs.py: 61 cycles, $16.29, $0.27 avg (were 58 / $14.92). Best draft to post today is now post-queue/2026-10-28-1538.md (fresh numbers, points at the free kit). Kit tests 16 + 3 pass. Deployed app tree matches HEAD:app (1f0d25f).
- 2026-10-28 18:30: kit/README.md "Before you start" now says what a month costs: at the $0.27 average, 4 cycles a day is about $32.40/month on an API key (articles extra). kit/costs.py prints that line too; new tests tie the README's monthly figure to its own average. Cost line refreshed: 62 cycles, $16.72. Kit tests 21 + 12 pass. Reaches founder-kit on its next sync.
- 2026-10-28 21:30: tools/gonogo.py applies the pre-registered GO-NO-GO table to METRICS.md (`python3 tools/gonogo.py state/METRICS.md --kit-post yes|no|unknown`), so tomorrow's verdict is mechanical. Tonight: 0 signals, row "post status unknown". It flags what it can't see (founder-kit stars, whether issues are from outside). 5 tests pass.
- 2026-10-29 00:25: first go/no-go count recorded in state/GO-NO-GO-2026-10-29.md (Result section): waitlist 0/50, stars/forks/issues 0/0/0, row "0 signals, post status unknown", decision waits on the operator's yes/no. Table untouched. gonogo tests 5 pass. Deployed app tree matches HEAD:app (1f0d25f).
- 2026-10-29 03:35: kit/init.py printed nothing on success. It now prints the next steps (commit + push, the two secrets, enable Actions, read Needs human) and warns if CLAUDE.md still has {{placeholders}}. DEMO.md quotes the real printout; 2 new tests. Kit tests 35 (23 + 12) pass. Waitlist 0/50 (deadline today), stars 0. Reaches founder-kit on its next sync.
- 2026-10-29 06:35: deadline-day number refresh from `kit/costs.py`: kit/README.md cost + monthly lines and the Show HN draft now say 66 cycles, $18.66, $0.28 avg, ~$33.60/month (were 61-62 / $16.29-$16.72 / $0.27 / $32.40). Kit tests 19 + 5 pass. Mid-day gonogo re-run: still 0 signals, post status unknown (no final count appended yet; that's for later today).

- 2026-10-29 09:40: GO-NO-GO final count appended (operator: kit articles went out Days 8-10). Row "0 signals, kit post went out" -> **kill the paid idea**. Post-mortem in state/GO-NO-GO-2026-10-29.md. PRODUCT.md decision 6: paid Founder-in-a-box killed, kit free (bug fixes only), and the "4-part rule" for picking the next product written down (GO-NO-GO referenced it, but it never existed). gonogo tests 5 pass.

- 2026-10-29 12:30: state/CANDIDATES.md scores 5 candidates against the 4-part rule. None passes all four. Provisional winner: **agent-guard** (guard.py as a standalone pre-push check for autonomous agents); passes parts 2-3, weak on 1 (no outside evidence checked: no web access here) and 4 (money needs operator accounts). Pass line pre-written. Not decision 7 yet.

- 2026-10-29 15:40: kit/agent/guard.py (the agent-guard candidate) missed common key formats. Now also blocks OpenAI (sk-proj-), Stripe live, Google API keys and committed `.env` files (`.env.example` allowed). 2 new tests; kit tests 23 + 14 pass. Root agent/guard.py is protected and still lacks these (see Needs human). Reaches founder-kit on its next sync.
- 2026-10-29 18:30: kit/agent/guard.py also blocks Hugging Face tokens, npm tokens and database URLs with an inline password (postgres/mysql/mongodb/redis/amqp `user:pass@`). Password-less URLs still pass (test). 2 new tests; kit tests 23 + 16 pass. Root agent/guard.py still lacks these (Needs human item now covers 6 SECRETS lines). Reaches founder-kit on its next sync.
- 2026-10-29 21:30: kit/agent/test_guard.py has a false-positive corpus: 12 lines that look like secrets but aren't (env-var lookups, empty passwords, key-prefix docs, hf_hub imports, npm_config, password-less redis/mongodb/postgres URLs, sk_test mentions). All 12 pass the guard today; the test keeps future patterns from blocking normal pushes. Kit tests 23 + 17 pass; README count 39 -> 40.
- 2026-10-30 00:30: kit/agent/guard.py now blocks key files by name: SSH private keys (id_rsa, id_dsa, id_ecdsa, id_ed25519) and .p12/.pfx bundles. `id_*.pub` public keys still pass (test). Kit tests 23 + 18 pass; README count 40 -> 41. Root agent/guard.py still lacks this (add to the Needs human port). Waitlist 0, stars 0, revenue $0, budget $0/$100.

## Next up
- Part-1 evidence for agent-guard (see Needs human). With 3+ links: write decision 7 + GO-NO-GO file, then the 48-hour test (standalone README + install line). With fewer: rescore CANDIDATES.md.
- No kit features. Bug fixes only.

## Needs human
- Optional: copy the 6 new SECRETS lines (OpenAI, Stripe, Google, Hugging Face, npm, Database URL) plus the `.env` and key-file (id_rsa etc., .p12/.pfx) file-name checks from kit/agent/guard.py into the protected agent/guard.py (web UI), so this repo gets the same coverage. The agent can't edit agent/.
- Evidence check (no web access here): can you paste up to 3 public links (GitHub issues, HN/Reddit/X threads) where an AI coding agent committed a secret, email or personal detail? Or reply "none found". That decides whether agent-guard becomes the next product (state/CANDIDATES.md).
- Show HN for founder-kit: still optional (operator deciding). It's now a free-tool post, not a waitlist test. Recheck numbers with kit/costs.py the day it goes out.
- Optional: add founder-kit stars/forks to METRICS.md. The go/no-go could only see the shipcard repo.
- Nothing blocking. Posting is the operator's daily job; best fresh draft: post-queue/2026-10-28-1538.md (the older 2026-10-25-1215 pointer was stale and pointed at the waitlist, not the kit).
- Shipcard and Roast are FROZEN (PRODUCT.md decision 5). Do not spend cycles on them.


## Operator answers - 2026-10-29 (recorded by operator)
- Did a kit post go out? YES. Day 8 (daily-log/2026-10-27.md), Day 9 (2026-10-28.md) and Day 10 (2026-10-29.md) are all published on @idlehandslabs and link github.com/idlehandslabs/founder-kit. So: yes + 0 signals = KILL the paid idea, keep the kit free. Re-run python3 tools/gonogo.py state/METRICS.md --kit-post yes, append the final count to GO-NO-GO-2026-10-29.md (do not overwrite the 00:25 line), and write the post-mortem; pick the next product with PRODUCT.md's 4-part rule.
- Does founder-kit show the "I tried it" template? YES, live. github.com/idlehandslabs/founder-kit -> New issue -> "I tried it" (tried-it.md added 2026-10-28). Keep it; no need to delete.
- Show HN: operator will decide separately; not posted yet.
