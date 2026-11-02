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
- agent-guard 48h test: post post-queue/2026-11-02-1000.md (links founder-kit's "Use guard.py on its own" section). That post is the "first linked mention" that starts the 7-day verdict clock in state/GO-NO-GO-agent-guard.md. Reply with the post date.
- Optional: copy the 6 new SECRETS lines (OpenAI, Stripe, Google, Hugging Face, npm, Database URL, plus Telegram, SendGrid, Webhook URL, Twilio, Mailgun, GitLab and DigitalOcean added 2026-10-30) plus the `.env` and key-file (id_rsa etc., .p12/.pfx) file-name checks from kit/agent/guard.py into the protected agent/guard.py (web UI), so this repo gets the same coverage. The agent can't edit agent/.
- Show HN: if you submit, use post-queue/2026-10-31-show-hn.md (fact-checked 15:30 UTC; the cost line was fixed from ~$1.30/day to ~$3.70/day). The older show-hn-founder-kit.md is superseded.
- Optional: add founder-kit stars/forks to METRICS.md. The go/no-go could only see the shipcard repo.
- Nothing blocking. Posting is the operator's daily job; best fresh draft: post-queue/2026-10-28-1538.md (the older 2026-10-25-1215 pointer was stale and pointed at the waitlist, not the kit).
- Shipcard and Roast are FROZEN (PRODUCT.md decision 5). Do not spend cycles on them.


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
