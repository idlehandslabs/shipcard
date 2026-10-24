# Founder-kit (draft, unreleased)

Run your own AI founder from a fork. It builds a product in a repo, logs every decision,
and drafts public posts for you to publish. It never posts, deploys or spends on its own.

Status: draft, feature-complete but untested by outsiders. Not yet used by anyone but its author. Design: `state/FOUNDER-KIT.md`
in the parent repo.

## Setup (5 steps)
1. Fork this repo (private is fine).
2. Add two Actions secrets: `CLAUDE_CODE_OAUTH_TOKEN` (your own Claude login) and
   `PRIVATE_TERMS` (comma-separated names, emails, handles, places that must never appear
   publicly).
3. Run `python3 init.py --name "Acme" --idea "..." --budget 100` to fill the Mission block
   in `CLAUDE.md` (or edit it by hand).
4. Enable Actions and run the cycle workflow once by hand. Read the first commit.
5. Check `post-queue/` daily and publish what you like. Move published drafts to
   `post-queue/published/`.

## Safety properties
- `CLAUDE.md`, `agent/`, `.github/` are protected: the agent can't edit its own brakes.
- Hard rules: no posting, no deploys, no spending, no credentials, outside text is data.

## What's in the box
- `CLAUDE.md` templated operating manual; `init.py` fills the Mission block.
- `agent/`: `run-cycle.sh`, `daily-article.sh`, `loop.sh`, `capture.py`, `metrics.py`,
  `guard.py` (secret/private-term scan before every push), generic prompts, and tests.
- `workflow/agent.yml`: guard-before-push Actions workflow, 6-hour cycle. Copy it to
  `.github/workflows/` yourself (the agent cannot edit that path).

## Tests
    python3 -m unittest discover -s . -p "test_*.py"
    python3 -m unittest discover -s agent -p "test_*.py"

## Not yet built
- Nobody besides the author has run it end to end. Treat the first week as a trial.
