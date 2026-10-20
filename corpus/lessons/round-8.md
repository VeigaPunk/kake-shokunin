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

## Gate

Label: **retrospective round-21 reconstruction, not original admission.** The round-8 landing (2026-09-28) recorded no `## Gate`, no admit/reject ledger, and no outside spot-check. Everything below is reconstructed from the original sections above, the `LOG.md` round-8 entry (`LOG.md:12`), and `corpus/knowledge/kimi-subpath-audit.md`.

Metadata:

- verified-at: original evidence 2026-09-28 (`LOG.md:12`); historical-not-live-reverified in round 21. No domain or live-state recheck was run.
- recheck: local reading only: `corpus/knowledge/kimi-subpath-audit.md` and `LOG.md:12`. The raw evidence `/tmp/kimi_audit.py` and `/tmp/kimi-subpath-audit.json` is transient and not in the repo; operator must restore those artifacts into the repo or retire these citations.
- source authority: S019 is the metadata-contract authority, not a platform authority (round-21 wave spec, Lesson14 prompt). The S019 contract text is not present under `corpus/` at read time; no S019 row is asserted as verified here.
- Cites: original sections lines 1-8 (cites), 10-15 (gap closed), 17-40 (what the audit found), 42-58 (learned); round-21 lesson `corpus/lessons/round-21.md`, not present in `corpus/lessons/` at read time, and nothing here depends on its contents.

Candidates considered (original sections):

- Close the README residual "kimi subpaths" with a two-enumeration audit (live-index link sweep plus canonical sitemap parity). Outcome: **admitted with qualification**. Landed per `LOG.md:12` and `kimi-subpath-audit.md:1-5`; the closure is the record's own claim and was not independently rechecked.
- ds4cc.kimi.page: 74 of 93 canonical paths missing, every miss post-vintage, zero rot (lines 19-25). Outcome: **admitted with qualification**. The count is superseded to **75** by sitemap commit `f3d2ecd` (`kimi-subpath-audit.md:39-43`, `LOG.md:13`, `corpus/knowledge/free-read-verbs.md:211`). The original "74" lines are preserved unchanged.
- `dir/` hrefs (`omarchy-usage/`, `omegag/`, `speedrun/`) 404 on kimi while `*/index.html` serves 200. Outcome: **admitted with qualification**. Recorded as a 2026-09-28 GET result (`kimi-subpath-audit.md:45-51`); not re-GET in round 21.
- Other 9 live kimi rows link-clean, "44 same-origin links, 0 real non-200" (lines 31-33). Outcome: **zero-real-non-200 admitted with qualification; the 44 count unverified**. The entry table (`kimi-subpath-audit.md:53-65`) lists 33 same-origin links across its nine rows, and the ds4cc row's link count is not in the table, so 44 is not reconciled in the record.
- Vault and veigapunk hide links client-side; a static sweep is blind to rendered PROPERTIES[] rot (lines 14-17). Outcome: **admitted** as a method limit (`kimi-subpath-audit.md:14-17, 63-64`).
- `update` sends index.html only while `recreate`/`rebuild` zip the whole tree (`kimi-surface.mjs` :459-466 vs :903-908; lines 49-55). Outcome: **unverified in round 21**. This seat did not re-read the script; `LOG.md:12` carries the same claim.
- Orphaned 09-26 `update` fire (code 7) never touched live (lines 53-55). Outcome: **unverified in round 21**. Recorded only in the original lesson and `LOG.md:12`.
- Publish vintage from max embedded DOM date when version timestamps are not persisted (lines 56-58). Outcome: **admitted as method** (`kimi-subpath-audit.md:85-86`). The claim that kimi-map whitelists updateTimes out was not rechecked.

Rejected candidates: not recorded.

Outside spot-check: not recorded. This seat found no independent non-author verifier record for the round-8 kimi audit in the corpus. The only later review is in-lane errata (`kimi-subpath-audit.md:39-43`, round-9 review; `LOG.md:13`), which is not an outside spot-check.

Limits: no live-state, domain, or `/tmp` re-verification; no network reads; no mirror commands run. The 74-to-75 change is a recorded supersession, not an edit to the original body.
