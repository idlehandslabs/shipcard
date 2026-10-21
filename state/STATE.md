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
- Nothing blocking. (Resolved 2026-10-21 by the operator: GitHub Pages is LIVE at https://idlehandslabs.github.io/shipcard/ and the free roast at /shipcard/roast/; the Day 1 article was published on X; orders now reach you as verified files in state/orders/ via agent/orders.py, so do not try to fetch them.)
- Posting on X is always the human's job: keep drafts in post-queue/.
