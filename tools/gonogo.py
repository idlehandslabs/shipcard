"""Apply the pre-registered go/no-go table (state/GO-NO-GO-2026-10-29.md) to METRICS.md.

Usage: python3 tools/gonogo.py state/METRICS.md --kit-post yes|no|unknown

Reads only numbers the runner collected. It does not know founder-kit's stars,
or whether open issues came from outside; it says so instead of guessing.
"""
import re
import sys

FIELDS = {
    "signups": r"Signups: \*\*(\d+)\*\*",
    "stars": r"Stars: \*\*(\d+)\*\*",
    "forks": r"Forks: \*\*(\d+)\*\*",
    "issues": r"Open issues: \*\*(\d+)\*\*",
}


def parse(text):
    out = {}
    for key, pat in FIELDS.items():
        m = re.search(pat, text)
        if not m:
            raise ValueError(f"METRICS.md has no {key} line")
        out[key] = int(m.group(1))
    return out


def decide(m, kit_post):
    """Return (row, decision). kit_post is 'yes', 'no' or 'unknown'."""
    w = m["signups"]
    if w >= 50:
        return "50+ waitlist", "Go. Stage 3: build the hosted version."
    if w >= 10:
        return "10-49 waitlist", "Go, smaller. Ask the list what they'd pay."
    signals = w + m["stars"] + m["forks"] + m["issues"]
    if signals >= 1:
        return "1-9 signals", "Keep the kit free, drop the paid plan; one more week on reach."
    if kit_post == "yes":
        return "0 signals, kit post went out", "Kill the paid idea. Write the post-mortem."
    if kit_post == "no":
        return "0 signals, nothing went out", "No verdict. Extend 7 days, ask for the Show HN again."
    return "0 signals, post status unknown", "Undecided until the operator answers: did a kit post go out?"


def main(argv):
    if len(argv) != 4 or argv[2] != "--kit-post" or argv[3] not in ("yes", "no", "unknown"):
        print(__doc__.strip().splitlines()[2])
        return 2
    with open(argv[1]) as f:
        m = parse(f.read())
    row, decision = decide(m, argv[3])
    print(f"Waitlist: {m['signups']}")
    print(f"Stars / forks / open issues (shipcard repo): {m['stars']} / {m['forks']} / {m['issues']}")
    print("Not counted here: founder-kit stars (not in METRICS); whether issues are from outside.")
    print(f"Row of the table: {row}")
    print(f"Decision: {decision}")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
