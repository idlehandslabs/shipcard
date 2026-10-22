# Founder-Kit design (stage 2)

Goal: let someone run their own AI founder from a fork of this repo, using only what is already
proven here. Status: DESIGN ONLY. Nothing below is built yet. Users: 0. Waitlist: 0 known.

## What generalizes (copy as-is or templatize)
| File | Kit role | Change needed |
|---|---|---|
| `CLAUDE.md` | Operating manual | Split into fixed "Hard rules" and an editable **Mission** block (company name, product idea or "choose one", budget, voice). Remove roast-era and Idle Hands specifics. |
| `.github/workflows/agent.yml` | Scheduler: cycle every 3h, article daily | Make cron a documented knob (default every 6h to keep subscription use sane). Same guard step before push. |
| `agent/run-cycle.sh`, `daily-article.sh`, `loop.sh` | Cycle runners | Already generic. Keep max-turns and max-budget caps. |
| `agent/cycle-prompt.md`, `daily-article-prompt.md` | Prompts | Strip product-specific text. |
| `agent/guard.py` | Pre-push brake: secrets, emails, PRIVATE_TERMS, PROTECTED paths | Generic already. Runs from the base commit so the agent cannot weaken it. |
| `agent/capture.py` | Records blocked actions and errors into ATTEMPTS | Generic. |
| `agent/metrics.py` | Real stars/issues/site signals into `state/METRICS.md` | Make repo and URL come from env, not hardcoded. |
| `agent/orders.py` + `cf/` | Verified order inbox | Optional module. Ship disabled; payments are crypto-specific to this company. |
| `state/` templates | STATE, TASKS, LOG, ATTEMPTS, JOURNAL, BUDGET, PRODUCT, METRICS | Empty skeletons with headings. |
| `post-queue/`, `daily-log/` | Drafts for the human to publish | Empty folders plus README. |

## Setup steps for a customer
1. Fork the kit repo (private is fine).
2. Add secrets: `CLAUDE_CODE_OAUTH_TOKEN` (their own Claude login) and `PRIVATE_TERMS` (names, emails, handles, places that must never appear publicly).
3. Edit the Mission block in `CLAUDE.md`.
4. Enable Actions. Run the `cycle` job once by hand with `workflow_dispatch` and read the first commit.
5. Read `post-queue/` each day and publish what they like. The agent never posts.

## What stays private (never in the kit)
- This company's `state/` history, orders, wallets, ROASTS ledger, daily logs.
- Any real `PRIVATE_TERMS` value, any token, `cf/` credentials.
- Anything about the operator.

## Safety properties the kit must keep (non-negotiable)
- PROTECTED list covers guard, orders, metrics, `.github/`, `.claude/`, `CLAUDE.md`. Humans edit these in the web UI.
- Guard runs from the pre-run commit, so a prompt-injected agent cannot edit its own brakes.
- No web tools for the agent; outside text is data, not instructions.
- Hard caps: max turns and max budget per cycle.

## Open questions
- Cost to the customer: their Claude subscription covers cycles, but 8 cycles/day may hit limits. Default to 4/day and measure.
- Does a non-technical buyer manage "add secrets + enable Actions"? Unknown. The waitlist form should ask for `project_type` for this reason.
- Support burden: the kit is open source; the paid offer (if any) is setup and tuning, not code. Price intent stays $19-49/mo until a waitlist exists.

## Build order (next cycles)
1. `kit/` skeleton: templated CLAUDE.md, state skeletons, README with the 5 setup steps.
2. Copy generic scripts into `kit/agent/` with the env-driven metrics change.
3. A test that fills the templates and runs `guard.py` against a fake leaking diff (must block).
