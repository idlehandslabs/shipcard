# Run the agent in the cloud with GitHub Actions — no laptop, no install

This runs the **build cycle every 3 hours** and writes the **daily article once a day**,
entirely on GitHub's servers. Your computer can be off. The agent's work (code, short
posts, daily articles) is committed back into the repo; you read the drafts and post them.

Everything below is done in a web browser.

## One-time setup

1. **GitHub account** — create a free one at github.com if you don't have it.
2. **New repository** — create one (Private is fine), e.g. `ai-founder`.
3. **Upload this project** — on the repo page: **Add file → Upload files**, then drag in
   everything from this folder (keep the structure, including the `.github` folder) and
   commit. (If `.github` is hard to drag on your OS, use the git method at the bottom.)
4. **Anthropic API key** — go to console.anthropic.com → **API keys** → **Create key**,
   copy it. (This is pay-as-you-go API billing — separate from a Claude chat subscription.)
5. **Add the key as a secret** — in the repo: **Settings → Secrets and variables →
   Actions → New repository secret**:
   - Name: `ANTHROPIC_API_KEY`
   - Value: *(paste the key)*
6. **Allow the workflow to write** — **Settings → Actions → General → Workflow
   permissions → Read and write permissions** → Save.
7. **Enable Actions** — open the **Actions** tab; if prompted, enable workflows.

Done. It now runs on the schedule above.

## Make Shipcard live, with your approval on every release

8. **Turn on Pages** — Settings → Pages → *Build and deployment* → Source: **GitHub Actions**.
9. **Require your approval** — Settings → Environments → **github-pages** → tick
   *Required reviewers*, add yourself → Save.

From then on, whenever the agent changes the app, a deploy starts and **waits**. You get a
notification; open it, click **Review deployments → Approve**, and Shipcard updates. If the
app didn't change, nothing happens and nobody gets pinged.

## What runs automatically, every cycle
- **Before the agent wakes:** a read-only step collects real stars, forks, open issues and
  whether the site is live, into `state/METRICS.md`. The agent never holds a GitHub key.
- **The agent:** builds, tests, commits, and logs every attempt in `state/ATTEMPTS.md`.
- **After it finishes:** a truth recorder reads the raw run record and logs any blocked
  actions or errors on its own, so failures can't go missing from the story.
- **Daily:** the article pulls from all of the above, with a "What I tried (and what
  broke)" section.

## Test it immediately

Actions tab → **ai-founder** → **Run workflow** → choose `cycle` → **Run workflow**.
Watch it run; when it finishes, your repo has a new commit and a fresh draft.

## Where the output appears

- Short per-cycle posts → `post-queue/`
- Daily articles → `daily-log/`

Read the newest, post it to X yourself, then move the file into the matching
`published/` folder. **Nothing is ever posted automatically.**

## Good to know

- **Cost:** roughly $0.15–0.25 of API usage per cycle; every 6 hours ≈ $0.80–1.00/day (fits the $100 budget for 2–3 months). To
  change the pace, edit the `cron:` lines in `.github/workflows/agent.yml` (times are UTC).
- GitHub pauses scheduled workflows after ~60 days with no repo activity — any commit or
  a manual run resets that.
- The agent commits locally during a cycle; the workflow is what pushes. The agent itself
  is still blocked from pushing, spending, or posting (see `.claude/settings.json` + `CLAUDE.md`).

## Alternative upload (if you know git)

```
# in this unzipped folder
git init && git add -A && git commit -m "ai-founder"
git branch -M main
git remote add origin https://github.com/<you>/ai-founder.git
git push -u origin main
```
