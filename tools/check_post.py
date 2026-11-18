"""Check a post-queue draft against the operator's 2026-11-16 X rules.

Rules (state/STATE.md, "X REACH IS LIMITED"): one plain update, under 270 chars,
no links, no wallet address, no 'DM me', no 'send USDC' / selling.
Lines starting with '#' are notes for the operator and are not counted.

Usage: python3 tools/check_post.py post-queue/<file>.md   (exit 1 = do not post)
"""
import re
import sys

LIMIT = 270
RULES = [
    ("link", re.compile(r"https?://|www\.|\b[\w-]+\.(com|io|xyz|dev|app|org)\b", re.I)),
    ("wallet address", re.compile(r"\b[1-9A-HJ-NP-Za-km-z]{32,44}\b|\b0x[0-9a-fA-F]{40}\b")),
    ("DM ask", re.compile(r"\bDMs?\b", re.I)),
    ("payment ask", re.compile(r"\bUSDC\b|\bsend\s+(me\s+)?(sol|usdc|crypto)\b|\bpay\b", re.I)),
]


def post_text(raw):
    return "\n".join(l for l in raw.splitlines() if not l.lstrip().startswith("#")).strip()


def problems(raw):
    text = post_text(raw)
    out = []
    if not text:
        out.append("empty post")
    if len(text) >= LIMIT:
        out.append(f"{len(text)} chars (limit: under {LIMIT})")
    for name, rx in RULES:
        if rx.search(text):
            out.append(name)
    return out


def main(argv):
    bad = 0
    for path in argv[1:]:
        with open(path, encoding="utf-8") as f:
            found = problems(f.read())
        print(f"{path}: {'OK' if not found else 'DO NOT POST: ' + ', '.join(found)}")
        bad += bool(found)
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
