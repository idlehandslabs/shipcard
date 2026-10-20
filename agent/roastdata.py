"""Public facts for a roast. Numbers only: no raw text from outside ever leaves
this module (it is untrusted data, never instructions).

summarize_* are pure and tested against fixtures. fetch does the network I/O.
Response shapes follow the Blockscout v2 / DexScreener / GitHub docs; they have
not been run against the live APIs yet (see state/ATTEMPTS.md).
"""
import json
import re
import sys
import urllib.request

BLOCKSCOUT = "https://base.blockscout.com/api/v2"
DEXSCREENER = "https://api.dexscreener.com/latest/dex/tokens"
GITHUB = "https://api.github.com"
EVM = re.compile(r"^0x[0-9a-fA-F]{40}$")
REPO = re.compile(r"^[\w.-]{1,100}/[\w.-]{1,100}$")
VAGUE = {"fix", "update", "wip", "stuff", "changes", "."}


def _num(x, default=0.0):
    try:
        return float(x)
    except (TypeError, ValueError):
        return default


def summarize_wallet(txs):
    """txs: Blockscout /addresses/<a>/transactions payload."""
    items = (txs or {}).get("items") or []
    failed = sum(1 for t in items if t.get("status") == "error" or t.get("result") not in (None, "success"))
    fees = sum(_num((t.get("fee") or {}).get("value")) for t in items) / 1e18
    return {
        "kind": "wallet",
        "txs_sampled": len(items),
        "failed_txs": failed,
        "failed_pct": round(100 * failed / len(items), 1) if items else 0,
        "eth_fees_burned": round(fees, 6),
    }


def summarize_token(pairs, holders):
    """pairs: DexScreener payload. holders: Blockscout /tokens/<a>/holders."""
    ps = sorted((pairs or {}).get("pairs") or [], key=lambda p: -_num((p.get("liquidity") or {}).get("usd")))
    out = {"kind": "token", "pairs": len(ps)}
    if ps:
        p = ps[0]
        out.update(
            liquidity_usd=_num((p.get("liquidity") or {}).get("usd")),
            volume_24h_usd=_num((p.get("volume") or {}).get("h24")),
            change_24h_pct=_num((p.get("priceChange") or {}).get("h24")),
            fdv_usd=_num(p.get("fdv")),
        )
    hs = (holders or {}).get("items") or []
    vals = [_num(h.get("value")) for h in hs]
    total = _num(((hs[0].get("token") if hs else None) or {}).get("total_supply"))
    if vals and total > 0:
        out["top1_holder_pct"] = round(100 * vals[0] / total, 1)
        out["top10_holders_pct"] = round(100 * sum(vals[:10]) / total, 1)
    return out


def summarize_repo(commits):
    """commits: GitHub /repos/<r>/commits list. Keeps counts, never messages."""
    commits = commits if isinstance(commits, list) else []
    days = {((c.get("commit") or {}).get("author") or {}).get("date", "")[:10] for c in commits}
    days.discard("")
    msgs = [((c.get("commit") or {}).get("message") or "").split("\n")[0].strip().lower() for c in commits]
    return {
        "kind": "repo",
        "commits_sampled": len(commits),
        "active_days": len(days),
        "vague_messages": sum(1 for m in msgs if m in VAGUE or len(m) < 4),
        "fix_commits": sum(1 for m in msgs if m.startswith("fix")),
    }


def _get(url):
    req = urllib.request.Request(url, headers={"User-Agent": "idle-hands-roast"})
    with urllib.request.urlopen(req, timeout=20) as r:
        return json.load(r)


def fetch(target):
    t = target.strip()
    if REPO.match(t):
        return summarize_repo(_get(f"{GITHUB}/repos/{t}/commits?per_page=100"))
    if EVM.match(t):
        # A token if DexScreener knows it, otherwise treat as a wallet.
        pairs = _get(f"{DEXSCREENER}/{t}")
        if pairs.get("pairs"):
            return summarize_token(pairs, _get(f"{BLOCKSCOUT}/tokens/{t}/holders"))
        return summarize_wallet(_get(f"{BLOCKSCOUT}/addresses/{t}/transactions"))
    raise ValueError("target must be owner/repo or a 0x address")


if __name__ == "__main__":
    print(json.dumps(fetch(sys.argv[1]), indent=2))
