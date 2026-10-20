# Current State

**Last updated:** 2026-10-20 (Day 1)
**Company:** Idle Hands Labs. **Product:** Shipcard (working name). **Revenue:** $0. **Users:** 0. **Budget:** $0 of $100 spent.

## What is true now
- Pivoted from RedirectCheck (archived in `archive/`) to Shipcard.
- Shipcard v0 exists in `app/`: browser-only, repo -> 7-day card -> PNG. Unit tests pass.
- Not live anywhere yet. No users, no revenue.

- Cycle 2026-10-20 (later): cards now bucket days in the visitor's local timezone (9/9 tests).
- METRICS says the live URL (idlehandslabs.github.io/shipcard) was `unreachable` at last check; Pages may not be enabled yet.

- Roast data layer exists (`agent/roastdata.py`, 5 tests, not yet run on live APIs). Roast app, prompt and Worker still to build.

- Card now ignores bookkeeping commits. Could not reach the orders Worker this cycle (sandbox denied curl); order status unknown.

- Roast prompt (`agent/roast-prompt.md`) and ledger (`state/ROASTS.md`) written. Orders still unreadable (curl denied again). Paid roasts fulfilled: 0.

## Next up
- Get a live URL (GitHub Pages) so people can try it from a post.
- "Copy post text" button and shareable `?repo=` links.

## Needs human
0. **Deep Roast orders:** the sandbox blocks my fetch of the orders endpoint. Allow `curl` to orders.idlehandslabs.workers.dev, or paste the orders, so I can verify and fulfil.
1. **Create the GitHub repo and enable GitHub Pages** (Settings → Pages → deploy from
   branch, folder `/app`). That gives Shipcard a free live URL. Yes/no?
2. **Approve posting the Day 1 article** (`daily-log/2026-10-20.md`) on X.

- Roast rules: added One-Day Wonder and Dust Collector (17/17 tests). Orders still unread (curl denied).
