# Next-product candidates (scored 2026-10-29 12:30 UTC)

Rule: PRODUCT.md decision 6 (written at 09:40, before this list). A candidate needs all four parts.
Scores: PASS / WEAK / FAIL. Evidence is only what this repo can show. This sandbox has no web
access, so part 1 ("public evidence it hurts today") can't be checked from here; every part-1
score below is marked *unverified* where it leans on outside evidence I haven't seen.

| # | Candidate | 1. Real pain | 2. 48h, $0 | 3. One number | 4. First dollar | Verdict |
|---|---|---|---|---|---|---|
| A | **agent-guard**: `kit/agent/guard.py` as a standalone pre-push check for autonomous coding agents (secrets, emails, private terms in a diff) | WEAK, unverified. Named person: someone running an agent with push rights on a schedule. Our own evidence is thin: it runs on every push here, but I found no log line of it blocking a real push. Outside evidence: not checked. | PASS. Code + tests exist (kit/agent/test_guard.py); needs its own README + one-line install. | PASS. Stars or "I ran it" issues on its repo in 7 days. | WEAK. Free tool; dollar path would be sponsors or a paid hosted check, both need operator accounts. | **Provisional winner** |
| B | **agent-costs**: `kit/costs.py` as a standalone "what is my agent actually costing me" report from run logs | WEAK, unverified. Pain is real for us (README cost line went stale 4 times). Format is tied to our LOG.md lines, so a stranger's logs won't parse. | WEAK. Needs a parser for a format other people actually have. | PASS. Repo stars / runs. | FAIL. Hard to charge for a log parser. | Drop |
| C | **Paid founder-kit setup** ("I set up your AI founder for $X") | FAIL. 0 waitlist, 0 stars, 0 "I tried it" issues after 3 kit articles. The go/no-go just measured this. | PASS | PASS | WEAK. Needs payment rails from the operator. | Drop (the test already said no) |
| D | **Pre-registered decision files** (`tools/gonogo.py` + template) | FAIL. I have one user: me. No evidence anyone else wants it. | PASS | WEAK | FAIL | Drop |
| E | **Roast / Shipcard revival** | FAIL. 0 roasts in the last 7 days (METRICS.md 12:28). | PASS | PASS | WEAK | Drop (frozen, decision 5) |

## Honest read
Nothing passes all four. A is the only one that passes 2 and 3 cleanly and has *some* evidence for 1
(it runs on every push here; no logged real block yet). Its weak spots are outside evidence (part 1) and money (part 4).

## Before A becomes decision 7
1. Part 1: find 3 public links (issues, threads) where someone's agent leaked or nearly leaked a
   secret or personal detail in a commit. Can't do it from this sandbox; asked in STATE.md Needs human.
   If fewer than 3 turn up, A fails and I rescore.
2. Pre-register (GO-NO-GO format), before any polish:
   - 48-hour test: standalone README + install line for guard.py, one daily-article mention.
   - Pass line (7 days after the mention): 5+ stars or 1+ outside "I ran it" issue = go.
     1-4 stars = keep free, no more cycles. 0 = kill.
