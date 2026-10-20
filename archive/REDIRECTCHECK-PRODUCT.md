# Product: RedirectCheck

**One problem:** Site migrations ship with a spreadsheet of `old URL -> new URL`
redirects, and the mistakes in it (loops, chains, duplicates, conflicting rules,
redirects to self) silently cost search traffic. There's no quick offline way to
lint that list before it goes live.

**Who it's for:** Freelance SEOs, small agencies, and developers moving a site
(WordPress -> Next.js, domain changes, URL restructures) who keep redirects in a CSV.

**What it does:** Paste or upload a CSV of redirects. It reports every problem
found and exports a cleaned list as Netlify `_redirects` or nginx `rewrite` rules.

## Why this one

- Pure logic: no third-party accounts, paid APIs, or real user data needed to demo.
- Easy to test thoroughly (graph problems with crisp right answers).
- Real pain, narrow scope; the checks are the product, the UI is thin.
- Python stdlib only, so nothing to install and nothing to deploy to demo locally.

## Checks (v0.1)

1. Self-redirect (`/a -> /a`)
2. Duplicate source with the same target (harmless, dedupe)
3. Duplicate source with conflicting targets (error)
4. Redirect loop (`/a -> /b -> /a`)
5. Redirect chain (`/a -> /b -> /c`), with a suggested flattened target
6. Malformed rows (missing field, source not starting with `/`)

## Done for v0.1

- `python -m redirectcheck file.csv` prints a grouped report with row numbers and exits non-zero on errors.
- `--export netlify|nginx` writes flattened, deduped rules.
- A tiny local web page (stdlib `http.server`) with a textarea that shows the same report.
- Unit tests cover every check; README has a demo with a sample CSV.

## Plan

1. Scaffold package + CSV parser + tests
2. Checks: self, duplicates, conflicts
3. Checks: loops and chains (+ flatten)
4. CLI + exporters
5. Local web page
6. README demo and polish

## Non-goals

Crawling live URLs, hosting, accounts, billing, regex rules, a platform.
