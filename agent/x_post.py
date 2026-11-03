#!/usr/bin/env python3
"""Post today's published article to X, once. Plain code, run by .github/workflows/x-post.yml
after the site deploys. Protected path: the agent can't edit it.

Safety, in order (any failure = no post):
  1. today's article must exist AND its page must already be live on the site;
  2. not already posted today (marker in state/x-posted/<date>.json);
  3. the post text must pass the same checks as the guard: no emails, no secrets,
     none of the owner's PRIVATE_TERMS (never printed);
  4. without all four X_* secrets it only prints a dry run.
"""
import datetime, json, os, re, sys, urllib.request

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SITE = "https://idlehandslabs.github.io/shipcard"
MARK_DIR = os.path.join(ROOT, "state", "x-posted")
EMAIL = re.compile(r"[A-Za-z0-9._%+\-]+@[A-Za-z0-9.\-]+\.[A-Za-z]{2,}")
SECRETS = re.compile(r"sk-ant-|gh[pousr]_[A-Za-z0-9]{30,}|github_pat_|AKIA[0-9A-Z]{16}|xox[baprs]-|"
                     r"-----BEGIN [A-Z ]*PRIVATE KEY-----|sk-[A-Za-z0-9]{20,}")
KEYS = ("X_API_KEY", "X_API_SECRET", "X_ACCESS_TOKEN", "X_ACCESS_SECRET")


def build_text(md, url):
    title = next((l[2:].strip() for l in md.splitlines() if l.startswith("# ")), "")
    title = re.sub(r"\s+—\s+[^:]+:\s*", ": ", title, count=1)          # "Day 16 — Kit: x" -> "Day 16: x"
    body = md.split("## What I thought", 1)[-1] if "## What I thought" in md else md
    para = next((p.strip() for p in re.split(r"\n\s*\n", body)
                 if p.strip() and not p.lstrip().startswith(("#", "```", "[", "-", "|", ">"))), "")
    para = re.sub(r"[*`_]", "", re.sub(r"\s+", " ", para))
    room = 280 - 23 - len(title) - 4                                    # X counts any URL as 23
    if len(para) > room:
        para = para[:max(0, room - 1)].rsplit(" ", 1)[0] + "…"
    return f"{title}\n\n{para}\n\n{url}".replace("\n\n\n\n", "\n\n") if para else f"{title}\n\n{url}"


def unsafe(text):
    low = text.lower()
    terms = [t.strip().lower() for t in re.split(r"[,\n]", os.environ.get("PRIVATE_TERMS", "")) if len(t.strip()) >= 3]
    problems = [f"private term #{i}" for i, t in enumerate(terms, 1) if t in low]
    if [e for e in EMAIL.findall(text) if not e.lower().endswith("example.com")]:
        problems.append("email address")
    if SECRETS.search(text):
        problems.append("secret-looking string")
    return problems


def live(url):
    try:
        req = urllib.request.Request(url, headers={"user-agent": "idlehands-poster"})
        return urllib.request.urlopen(req, timeout=20).status == 200
    except Exception:
        return False


def main():
    date = os.environ.get("POST_DATE") or datetime.datetime.utcnow().strftime("%Y-%m-%d")
    md_path = os.path.join(ROOT, "daily-log", f"{date}.md")
    mark = os.path.join(MARK_DIR, f"{date}.json")
    url = f"{SITE}/blog/{date}/"
    if not os.path.exists(md_path):
        print(f"no article for {date}; nothing to post"); return 0
    if os.path.exists(mark):
        print(f"already posted {date}"); return 0
    if not live(url):
        print(f"{url} is not live yet; will try after the next deploy"); return 0
    text = build_text(open(md_path).read(), url)
    problems = unsafe(text)
    if problems:
        print("POST BLOCKED:", ", ".join(problems)); return 1
    if not all(os.environ.get(k) for k in KEYS):
        print("DRY RUN (X secrets not set). Would post:\n" + text); return 0
    from requests_oauthlib import OAuth1Session
    s = OAuth1Session(os.environ["X_API_KEY"], os.environ["X_API_SECRET"],
                      os.environ["X_ACCESS_TOKEN"], os.environ["X_ACCESS_SECRET"])
    r = s.post("https://api.x.com/2/tweets", json={"text": text}, timeout=30)
    if r.status_code not in (200, 201):
        print(f"X API error {r.status_code}: {r.text[:300]}"); return 1
    tid = r.json().get("data", {}).get("id")
    os.makedirs(MARK_DIR, exist_ok=True)
    with open(mark, "w") as f:
        json.dump({"date": date, "id": tid, "url": f"https://x.com/idlehandslabs/status/{tid}"}, f)
    print(f"posted {date}: https://x.com/idlehandslabs/status/{tid}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
