# Backlog

## GOAL (2026-10-22, replaces the $1k-by-Oct-31 goal): validate FOUNDER-IN-A-BOX
50 waitlist signups by 2026-10-29. First paying customer ~2026-11-20. See PRODUCT.md decision 5. Report the waitlist count (from state/METRICS.md) in every daily article.

## NOW (2026-10-29): pick the next product
- [x] (2026-10-29 12:30) state/CANDIDATES.md: 5 candidates scored; none passes all 4; provisional winner agent-guard.
- [x] (2026-10-29 15:40) agent-guard coverage: OpenAI/Stripe/Google keys + .env files blocked in kit/agent/guard.py, tests.
- [x] (2026-10-29 18:30) Hugging Face / npm tokens + database URLs with inline passwords blocked; password-less URLs allowed; tests.
- [x] (2026-10-29 21:30) Clean-diff false-positive corpus for guard.py (12 lookalike lines, all pass).
- [x] (2026-10-30 00:30) Key files by name: SSH private keys + .p12/.pfx blocked, .pub allowed; test.
- [x] (2026-10-30 06:35) Telegram bot tokens + SendGrid keys blocked; 2 lookalikes added to the corpus.
- [x] (2026-10-30 09:40) Slack + Discord webhook URLs blocked; 2 lookalikes added to the corpus.
- [x] (2026-10-30 12:35) Twilio API keys + legacy Mailgun keys blocked; 2 lookalikes added to the corpus.
- [x] (2026-10-30 15:45) GitLab PATs + DigitalOcean tokens blocked; 1 lookalike added to the corpus.
- [x] (2026-10-30 21:24) Shopify access tokens blocked; subtest.
- [ ] Next coverage gap if agent-guard goes ahead: newer Mailgun key format, high-entropy strings in config files, phone numbers. Add each new lookalike to the corpus test first.
- [ ] Part-1 evidence for agent-guard (operator asked for 3 links). 3+ -> decision 7; fewer -> rescore.
- [ ] For the winner: pre-register a pass/fail line (GO-NO-GO format) and a 48-hour first test, before any polish.

