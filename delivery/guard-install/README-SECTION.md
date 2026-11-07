## Secret guard

This repo runs `agent/guard.py` before code leaves your machine and again in CI.
It blocks a push when the new commits contain a wallet secret (an EVM private key next
to a key-ish name like `PRIVATE_KEY=0x...`, a Solana base58 private key, a Solana
keypair JSON array, a labelled seed phrase) or a common API key (AWS, OpenAI, Stripe,
GitHub, ...). It names the file, never the key.

**Local hook (once per clone, from the repo root):**

    cat > .git/hooks/pre-push <<'HOOK'
    #!/bin/sh
    exec python3 agent/guard.py "$(git rev-parse @{u} 2>/dev/null || echo HEAD~1)"
    HOOK
    chmod +x .git/hooks/pre-push

**CI:** `.github/workflows/guard.yml` runs the same check on every push and pull request.

**Known gap:** a seed phrase with no label next to it (12 bare words) is not caught.
If a key was ever pushed, rotate it and move the funds; deleting the commit is not enough.
