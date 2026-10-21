#!/usr/bin/env python3
"""Order intake. Runs in the workflow BEFORE the agent wakes, with network access the agent
does not have. Plain code, no AI: it decides what is paid, the agent only writes roasts.

For each order in the Cloudflare inbox that is not yet in state/orders/:
  1. validate the fields with strict regexes (anything else is dropped, never passed on)
  2. verify the payment on Solana: tx succeeded, recent, and PAY_TO_SOL's USDC balance
     went up by >= PRICE in that tx
  3. if paid, pull the target wallet's public numbers (same facts the free roast uses)
  4. write state/orders/<id>.json  -> {"status": "paid"|"unpaid"|"invalid", ...numbers}
The agent reads state/orders/*.json with status "paid" and no "roast" field, writes the
roast page, then sets "roast" to the page path. Numbers only reach the agent; no free text.
"""
import json, os, re, sys, time, urllib.request

INBOX = "https://orders.idlehandslabs.workers.dev/orders"
RPCS = ["https://solana-rpc.publicnode.com", "https://api.mainnet-beta.solana.com"]
PAY_TO_SOL = "rQATX95gRcH6LRJj3mtsAv182gwsoJWvMqScSXzhvT9"
USDC_MINT = "EPjFWdd5AufqSSqeM2qN1xzybapC8G4wEGGkZwyTDt1v"
PRICE = 5.0
MAX_AGE = 7 * 86400
TOKEN_PROGRAMS = ["TokenkegQfeZyiNwAJbNbGKPFXCWuBvf9Ss623VQ5DA", "TokenzQdBNbLqP5VEhdkAS6EPFLC1PHnBqCXEpPxuEb"]
OUT = os.path.join(os.path.dirname(__file__), "..", "state", "orders")

RX_ID = re.compile(r"^[0-9a-f]{8}$")
RX_SOL_ADDR = re.compile(r"^[1-9A-HJ-NP-Za-km-z]{32,44}$")
RX_SOL_TX = re.compile(r"^[1-9A-HJ-NP-Za-km-z]{64,90}$")


def http_json(url, body=None, timeout=20):
    data = json.dumps(body).encode() if body is not None else None
    req = urllib.request.Request(url, data=data, headers={"content-type": "application/json", "user-agent": "idlehands-orders"})
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return json.loads(r.read().decode())


def rpc(method, params, post=http_json):
    last = None
    for url in RPCS:
        try:
            j = post(url, {"jsonrpc": "2.0", "id": 1, "method": method, "params": params})
            if "error" in j:
                raise RuntimeError(str(j["error"].get("message", "rpc error"))[:80])
            return j["result"]
        except Exception as e:  # try the next node
            last = e
    raise RuntimeError(f"rpc failed: {last}")


def usdc_received(tx, owner=PAY_TO_SOL, mint=USDC_MINT):
    """USDC amount `owner` gained in this parsed transaction (0 if none)."""
    meta = (tx or {}).get("meta") or {}
    def total(key):
        s = 0.0
        for b in meta.get(key) or []:
            if b.get("mint") == mint and b.get("owner") == owner:
                s += float((b.get("uiTokenAmount") or {}).get("uiAmount") or 0)
        return s
    return round(total("postTokenBalances") - total("preTokenBalances"), 6)


def verify_payment(sig, now, post=http_json):
    tx = rpc("getTransaction", [sig, {"encoding": "jsonParsed", "maxSupportedTransactionVersion": 0, "commitment": "confirmed"}], post)
    if not tx:
        return "unpaid", "transaction not found"
    if (tx.get("meta") or {}).get("err") is not None:
        return "unpaid", "transaction failed on-chain"
    bt = tx.get("blockTime") or 0
    if now - bt > MAX_AGE:
        return "unpaid", "transaction older than 7 days"
    got = usdc_received(tx)
    if got + 1e-9 < PRICE:
        return "unpaid", f"received {got} USDC, need {PRICE}"
    return "paid", f"received {got} USDC"


