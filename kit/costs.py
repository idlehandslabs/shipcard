"""Recount Claude usage from state/LOG.md so nobody has to do it by hand.

run-cycle.sh appends one line per cycle, e.g.
    2026-10-25T12:15:24Z  cycle rc=0 cost=$0.42  log=logs/cycle-...json
Usage: python3 costs.py [path/to/LOG.md]
"""
import pathlib
import re
import sys

LINE = re.compile(r"^\S+\s+cycle rc=-?\d+ cost=\$([0-9.]+)", re.M)


def summarize(text):
    costs = [float(c) for c in LINE.findall(text)]
    paid = [c for c in costs if c > 0]
    return {
        "cycles": len(costs),
        "total": round(sum(costs), 2),
        "average": round(sum(costs) / len(costs), 2) if costs else 0.0,
        "min": round(min(paid), 2) if paid else 0.0,
        "max": round(max(paid), 2) if paid else 0.0,
        "free": len(costs) - len(paid),
    }


def sentence(s):
    return (f"{s['cycles']} logged cycles, ${s['total']:.2f} total, "
            f"${s['average']:.2f} average, ${s['min']:.2f}-${s['max']:.2f} range "
            f"({s['free']} of the {s['cycles']} cost $0)")


def monthly(s, per_day=4):
    """What a month costs at this average; the workflow runs 4 cycles a day."""
    return round(s["average"] * per_day * 30, 2)


if __name__ == "__main__":
    path = pathlib.Path(sys.argv[1] if len(sys.argv) > 1 else "state/LOG.md")
    s = summarize(path.read_text())
    print(sentence(s))
    print(f"At 4 cycles a day: about ${monthly(s):.2f} a month on an API key "
          "(daily articles extra; a Claude plan uses its allowance instead)")
