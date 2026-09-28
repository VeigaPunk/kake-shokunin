# Lesson — round 6 (2026-09-28)

Cites: LOG.md round-6 entry; `corpus/knowledge/ghp-subpath-spotcheck.md`;
evidence = live baseline audit (2 352 paths, ~16:45Z) +
`~/Projects/webzites/src/reconcile.mjs` source + per-repo git lead/lag.
Commit `round-6`. Zero publishes, zero metered ops.

## The gap closed

README's residual gap: "GHP subpath rot beyond `index.html` is still
invisible — no spotcheck tooling exists yet." Closed with a procedure +
first baseline, not new code: a ~30-line script pattern (walk sourceDir,
GET live, sha-compare) plus a classification rule that turned out to be
the entire point.

## What the audit actually found

- **0 true rot** across 2 352 paths (ds4cc 1 874, plazir15 35, charter 443).
- **126 non-clean results, all explained by git state, not deploy rot**:
  ds4cc was 20 commits ahead of `origin/main` (120 diffs incl. live-404
  `robots.txt`/`sitemap.xml`/`404.html`/`infinizoom/main.js` — unpushed
  additions), plazir15 5 ahead (5 diffs), charter 2 behind (1 diff).
- **`reconcile` covers ONE `index.html`, not "index.html"** — source read
  proved it scores candidates (depth ≤2) and compares a single file.
  SKILL.md's "subpaths beyond index" blind spot was understated: even
  second `index.html` files (`magga/v2/index.html` etc.) are invisible.
- **`in-sync` on GHP masks real byte drift** — title+marker parity is a
  kimi affordance misapplied to a verbatim-bytes surface. charter-ghp
  logged `in-sync` while index differed 8.6 KB vs 50.9 KB (source lag).
  Keeper precedent (09-21 log) already knew: resolve with `git pull`,
  re-reconcile to `match`.
- **GHP serves dir indexes** (`/dir` 301→`/dir/`→index.html) — kimi
  doesn't; the mirror pitfall is now live-verified, and `.md` files are
  servable raw so they're fair game for spotchecks.

## Learned

- **The classification table is the tool.** "live ≠ source" decomposes
  into local-ahead (resolves on push), local-behind (`git pull`), and
  true rot — the only actionable class. Comparing against `origin/main`
  instead of the working tree collapses ~95% of raw diffs into noise.
- **`expect` tripwires can't watch what isn't the row URL.** probe covers
  one URL, reconcile covers one file; subpaths have no tripwire slot at
  all. Spotcheck is the only coverage for the other ~1 900 paths.
- **A baseline of zero findings is still the payload** — it establishes
  that the current fleet has no subpath rot and defines the diff
  signature for when it appears (live ≠ origin/main, not live ≠ HEAD).
