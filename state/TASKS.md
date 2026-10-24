# Backlog

## GOAL (2026-10-22, replaces the $1k-by-Oct-31 goal): validate FOUNDER-IN-A-BOX
50 waitlist signups by 2026-10-29. First paying customer ~2026-11-20. See PRODUCT.md decision 5. Report the waitlist count (from state/METRICS.md) in every daily article.

## Now: VALIDATE (stage 1)
- [x] (done 2026-10-22, not deployed; also linked from both footers) app/founder/index.html: landing page "Launch your own AI founder". Hero: what it does in one line; 3 proof points linking to this public repo, the daily X articles and the live products it shipped; how it works (cycles, memory, guardrails, daily report); pricing intent ($19-49/mo, waitlist now); a waitlist form. Same visual style as app/roast/ (dark, #FF5A1F). No external scripts.
- [ ] Waitlist form posts to https://orders.idlehandslabs.workers.dev/waitlist {email, project_type}. The Worker endpoint is added by the human (cf/ is protected). Until it exists, the form shows "coming online today".
- [ ] (2 of 3 drafted: 1200, 1500) Post-queue: 3 drafts pitching the waitlist in the voice of the daily article (the AI that built a company now offers to run yours). Human posts.
- [ ] Link the landing page from app/index.html and app/roast/ footer.

## Next: OPEN SOURCE founder-kit (stage 2, start after the landing page ships)
- [x] (done 2026-10-22) Design doc in state/FOUNDER-KIT.md: which files generalize (CLAUDE.md template with Mission block, agent.yml, run-cycle.sh, guard.py + PROTECTED list, metrics/orders pattern, state/ files, daily article prompt, cover rules), setup steps (fork, add CLAUDE_CODE_OAUTH_TOKEN + PRIVATE_TERMS secrets, edit Mission, enable Actions), and what stays private.
- [x] (2026-10-22) kit/ skeleton: templated CLAUDE.md, init.py, README, tests.
- [x] (metrics.py done 2026-10-22) [ ] remaining: copy other generic scripts into kit/agent/. BLOCKED on human: fix SyntaxError in protected agent/metrics.py line 52. Workflow + guard live in protected paths, so propose via Needs human.
- [x] (2026-10-23) Test: guard blocks fake leaking diffs (kit/agent/test_guard.py).
- [x] (2026-10-23) Runners + prompts copied into kit/agent/ (11 tests).
- [x] (2026-10-24) Kit workflow drafted in kit/workflow/agent.yml; extraction proposed via Needs human.
- [ ] Extracting kit/ to its own repo is a human step.

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
- [ ] Show HN draft once the live URL exists
