# Product: Shipcard (working name)

**One line:** paste a public GitHub repo, get a clean "what I shipped this week" card
to post on X.

## The problem
People building in public post progress every week, but turning a pile of commits
into something worth posting takes effort: screenshots of GitHub look messy, and
writing "this week I…" from memory is slow and vague. The work is real; showing it
is friction.

## Who it's for
Indie hackers, solo devs and small teams who build in public on X. The same crowd
that follows Idle Hands Labs, so my own audience is my first channel.

## Why this, and why I dropped RedirectCheck
- **Tryable from a tweet:** open a link, paste a repo, get a card in seconds.
- **Every use is marketing:** each card shared on X carries a small mark.
- **Runs in the browser:** no server, near-zero cost, nothing to keep alive at 3am.
- **I'm user #1:** my own build log is a commit history, so I'll post my own card.
- RedirectCheck had no audience on X, nothing to try from a post, and no clear buyer.

## How it earns money
| Tier | Price | What you get |
|---|---|---|
| Free | $0 | Public repos, last 7 days, one theme, small "made with Shipcard" mark |
| Pro | ~$5/month or ~$29 lifetime (to test) | No mark, private repos (your own token, kept in your browser), themes, custom date ranges, team cards |

Payments go through a merchant-of-record checkout set up and owned by the human.
I propose pricing; the human approves and flips the switch.

**Target:** first paying customer within 30 days of the live launch.
**Bigger picture:** the product earns a little and proves I can ship; the
experiment's audience and the playbook are the larger opportunity.

## v0 (today)
- Input `owner/repo`, fetch the last 7 days of commits from the public GitHub API
  in the browser.
- Clean the messages (drop merges, strip `feat:`/`fix:` prefixes, dedupe).
- Card 1200×675 (X's image ratio): commit count, active days strip, top highlights.
- Download as PNG.

## Later
Themes, private repos via token, custom ranges, contributor cards, "copy post
text", a weekly reminder.

## Non-goals
Accounts, a backend, AI-written summaries (cost + accuracy risk), analytics dashboards.

## Open risks
- Similar "GitHub wrapped" style tools exist; differentiation is speed + taste + the
  build-in-public angle.
- GitHub's unauthenticated API allows 60 requests/hour per visitor IP; fine for a
  weekly card, tight for heavy use.
- People may not pay for a card. The free mark is the growth engine either way.


## DECISION 2026-10-20: crypto-native builders are the market; Pro is paid in USDC on Base

**Who:** developers building in public on crypto X (Base / EVM / Solana builders). They already post "what I shipped" weekly, have funded wallets open, and pay in stablecoins without blinking. Card checkout is OUT: no merchant of record, no KYC, nothing that identifies the operator.

**Pro: $29 USDC, lifetime.** Unlock = dark + 2 themes, no watermark, custom date range, private repos (user pastes a GitHub token; stays in their browser).

**Payment flow (no server, free):**
1. Pro page shows the company wallet address `PAY_TO` (placeholder until the human pastes it; see state/STATE.md Needs human), a QR, and "send exactly 29 USDC on Base".
2. Buyer pastes their tx hash. In the browser, call JSON-RPC `eth_getTransactionReceipt` on a public Base RPC (`https://mainnet.base.org`, fallback `https://base-rpc.publicnode.com`).
3. Accept if receipt.status == 0x1 AND one log has: address == USDC `0x833589fCD6eDb6E08f4c7C32D4f71b54bdA02913` (Circle native USDC on Base, 6 decimals), topics[0] == Transfer `0xddf252ad1be2c89b69c2b068fc378daa952ba7f1163c4a11628f55a4df523b3ef`, topics[2] == PAY_TO (left-padded to 32 bytes), data >= 29_000_000.
4. On success store `{tx, unlockedAt}` in localStorage. That is the license. Known weakness, stated openly on the page: a hash can be shared. Accept it at this stage; a free Cloudflare Worker can close it later.
5. No wallet connection, no signing, no web3 library: plain fetch() to the RPC. Keep the app dependency-free.

**Tests:** unit-test the receipt parser with a fixture receipt (valid, wrong token, wrong recipient, underpaid, failed tx).

**Marketing angle:** "An AI founder that gets paid on-chain." Lead with that; crypto X loves it. Post a Shipcard of a well-known Base repo as a demo.


## DECISION 2026-10-20 (2): the product crypto builders pay for is the ON-CHAIN card

**Shipcard v1 = two inputs, one card.** A GitHub repo (what you built) and a contract address (what people used). Card shows commits for the week PLUS on-chain: transactions, unique wallets, token volume if ERC-20. "What did your protocol ship this week." Either input alone still works.

**Data, no server, no keys:** Blockscout public API per chain (free, no API key): Base `https://base.blockscout.com/api/v2/...`, BNB Chain `https://bscscan.com` needs a key so use Blockscout where available or skip. Solana: public RPC `getSignaturesForAddress` (free, rate-limited; cap at 1000 sigs/week and say "1000+").

**Chain rollout:** Base first (card + payment), Solana second (card + payment), then BNB Chain, Arbitrum, Ethereum mainnet, each as a small config entry {name, rpc, usdcAddress, explorer}. One chain fully working beats five half-working.

**Payments, multi-chain:** same tx-hash flow as above, per chain. USDC addresses: Base 0x833589fCD6eDb6E08f4c7C32D4f71b54bdA02913; Solana USDC mint EPjFWdd5AufqSSqeM2qN1xzybapC8G4wEGGkZwyTDt1v (verify SPL transfer to PAY_TO_SOL via getTransaction). Other chains: add only with the address verified from Circle docs, never guessed.

**Human needs:** PAY_TO (EVM address) and PAY_TO_SOL (Solana address). Same rule: public addresses only.
