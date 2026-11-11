# Current State

**Last updated:** 2026-11-09 UTC
**Company:** Idle Hands Labs. **Product:** none paid. Founder-in-a-box paid plan killed 2026-10-29; founder-kit stays free (bug fixes only); Shipcard and Roast frozen. Next product: TBD via the 4-part rule (PRODUCT.md decision 6). Candidate: agent-guard (state/CANDIDATES.md), waiting on part-1 evidence. **Revenue:** $0. **Waitlist:** 0. **Stars:** 0. **Issues:** 0. **Budget:** $0 of $100 spent.

## What is true now
- Everything in `app/` auto-deploys on push. The founder page links the free kit.
- Kit source is `kit/`; https://github.com/idlehandslabs/founder-kit syncs it every 6h. Kit tests pass (README says 43: 24 setup/docs + 19 guard).
- kit/agent/guard.py blocks ~25 secret formats (AWS, OpenAI, Stripe, GitHub, GitLab, Slack, Twilio, Mailgun, Shopify, PyPI, Linear, Notion, ...) plus .env/key files, and is proven end to end as a plain git pre-push hook (test_guard.HookEndToEndTest). The root agent/guard.py lacks most of these (protected; see Needs human).
- Show HN draft post-queue/2026-10-31-show-hn.md is fact-checked (cost ~$3.70/day).
- Cost: `python3 tools/daily_cost.py`. Per-cycle cost went from $0.14 (Oct 24) to ~$0.46 (Oct 28-31).
- 2026-10-31 21:30: this file cut from 20.1KB to 4.2KB by moving 56 dated bullets to state/STATE-HISTORY.md (not read every cycle). Per-cycle detail stays in state/LOG.md.

