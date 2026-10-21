// Idle Hands Labs order inbox. One Cloudflare Worker + one KV namespace bound as ORDERS.
// No secrets, no auth: everything in an order (a public address/repo and a public tx hash)
// is already public on-chain. The agent reads the queue each cycle, verifies each tx
// on-chain itself, and keeps its own done-list in state/ROASTS.md.
//
//   POST /order   {"kind":"wallet|token|repo","chain":"base|solana","target":"...","tx":"..."}
//   GET  /orders  -> last 200 orders, newest first
//   POST /hit     {"e":"roast|share|download|copy|deep_submit"}  -> counts only
//   GET  /stats?days=7 -> daily counts
//   GET  /health  -> ok

const ALLOW_ORIGIN = "https://idlehandslabs.github.io";
const MAX_PER_IP_PER_HOUR = 10;
// Usage events from the roast page. Counting stops at DAILY_COUNT_CAP writes a day so a
// traffic spike can never use up the free KV write quota (1,000/day) that orders rely on.
const EVENTS = ["roast", "share", "download", "copy", "deep_submit"];
const DAILY_COUNT_CAP = 500;

const RX = {
  evmAddr: /^0x[0-9a-fA-F]{40}$/,
  evmTx: /^0x[0-9a-fA-F]{64}$/,
  solAddr: /^[1-9A-HJ-NP-Za-km-z]{32,44}$/,
  solTx: /^[1-9A-HJ-NP-Za-km-z]{64,90}$/,
  repo: /^[A-Za-z0-9_.-]{1,39}\/[A-Za-z0-9_.-]{1,100}$/,
};

function cors(extra = {}) {
  return {
    "access-control-allow-origin": ALLOW_ORIGIN,
    "access-control-allow-methods": "GET, POST, OPTIONS",
    "access-control-allow-headers": "content-type",
    "content-type": "application/json",
    ...extra,
  };
}
const json = (obj, status = 200) => new Response(JSON.stringify(obj), { status, headers: cors() });

function validate(o) {
  if (!o || typeof o !== "object") return "bad body";
  const { kind, chain, target, tx } = o;
  if (!["wallet", "token", "repo"].includes(kind)) return "kind must be wallet, token or repo";
  if (!["base", "solana"].includes(chain)) return "chain must be base or solana";
  if (typeof target !== "string" || typeof tx !== "string") return "target and tx must be strings";
  if (kind === "repo") {
    if (!RX.repo.test(target)) return "repo must look like owner/name";
  } else if (chain === "base") {
    if (!RX.evmAddr.test(target)) return "target must be a 0x address";
  } else if (!RX.solAddr.test(target)) return "target must be a Solana address";
  if (chain === "base" ? !RX.evmTx.test(tx) : !RX.solTx.test(tx)) return "tx hash format is wrong";
  return null;
}

export default {
  async fetch(request, env) {
    const url = new URL(request.url);
    if (request.method === "OPTIONS") return new Response(null, { status: 204, headers: cors() });
    if (url.pathname === "/health") return json({ ok: true });

    // --- usage counter: counts only, no addresses, no IPs stored ---
    if (url.pathname === "/hit" && request.method === "POST") {
      let e;
      try { e = (await request.json()).e; } catch { return json({ error: "bad body" }, 400); }
      if (!EVENTS.includes(e)) return json({ error: "unknown event" }, 400);
      const key = `c:${new Date().toISOString().slice(0, 10)}`;
      const day = (await env.ORDERS.get(key, "json")) || {};
      if ((day._w || 0) >= DAILY_COUNT_CAP) return json({ ok: true, capped: true }, 202);
      day[e] = (day[e] || 0) + 1;
      day._w = (day._w || 0) + 1;
      await env.ORDERS.put(key, JSON.stringify(day), { expirationTtl: 90 * 86400 });
      return json({ ok: true });
    }

    if (url.pathname === "/stats" && request.method === "GET") {
      const n = Math.min(30, Math.max(1, parseInt(url.searchParams.get("days") || "7", 10) || 7));
      const out = [];
      for (let i = 0; i < n; i++) {
        const d = new Date(Date.now() - i * 86400000).toISOString().slice(0, 10);
        const c = (await env.ORDERS.get(`c:${d}`, "json")) || {};
        out.push({ day: d, ...Object.fromEntries(EVENTS.map((k) => [k, c[k] || 0])), capped: (c._w || 0) >= DAILY_COUNT_CAP });
      }
      return json({ days: out });
    }

    if (url.pathname === "/orders" && request.method === "GET") {
      const list = (await env.ORDERS.get("queue", "json")) || [];
      return json({ orders: list.slice(0, 200) });
    }

    if (url.pathname === "/order" && request.method === "POST") {
      const ip = request.headers.get("cf-connecting-ip") || "unknown";
      const hourKey = `ip:${ip}:${Math.floor(Date.now() / 3600000)}`;
      const used = parseInt((await env.ORDERS.get(hourKey)) || "0", 10);
      if (used >= MAX_PER_IP_PER_HOUR) return json({ error: "too many orders, try later" }, 429);

      let body;
      try { body = await request.json(); } catch { return json({ error: "body must be JSON" }, 400); }
      const err = validate(body);
      if (err) return json({ error: err }, 400);

      const list = (await env.ORDERS.get("queue", "json")) || [];
      if (list.some((o) => o.tx === body.tx)) return json({ error: "that tx hash was already submitted" }, 409);

      const order = {
        id: crypto.randomUUID().slice(0, 8),
        kind: body.kind, chain: body.chain, target: body.target, tx: body.tx,
        createdAt: new Date().toISOString(),
      };
      list.unshift(order);
      await env.ORDERS.put("queue", JSON.stringify(list.slice(0, 500)));
      await env.ORDERS.put(hourKey, String(used + 1), { expirationTtl: 3600 });
      return json({ ok: true, id: order.id }, 201);
    }

    return json({ error: "not found" }, 404);
  },
};