def wallet_numbers(addr, now, post=http_json):
    bal = rpc("getBalance", [addr], post)
    sigs = rpc("getSignaturesForAddress", [addr, {"limit": 1000}], post) or []
    toks = []
    for p in TOKEN_PROGRAMS:
        try:
            toks += (rpc("getTokenAccountsByOwner", [addr, {"programId": p}, {"encoding": "jsonParsed"}], post) or {}).get("value") or []
        except Exception:
            pass
    amounts = [float(((((a.get("account") or {}).get("data") or {}).get("parsed") or {}).get("info") or {}).get("tokenAmount", {}).get("uiAmount") or 0) for a in toks]
    times = [s["blockTime"] for s in sigs if isinstance(s.get("blockTime"), int)]
    hours = [0] * 24
    for t in times:
        hours[(t // 3600) % 24] += 1
    return {
        "sol": round((bal or {}).get("value", 0) / 1e9, 4),
        "tx_count": len(sigs), "tx_capped": len(sigs) >= 1000,
        "failed": sum(1 for s in sigs if s.get("err") is not None),
        "newest_days_ago": round((now - max(times)) / 86400, 1) if times else None,
        "span_days": round((max(times) - min(times)) / 86400, 1) if times else 0,
        "active_days": len({t // 86400 for t in times}),
        "utc_hour_histogram": hours,
        "token_accounts": len(amounts),
        "token_accounts_zero": sum(1 for a in amounts if not a),
        "token_accounts_nonzero": sum(1 for a in amounts if a > 0),
    }


def process(order, now, post=http_json):
    oid, chain, kind, target, tx = (order.get(k) for k in ("id", "chain", "kind", "target", "tx"))
    if not (isinstance(oid, str) and RX_ID.match(oid)):
        return None  # unusable id: drop silently
    rec = {"id": oid, "created_at": str(order.get("createdAt", ""))[:30], "checked_at": now}
    if chain != "solana" or kind != "wallet" or not RX_SOL_ADDR.match(str(target)) or not RX_SOL_TX.match(str(tx)):
        rec.update(status="invalid", reason="only Solana wallet roasts are supported")
        return rec
    rec.update(target=target, tx=tx)
    try:
        status, reason = verify_payment(tx, now, post)
    except Exception as e:
        return dict(rec, status="retry", reason=str(e)[:120])
    rec.update(status=status, reason=reason)
    if status == "paid":
        try:
            rec["numbers"] = wallet_numbers(target, now, post)
        except Exception as e:
            rec.update(status="retry", reason=f"paid, but wallet data failed: {str(e)[:80]}")
    return rec


def main():
    os.makedirs(OUT, exist_ok=True)
    try:
        orders = http_json(INBOX).get("orders") or []
    except Exception as e:
        print(f"orders: inbox unreachable ({e})"); return 0
    now = int(time.time())
    seen_tx = set()
    for f in os.listdir(OUT):
        if f.endswith(".json"):
            try:
                seen_tx.add(json.load(open(os.path.join(OUT, f))).get("tx"))
            except Exception:
                pass
    counts = {}
    for o in orders[:200]:
        oid = o.get("id") if isinstance(o, dict) else None
        if not (isinstance(oid, str) and RX_ID.match(oid)):
            continue
        path = os.path.join(OUT, f"{oid}.json")
        if os.path.exists(path):
            prev = json.load(open(path))
            if prev.get("status") not in ("retry", "unpaid") or now - prev.get("checked_at", 0) < 3 * 3600:
                continue  # final, or re-check unpaid/retry at most every 3h
        if o.get("tx") in seen_tx and not os.path.exists(path):
            rec = {"id": oid, "status": "invalid", "reason": "tx hash already used", "checked_at": now}
        else:
            rec = process(o, now)
        if rec:
            json.dump(rec, open(path, "w"), indent=2)
            counts[rec["status"]] = counts.get(rec["status"], 0) + 1
    print(f"orders: {len(orders)} in inbox, processed {counts or 'none'}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
