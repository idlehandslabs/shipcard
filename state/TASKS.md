# Backlog

## GOAL (set by the operator, 2026-10-20): $1,000/month revenue by 2026-10-31
Stretch target. Honest odds are low; the point is to force bolder moves. Every cycle, pick the task
that moves revenue soonest. Report real numbers against this goal in every daily article, zeros included.
Math: 200 x $5/mo, or ~35 x $29 lifetime. Nothing counts until checkout exists (human job, see below).

## Now (turbo): ROASTED BY IDLE HANDS (PRODUCT.md decision 4, final; 2 and 3 are dead)
- [ ] roast/ app: order page (wallet | token | repo input, 5 USDC, PAY_TO + QR, tx-hash field) and /roasts/<id> page with the card, the thread text and a Copy post text button. Reuse Shipcard styling and card.js.
- [x] (code + fixture tests done; live API check pending) agent/roastdata.py: fetch public facts for a wallet (Blockscout Base), token (DexScreener + Blockscout holders) or repo (GitHub). Output a small JSON of numbers only. Unit tests with fixtures.
- [ ] agent/roast-prompt.md: voice guide + guardrails (facts about numbers, never fraud claims, never real names, playful). Produces card text + thread (5-7 posts) + alt text.
- [ ] Order intake: a free Cloudflare Worker with KV that stores {kind, target, txHash, createdAt}. The cycle reads the queue, verifies the tx (decision 1), writes the roast, marks done. Keep the Worker tiny and the code in cf/worker.js.
- [ ] state/ROASTS.md public ledger: date, kind, target (shortened), tx, page URL.
- [ ] Seed: 5 free roasts of loud, public, consenting-by-reply accounts (ask in a post: reply with your wallet to get roasted). Drafts to post-queue/.
- [ ] (human) Paste PAY_TO (EVM) and PAY_TO_SOL. Deploy the Worker (one command, I will write the exact steps).
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
