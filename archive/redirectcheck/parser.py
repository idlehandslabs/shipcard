"""Parse a redirects CSV into rows, collecting malformed rows as problems."""

import csv
import io
from dataclasses import dataclass


@dataclass(frozen=True)
class Redirect:
    row: int  # 1-based line number in the input
    source: str
    target: str


@dataclass(frozen=True)
class Problem:
    kind: str
    row: int
    message: str


def parse(text):
    """Return (redirects, problems). Accepts an optional `source,target` header."""
    redirects, problems = [], []
    reader = csv.reader(io.StringIO(text))
    for row_no, fields in enumerate(reader, start=1):
        fields = [f.strip() for f in fields]
        if not any(fields):
            continue
        if row_no == 1 and [f.lower() for f in fields[:2]] == ["source", "target"]:
            continue
        if len(fields) < 2 or not fields[0] or not fields[1]:
            problems.append(Problem("malformed", row_no, "needs both a source and a target"))
            continue
        source, target = fields[0], fields[1]
        if not source.startswith("/"):
            problems.append(Problem("malformed", row_no, f"source {source!r} must start with '/'"))
            continue
        redirects.append(Redirect(row_no, source, target))
    return redirects, problems
