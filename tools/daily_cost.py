"""Per-day Claude cost from state/LOG.md runner lines, for the Sunday review.

Answers one question: what does a day of cycles cost, and is it rising?
Usage: python3 tools/daily_cost.py [LOG ...]
Default: state/LOG-HISTORY.md (if present) + state/LOG.md, so archiving old
log lines never drops days from the report.
"""
import collections
import pathlib
import re
import sys

LINE = re.compile(r"^(\d{4}-\d{2}-\d{2})T\S+\s+cycle rc=-?\d+ cost=\$([0-9.]+)", re.M)


def by_day(text):
    days = collections.OrderedDict()
    for day, cost in LINE.findall(text):
        n, total = days.get(day, (0, 0.0))
        days[day] = (n + 1, total + float(cost))
    return [(d, n, round(t, 2), round(t / n, 2)) for d, (n, t) in sorted(days.items())]


def report(rows):
    out = ["day         cycles  cost     avg/cycle"]
    out += [f"{d}  {n:>6}  ${t:>6.2f}  ${a:.2f}" for d, n, t, a in rows]
    return "\n".join(out)


DEFAULT = ["state/LOG-HISTORY.md", "state/LOG.md"]


def read_logs(paths):
    return "\n".join(pathlib.Path(p).read_text() for p in paths if pathlib.Path(p).exists())


if __name__ == "__main__":
    print(report(by_day(read_logs(sys.argv[1:] or DEFAULT))))
