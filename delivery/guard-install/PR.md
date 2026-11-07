# Operator checklist: deliver one guard install (49 USDC, kind "repo")

Only after state/orders/<id>.json says status "paid". Target = owner/name from the order.

1. Fork owner/name, branch `add-secret-guard`.
2. Copy into the fork:
   - `kit/agent/guard.py` -> `agent/guard.py` (if `agent/` is taken, use `tools/guard.py`
     and change the path in the workflow and the README section)
   - `delivery/guard-install/.github/workflows/guard.yml` -> `.github/workflows/guard.yml`
   - `delivery/guard-install/README-SECTION.md` -> append to their README
3. Open the PR. Title: `Add secret guard (blocks wallet keys and seed phrases)`.
   Body: the README section, plus "Paid order <id>. Merging is your call."
4. Never run a history scan on their repo and never put findings in the PR.
   The PR adds the guard; it reports nothing about their past commits.
