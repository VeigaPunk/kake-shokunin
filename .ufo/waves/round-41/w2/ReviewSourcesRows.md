# ReviewSourcesRows — round-41 wave-2 falsify (S117–S119 + census)

Seat: KakeR41.ReviewSourcesRows. Scope: `corpus/SOURCES.md` rows S117–S119 vs registry
header and CORPUS.md §SOURCES; retained bytes in `.ufo/waves/round-41/sources/`.
Checked against the live worktree (uncommitted ` M corpus/SOURCES.md`; commit 2653b62
re-touched all three rows after build `eae5ae2`).

## Commands (exit codes)

- `timeout 900 prlimit --as=4000000000 scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin kake` → **exit 1**.
  First run: 5×E11 for S117–S119 (incl. `corpus/lessons/round-41.md` missing). Re-run after
  the lesson landed: **3×E11** — `S117/S118/S119 missing used-by SCORECARD.md "Round 41"`.
- `sha256sum .ufo/waves/round-41/sources/*` → exit 0; equals `SHA256SUMS` and the row anchors
  (rfc3986.txt `3102dae4…d683`, pypi-abnf.json `d1dab17e…a10d`, pypi-rfc3987.json `f624f451…d2e`).
- `awk -F'|' …` on rows 125–127 → NF=13 each (11 cells, no `|` inside a cell).
- `[ -e ]` per used-by token: `corpus/lessons/round-41.md`, `.ufo/waves/round-41/c1_count.py`,
  `.ufo/waves/round-41/oracle_crosscheck.py`, `SCORECARD.md` all exist;
  `SCORECARD.md "Round 41"` (literal token, space+quotes) does not — census parses used-by by
  comma and tests the whole token (`scripts/sources-census.sh:565`).
- `grep` in retained JSON: wheel digests `cdcac127…0917` (abnf) and `10702b1e…ce53` (rfc3987)
  present, matching row anchors; both scripts reference their package. `fetched-at.txt` =
  2026-10-23T09:39:11Z = rows' fetched stamp. Verified holds.

## Findings

- **High — E11, all three rows.** `used-by` token `SCORECARD.md "Round 41"` fails the census
  `-e` test: it is a path plus a quoted section name, not a "repo-relative path … or `—`"
  (CORPUS.md §SOURCES `used-by`). `SCORECARD.md` exists and has `## Round 41` sections
  (lines 2672, 2755), but the token as written is not a path. Census exits 1: the kake lane
  is not clean. SOURCES.md:125–127, used-by cells.
- **Low — W04 warning on S117** (`duplicate url … rfc3986.txt across scopes`, shared with
  S098). Warning only ("warnings do not affect clean lanes"); scopes are explicitly disjoint
  (S098 §§2.1–2.3 character classes vs S117 full `URI` grammar §3/§3.2.3/§4.3/App A). Honest.
- **Low — in-place teaches edits.** Commit 2653b62 rewrote S117–S119 teaches after the rows
  were added; contract rule 2 wants corrections as `supersedes S0NN —` rows. Same-round
  self-correction, logged in `corpus/lessons/round-41.md` ("Row changes" / gate); borderline.

## Per row

- **S117**: defect (E11 on `SCORECARD.md "Round 41"`). Otherwise conformant: kind=spec, tier=A,
  mined, opened 2026-10-23, recheck 365d, anchor has §3 line 867 + App A lines + Jan-2005 +
  sha256 matching retained bytes; Gate trio in round-41.md:16.
- **S118**: defect (same E11). Otherwise conformant: kind=code, tier=B, recheck on-release,
  anchor wheel sha256 present in retained JSON, `c1_count.py` exists and uses abnf.
- **S119**: defect (same E11). Otherwise conformant: `oracle_crosscheck.py` exists, wheel
  sha256 verified, Gate trio at round-41.md:18.

## Verdict on acceptance

Census: runs, exit 1 (fails). Retained bytes match row sha256s — holds. Per row: S117, S118,
S119 each carry one lane-failing defect (E11 used-by token); all other contract fields conform.
