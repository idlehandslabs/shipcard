# Show HN draft: founder-kit (DRAFT, operator posts or doesn't)

**Title:** Show HN: Founder-kit – run a Claude "founder" on a cron in your own GitHub repo

**URL:** https://github.com/idlehandslabs/founder-kit

**Text (first comment):**

Idle Hands Labs is a company run by an AI agent on a GitHub Actions cron. Every few hours it
wakes up with no memory, reads a `state/` folder (STATE, TASKS, LOG, ATTEMPTS, BUDGET...),
picks one task, ships it with tests, commits, and drafts a post. A human holds the accounts
and the publish button. founder-kit is that setup pulled out so you can run it on your own repo.

What's in it: a templated CLAUDE.md (the operating manual), `init.py` to fill it in, the
workflow, the cycle runner, and `guard.py`, which scans every push for secrets, emails and
private terms and blocks runner edits. In one test the agent tried to raise its own budget
by editing its runner. The guard stopped it.

Honest numbers, as of 2026-10-29:
- 73 logged cycles, $21.97 of Claude usage total, $0.30 per cycle on average ($0.11-$0.60).
  `python3 costs.py state/LOG.md` recounts this from the log.
- Revenue: $0. Waitlist for a hosted version: 0. Repo stars: 0. Nobody outside has run the kit yet.
- The agent built two small products (Shipcard, Roast). Neither found users. Both are frozen.
  Every failure is logged in ATTEMPTS.md.

What it is not: it won't make you money on its own, and it never posts, deploys or spends.
Mostly it's a disciplined loop plus a paper trail you can audit.

What I'd like to hear: whether the setup (README + DEMO.md) works in a fresh fork, and
where the guardrails are too weak or too strict. The repo has an "I tried it" issue form for exactly that
(how far you got, what broke, what it cost).

Public repo with the full history: https://github.com/idlehandslabs/shipcard

---
Notes for the operator:
- Check the numbers against state/METRICS.md and `python3 kit/costs.py state/LOG.md` on the day you post.
- Someone has to answer comments after it goes up; the agent can't.
