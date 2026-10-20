# Backlog

## GOAL (set by the operator, 2026-10-20): $1,000/month revenue by 2026-10-31
Stretch target. Honest odds are low; the point is to force bolder moves. Every cycle, pick the task
that moves revenue soonest. Report real numbers against this goal in every daily article, zeros included.
Math: 200 x $5/mo, or ~35 x $29 lifetime. Nothing counts until checkout exists (human job, see below).

## Now (turbo): ROASTED BY IDLE HANDS (PRODUCT.md decision 4, final; 2 and 3 are dead)
- [x] FREE INSTANT ROAST IS LIVE: https://idlehandslabs.github.io/shipcard/roast/ (app/roast/: roastcore.js pure rules + tests in app/tests/roast.test.mjs, roast.js UI, Solana public RPC, card PNG, Post on X, ?w= share links). Do NOT rebuild it; improve it (more rules, better jokes, wallet age, token prices) with tests.
- [ ] DEEP ROAST FULFILMENT (top priority, money path): each cycle GET https://orders.idlehandslabs.workers.dev/orders; for each new order verify the Solana tx via public RPC getTransaction: success, a USDC (mint EPjFWdd5AufqSSqeM2qN1xzybapC8G4wEGGkZwyTDt1v) transfer of >= 5 to the token account owned by PAY_TO_SOL (state/WALLETS.md). Then write a long roast (thread of 5-7 posts + card text) from the wallet's public data, publish it as app/roast/r/<order id>.html, log it in state/ROASTS.md. Unpaid/invalid orders: log and skip. Refunds: propose to the human, never send.
- [x] (code + fixture tests done; live API check pending) agent/roastdata.py: fetch public facts for a wallet (Blockscout Base), token (DexScreener + Blockscout holders) or repo (GitHub). Output a small JSON of numbers only. Unit tests with fixtures.
- [ ] agent/roast-prompt.md: voice guide + guardrails (facts about numbers, never fraud claims, never real names, playful). Produces card text + thread (5-7 posts) + alt text.
- [x] Order intake: Cloudflare Worker LIVE at https://orders.idlehandslabs.workers.dev (POST /order, GET /orders). Code in cf/worker.js; Cloudflare auto-deploys cf/ on every push to main, so edit cf/worker.js and commit to change it. Keep tests for it in cf/.
- [ ] state/ROASTS.md public ledger: date, kind, target (shortened), tx, page URL.
- [ ] Seed: 5 free roasts of loud, public, consenting-by-reply accounts (ask in a post: reply with your wallet to get roasted). Drafts to post-queue/.
- [x] PAY_TO_SOL is in state/WALLETS.md. Build Solana-first (USDC SPL transfer to that address).
- [ ] (human) PAY_TO for Base/EVM still pending; until then the order page offers Solana only.
- [ ] Launch thread + Show HN + Product Hunt drafts in post-queue/.
- [ ] Shipcard: frozen. Bug fixes only.

## Next
- [ ] Card bug (seen on the first live card): "Run bookkeeping ..." harness commits show up as highlights. Treat chore:/bookkeeping commits as noise in core.js isNoise().
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
