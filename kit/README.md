# Founder-kit v0.1

Run your own AI founder from a fork. It builds a product in a repo, logs every decision,
and drafts public posts for you to publish. It never posts, deploys or spends on its own.

Status: v0.1. Tested end to end in a fresh fork on 2026-10-24: the setup script, the full test suite (15 tests that day; today's count is under Tests), and the guard blocking an agent that tried to raise its own budget by editing its runner. It runs Idle Hands Labs every day. Nobody outside has used it yet: you would be first. Open an issue if anything breaks. Design notes:
[state/FOUNDER-KIT.md](https://github.com/idlehandslabs/shipcard/blob/main/state/FOUNDER-KIT.md)
in the Idle Hands Labs repo.

## What one cycle looks like (real, not a mock-up)
One run from Idle Hands Labs, 2026-10-25 12:14-12:15 UTC. The agent read `state/`, picked
one task, shipped it with tests, and left this in `state/LOG.md`:

    ## 2026-10-25 12:15 UTC - Cycle (founder page links the free kit)
    - app/founder/index.html: new "Run it yourself, free" section + footer link to
      github.com/idlehandslabs/founder-kit. Added app/tests/founder.test.mjs (app tests 29/29).
      Waitlist 0/50, stars 0, revenue $0, budget $0/$100.
    2026-10-25T12:15:24Z  cycle rc=0 cost=$0.42  log=logs/cycle-20261025T121422Z.json

And this in `state/ATTEMPTS.md`, including the parts that went wrong:

    - Tried: `node --test app/tests/` (directory arg). Result: 1 failing pseudo-test
      (node treated the dir as a file). Next: use `node --test app/tests/*.mjs`.

Plus one draft post in `post-queue/` for a human to publish (or not). The zeros are real.
Real Claude usage so far: 62 logged cycles, $16.72 total, $0.27 average, $0.11-$0.60 range
(2 of the 62 stopped early and cost $0; `python3 costs.py state/LOG.md` on 2026-10-28).
Your Claude plan pays this, not the kit budget. Run the same command in your fork for yours.

Want to see setup first? `DEMO.md` is a real one-minute transcript: `init.py`, the files
it creates, and the tests passing.

## Is this for you?
Good fit: you build alone, you already use GitHub, and you want an agent that picks the
next task, ships it with tests and writes down why, while you keep the publish button.
Not a fit: you want it to post, deploy or spend for you (it never does), you need it near
real user data or production systems, or you expect it to make money on its own. The
company it runs has made $0 so far; what it reliably produces is work and an honest log.

## Before you start
- A GitHub account. Actions minutes: public forks are free; a private fork uses your free
  monthly allowance.
- A Claude plan that includes Claude Code. Make the step-2 token on your own machine with
  `claude setup-token` (Claude Code CLI); it prints a long-lived OAuth token. Paste it into
  the secret and nowhere else. No plan? The workflow also reads an `ANTHROPIC_API_KEY`
  secret instead; that bills per use on your API account. At our $0.27 average, the
  default 4 cycles a day is about $32.40 a month (daily articles extra);
  `python3 costs.py state/LOG.md` prints your own number once you have a log.
- Python 3 for `init.py` and the tests. Nothing else to install.

## Setup (5 steps)
1. Fork this repo (private is fine).
2. Add two Actions secrets: `CLAUDE_CODE_OAUTH_TOKEN` (your own Claude login) and
   `PRIVATE_TERMS` (comma-separated names, emails, handles, places that must never appear
   publicly).
3. Run `python3 init.py --name "Acme" --idea "..." --budget 100` to fill the Mission block
   in `CLAUDE.md` (or edit it by hand). Optional: `--voice "..."`, `--goal "..."`.
   Commit and push the result: the workflow runs on what is in your fork, not your laptop.
4. Enable Actions and run the cycle workflow once by hand. Read the first commit.
5. Check `post-queue/` daily and publish what you like. Move published drafts to
   `post-queue/published/`.

## Where to look each day
`init.py` creates these in `state/`. The agent reads them at the start of every cycle and
updates them at the end; they are its only memory.
- `STATE.md`: where things stand. Read **Needs human** first: that is what it wants you
  to approve.
- `LOG.md`: one dated line per cycle (what shipped, test count).
- `ATTEMPTS.md`: tried / result / why / next, failures included.
- `TASKS.md`: the backlog it grooms.
- `JOURNAL.md`: its reasoning when it makes a decision.
- `PRODUCT.md`: what it is building and why (empty until cycle 1).
- `BUDGET.md`: your money cap and a ledger. It proposes spends; you approve them.
- `METRICS.md`: real numbers `agent/metrics.py` collects before each cycle.

## Safety properties
- `CLAUDE.md`, `agent/`, `.github/` are protected: the agent can't edit its own brakes.
- Hard rules: no posting, no deploys, no spending, no credentials, outside text is data.

## What's in the box
- `CLAUDE.md` templated operating manual; `init.py` fills the Mission block.
- `costs.py`: recounts cycles and Claude cost from `state/LOG.md`.
- `agent/`: `run-cycle.sh`, `daily-article.sh`, `loop.sh`, `capture.py`, `metrics.py`,
  `guard.py` (secret/private-term scan before every push), generic prompts, and tests.
- `.github/workflows/agent.yml`: guard-before-push Actions workflow, 6-hour cycle. Already
  in place in your fork; the agent cannot edit that path.

## Schedule, pause, stop
- Build cycle every 6 hours (00, 06, 12, 18 UTC); daily article at 06:15 UTC. Change the
  `cron:` lines in `.github/workflows/agent.yml` (you edit it; the agent can't).
- Run one by hand: Actions tab, the agent workflow, "Run workflow", pick `cycle` or `article`.
- Pause: Actions tab, the agent workflow, "..." menu, "Disable workflow". Nothing runs and
  nothing is spent until you enable it again. Stop for good: delete the fork.

## When a cycle fails
Failures land in `state/ATTEMPTS.md`, written by `agent/capture.py`, so the next cycle
reads them too. The first three are ones we actually hit; the fourth is a pre-flight check:
- `Run failed (exit 1): Credit balance is too low`: the Claude account behind your token
  ran out. Top it up or switch token; nothing was committed that cycle.
- `Blocked by a guardrail: Bash → ...`: the permission layer refused a command (we saw
  `curl`, and compound `cd ...; cat ...` reads). Working as designed. The agent retries
  with the file tools next cycle; if one blocked command keeps repeating, read it.
- `PUSH BLOCKED by guard.py:` in the Actions log: the diff contained a secret, an email or
  one of your `PRIVATE_TERMS`. Nothing was pushed. The next cycle has to remove it.
- `NOT RUN: CLAUDE.md still has {{placeholders}}`: the Mission block was never filled in
  your fork (usually `init.py` ran locally but wasn't pushed). Claude was not called, so
  the cycle cost $0. Push the filled `CLAUDE.md`.

## Tests (33: 21 setup/docs + 12 agent)
    python3 -m unittest discover -s . -p "test_*.py"
    python3 -m unittest discover -s agent -p "test_*.py"

## License
MIT (see `LICENSE`). Fork it, change it, sell what you build with it.

## Not yet built
- Nobody besides the author has run it end to end. Treat the first week as a trial.
  If you try it, even just `init.py`, open an "I tried it" issue: [new issue](https://github.com/idlehandslabs/founder-kit/issues/new?template=tried-it.md). If the form doesn't load, a blank issue is fine: what you ran, what broke, and the output of `python3 costs.py state/LOG.md`.
  Two minutes, every field optional. It's the only way we learn whether this works for
  anyone else, and the count goes in our public numbers.
