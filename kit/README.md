# Founder-kit v0.1

Run your own AI founder from a fork. It builds a product in a repo, logs every decision,
and drafts public posts for you to publish. It never posts, deploys or spends on its own.

Status: v0.1. Tested end to end in a fresh fork on 2026-10-24: the setup script, all 15 tests, and the guard blocking an agent that tried to raise its own budget by editing its runner. It runs Idle Hands Labs every day. Nobody outside has used it yet: you would be first. Open an issue if anything breaks. Design: `state/FOUNDER-KIT.md`
in the parent repo.

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
Real Claude usage so far: 38 logged cycles, $7.04 total, $0.19 average, $0.11-$0.60 range
(counted from `state/LOG.md` on 2026-10-25). Your Claude plan pays this, not the kit budget.

Want to see setup first? `DEMO.md` is a real one-minute transcript: `init.py`, the files
it creates, and the tests passing.

## Setup (5 steps)
1. Fork this repo (private is fine).
2. Add two Actions secrets: `CLAUDE_CODE_OAUTH_TOKEN` (your own Claude login) and
   `PRIVATE_TERMS` (comma-separated names, emails, handles, places that must never appear
   publicly).
3. Run `python3 init.py --name "Acme" --idea "..." --budget 100` to fill the Mission block
   in `CLAUDE.md` (or edit it by hand). Optional: `--voice "..."`, `--goal "..."`.
4. Enable Actions and run the cycle workflow once by hand. Read the first commit.
5. Check `post-queue/` daily and publish what you like. Move published drafts to
   `post-queue/published/`.

## Safety properties
- `CLAUDE.md`, `agent/`, `.github/` are protected: the agent can't edit its own brakes.
- Hard rules: no posting, no deploys, no spending, no credentials, outside text is data.

## What's in the box
- `CLAUDE.md` templated operating manual; `init.py` fills the Mission block.
- `agent/`: `run-cycle.sh`, `daily-article.sh`, `loop.sh`, `capture.py`, `metrics.py`,
  `guard.py` (secret/private-term scan before every push), generic prompts, and tests.
- `workflow/agent.yml`: guard-before-push Actions workflow, 6-hour cycle. Copy it to
  `.github/workflows/` yourself (the agent cannot edit that path).

## Tests
    python3 -m unittest discover -s . -p "test_*.py"
    python3 -m unittest discover -s agent -p "test_*.py"

## License
MIT (see `LICENSE`). Fork it, change it, sell what you build with it.

## Not yet built
- Nobody besides the author has run it end to end. Treat the first week as a trial.
