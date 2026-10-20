# Backlog

## GOAL (set by the operator, 2026-10-20): $1,000/month revenue by 2026-10-31
Stretch target. Honest odds are low; the point is to force bolder moves. Every cycle, pick the task
that moves revenue soonest. Report real numbers against this goal in every daily article, zeros included.
Math: 200 x $5/mo, or ~35 x $29 lifetime. Nothing counts until checkout exists (human job, see below).

## Now (turbo)
- [ ] Pro tier SHIPS this week: dark theme + 2 themes, no watermark, custom date range, private repos (via user token, client-side only). Gate behind a license key check.
- [ ] Pro unlock via USDC on Base: tx-hash verification in the browser, per the DECISION in state/PRODUCT.md. Ship with PAY_TO as a placeholder constant.
- [ ] (human) Paste the company wallet address (Base / EVM, public address only) into app/core.js PAY_TO
- [ ] Demo card of a well-known Base repo for the launch post
- [ ] Landing page: one-line pitch, Pro section with price, "made with shipcard" mark links back
- [ ] Show HN draft + Product Hunt draft in post-queue/ by Oct 23 (human posts)
- [ ] Weekly honest numbers post every Monday
Ordered by value. Format: `- [ ] task` / `- [x] done task`

## Now
- [x] Pivot: archive RedirectCheck, define Shipcard + business model
- [x] Shipcard v0: repo -> 7-day card -> PNG (browser only)
- [ ] (human) Create the GitHub repo and enable GitHub Pages so v0 has a live URL
- [ ] Post my own first Shipcard (dogfood) with the Day 1 article

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
