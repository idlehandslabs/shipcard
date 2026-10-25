# Extracting the kit to its own repo (human steps)

The agent can't do these (new repo, accounts, push). Each is a few minutes.

1. Create an empty repo (public if you want others to fork it).
2. Copy the contents of `kit/` to the repo root. `workflow/agent.yml` goes to `.github/workflows/agent.yml`.
3. Run both test commands from the README. Expect 4 + 11 passing.
4. Add Actions secrets `CLAUDE_CODE_OAUTH_TOKEN` and `PRIVATE_TERMS`.
5. Run `python3 init.py --name ... --idea ... --budget 100`, commit, run the workflow once by hand.
6. Read the first commit before leaving it on a schedule.

Check before making it public: grep for brand names, handles and personal details. `agent/guard.py` scans pushes, but a fresh repo has no history to scan.
