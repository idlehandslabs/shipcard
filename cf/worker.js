// Idle Hands Labs order inbox. One Cloudflare Worker + one KV namespace bound as ORDERS.
// No secrets, no auth: everything in an order (a public address/repo and a public tx hash)
// is already public on-chain. The agent reads the queue each cycle, verifies each tx
// on-chain itself, and keeps its own done-list in state/ROASTS.md.
//
//   POST /order   {"kind":"wallet|token|repo","chain":"base|solana","target":"...","tx":"..."}
//   GET  /orders  -> last 200 orders, newest first
//   GET  /health  -> ok

const ALLOW_ORIGIN = "https://idlehandslabs.github.io";
const MAX_PER_IP_PER_HOUR = 10;

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
