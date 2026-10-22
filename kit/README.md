# Founder-kit (draft, unreleased)

Run your own AI founder from a fork. It builds a product in a repo, logs every decision,
and drafts public posts for you to publish. It never posts, deploys or spends on its own.

Status: skeleton. Not yet used by anyone but its author. Design: `state/FOUNDER-KIT.md`
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

## Not yet built
- `agent/` scripts and the workflow are copied in a later step.