## KILLED 2026-10-29: Founder-in-a-box paid plan (0/50 waitlist after 3 kit articles). Kit stays free, bug fixes only. History below.
## (was) VALIDATE (stage 1)
- [x] (done 2026-10-22, not deployed; also linked from both footers) app/founder/index.html: landing page "Launch your own AI founder". Hero: what it does in one line; 3 proof points linking to this public repo, the daily X articles and the live products it shipped; how it works (cycles, memory, guardrails, daily report); pricing intent ($19-49/mo, waitlist now); a waitlist form. Same visual style as app/roast/ (dark, #FF5A1F). No external scripts.
- [x] (endpoint live since 2026-10-23) Waitlist form posts to https://orders.idlehandslabs.workers.dev/waitlist {email, project_type}. The Worker endpoint is added by the human (cf/ is protected). Until it exists, the form shows "coming online today".
- [x] (3 of 3 drafted: 1200, 1500, 2026-10-24-1230) Post-queue: 3 drafts pitching the waitlist in the voice of the daily article (the AI that built a company now offers to run yours). Human posts.
- [x] Link the landing page from app/index.html and app/roast/ footer (done 2026-10-22).
- [x] (resolved 2026-10-25: auto-deploy is live; posting is daily) Deploy app/founder/ and post one draft (best: post-queue/2026-10-24-1230.md). Only blocker to the waitlist test; deadline 2026-10-29.

## Next: OPEN SOURCE founder-kit (stage 2, start after the landing page ships)
- [x] (done 2026-10-22) Design doc in state/FOUNDER-KIT.md: which files generalize (CLAUDE.md template with Mission block, agent.yml, run-cycle.sh, guard.py + PROTECTED list, metrics/orders pattern, state/ files, daily article prompt, cover rules), setup steps (fork, add CLAUDE_CODE_OAUTH_TOKEN + PRIVATE_TERMS secrets, edit Mission, enable Actions), and what stays private.
- [x] (2026-10-22) kit/ skeleton: templated CLAUDE.md, init.py, README, tests.
- [x] (metrics.py done 2026-10-22) [ ] remaining: copy other generic scripts into kit/agent/. BLOCKED on human: fix SyntaxError in protected agent/metrics.py line 52. Workflow + guard live in protected paths, so propose via Needs human.
- [x] (2026-10-23) Test: guard blocks fake leaking diffs (kit/agent/test_guard.py).
- [x] (2026-10-23) Runners + prompts copied into kit/agent/ (11 tests).
- [x] (2026-10-24) Kit workflow drafted in kit/workflow/agent.yml; extraction proposed via Needs human.
- [x] (2026-10-25) Kit extracted to github.com/idlehandslabs/founder-kit.
- [x] (2026-10-25) Founder page links to the kit repo ("Run it yourself, free").
- [x] (2026-10-25, in kit/README.md; sync to founder-kit repo pending) founder-kit README: real one-cycle example (LOG + ATTEMPTS lines) as proof before forking.
- [x] (2026-10-25, kit/DEMO.md; sync to founder-kit repo pending) Kit: text transcript demo of init.py + tests.
- [x] (2026-10-26, kit/LICENSE MIT + test; sync to founder-kit repo pending) Kit license so forks are legal.
- [~] (dropped 2026-10-29: kit is bug-fix-only) Kit: GIF version of DEMO.md.
- [ ] Post drafts that point to the free kit, not only the waitlist. (2026-10-25: drafts 1813 and 2115 do; 2026-10-28-0635 too; keep going.)
- [ ] Show HN draft: recheck numbers with kit/costs.py the day it is posted (refreshed 2026-10-30 18:35: 78 cycles, $24.22, $0.31 avg, ~$37.20/mo on an API key). Average is creeping up (0.22 -> 0.31 in 4 days; look at it in the 2026-11-01 review): the agent-guard cycles cost more.
- [x] (2026-10-28 18:30) Kit README: monthly cost estimate (costs.monthly + test tied to the README average).
- [x] (2026-10-26 00:13) Test: README/DEMO only use real init.py flags.
- [x] (closed: Sunday was 2026-10-25, REVIEW-2026-10-25.md exists; next review Sunday 2026-11-01) Sunday review.
- [x] (2026-10-26 09:35) Kit docs no longer point at files the founder-kit sync skips (workflow/, EXTRACT.md); test guards it.
- [x] (2026-10-26 14:15) Kit README: how to schedule, pause and stop the agent; test count is checked by a test.
- [x] (2026-10-26 15:55) Kit README: prerequisites + how to get the token; test checks every workflow secret is documented.
- [x] (2026-10-26 18:25, dated + test bans stale "all N tests") Kit README: "Status" line says "all 15 tests" (true on 2026-10-24, reads stale next to 22). Reword as dated or drop the number.
- [x] (2026-10-26 21:21) Kit README: "When a cycle fails" troubleshooting from real ATTEMPTS failures; test ties it to capture.py/guard.py output.
- [x] (2026-10-27 00:16) Kit README: what each state/ file is for; test ties it to init.STATE_FILES.
- [x] (2026-10-27 12:25) Kit: run-cycle.sh refuses to spend a cycle on an unfilled CLAUDE.md; test with a fake claude binary.
- [x] (2026-10-27 15:40) Pre-register go/no-go rules: state/GO-NO-GO-2026-10-29.md.
- [x] (2026-10-27 18:35) Kit: "I tried it" issue template so first users can report back; README asks for it; test.
- [x] (2026-10-27 21:30) Founder page cost card understated the range ($0.12-$0.26 vs real $0.11-$0.60); fixed + test. Kit README refreshed to 55 cycles / $13.67.
- [x] (2026-10-28 00:25) Kit README cost line said "55 cycles" and "2 of the 50"; fixed to 56 + test for self-consistency.
- [x] (2026-10-28 03:29) Kit README: "Is this for you?" (good fit / not a fit, honest $0) before setup; test.
- [x] (2026-10-28 12:27) Template sync: can't verify (network blocked); asked operator yes/no in STATE.md. README now links the form directly with a blank-issue fallback, so it works either way.
- [x] (2026-10-28 09:40) Pre-count evidence in GO-NO-GO: no recorded kit post; operator asked yes/no.
- [x] (2026-10-28 21:30) tools/gonogo.py: the go/no-go table as code, 5 tests.
- [x] (2026-10-29 00:25) First count in GO-NO-GO Result: 0 signals, row "post status unknown".
- [x] (2026-10-29 03:35) Kit: init.py prints next steps + warns on leftover placeholders; 2 tests.
- [x] (2026-10-29 09:40) Final count appended: 0 signals + kit post went out = KILL the paid idea. Post-mortem in GO-NO-GO; PRODUCT.md decision 6.
- [x] (2026-10-25 21:15; refreshed 2026-10-27 03:25: 49 cycles, $10.99, $0.22 avg) Kit README cost claim matches LOG.md.
- [x] (2026-10-27 06:30, kit/costs.py + 3 tests) Kit: small script that recounts cycles/cost from LOG.md so the README number never goes stale by hand.

## Frozen
- Roast (app/roast/): live as a demo, bug fixes only. No new rules.
- Shipcard: live, bug fixes only.

## Next
- [x] Card bug (seen on the first live card): "Run bookkeeping ..." harness commits show up as highlights. Treat chore:/bookkeeping commits as noise in core.js isNoise().
- [ ] Card nuance: a day of repo restructuring looks like "46 commits shipped". Consider counting files touched or de-duping move-only commits.
- [x] "Copy post text" button (pre-written tweet with the card)
- [ ] Dark theme + 2 more themes
- [x] Use the visitor's local timezone for day buckets
- [ ] Handle repos with 0 commits / huge weeks / rate limit gracefully (partly done)
- [x] Shareable URL (`?repo=owner/name`) so a card link can be passed around
- [ ] Landing copy + one-line pitch on the page

## Money
- [ ] Draft Pro tier: what's paid, price test ($5/mo vs $29 lifetime)
- [ ] (human) Pick a merchant-of-record checkout
- [ ] First paying customer within 30 days of launch

## Marketing (drafts for the human to post)
- [x] Day 1 article + my own card (published as an X Article)
- [ ] Weekly honest numbers post
- [x] (2026-10-27 09:27, post-queue/show-hn-founder-kit.md, for the kit not Shipcard) Show HN draft
