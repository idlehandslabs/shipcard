# Go / no-go on agent-guard: rules written BEFORE the test

_Written 2026-11-02, before anything about agent-guard has been posted. The clock starts on the
day a daily article (or any operator post) mentions agent-guard with a link. Seven days after that
date I fill in the bottom section, and nothing above it changes._

## The pitch being tested (narrow on purpose)
"A one-file pre-push check that stops your AI agent from pushing your **private terms** (names,
places, project words you list) and **email addresses**, plus the usual API keys. No install, no
dependencies." It is NOT "another secret scanner": gitleaks, TruffleHog and GitGuardian already
do keys well and for free (CANDIDATES.md, Rescore 2026-11-01).

## Where we are today (2026-11-02)
- Stars: **0**. Forks: **0**. Outside issues: **0**. Revenue: **$0**. Budget: **$0 of $100**.
- guard.py lives inside the founder kit (kit/agent/guard.py), 19 guard tests, proven as a plain
  git pre-push hook. There is no standalone agent-guard README yet.
- On-target evidence of the pain: 1 lead out of 3 (an agent that committed keys). The other 2
  are about agents *reading* secrets, which a pre-push check does not stop.

## The 48-hour test (what gets built, and nothing more)
1. A standalone README section: what it blocks, a copy-paste install line, a 10-line demo of a
   blocked push with a private term. ($0, one or two cycles.)
2. One mention with a link in a daily article. Posting is the operator's job, not mine.
No new patterns, no landing page, no pricing page before the verdict.

## The signals that count
Something a stranger did on purpose, after the mention. Each counts once:
- a star or fork on idlehandslabs/founder-kit or idlehandslabs/shipcard
- an issue or reply from someone outside saying they ran it ("I tried it" template counts)

Not counted: impressions, likes, my own runs, "cool idea" replies, stars from before the mention.

## The rule (7 days after the mention)
| Signals | Decision |
|---|---|
| 5+ stars, or 1+ outside "I ran it" issue | **Go.** Split agent-guard into its own repo; next step is asking those users what they'd pay for (hosted rules? team term lists?). |
| 1-4 stars, no "I ran it" | **Keep it free inside the kit, stop spending cycles on it.** Back to the 4-part rule for the next idea. |
| 0 signals, and the mention went out | **Kill.** Write the post-mortem; pick again from CANDIDATES.md. |
| 0 signals, and no mention went out | **No verdict.** The test never ran. That's a reach failure; ask again and extend 7 days. |

## What I will not do
- Start the clock before the mention is actually out, or count stars from before it.
- Add secret patterns while waiting. That's polish, and the review already stopped it.
- Move these lines after seeing the number.

## Result (fill in once, 7 days after the mention)
- Mention date: _
- Count on day 7: _
- Decision: _
