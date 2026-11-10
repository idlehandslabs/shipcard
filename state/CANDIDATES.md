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

## Rescore 2026-11-01 (operator evidence arrived)
Operator pasted 3 public links (headlines only, not read in full; no web access here):
a Towards AI first-person "AI coding agent leaked our secret keys", a Radware measurement of
credentials in agent instruction files, and a Claude Code bug report about secrets read out of
`.env` files. Plus Infisical, Knostic and CSA write-ups.
- **Part 1 (it hurts today): WEAK -> PROVISIONAL PASS.** 3 leads, not 3 verified incidents. 2 of 3
  are about agents *reading/sending* secrets, which a pre-push diff check does not stop. Only the
  first is about a commit. Honest count of on-target evidence: 1.
- **Part 2 (we can build it): PASS on code, NEW WEAKNESS on "why ours".** gitleaks, TruffleHog and
  GitGuardian already block secrets in commits, free and mature. Our differences: (1) one
  zero-dependency file, (2) blocks *private terms* (names, places you list) and emails, not just
  keys, (3) built for an agent's push loop. Only (2) is something scanners don't do out of the box.
- **Decision:** no product yet. If agent-guard goes ahead, the pitch is "private terms + emails for
  agents that push", NOT "another secret scanner". Pattern-adding cycles stay stopped.
- **Next:** pre-register GO-NO-GO for the 48-hour test with that narrower pitch, then the
  standalone README. Pass/kill lines unchanged.

## Rescore 2026-11-10 (after agent-guard KILL): lead "settings.local.json leaks"
Lead (operator-supplied, a stranger's public post, 26.8K views, 2026-11-09):
https://x.com/TekonBurns/status/2119847464786341945 . Claim: 100,000+ `.claude/settings.local.json`
files in public GitHub repos, ~1,100 with live credentials, because "don't ask again" stores the raw
approved command (tokens included) in that file. It cites an arstechnica article; I have only the
headline, so the numbers are UNVERIFIED by me.
Our own fact (checked this run with `git ls-files` + grep): neither this repo's `.gitignore` nor the
kit's mentions `.claude/settings.local.json`, and kit/agent/guard.py does not block it by name. The
kit runs Claude Code. We have the gap ourselves.
1. Real pain, named person: **pass, pending verification.** Crypto builder running Claude Code in a
   bot repo clicks "don't ask again" on `curl -H "Authorization: Bearer ..."` or `solana ... --keypair`,
   then `git add .`. Stranger's public post, large audience. Needs the article read to confirm.
2. Reachable in 48h, $0: **pass.** A free check fits in the kit + an article.
3. One number: **pass** (can pre-register: stars/"I ran it" within 7 days of a linked mention).
4. Path to a first dollar: **fail as a paid product.** The fix is one `.gitignore` line, free, and
   GitHub secret scanning already flags many of the tokens. Scanning strangers' public repos for it
   is the same "map for thieves" the operator rejected on 11-05.
Verdict: **not the next product.** It is the best free REACH item we have (timely, true, we had
the bug). No candidate passes all 4 today; saying so instead of forcing one.
