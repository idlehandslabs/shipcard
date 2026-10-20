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
