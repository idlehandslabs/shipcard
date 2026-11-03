#!/usr/bin/env python3
"""Publish daily-log/<date>.md articles as static pages under app/blog/ (GitHub Pages).

Plain code, run by the workflow after the agent writes the daily article. Protected path:
the agent can't edit it. No third-party packages needed; if `cairosvg` is installed the
cover SVG is also rendered to cover.png for link previews on X.

    python3 agent/publish_blog.py            # (re)build every article
"""
import html, json, os, re, shutil, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LOG_DIR = os.path.join(ROOT, "daily-log")
OUT_DIR = os.path.join(ROOT, "app", "blog")
SITE = "https://idlehandslabs.github.io/shipcard"
DATE_RX = re.compile(r"^(\d{4}-\d{2}-\d{2})\.md$")
SKIP_SECTIONS = ("meme ideas",)


def inline(text):
    """Escape, then apply **bold**, `code` and [text](https://url) links."""
    codes = []
    def keep(m):
        codes.append("<code>" + html.escape(m.group(1)) + "</code>")
        return f"\x00{len(codes) - 1}\x00"
    s = re.sub(r"`([^`]+)`", keep, text)
    s = html.escape(s, quote=False)
    s = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", s)
    s = re.sub(r"(?<![\w*])\*(?!\s)(.+?)(?<!\s)\*(?![\w*])", r"<em>\1</em>", s)
    s = re.sub(r"\[([^\]]+)\]\((https?://[^\s)\"]+)\)", r'<a href="\2">\1</a>', s)
    s = re.sub(r'(?<!href=")(?<!">)(https?://[^\s<"\x00]+[^\s<".,;:)\x00])', r'<a href="\1">\1</a>', s)
    return re.sub(r"\x00(\d+)\x00", lambda m: codes[int(m.group(1))], s)


def md_to_html(md, images):
    lines, out, i = md.splitlines(), [], 0
    title, skipping, para, lst = "", False, [], None

    def flush():
        nonlocal para, lst
        if para:
            out.append("<p>" + inline(" ".join(para)) + "</p>")
            para = []
        if lst:
            tag = lst[0]
            out.append(f"<{tag}>" + "".join(f"<li>{inline(x)}</li>" for x in lst[1]) + f"</{tag}>")
            lst = None

    while i < len(lines):
        ln = lines[i].rstrip()
        if ln.startswith("```"):
            flush()
            block, i = [], i + 1
            while i < len(lines) and not lines[i].startswith("```"):
                block.append(lines[i]); i += 1
            if not skipping:
                out.append("<pre>" + html.escape("\n".join(block)) + "</pre>")
            i += 1
            continue
        m = re.match(r"^(#{1,3})\s+(.*)$", ln)
        if m:
            flush()
            level, text = len(m.group(1)), m.group(2).strip()
            if level == 1 and not title:
                title = text
                i += 1
                continue
            skipping = text.lower() in SKIP_SECTIONS
            if not skipping:
                out.append(f"<h{level}>{inline(text)}</h{level}>")
            i += 1
            continue
        if skipping:
            i += 1
            continue
        img = re.match(r"^\[\s*IMAGE\s+(\d+)\s*\]$", ln.strip())
        if img:
            flush()
            src = images.get(int(img.group(1)))
            if src:
                out.append(f'<p><img src="{src}" alt="meme {img.group(1)}"></p>')
        elif re.match(r"^\s*[-*]\s+", ln):
            if para: flush()
            if not lst or lst[0] != "ul":
                flush(); lst = ("ul", [])
            lst[1].append(re.sub(r"^\s*[-*]\s+", "", ln))
        elif re.match(r"^\s*\d+\.\s+", ln):
            if para: flush()
            if not lst or lst[0] != "ol":
                flush(); lst = ("ol", [])
            lst[1].append(re.sub(r"^\s*\d+\.\s+", "", ln))
        elif ln.startswith(">"):
            flush()
            out.append("<blockquote>" + inline(ln.lstrip("> ")) + "</blockquote>")
        elif ln.strip() in ("", "---"):
            flush()
        elif lst and ln.startswith("  "):
            lst[1][-1] += " " + ln.strip()
        else:
            if lst: flush()
            para.append(ln.strip())
        i += 1
    flush()
    return title, "\n".join(out)


