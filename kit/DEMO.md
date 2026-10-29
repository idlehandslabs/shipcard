# Demo: from fresh fork to ready in under a minute

A real run, not a mock-up. Captured 2026-10-25 ~18:13 UTC on a clean copy of this kit
(Linux, Python 3, no installs). Commands and output are copied as they ran (paths shortened).

## 1. Fill the Mission block

    $ python3 init.py --name "Acme" --idea "a tiny invoice tool for freelancers" --budget 50
    Done: CLAUDE.md filled, state/ ready.
    Next:
      1. git add -A && git commit -m "init" && git push   (the workflow runs on your fork)
      2. Add Actions secrets: CLAUDE_CODE_OAUTH_TOKEN (from `claude setup-token`) and PRIVATE_TERMS
      3. Enable Actions and run the cycle workflow once by hand
      4. Read the first commit, then state/STATE.md under "Needs human"
    $ echo $?
    0

(The next-steps printout was added 2026-10-29; the rest of this transcript is from 2026-10-25,
when init.py printed nothing.) What it changed:

    $ grep -c "{{" CLAUDE.md
    0
    $ grep -n "Acme\|invoice\|\$50" CLAUDE.md
    1:# Acme — Founder Operating Manual
    3:You are **Acme**: an AI founder building a startup in public. You make the
    12:- Company name: Acme
    13:- Product idea: a tiny invoice tool for freelancers   <!-- or write "choose one and justify it in state/PRODUCT.md" -->
    14:- Budget (total, for APIs, tools, services): $50
    36:numbers only, including zeros. Report "Budget: $X of $50 spent".
    57:  names, location, job or personal details. Public writing is about Acme only.

## 2. The memory it starts with

    $ find state post-queue daily-log app | sort
    app/.gitkeep
    daily-log/.gitkeep
    post-queue/published/.gitkeep
    state/ATTEMPTS.md
    state/BUDGET.md
    state/JOURNAL.md
    state/LOG.md
    state/METRICS.md
    state/PRODUCT.md
    state/STATE.md
    state/TASKS.md

Eight empty-ish files. That is all the agent remembers between runs, on purpose: you can
read every byte of its memory in `git log`.

## 3. Run the tests

    $ python3 -m unittest discover -s . -p "test_*.py"
    Ran 4 tests in 0.009s
    OK
    $ python3 -m unittest discover -s agent -p "test_*.py"
    Ran 11 tests in 0.255s
    OK

(Since this capture there is a 5th init test: it fails if this file's list of state
files drifts from what `init.py` really creates.) The 11 include the guard: fake diffs with a secret, an email, a private term, and an
edit to a protected file (the agent's own brakes) all get blocked before push.

## 4. What happens next
Add the two secrets (see README), enable Actions, and run the workflow in
`.github/workflows/agent.yml` once. Cycle 1 picks or justifies the product in `state/PRODUCT.md`,
commits, and leaves one draft post in `post-queue/`. For what a later cycle looks like,
see "What one cycle looks like" in the README.

Honest note: the only company this has run end to end is Idle Hands Labs. Waitlist 0,
stars 0, revenue $0 as of this demo. If you try it, you are user #1.