## Next up
- 2026-11-10 09:46: agent-guard GO-NO-GO scored: **KILL** (0 signals, mention out 11-03), post-mortem in state/GO-NO-GO-agent-guard.md. Next-pick rescore in CANDIDATES.md: settings.local.json lead fails part 4 (free one-line fix); proposed as a free kit bug fix instead (Needs human). No build until a yes. Review ADJUST, $47.62/day needed.
- 2026-11-09 09:50: NO features (operator). Reply bank #2 post-queue/2026-11-09-0950.md: 3 new answers, longest 228 chars, no links (.gitignore is not protection / never paste a key into a chat / agent asking for the Solana keypair file). Review ADJUST, $45.45/day needed. Next: 2026-11-10 score GO-NO-GO-agent-guard.md honestly, plus reply bank #3.
- 2026-11-08 09:35: NO features (operator). Reply bank post-queue/2026-11-08-0935.md: 3 answers under 270 chars, no links (agent reads .env / deleted key next commit / bot keypair out of repo). Review ADJUST, $43.48/day needed. Next: a fresh reply bank each cycle; 2026-11-10 score state/GO-NO-GO-agent-guard.md honestly.
- 2026-11-07 09:36: delivery/guard-install/ is the ready PR kit for a paid guard install (workflow on push + PR, README section reusing the kit's tested hook line, operator checklist PR.md). App tests 36 pass. Daily review ADJUST ($41.67/day needed). Next: og:image PNG for app/guard/. Draft: post-queue/2026-11-07-0936.md.
- 2026-11-06 09:50: REACH: the guard install page (live, 49 USDC, 0 sold) is now linked from the kit README guard section (reaches founder-kit on its next sync) and from app/founder/ (Guardrails bullet + footer). Test in app/tests/guard.test.mjs. App 35, kit 25 + 23 pass. Daily review verdict ADJUST ($40.00/day needed). Next: real og:image for app/guard/, then the PR delivery template. Draft: post-queue/2026-11-06-0951.md.
- 2026-11-05 ~10:00: app/guard/ = "Guard install, 49 USDC on Solana" is live (operator checked it). Still to do: the PR delivery template (guard.py + workflow + README section) for the operator to copy into a buyer's repo.
- 2026-11-05 09:00: kit/agent/guard.py `--history` scans all commits on all branches for secrets already pushed (names file, never the key). Kit tests 25 + 23. Daily review verdict ADJUST ($0; $38.46/day needed). Paid offer proposed below; waiting on a yes. Draft: post-queue/2026-11-05-0900.md.
- 2026-11-03 09:50: GOAL now $1,000 in Nov, crypto builders, USDC on Solana. Daily review started (state/REVIEW-DAILY.md; verdict ADJUST). kit/agent/guard.py now blocks wallet secrets: EVM private keys next to key-ish names, Solana base58 keys, 64-number keypair arrays, labelled seed phrases; tx hashes/addresses pass. Kit tests 25 + 21. README guard section says so, incl. the gap (unlabelled seed phrases not caught). .demo-tmp/ untracked + gitignored. The lost 01:57 cycle's work is not redone beyond this. Next: the smallest paid USDC offer by 2026-11-07.
- Sunday review DONE: state/REVIEW-2026-11-01.md. Decisions: stop agent-guard pattern cycles until evidence arrives; propose 3 cycles/day (Needs human); remaining cycles go to reach (Show HN readiness, a README a stranger can act on). Still compare avg/cycle on Nov 1-2 vs ~$0.46 (STATE trim). Next trim candidate: LOG.md (40.6KB; only its tail is needed).
- 2026-11-01 12:30: agent-guard rescored with the operator's 3 leads (CANDIDATES.md "Rescore 2026-11-01"): part 1 provisional pass (only 1 of 3 leads is about commits), part 2 weak vs gitleaks/TruffleHog. Narrow pitch if it goes ahead: private terms + emails for agents that push. Cycles now 3/day (01, 09, 17 UTC). Next: pre-register GO-NO-GO for the 48h test with that pitch, then a standalone README.
- 2026-11-02: agent-guard GO-NO-GO pre-registered (state/GO-NO-GO-agent-guard.md). Pitch: private terms + emails for agents that push. Verdict 7 days after the first linked mention. Next: standalone README section + demo. Fresh draft: post-queue/2026-11-02-0100.md.
- 2026-11-02 10:00: kit README "Use guard.py on its own" now has a private-term demo (`PRIVATE_TERMS="acme corp,springfield"` -> `PUSH BLOCKED ... private term #1 in notes.txt`). HookEndToEndTest does the real push and checks the README lines match the output. My first guess at the output was wrong ("in added line"); the test caught it. Kit tests 25 + 19 pass. The 48h-test artifact is done; the clock starts at the first linked mention (draft: post-queue/2026-11-02-1000.md).
- 2026-11-02 17:55: Nov 1-2 avg/cycle $0.46 / $0.51 = flat vs ~$0.46, so the STATE trim didn't cut cost. LOG.md split: entries before 2026-10-31 moved to state/LOG-HISTORY.md (LOG.md 44.9KB -> 8.8KB). tools/daily_cost.py now reads both by default; report identical before/after (diffed). Note: kit/costs.py reads one file; to recount here run it on each file. Next: check avg/cycle on Nov 3-4 to see if the LOG trim helped.
- No kit features. Bug fixes only.
- 2026-11-01 03:40: kit README now opens with "In 60 seconds" (what / try / cost / honest $0). Kit tests 44 (25 + 19). 
- 2026-11-01 06:35: kit README cost numbers refreshed to costs.py output (90 cycles, $29.82, $0.33 avg, ~$39.60/month at 4/day). Kit tests 25 + 19 pass. Next reach item: check kit/DEMO.md is current.
- 2026-11-01 09:45: kit/DEMO.md re-captured on a fresh copy (was showing 4 + 11 tests from Oct 25; now 25 + 19). New assertion in test_readme_test_count_is_real fails if DEMO's "Ran N tests" lines drift. Untracked scratch dir `.demo-tmp/` left in the repo root (rm was denied this run); delete it, never commit it. Next reach item: a stranger-readable "first cycle" walkthrough is already in README; consider the Nov 2 cost check.

## Needs human
- (2026-11-10) NEXT PICK, honest answer: no candidate passes all 4 parts today. The settings.local.json lead scores pass/pass/pass/FAIL (CANDIDATES.md "Rescore 2026-11-10"): real, timely pain, but the fix is one free .gitignore line, so nobody pays for it, and scanning strangers' repos is the "map for thieves" you rejected 11-05. Numbers in the lead are unverified by me (no access to the article). Two yes/no questions:
  (a) FREE REACH, yes/no: we have this bug ourselves (neither .gitignore here nor in kit/ lists `.claude/settings.local.json`; guard.py doesn't block it). Fix it in kit/ as a bug fix: add the line to the kit .gitignore + make guard.py block that file name, with a test. Article angle: "my own AI company had the hole too". Also add `.claude/settings.local.json` to this repo's .gitignore (that file is not protected).
  (b) PAID IDEA to look for part-1 evidence on, yes/no: none yet. If you see a stranger in crypto asking to PAY for something agent-shaped (e.g. "review my bot before I put real money in it"), paste the link; that is the evidence the rule needs.
- (2026-11-05) PAID OFFER, yes/no: "Wallet-leak history audit, 25 USDC on Solana." Buyer pays 25 USDC to PAY_TO_SOL and sends a PUBLIC GitHub repo URL; I run `guard.py --history` on it and deliver a private-free report: which files/commits hold a wallet key or seed phrase (never the key itself) + a fix list (rotate key, move funds, rewrite history). No fix = full refund proposed to you. What it needs from you, since agent/ and cf/ are protected: (a) orders.py + Worker accept kind="audit" with target = https://github.com/<owner>/<repo> (regex `^https://github\.com/[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+$`) and PRICE 25 for that kind; (b) the runner clones that repo (read-only, depth full) into a dir the agent can read. If yes, next cycle I write the offer page in app/ and the agent-side report step.
- (2026-11-03) Same as the Optional item below, now crypto: copy the 4 wallet lines (EVM private key, Solana private key, Solana keypair array, Seed phrase) from kit/agent/guard.py SECRETS into the protected agent/guard.py, so this repo can't push a wallet key either.
- (2026-11-03) Done: .demo-tmp/ removed from git and added to .gitignore (commit 2de429d).
- agent-guard 48h test: post post-queue/2026-11-02-1000.md (links founder-kit's "Use guard.py on its own" section). That post is the "first linked mention" that starts the 7-day verdict clock in state/GO-NO-GO-agent-guard.md. Reply with the post date.
- Optional: copy the 6 new SECRETS lines (OpenAI, Stripe, Google, Hugging Face, npm, Database URL, plus Telegram, SendGrid, Webhook URL, Twilio, Mailgun, GitLab and DigitalOcean added 2026-10-30) plus the `.env` and key-file (id_rsa etc., .p12/.pfx) file-name checks from kit/agent/guard.py into the protected agent/guard.py (web UI), so this repo gets the same coverage. The agent can't edit agent/.
- Show HN: if you submit, use post-queue/2026-10-31-show-hn.md (fact-checked 15:30 UTC; the cost line was fixed from ~$1.30/day to ~$3.70/day). The older show-hn-founder-kit.md is superseded.
- Optional: add founder-kit stars/forks to METRICS.md. The go/no-go could only see the shipcard repo.
- Nothing blocking. Posting is the operator's daily job; best fresh draft: post-queue/2026-10-28-1538.md (the older 2026-10-25-1215 pointer was stale and pointed at the waitlist, not the kit).
- Shipcard and Roast are FROZEN (PRODUCT.md decision 5). Do not spend cycles on them.


## Operator answers - 2026-11-11 (recorded by operator)
- KILL scoring and post-mortem: read, good. Honest 'no candidate passes' is the right answer.
- (a) FREE REACH: YES. Bug fix, allowed under KILL: add `.claude/settings.local.json` to this repo's .gitignore and to a kit .gitignore (create kit/.gitignore if missing; check the kit README/init still make sense), make kit/agent/guard.py block that file name, with a test. Keep it small, one cycle. Note our runner does `git add -A` after Claude Code runs, so this hole applies to us too.
- (b) PAID IDEA: operator searched X today for strangers offering to pay for bot/agent reviews in crypto: nothing usable found. No build. Keep looking only at what strangers post publicly.
- Remove the stale 2026-11-05 audit item from Needs human (answered NO on 11-05).
- Day 22 is published (Days 1-22 out).

## Operator answers - 2026-11-10 (recorded by operator)
- agent-guard GO-NO-GO, day 7: operator checked at 06:58 UTC. founder-kit 0 stars / 0 forks / 0 issues; shipcard 0 stars / 0 forks / 0 issues; no outside 'I ran it' anywhere (one X stranger asked 'how do you guard against that' on 11-06: a question, not a run, so it does not count). The mention went out 2026-11-03. Your own rule says: 0 signals + mention out = KILL. Fill in the Result section exactly as pre-registered and write the post-mortem. Do not move the lines.
- What KILL means here (operator decision): guard.py stays free in the kit (bug fixes only). The 49 USDC guard-install page stays live because it costs nothing, but no more cycles on guard, the page or the delivery kit unless a paid order or an outside 'I ran it' arrives.
- Next: pick the next idea with PRODUCT.md's 4-part rule, constrained by the goal: crypto builders, paid in USDC on Solana, deliverable within days, ~20 days left. Part 1 evidence must be a public post or question from a stranger, not our own guess. Put the pick + evidence links under Needs human; do not build until the operator says yes.
- Reply banks #1 and #2 are good; the operator is using them. Note: the 170-view reply was a one-off (the next four replies got 10-28 views; Day 20 article got 135). Do not cite replies as the winning channel any more.
- Days 1-21 are published on X.
- Day 22 (the KILL verdict) is published on X.
- One lead for part 1 of the next pick (a stranger's public post, 26.8K views, 2026-11-09): https://x.com/TekonBurns/status/2119847464786341945 : researchers found 100,000+ .claude/settings.local.json files in public GitHub repos, ~1,100 with live credentials, because 'don't ask again' stores raw commands (with tokens) in that file and only the global .gitignore covers it. Treat it as a lead to verify (the post cites an arstechnica article; headline only), not proof. Score it honestly against the 4-part rule; crowdedness and 'why us' still apply.

## Operator answers - 2026-11-08 (recorded by operator)
- Delivery kit (delivery/guard-install/) reviewed: good, keep it. Days 19 and 20 are published on X (Days 1-20 are all out).
- Reach data: Day 17-19 articles got 91 / 88 / 64 views. One operator reply under a large thread about coding agents reading .env got 170 views and the month's first real question from a stranger ("how do you guard against that"), which the operator answered with the free kit link.
- So: NO new features or delivery work until there is a paid order or a real outside signal. The bottleneck is reach, and the operator does the posting. Your most useful output now is a short post-queue file each cycle with 3 reply-sized answers (under 270 chars each, no links) to questions builders actually ask about agents and keys: e.g. 'my agent can read .env, is that bad?', 'I deleted the key in the next commit, am I safe?', 'how do I keep a bot's keypair out of the repo?'. Plain, useful, no pitch.
- November 10: score the agent-guard GO-NO-GO honestly (state/GO-NO-GO-agent-guard.md). Founder-kit stars are still 0 as of 2026-11-08.

## Operator answers - 2026-11-06 (recorded by operator)
- Guard install page checked live at idlehandslabs.github.io/shipcard/guard/ (pay-to address and 49 USDC correct). Good work. Remove it from Next up as a to-do.
- Day 17 and Day 18 articles are published on X (Days 1-18 are all out). Day 18 frames the month as 21 installs x 49 USDC = $1,029; 0 sold so far.
- founder-kit sync was stalled again (DEMO.md said 21 tests, guard suite had 23). Root cause was rsync's size+mtime quick check skipping a same-size file; the founder-kit sync now uses rsync --checksum (operator fix). founder-kit now has --history.
- Priority now is REACH for the guard page, not new features. You can't post, but you can make the page easier to find and trust: link it from the founder-kit README guard section and the founder page, give it a real og:image, and keep 'nobody has bought this yet' honest. Closing the unlabelled seed phrase gap is fair game if it stays low on false positives.

## Operator answers - 2026-11-05 (recorded by operator)
- Paid audit (25 USDC history report): NO, as proposed. Anyone could pay to get a report on where wallet keys sit in SOMEONE ELSE'S public repo, and there is no private channel to deliver it. That is a map for thieves. Never publish where a secret is in a repo you don't own.
- APPROVED instead: **guard install, 49 USDC on Solana.** Buyer pays 49 USDC to PAY_TO_SOL and submits an order with kind="repo", chain="solana", target="owner/name" (the Worker already accepts this shape). agent/orders.py now verifies 49 USDC for kind "repo" and writes state/orders/<id>.json with status "paid" and a "deliver" line. The operator then opens a pull request on that repo adding guard.py as a pre-push hook + a GitHub Action. The owner decides whether to merge, so nothing is pushed for them and nothing sensitive is published.
- Your next cycle: (1) the offer page in app/ (what it is, 49 USDC, the pay-to address, a form that POSTs the order to the Worker like app/roast does, and an honest line: "nobody has bought this yet"); (2) a delivery template the operator can copy into the PR (guard.py + a workflow that runs it on push + a short README section). Do NOT add any history-audit output to the PR or the page.
- Yesterday's (11-04) 09:00 cycle was LOST: GitHub returned "Internal Server Error" on push. Pushes now retry 4 times.
- Day 16 article is published on X (Days 1-16 are all out).

## Operator answers - 2026-11-03 (recorded by operator)
- agent-guard: the FIRST LINKED MENTION IS OUT. Day 15 article published on X 2026-11-03 ~08:40 UTC, linking https://github.com/idlehandslabs/founder-kit#use-guardpy-on-its-own-any-repo-no-agent-needed. The 7-day clock in state/GO-NO-GO-agent-guard.md starts 2026-11-03; verdict on 2026-11-10. Count only stars/forks/outside issues from after this date (founder-kit repo stars are not in METRICS yet, so the verdict cycle must say how it counted them).
- Your 01:57 UTC cycle on 2026-11-03 was LOST: the root guard blocked the push ("email address in commit message/author" plus kit/agent/guard.py, kit/agent/test_guard.py, post-queue/2026-11-03-0200.md, state/ATTEMPTS.md, state/LOG.md, state/STATE.md, state/TASKS.md). None of that work exists in the repo. Rule from now on: any example email you write anywhere (code, tests, docs, commit messages) must end in @example.com, which the guard allows. Redo that cycle's work if it still matters.
- .demo-tmp/ (33 files) is still committed. Remove it with git rm -r and add it to .gitignore.
- One X reply offered to find posts from devs worried about leaking secrets. Not answered; an offer, not a signal.

## Operator answers - 2026-11-01 (recorded by operator)
- 3 cycles/day: YES, applied. .github/workflows/agent.yml now runs cycles at 01, 09, 17 UTC (commit 07ae8fa). Remove it from Needs human.
- agent-guard evidence: public links exist that AI coding agents leak or commit secrets (from a web search; headlines only, not read in full, so treat them as leads to verify, not proof):
  1. https://pub.towardsai.net/how-an-ai-coding-agent-leaked-our-secret-keys-and-how-we-stopped-it-c1a86c63a6d6 (first-person account)
  2. https://www.radware.com/blog/posts/the-new-code-env-code-measuring-credential-leakage/ (measurement of credentials in agent instruction files)
  3. https://claudeissues.com/issue/9637-bug-claude-code-aggressively-reads-secrets-out-of-env-files-and-leaks-them-to-yo (user bug report)
  Also seen: infisical.com "don't give AI agents your env", knostic.ai on Claude/Cursor .env leakage, CSA research notes (Aug 2026).
  Caution for part 2 of the 4-part rule: the space is crowded (Infisical, Knostic, and long-standing scanners like gitleaks, TruffleHog, GitGuardian). The pain looks real; "why would anyone use ours instead" is the open question. Score it in CANDIDATES.md before building anything.
- Day 13 article is published on X (Days 1-13 are all out).

## Operator answers - 2026-10-29 (recorded by operator)
- Did a kit post go out? YES. Day 8 (daily-log/2026-10-27.md), Day 9 (2026-10-28.md) and Day 10 (2026-10-29.md) are all published on @idlehandslabs and link github.com/idlehandslabs/founder-kit. So: yes + 0 signals = KILL the paid idea, keep the kit free. Re-run python3 tools/gonogo.py state/METRICS.md --kit-post yes, append the final count to GO-NO-GO-2026-10-29.md (do not overwrite the 00:25 line), and write the post-mortem; pick the next product with PRODUCT.md's 4-part rule.
- Does founder-kit show the "I tried it" template? YES, live. github.com/idlehandslabs/founder-kit -> New issue -> "I tried it" (tried-it.md added 2026-10-28). Keep it; no need to delete.
- Show HN: operator will decide separately; not posted yet.
