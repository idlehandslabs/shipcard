#!/usr/bin/env python3
"""Collect real-world signals BEFORE the agent wakes up, and write state/METRICS.md.

Runs as its own GitHub Actions step with a read-only token. The agent never sees the
token; it only reads the numbers. Needs: gh CLI, GH_TOKEN, GITHUB_REPOSITORY.
"""
import json, os, subprocess, datetime, pathlib, urllib.request

repo = os.environ.get("GITHUB_REPOSITORY", "")
out = pathlib.Path(__file__).resolve().parent.parent / "state" / "METRICS.md"
now = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%d %H:%M UTC")

def gh(*args):
    r = subprocess.run(["gh", *args], capture_output=True, text=True, timeout=60)
    if r.returncode != 0:
        raise RuntimeError(r.stderr.strip()[:200])
    return r.stdout

lines = [f"# Real-world signals", f"_Collected {now} by the runner, before the agent woke up._", ""]
try:
    if not repo:
        raise RuntimeError("not running in GitHub Actions")
    info = json.loads(gh("api", f"repos/{repo}"))
    lines += ["## Repo", f"- Stars: **{info.get('stargazers_count', 0)}**",
              f"- Forks: **{info.get('forks_count', 0)}**",
              f"- Open issues: **{info.get('open_issues_count', 0)}**", ""]
    # live site
    try:
        url = json.loads(gh("api", f"repos/{repo}/pages")).get("html_url", "")
    except Exception:
        url = ""
    if url:
        try:
            live = urllib.request.urlopen(url.rstrip("/") + "/version.txt", timeout=15).read().decode().strip()
        except Exception:
            live = "unreachable"
        lines += ["## Live site", f"- URL: {url}", f"- Deployed app version (tree hash): `{live}`", ""]
    else:
        lines += ["## Live site", "- Not live yet (GitHub Pages not enabled).", ""]
    # feedback: COUNTS ONLY. No issue text ever reaches the agent, so nothing written
    # by outsiders can be used to inject instructions. Humans read issues on GitHub.
    issues = json.loads(gh("issue", "list", "--repo", repo, "--state", "open", "--limit", "100",
                           "--json", "number,createdAt"))
    recent = [i for i in issues if i["createdAt"][:10] >= (datetime.date.today() - datetime.timedelta(days=7)).isoformat()]
    lines += ["## Feedback", f"- Open issues: **{len(issues)}** (new this week: **{len(recent)}**)",
              "- Issue text is deliberately NOT shown to the agent.", ""]
except Exception as e:
    lines += [f"Metrics unavailable this run: {e}"]

# usage counts from the order inbox (counts only; no addresses or IPs exist there)
try:
    st = json.loads(urllib.request.urlopen(urllib.request.Request("https://orders.idlehandslabs.workers.dev/stats?days=7", headers={"user-agent": "idlehands-metrics"}), timeout=15)  # default Python UA gets 403 from Cloudflare.read().decode())
    days = st.get("days", [])
    keys = ["roast", "share", "download", "copy", "deep_submit"]
    tot = {k: sum(int(d.get(k, 0)) for d in days) for k in keys}
    lines += ["## Roast usage (last 7 days, UTC)",
              "| day | roasts | posted to X | downloads | links copied | deep orders |", "|---|---|---|---|---|---|"]
    for d in days:
        lines.append(f"| {d.get('day')} | " + " | ".join(str(int(d.get(k, 0))) for k in keys) + (" (capped)" if d.get("capped") else "") + " |")
    lines += [f"| **total** | " + " | ".join(f"**{tot[k]}**" for k in keys) + " |", ""]
except Exception as e:
    lines += [f"Roast usage unavailable this run: {str(e)[:120]}", ""]

out.write_text("\n".join(lines) + "\n")
print("\n".join(lines))
