# Company wallets (public addresses only)

These are receive addresses. Nothing in this repo can spend from them.

| Chain | Purpose | Address |
|-------|---------|---------|
| Solana | PAY_TO_SOL: roasts, Pro, tips (USDC, mint EPjFWdd5AufqSSqeM2qN1xzybapC8G4wEGGkZwyTDt1v) | `rQATX95gRcH6LRJj3mtsAv182gwsoJWvMqScSXzhvT9` |
| Base | PAY_TO: pending, human to add | `TBD` |

Order inbox (Cloudflare Worker, auto-deploys from cf/ on push): https://orders.idlehandslabs.workers.dev
- POST /order {kind, chain, target, tx}  - GET /orders  - GET /health
