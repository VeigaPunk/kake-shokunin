# KakeR33.ScribeS065RowDraft — S065 row draft (freshness, r33-build)

Built: the SOURCES row S065 for the ds4cc-marketplace source opened this round, verified against the
retained bytes and a fresh sandbox clone of the public repository. Draft: `/fast/scratch/hyaku/kake-r33/w1/ScribeS065RowDraft/S065.md`.

## Access
Commit page GET 200 at **2026-10-22T20:02:31Z** (`curl -sS -o /dev/null -w '%{http_code}'` on the commit URL) and
`git clone --filter=blob:none --no-checkout` of https://github.com/VeigaPunk/ds4cc-marketplace.git into
`/fast/scratch/hyaku/kake-r33/w1/ScribeS065RowDraft/up`; `git log -1 7fc6aa2f` → `2026-10-21T17:32:55Z magga: Frostbite — Classic & Remastered at /magga/frostbite/`.
No request to ds4cc.com or any owned host.

## Row (paste-ready, single line, 11 cells; no cell contains `|`, so no escaping needed)

| S065 | ds4cc-marketplace sitemap.xml and the three magga/frostbite index.html pages at upstream commit 7fc6aa2fc12451dd451fed5a9ee7125f3a90e884 — https://github.com/VeigaPunk/ds4cc-marketplace/commit/7fc6aa2fc12451dd451fed5a9ee7125f3a90e884; read through a sandbox clone of https://github.com/VeigaPunk/ds4cc-marketplace.git (the local clone ~/Projects/ds4cc-marketplace is one commit behind, at 1fbdb8ed); retained byte-identical at .ufo/waves/round-33/sources/ds4cc-7fc6aa2f/ | code | A | The content of the operator's own sitemap file and three page files at one commit, read offline; not a statement about what ds4cc.com serves, when or whether the commit deployed, or any later commit | commit 7fc6aa2f (2026-10-21T17:32:55Z, "magga: Frostbite — Classic & Remastered at /magga/frostbite/"); sitemap.xml blob 67d8c7a50dc3a3734ce4be97ffa4810e1e257e12, lines 15–17 add the three frostbite locs; magga/frostbite/index.html blob e0d9ee29d9f1bf21faa0238e3253d4e9199304de line 9 `<link rel="canonical" href="https://ds4cc.com/magga/frostbite/">`; classic/index.html blob 12c58e2dae534f6569015fa3c0ec8cde502c5119 line 12; remastered/index.html blob 4e6d70ae05272e089f4564b1ed6f3c9b21a440a2 line 12 | The source-side state of the ds4cc sitemap and the canonical links of the newest pages at the current upstream head: 100 locs (97 at 1fbdb8ed), three added under /magga/frostbite/, each page's explicit canonical equal to its sitemap loc | mined | 2026-10-22 | 90d | corpus/knowledge/sitemap-orphan-audit.md |

## Quotes (located, verbatim from the retained bytes)
Primary, `sitemap.xml:15–17` — the three added locs, **3 words** (whitespace-token convention used by round-33.md's Gate):
`  <url><loc>https://ds4cc.com/magga/frostbite/</loc></url>` / `  <url><loc>https://ds4cc.com/magga/frostbite/classic/</loc></url>` / `  <url><loc>https://ds4cc.com/magga/frostbite/remastered/</loc></url>`
Secondary, `magga/frostbite/index.html:9` — **3 words**: `<link rel="canonical" href="https://ds4cc.com/magga/frostbite/">` (same shape at classic:12, remastered:12).

## Gate line for the lesson (`### Source openings`, same shape as round-33.md:31)
| S065 | https://github.com/VeigaPunk/ds4cc-marketplace/commit/7fc6aa2fc12451dd451fed5a9ee7125f3a90e884 (read through a sandbox clone of https://github.com/VeigaPunk/ds4cc-marketplace.git, commit page GET 200 at 2026-10-22T20:02:31Z) | 2026-10-22 | “`<link rel="canonical" href="https://ds4cc.com/magga/frostbite/">`” (magga/frostbite/index.html line 9; 3 words); “`<url><loc>https://ds4cc.com/magga/frostbite/</loc></url>`” (sitemap.xml line 15; 1 word) | admit, tier A for the files' own content at that commit, status `mined` |

## Commands run (all in the sandbox; exit 0 unless noted)
- `git clone -q --filter=blob:none --no-checkout https://github.com/VeigaPunk/ds4cc-marketplace.git up` → 0; `git log -1 7fc6aa2f` → hash/date/subject above.
- `git ls-tree`/`rev-parse 7fc6aa2f:<path>` → `100644 67d8c7a5…` sitemap.xml, `100644 e0d9ee29…` hub, `100644 12c58e2d…` classic, `100644 4e6d70ae…` remastered (blob ids match the anchor cell).
- `git show 7fc6aa2f:<path> | cmp - .ufo/…/ds4cc-7fc6aa2f/<path>` ×4 → `identical` (retained bytes = upstream blobs).
- `grep -c '<loc>'` retained → 100; `git show 1fbdb8ed:sitemap.xml | grep -c '<loc>'` → 97; Python ElementTree parse → 100 loc elements, 100 unique.
- `grep -n 'rel="canonical"'` → 9 / 12 / 12, one tag per page, each href present in the parsed loc set.
- `git diff 1fbdb8ed 7fc6aa2f -- sitemap.xml` → three `+` loc lines only; `git diff --stat … -- render.yaml apps-sdk/Dockerfile apps-sdk/src/server.ts .dockerignore` → empty; `diff-tree --name-status` → 11 paths (3 M, 8 A incl. covers).
- Census on `git show bc6c4a8:corpus/SOURCES.md` plus my row: rows 65, malformed 0, duplicate ids none, `mined=50 queued=6 rejected=9`, my row NF=13.

## Findings (advisory)
- Lane HEAD b1752a24 already carries S065 at `corpus/SOURCES.md:73`; my independent draft is **cell-for-cell identical** to it after trailing-space trim (`diff` empty). Row cells match the blocks I re-derived; no correction needed.
- `corpus/lessons/round-33.md:31` Gate row records the URL, 2026-10-22, and two ≤25-word quotes (3 and 1 words) — contract rule 1 satisfied as written. That file is **untracked** at HEAD b1752a24 (`git ls-tree` finds no entry; `git status --porcelain` shows `??`), so the Gate row is in-progress working-tree content, not landed state; the S065 row and the audit section are both committed at b1752a24.
- `corpus/knowledge/sitemap-orphan-audit.md:191,199` cite S065 by id (not by title), so the used-by `mined` status has its citing path; section states `sitemap-locs: 100` and three `canonical …: clean` lines (203–206).

## Not verified (and out of scope)
Live site: no fetch to ds4cc.com, so deployment, live sitemap content and status codes are unknown — creation of this row relies on that. I did not run `scripts/canonical_audit.py`, so the three `clean` verdicts are not independently reproduced; I confirmed only the fact they rest on (exactly one explicit head canonical per page, equal to its sitemap loc). No claim about commits later than 7fc6aa2f. No tools installed.

Draft file: `/fast/scratch/hyaku/kake-r33/w1/ScribeS065RowDraft/S065.md` (row, quotes, gate line, census, limits).
