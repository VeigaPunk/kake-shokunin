# W2 ReviewLessonGate — round-33 `## Gate` vs SOURCES contract v1

Seat: KakeR33.ReviewLessonGate. Rev: `0a0acfb1b2e74494ccc591e317f6a4c3e048f2a0` (lane tip).
Clone: `/fast/scratch/hyaku/kake-r33/w2/ReviewLessonGate/clone` (fresh clone, all reads via `git show`/files at tip; lane working tree never read).
Contract: `/home/vgpnk/Projects/shokunin/CORPUS.md` lines 64–140 ("SOURCES.md — where a shokunin learns", frozen v1).
Target: `corpus/lessons/round-33.md` `## Gate` (lines 25–36): `### Source openings` table (S065, S066) plus old→new paragraph.

## Conformance table

| Contract requirement | Evidence | Result |
|---|---|---|
| Rule 1: Gate records URL per new row | `round-33.md:31` — S065 names `…/commit/7fc6aa2f…884` + read method; `:32` — S066 names both `api.github.com` URLs; matches `SOURCES.md` rows 73–74 `source` cells | conformant |
| Rule 1: access date per new row | Gate `opened` col = `2026-10-22` for both; S065 clone 19:49:58Z, S066 `gh api` 20:05:11Z/20:06:32Z; matches row `opened` cells | conformant |
| Rule 1: ≤25-word quote + location, verbatim in retained bytes | S065 q1 `<link rel="canonical" href="https://ds4cc.com/magga/frostbite/">` = 3 words, verbatim `ds4cc-7fc6aa2f/magga/frostbite/index.html:9`; q2 `<url><loc>…</loc></url>` = 1 word, verbatim `sitemap.xml:15`. S066 q `"name":"Deploy marketplace to GitHub Pages" … "status":"completed","conclusion":"success"` = 6–7 whitespace tokens; both fragments verbatim in `gh-actions-runs-7fc6aa2f.json` (compact JSON, no space after colons) on run `39644779773` (unique to that file across the two retained JSONs) | conformant |
| Quote grounds `teaches` | S065 quotes witness canonical=sitemap loc; S066 quote witnesses success conclusion — both match `teaches` cells | conformant |
| Rule 2: old→new logging | `round-33.md:34-36` logs `—`→`mined`/`2026-10-22`/`90d`/`sitemap-orphan-audit.md` for both rows; values equal tip cells | conformant |
| Rule 2: append-only, no other row changed | `git diff 5777d5af..0a0acfb -- corpus/SOURCES.md` = 2 insertions, 0 deletions (only lines 73–74) | conformant |
| Rule 1: every new row recorded | diff adds only S065, S066; both appear in Gate table | conformant |

## Commands run (all exit 0)

- `git clone -q <lane> …/clone && git checkout -q 0a0acfb1` — HEAD = tip.
- `git diff 5777d5af79cac1ebf9144b348a9d274099e77338 0a0acfb1… — corpus/SOURCES.md`; `--unified=0 | grep -c '^[+-][^+-]'` → `2`.
- `git show 0a0acfb1:corpus/SOURCES.md | grep -nE '^\|[[:space:]]*S06[56]'` → rows at lines 73, 74.
- Census on tip `SOURCES.md`: rows=66; malformed (`NF!=13`)=0; dup ids=none.
- `grep -nE 'S06[56]' corpus/knowledge/sitemap-orphan-audit.md` → citations at lines 191, 199, 230, 236 (`mined` status consistent with used-by).
- `grep -c '<loc>' …/sitemap.xml` → 100; upstream `git show 1fbdb8ed:sitemap.xml | grep -c '<loc>'` → 97 (row anchor "100 (97 at 1fbdb8ed)" true).
- `git hash-object` on 4 retained files vs `git rev-parse 7fc6aa2f:<path>` in `/fast/scratch/hyaku/kake-r33/ds4cc-upstream`: all 4 blob ids identical and equal the S065 anchor ids (`67d8c7a5…`, `e0d9ee29…`, `12c58e2d…`, `4e6d70ae…`).

## Defects

None blocking. Minor nit (not a contract violation): S066's quote location is `run 39644779773 object` and omits the filename; it is still uniquely locatable (the id appears only in `gh-actions-runs-7fc6aa2f.json`), and the quote is elided (`…` between fragments) — each fragment is a verbatim substring but the joined string is not contiguous. S065 quotes carry exact file:line and are contiguous; same standard would have fit S066.

## Not verified

- "clone made 2026-10-22T19:49:58Z per wave-1 `CriticDeclarationOrder`" timestamp (not re-checkable cheaply).
- Whether other `SOURCES.md` sections (Paths/Search log/Leads) needed updates for these rows — outside the Gate diff; Search log/Paths unchanged per the diff (2 insertions only).

## Tooling

No installs; git/awk/grep/python3 already present.

Verdict (scoped to `corpus/lessons/round-33.md` `## Gate` + the two added rows): **conformant** to SOURCES contract v1.
