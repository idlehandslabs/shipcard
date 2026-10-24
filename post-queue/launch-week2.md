# Launch drafts: Hacker News, Reddit, Indie Hackers

Posted from the Idle Hands Labs accounts only (never a personal account). Each post says plainly
that a human operator presses "submit" and the AI wrote the code and the logs.

---

## 1. Show HN  (best: Tue/Wed, 8-10am US Eastern)

**Title:** Show HN: I let an AI run a startup in public for a week, with guardrails it can't turn off

**URL:** https://github.com/idlehandslabs/shipcard/tree/main/kit

**Text:**

For the past week an AI agent (Claude Code, headless, on GitHub Actions) has been running a tiny
company in public: picking products, writing the code, shipping, and writing an honest daily log.
I'm the human operator. I approve money, hold the accounts, and press "post". It did the rest.

What happened, honestly:

- It shipped 3 products in 4 days. Strangers who used any of them: zero.
- It killed one product on day 2 because it couldn't say who would pay.
- Its memory is just files in the repo. On day 5 a stale note told it it was "blocked", so it spent a
  day polishing a product it had already frozen.
- It tried to read its own order inbox 4 times and got blocked every time, because by design it has
  no network access. Paid orders are now verified on-chain by plain code before it wakes up.

The part I think is actually useful is the safety setup, which is what the kit packages:

- A pre-push guard scans every diff for secrets, emails and a private list of terms.
- The agent can't modify its own rulebook, runner, guard or workflows. Any run that touches them is
  blocked, whoever the commit author is.
- The guard that runs is the version from before the agent's run, so it can't rewrite its own brakes.
- It never posts, deploys or spends. It drafts, and a human decides.

The kit is v0.1: setup script, 15 tests, tested end to end in a fresh fork. It runs this company
every day, but nobody outside has used it yet.

Repo, daily logs and every failure: https://github.com/idlehandslabs/shipcard

Happy to answer questions about what broke. There's a lot.

---

## 2. r/ClaudeAI  (flair: Project / Showcase)

**Title:** I ran Claude Code headless on GitHub Actions as an "AI founder" for a week. Here's the setup and what went wrong

**Body:**

Setup: `claude -p` in a GitHub Actions cron (8 cycles a day), `--permission-mode bypassPermissions`
plus a deny-list in `.claude/settings.json`, no web tools, a $0.60 budget cap per cycle, and memory
kept in plain markdown files (STATE, TASKS, LOG, ATTEMPTS).

Things I learned the hard way:

1. `dontAsk` mode refused every chained shell command, so cycles stalled. `bypassPermissions` plus a
   deny-list worked. The agent still tries `cd x && cat y` almost every cycle and gets blocked.
2. Give it no network, and do every fetch in a workflow step BEFORE it wakes. It sees only verified
   numbers, never raw text from the internet, so prompt injection has nothing to grab.
3. The guard must run from the pre-run commit (`git show $BASE:agent/guard.py`), or a confused agent
   can edit its own guard.
4. Stale memory files are the #1 failure. It believed a fixed blocker was still open for a whole day.
5. It's great at shipping and bad at knowing whether anyone wants what it shipped.

Kit (MIT, v0.1, 15 tests): https://github.com/idlehandslabs/shipcard/tree/main/kit
Daily logs: https://github.com/idlehandslabs/shipcard/tree/main/daily-log

I'm the human operator; the agent wrote the code and the logs.

---

## 3. r/SideProject

**Title:** My side project is an AI that runs side projects. Week 1: 3 products, 0 users, 1 honest lesson

**Body:**

I gave an AI agent a GitHub repo, a $100 budget and strict rules (it can't post, deploy, spend, or
change its own safety rails), and let it build a company in public for a week.

It built a weekly "what I shipped" card for GitHub, a Solana wallet roaster, and a redirect linter.
Nobody used any of them. Its conclusion on day 4: the only thing it had built that worked was the
system building it. So that's now the product. The open-source kit is free; a hosted version is on a
waitlist.

Every day is logged, failures first: https://github.com/idlehandslabs/shipcard/tree/main/daily-log
Kit: https://github.com/idlehandslabs/shipcard/tree/main/kit
Waitlist: https://idlehandslabs.github.io/shipcard/founder/

---

## 4. Indie Hackers  (post in "Building in Public")

Reuse the r/SideProject text, and add the numbers table from the latest daily log
(views, waitlist, revenue $0, budget $0 of $100).

---

## Rules for replying in these threads

- Answer every technical question with specifics and links to the actual file.
- Never argue. When someone finds a flaw, thank them and add it to state/TASKS.md.
- Never claim users, revenue or results that aren't in the logs.
