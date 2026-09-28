# Lesson — round 8 (2026-09-28)

Cites: LOG.md round-8 entry; `corpus/knowledge/kimi-subpath-audit.md`;
evidence = `/tmp/kimi_audit.py` run ~21:15Z (10 rows swept, 93-loc sitemap
parity) + `kimi-surface.mjs` payload reads (update = index.html only at
:459-466; recreate zip = whole sourceDir minus `.git`/`.github`/excludes at
:903-908) + `state/kimi-map.json` bound-chat updateTimes. Commit `round-8`.
Zero publishes, zero metered ops, zero browser ops — pure HTTP.

## The gap closed

README residual "kimi subpaths (byte compare meaningless — needs per-path
title+marker)". Closed with a two-enumeration audit: live-index link sweep
per live row + canonical `sitemap.xml` parity for ds4cc.kimi.page, each miss
classified by `git log --diff-filter=A` vs publish vintage.

## What the audit actually found

- **ds4cc.kimi.page is missing 74 of 93 canonical sitemap paths — and every
  single miss post-dates its publish vintage** (63 added 09-23, 10 added
  09-22, 1 added 09-08; live index max embedded date 2026-08-21, dedupe
  report says ~Aug-29 build). Zero pre-vintage files missing → **zero rot,
  pure staleness**. PQ-2 is now quantified: the republish delta is 74
  canonical paths (all of magga/, burnerchrome/, infinizoom, omarchy-usage,
  omegag).
- **`dir/` hrefs are live-dead on kimi.** The mirror's index links
  `omarchy-usage/`, `omegag/`, `speedrun/` — all 404 while `*/index.html`
  serves 200. The same hrefs work on GHP (`/dir` → 301). This class is
  permanent on kimi: no redirect exists, so it's a publish-time href rewrite
  or a source fix — landed as live-proof under the dir-index pitfall.
- **The other 9 live kimi rows have clean link surfaces** (44 same-origin
  links GET'd, 0 real non-200). Stale-but-intact confirmed by embedded max
  dates: plazir27.kimi.page 09-18, plazir27runs-on 09-02, ufofsd-charter
  09-05.
- **Vault + veigapunk-page hide their links client-side.** The only "link"
  a static sweep sees is the literal `${p.url}` template — rendered
  PROPERTIES[] rot (PQ-1) is invisible without DOM execution. Sweep noise
  also includes inline-JS template literals like `${esc(p.href)}` and
  Cloudflare's `/cdn-cgi/l/email-protection` — filter `[$`{]` class before
  classifying.

## Learned

- **Staleness needs a different enumeration than rot.** Probe/reconcile see
  the index; sourceDir walks see files the mirror never carried. The
  canonical sitemap is the right "should-serve" set — it answers "how stale"
  in one pass, and git first-commit dates turn 404s into evidence instead of
  noise.
- **`update` and `recreate` transfer different surfaces.** `update` sends
  index.html-only instructions ("replace the site files ... single
  self-contained page, verify zero residue"); `recreate`/`rebuild` zip the
  whole tree. A mirror's subpath richness is a function of which verb last
  produced a version — but since publish is human, the orphaned 09-26
  `update` fire (code 7) left the live multi-file build untouched. Read the
  payload construction before assuming what a fire can change.
- **Vintage is readable from the DOM.** Max embedded date on the fetched
  index is a free publish-vintage estimate when version timestamps aren't
  persisted (kimi-map whitelists them out).
