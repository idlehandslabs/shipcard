# Current State

**Last updated:** 2026-11-02 UTC
**Company:** Idle Hands Labs. **Product:** none paid. Founder-in-a-box paid plan killed 2026-10-29; founder-kit stays free (bug fixes only); Shipcard and Roast frozen. Next product: TBD via the 4-part rule (PRODUCT.md decision 6). Candidate: agent-guard (state/CANDIDATES.md), waiting on part-1 evidence. **Revenue:** $0. **Waitlist:** 0. **Stars:** 0. **Issues:** 0. **Budget:** $0 of $100 spent.

## What is true now
- Everything in `app/` auto-deploys on push. The founder page links the free kit.
- Kit source is `kit/`; https://github.com/idlehandslabs/founder-kit syncs it every 6h. Kit tests pass (README says 43: 24 setup/docs + 19 guard).
- kit/agent/guard.py blocks ~25 secret formats (AWS, OpenAI, Stripe, GitHub, GitLab, Slack, Twilio, Mailgun, Shopify, PyPI, Linear, Notion, ...) plus .env/key files, and is proven end to end as a plain git pre-push hook (test_guard.HookEndToEndTest). The root agent/guard.py lacks most of these (protected; see Needs human).
- Show HN draft post-queue/2026-10-31-show-hn.md is fact-checked (cost ~$3.70/day).
- Cost: `python3 tools/daily_cost.py`. Per-cycle cost went from $0.14 (Oct 24) to ~$0.46 (Oct 28-31).
- 2026-10-31 21:30: this file cut from 20.1KB to 4.2KB by moving 56 dated bullets to state/STATE-HISTORY.md (not read every cycle). Per-cycle detail stays in state/LOG.md.

## Next up
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
- (2026-11-05) PAID OFFER, yes/no: "Wallet-leak history audit, 25 USDC on Solana." Buyer pays 25 USDC to PAY_TO_SOL and sends a PUBLIC GitHub repo URL; I run `guard.py --history` on it and deliver a private-free report: which files/commits hold a wallet key or seed phrase (never the key itself) + a fix list (rotate key, move funds, rewrite history). No fix = full refund proposed to you. What it needs from you, since agent/ and cf/ are protected: (a) orders.py + Worker accept kind="audit" with target = https://github.com/<owner>/<repo> (regex `^https://github\.com/[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+$`) and PRICE 25 for that kind; (b) the runner clones that repo (read-only, depth full) into a dir the agent can read. If yes, next cycle I write the offer page in app/ and the agent-side report step.
- (2026-11-03) Same as the Optional item below, now crypto: copy the 4 wallet lines (EVM private key, Solana private key, Solana keypair array, Seed phrase) from kit/agent/guard.py SECRETS into the protected agent/guard.py, so this repo can't push a wallet key either.
- (2026-11-03) Done: .demo-tmp/ removed from git and added to .gitignore (commit 2de429d).
- agent-guard 48h test: post post-queue/2026-11-02-1000.md (links founder-kit's "Use guard.py on its own" section). That post is the "first linked mention" that starts the 7-day verdict clock in state/GO-NO-GO-agent-guard.md. Reply with the post date.
- Optional: copy the 6 new SECRETS lines (OpenAI, Stripe, Google, Hugging Face, npm, Database URL, plus Telegram, SendGrid, Webhook URL, Twilio, Mailgun, GitLab and DigitalOcean added 2026-10-30) plus the `.env` and key-file (id_rsa etc., .p12/.pfx) file-name checks from kit/agent/guard.py into the protected agent/guard.py (web UI), so this repo gets the same coverage. The agent can't edit agent/.
- Show HN: if you submit, use post-queue/2026-10-31-show-hn.md (fact-checked 15:30 UTC; the cost line was fixed from ~$1.30/day to ~$3.70/day). The older show-hn-founder-kit.md is superseded.
- Optional: add founder-kit stars/forks to METRICS.md. The go/no-go could only see the shipcard repo.
- Nothing blocking. Posting is the operator's daily job; best fresh draft: post-queue/2026-10-28-1538.md (the older 2026-10-25-1215 pointer was stale and pointed at the waitlist, not the kit).
- Shipcard and Roast are FROZEN (PRODUCT.md decision 5). Do not spend cycles on them.


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
