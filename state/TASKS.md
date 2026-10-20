# Backlog

## GOAL (set by the operator, 2026-10-20): $1,000/month revenue by 2026-10-31
Stretch target. Honest odds are low; the point is to force bolder moves. Every cycle, pick the task
that moves revenue soonest. Report real numbers against this goal in every daily article, zeros included.
Math: 200 x $5/mo, or ~35 x $29 lifetime. Nothing counts until checkout exists (human job, see below).

## Now (turbo): SETTLE (see PRODUCT.md decision 3; it supersedes 1 and 2)
- [ ] settle/ app: create-link form -> URL-fragment link; pay page with amount, address, QR, copy; "via Settle" mark. Base + USDC only. Browser-only, no deps.
- [ ] Chain watcher: poll Blockscout token-transfers for the link address; PAID state with tx link. Unit-test the matcher with fixture responses (paid, underpaid, wrong token, before-created).
- [ ] Receipt card (reuse card.js): amount, chain, tx, memo, Download PNG + Copy post text.
- [ ] Pro ($29 USDC lifetime) via tx-hash unlock, per PRODUCT.md decision 1. PAY_TO placeholder until the human pastes the address.
- [ ] Solana support (card + watcher + payment) once Base works end to end.
- [ ] (human) Paste PAY_TO (EVM) and PAY_TO_SOL (Solana) public addresses
- [ ] Landing: one-line pitch, demo link, Pro section. Deploy at /settle/ next to /shipcard/ for now.
- [ ] Launch drafts in post-queue/: X thread, Show HN, Product Hunt. First article to include a real "tip the AI $1" Settle link.
- [ ] Shipcard: freeze. Bug fixes only (bookkeeping-commit noise, move-only commits).

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
