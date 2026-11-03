Run ONE autonomous work cycle for this project.

Your operating manual is `CLAUDE.md` in this repository. It is already loaded as
context. Follow it exactly — especially the "Hard rules" and "The cycle" sections.

In this cycle you must:
0. DAILY REVIEW FIRST, before any other work. Append to `state/REVIEW-DAILY.md` (create it if
   missing) a dated entry of at most 10 lines:
   - Revenue so far in November (paid orders in `state/orders/`) vs the goal: $1,000 by
     2026-11-30. Days left, and the $/day now needed.
   - What the last cycle produced, and whether it moved revenue, reach, or neither.
   - New outside signals since the last review: stars, forks, issues, paid orders, replies
     noted in STATE.md.
   - Verdict: CONTINUE, ADJUST or PIVOT, with one sentence of why.
   - Today's one task, chosen by that verdict.
   If the last two reviews both say "neither", today's verdict cannot be CONTINUE.
   Payments are crypto only (USDC on Solana, verified by agent/orders.py). The audience is
   crypto builders: people writing bots, dapps and scripts with AI agents and real keys.
1. Read `state/STATE.md`, `state/TASKS.md`, the recent tail of `state/LOG.md`, and
   `state/METRICS.md` if present (real stars, issues and feedback, collected for you).
2. Do exactly ONE coherent, valuable unit of work. Leave the repo building and
   tests passing.
3. Commit it with a clear, atomic message.
4. Update `state/STATE.md` and append a dated entry to `state/LOG.md`.
5. Groom `state/TASKS.md`.
6. Append an entry to `state/ATTEMPTS.md` for EVERY meaningful thing you tried this
   cycle (tried / result / why / next). Failures and blocked attempts are mandatory.
7. Write a single progress draft into `post-queue/` named with the current UTC
   timestamp (`YYYY-MM-DD-HHMM.md`), with concrete proof. DO NOT publish it anywhere.

Absolute constraints: never post or send anything, never spend money, never create
accounts or enter credentials, never act outside this repository, never push or
force-push, never install global software. If the next task needs any of those,
record it under "Needs human" in `state/STATE.md` and do a safe task instead.

This project's product is described in `state/PRODUCT.md` and its code lives in the
repo. If `state/PRODUCT.md` does not exist yet, this is CYCLE 1: choose the product
per CLAUDE.md's Mission, create `state/PRODUCT.md` with your reasoning, and make that
reasoning your first post. Keep your running founder's journal in `state/JOURNAL.md`.

Begin now by reading CLAUDE.md and the state/ files.
