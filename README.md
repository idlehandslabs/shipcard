# Autopilot — a 24/7 build-in-public agent, powered by Claude Code

This is a small harness that runs **Claude Code** as an autonomous engineer on a
loop. Each cycle it reads its own state, does one unit of work, commits, updates
its memory, and drafts a progress post for you to approve. Chained across days,
it behaves like a tireless operator building a project in public.

**What's yours vs the agent's**

- **You** hold all credentials, approve every X post, and control spend. You never
  hand the agent your X login — it only writes drafts.
- **The agent** does all the engineering, testing, committing, and self-reporting,
  inside this one folder, under the hard rules in `CLAUDE.md`.

---

## What's in here

```
autopilot/
├── CLAUDE.md              # the agent's constitution (mission + hard rules). EDIT the Mission block.
├── agent/
│   ├── cycle-prompt.md    # the instruction handed to Claude Code each cycle
│   ├── run-cycle.sh       # runs ONE cycle (safe to test by hand)
│   └── loop.sh            # the 24/7 driver: cycle → sleep → repeat
├── state/
│   ├── STATE.md           # "what's true now / next up / needs human" — agent updates it
│   ├── TASKS.md           # the backlog — agent grooms it
│   └── LOG.md             # append-only run log
├── post-queue/            # agent drops drafts here; you approve + post; move to published/
├── .claude/settings.json  # scoped permissions (deny list + guardrails)
├── .mcp.json              # add project MCP servers here later (empty for now)
└── logs/                  # raw per-cycle JSON output (created on first run; gitignored)
```

---

## Setup from zero (≈ 10 minutes)

Works on macOS 13+ and Linux (Ubuntu 20.04+/Debian 10+). Commands are for a terminal.

### 1. Install Claude Code

```bash
curl -fsSL https://claude.ai/install.sh | bash
```

Then make sure its folder is on your PATH (the installer puts `claude` in `~/.local/bin`):

```bash
echo 'export PATH="$HOME/.local/bin:$PATH"' >> ~/.zshrc   # use ~/.bashrc on Linux
exec $SHELL
claude --version
```

### 2. Authenticate

You need an **Anthropic account**. Two billing options:

- **Claude subscription (recommended for this):** run `claude` once, use `/login` in the
  prompt, then create a long-lived token for unattended runs:
  ```bash
  claude setup-token          # interactive once; prints a token valid ~1 year
  ```
  Copy that token — you'll set it as `CLAUDE_CODE_OAUTH_TOKEN` in step 4.

- **API key (pay-as-you-go):** get a key from console.anthropic.com and use
  `ANTHROPIC_API_KEY` instead. Simpler, but you pay per token with no subscription cap.

> Create the account and the token yourself — I can't make accounts or enter credentials for you.

### 3. Put this folder where you want it, and make it a git repo

```bash
cd ~/path/to/autopilot
git init && git add -A && git commit -m "autopilot harness"
chmod +x agent/run-cycle.sh agent/loop.sh
```

### 4. Point the agent at your auth

Pick ONE. Put it in your shell profile so every run sees it:

```bash
# Subscription token (recommended):
echo 'export CLAUDE_CODE_OAUTH_TOKEN="paste-your-token-here"' >> ~/.zshrc

# …OR an API key instead:
echo 'export ANTHROPIC_API_KEY="sk-ant-…"' >> ~/.zshrc

exec $SHELL
```

### 5. Define the mission

Open `CLAUDE.md` and replace the **Mission** block (the `PLACEHOLDER` section) with your
real project: a name, a one-sentence description, what "v0.1 done" means, and non-goals.
This is the single most important edit — it's *what the agent builds*. (If you leave it as
PLACEHOLDER, the first cycle just scaffolds a repo and waits for you.)

### 6. Test one cycle by hand, watching it work

```bash
./agent/run-cycle.sh
cat state/LOG.md          # see the one-line cycle record (exit code + cost)
git log --oneline         # see what it committed
ls post-queue/            # read the draft it wrote for you
```

If that looks right, you're ready to run it continuously.

### 7. Go 24/7

On your laptop, in a terminal (keep the machine awake):

```bash
# macOS — caffeinate stops it sleeping while the loop runs:
caffeinate -s ./agent/loop.sh

# Linux:
./agent/loop.sh
```

Default cadence is **one cycle every 3 hours**. Change it:

```bash
INTERVAL_SECONDS=3600 caffeinate -s ./agent/loop.sh   # hourly
```

Stop with **Ctrl-C**.

---

## Your daily 30 seconds

1. Skim new files in `post-queue/`.
2. Post the good ones to X yourself → move them to `post-queue/published/`.
3. Glance at `state/STATE.md` → **Needs human** for anything the agent is blocked on.

---

## Cost & the honest caveats

- **Usage is the real cost.** Each cycle spends tokens; `--max-budget-usd 3.00` in
  `run-cycle.sh` caps a single cycle, and the 3-hour cadence keeps daily spend sane.
  Lower the interval and you pay more. On a subscription, cycles draw against your plan limits.
- **Laptops aren't truly 24/7.** Sleep, reboots, and wifi drops pause the loop. `caffeinate`
  helps on macOS, but for real always-on, a ~$5/mo VPS or a scheduled CI job is more robust —
  ask and I'll convert this to either.
- **The agent is sandboxed by policy, not by the OS.** `.claude/settings.json` denies pushes,
  `sudo`, `curl`/`wget`, reading `.env`/`secrets`, and web tools; `run-cycle.sh` only
  auto-approves a scoped tool list; `CLAUDE.md` forbids posting, spending, and acting outside
  this folder. These are strong guardrails, but permission rules are not a kernel sandbox —
  keep the folder free of anything you wouldn't want an energetic engineer touching.
- **It never posts.** Publishing to X is always your action.

## Tuning later

- **Let it do web research:** remove `WebFetch`/`WebSearch` from the `deny` list in
  `.claude/settings.json` and from `--disallowedTools` in `run-cycle.sh`.
- **Give it project tools:** add MCP servers to `.mcp.json`, then allow them in
  `run-cycle.sh` via `--allowedTools "mcp__<server>"`.
- **Resume context instead of fresh each cycle:** ask and I'll switch the runner to
  `--resume` with a saved session id (trades cost for continuity).