PAGE = """<!doctype html>
<html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<meta name="description" content="{desc}">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{desc}">
<meta property="og:url" content="{url}">
{og_image}<meta name="twitter:card" content="summary_large_image">
<style>
body{{margin:0;background:#121212;color:#F4F1EA;font:18px/1.65 system-ui,-apple-system,Segoe UI,sans-serif}}
main{{max-width:720px;margin:0 auto;padding:32px 16px 80px}}
a{{color:#FF5A1F}} h1{{font-size:34px;line-height:1.2}} h2{{margin-top:36px}}
img{{max-width:100%;border-radius:12px}} pre,code{{background:#1C1C1C;border-radius:6px}}
pre{{padding:12px;overflow:auto;font-size:15px}} code{{padding:1px 4px}}
blockquote{{border-left:3px solid #FF5A1F;margin:0;padding-left:14px;color:#A8A296}}
.top{{color:#A8A296;font-size:15px}}
</style></head><body><main>
<p class="top"><a href="{site}/blog/">Idle Hands Labs</a> &middot; an AI building a startup in public &middot; {date}</p>
{cover}<h1>{h1}</h1>
{body}
<p class="top"><a href="{site}/blog/">All days</a> &middot; <a href="https://github.com/idlehandslabs/founder-kit">The free kit</a> &middot; <a href="https://x.com/idlehandslabs">@idlehandslabs</a></p>
</main></body></html>
"""


def publish_one(date, md):
    out = os.path.join(OUT_DIR, date)
    os.makedirs(out, exist_ok=True)
    assets = os.path.join(LOG_DIR, "assets", date)
    images, cover_html, og = {}, "", ""
    if os.path.isdir(assets):
        for name in sorted(os.listdir(assets)):
            if not name.endswith(".svg"):
                continue
            shutil.copyfile(os.path.join(assets, name), os.path.join(out, name))
            m = re.match(r"meme-(\d+)\.svg$", name)
            if m:
                images[int(m.group(1))] = name
        if os.path.exists(os.path.join(assets, "cover.svg")):
            cover_html = '<p><img src="cover.svg" alt="cover"></p>\n'
            try:
                import cairosvg
                cairosvg.svg2png(url=os.path.join(assets, "cover.svg"),
                                 write_to=os.path.join(out, "cover.png"), output_width=1500)
                og = f'<meta property="og:image" content="{SITE}/blog/{date}/cover.png">\n'
            except Exception:
                pass
    title, body = md_to_html(md, images)
    title = title or f"Idle Hands Labs, {date}"
    first_p = re.search(r"<p>(.*?)</p>", body)
    desc = re.sub(r"<[^>]+>", "", first_p.group(1))[:200] if first_p else title
    page = PAGE.format(title=html.escape(title), desc=html.escape(desc, quote=True),
                       url=f"{SITE}/blog/{date}/", og_image=og, site=SITE, date=date,
                       cover=cover_html, h1=html.escape(title), body=body)
    with open(os.path.join(out, "index.html"), "w") as f:
        f.write(page)
    return {"date": date, "title": title, "url": f"{SITE}/blog/{date}/"}


def main():
    posts = []
    for name in sorted(os.listdir(LOG_DIR), reverse=True):
        m = DATE_RX.match(name)
        if m:
            with open(os.path.join(LOG_DIR, name)) as f:
                posts.append(publish_one(m.group(1), f.read()))
    items = "\n".join(f'<li><a href="{p["date"]}/">{html.escape(p["title"])}</a> <span class="top">{p["date"]}</span></li>' for p in posts)
    index = PAGE.format(title="Idle Hands Labs: daily log", desc="An AI building a startup in public. Every day, every failure.",
                        url=f"{SITE}/blog/", og_image="", site=SITE, date="all days", cover="",
                        h1="Daily log", body=f"<ul>{items}</ul>")
    os.makedirs(OUT_DIR, exist_ok=True)
    with open(os.path.join(OUT_DIR, "index.html"), "w") as f:
        f.write(index)
    with open(os.path.join(OUT_DIR, "posts.json"), "w") as f:
        json.dump(posts, f, indent=1)
    print(f"published {len(posts)} articles to app/blog/")


if __name__ == "__main__":
    sys.exit(main())
