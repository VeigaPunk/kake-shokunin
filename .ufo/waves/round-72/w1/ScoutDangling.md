cited_unregistered=3 ids=S303,S304,S352 resolver_last_line=ids_cited=121 ids_resolved=118 dangling=3 owned_elsewhere=3 unowned=0

# ScoutDangling — Read-Only Recount of Dangling-ID Defect at Base 3c68645a

## L0 Question Draft
kake | round-72 | For adopted entry corpus/knowledge/crux-bigquery-origin-membership.md citing dangling ids S303, S304, S352, which ruling applies: rewrite-by-document versus registration of staged ids, given the append-only guard and the id rule?

## 1. Citation and Registry Inventory at Base 3c68645a

- Base commit: `3c68645af27706d1d09b8dc7e27b0b0a9ffef6f1` (committed bytes inspected via `git show` / `git grep`).
- Knowledge files examined: 60 markdown files (`git ls-tree -r --name-only 3c68645a corpus/knowledge`).
- Citation pattern: regex `(?<![A-Za-z0-9_])S[0-9]{3,}(?![A-Za-z0-9_])` matching `S###` IDs.
- Total citation occurrences: 1292 citations across 60 knowledge files; 121 unique IDs cited.
- Registry rows in `corpus/SOURCES.md`: 176 rows matching `^ {0,3}\| *S[0-9]{3,} *\|` (176 unique IDs).
- Resolved IDs (`comm -12`): 118 IDs.
- Unregistered cited IDs (`comm -23`): 3 IDs (`S303`, `S304`, `S352`).

Citations for cited-but-unregistered IDs (file and line at base):
- `corpus/knowledge/crux-bigquery-origin-membership.md:11`: cites `S303` and `S304`
  `(staged S303/S304 rows) that this lane neither holds as registry rows nor re-ran this round. The`
- `corpus/knowledge/crux-bigquery-origin-membership.md:43`: cites `S352`
  `(staged id S352, fetched there 2026-10-24) and re-grounded in-round on 2026-11-03; the retained`

Artifacts in `.ufo/waves/round-72/w1/`:
- `citations-base.txt`: complete list of all 1292 citations with file and line.
- `registry-ids-base.txt`: complete list of all 176 registry IDs and source row line numbers.

## 2. id_resolver.py Execution and Output

Command:
```
python3 -B /home/vgpnk/Projects/shokunin/kake-shokunin/scripts/id_resolver.py \
  --root /home/vgpnk/Projects/shokunin/kake-shokunin \
  --revision 3c68645af27706d1d09b8dc7e27b0b0a9ffef6f1
```
Exit code: 1

Standard output / findings:
```
DANGLING S303 cited-by=corpus/knowledge/crux-bigquery-origin-membership.md owners=kotodama-shokunin,mado-shokunin,revenger-shokunin url-match=-
DANGLING S304 cited-by=corpus/knowledge/crux-bigquery-origin-membership.md owners=kotodama-shokunin,mado-shokunin,revenger-shokunin url-match=-
DANGLING S352 cited-by=corpus/knowledge/crux-bigquery-origin-membership.md owners=kama-shokunin,kotodama-shokunin,mado-shokunin,revenger-shokunin url-match=-
ids_cited=121 ids_resolved=118 dangling=3 owned_elsewhere=3 unowned=0
```

Final line:
`ids_cited=121 ids_resolved=118 dangling=3 owned_elsewhere=3 unowned=0`

## 3. Staged Rows in shokuknow and URL Match Check

Read-only check of `/home/vgpnk/Projects/shokuknow/merge/kake/SOURCES.append.md` (via `grep` only, exit 0):

1. `S303`:
   - Title / source (first 120 chars): `Chrome for Developers — CrUX Vis — https://developer.chrome.com/docs/crux/vis`
   - URL: `https://developer.chrome.com/docs/crux/vis`
   - Lane registry URL match (`git show 3c68645a:corpus/SOURCES.md | grep -F "https://developer.chrome.com/docs/crux/vis"`): NONE (exit 1, 0 matches).
2. `S304`:
   - Title / source (first 120 chars): `Chrome UX Report API — unregistered-caller probe (own-work) — https://chromeuxreport.googleapis.com/v1/records:queryReco`
   - Full title / source: `Chrome UX Report API — unregistered-caller probe (own-work) — https://chromeuxreport.googleapis.com/v1/records:queryRecord`
   - URL: `https://chromeuxreport.googleapis.com/v1/records:queryRecord`
   - Lane registry URL match (`git show 3c68645a:corpus/SOURCES.md | grep -F "https://chromeuxreport.googleapis.com/v1/records:queryRecord"`): NONE (exit 1, 0 matches).
3. `S352`:
   - Title / source (first 120 chars): `Chrome for Developers: CrUX on BigQuery — https://developer.chrome.com/docs/crux/bigquery`
   - URL: `https://developer.chrome.com/docs/crux/bigquery`
   - Lane registry URL match (`git show 3c68645a:corpus/SOURCES.md | grep -F "https://developer.chrome.com/docs/crux/bigquery"`): YES, row `S438` (exit 0, 1 match).
     Matching row:
     `| S438 | Chrome for Developers: CrUX on BigQuery — https://developer.chrome.com/docs/crux/bigquery | docs | A | Where origin membership in the CrUX dataset can be read without a CrUX API key — the dataset's own origin list, its table and its cost | § CrUX on BigQuery → Materialized table schema → origin_summary; doc prints Last updated 2026-10-13 UTC | the raw CrUX dataset is queryable on BigQuery, the monthly origin list is published as a table that is refreshed every month, and the dataset is free to explore within BigQuery's free tier — so eligibility can be answered with a project rather than an API key | mined | 2026-11-03 | 180d | corpus/knowledge/crux-bigquery-origin-membership.md |`

## 4. Verification of Single Citing Knowledge File

Positive search in `corpus/knowledge/**`:
- Command: `git -C /home/vgpnk/Projects/shokunin/kake-shokunin grep -n -E '\b(S303|S304|S352)\b' 3c68645af27706d1d09b8dc7e27b0b0a9ffef6f1 -- 'corpus/knowledge/**'`
- Exit code: 0
- Matches:
  - `corpus/knowledge/crux-bigquery-origin-membership.md:11`
  - `corpus/knowledge/crux-bigquery-origin-membership.md:43`

Negative search across all other 59 knowledge files:
- Command: `git -C /home/vgpnk/Projects/shokunin/kake-shokunin grep -n -E '\b(S303|S304|S352)\b' 3c68645af27706d1d09b8dc7e27b0b0a9ffef6f1 -- 'corpus/knowledge/**' ':!corpus/knowledge/crux-bigquery-origin-membership.md'`
- Exit code: 1 (0 matches).

Result: `corpus/knowledge/crux-bigquery-origin-membership.md` is verified as the sole knowledge file citing any of S303, S304, or S352.

## 5. Counterexample and Boundary Observations

- **URL registration vs ID token (S352 vs S438)**: S352's source URL (`https://developer.chrome.com/docs/crux/bigquery`) is present in the lane registry under ID `S438` and referenced on line 1 of `crux-bigquery-origin-membership.md`. `id_resolver.py` scans sibling registries for URL matches (`url-match=-`), but intra-lane resolution operates purely on token ID matching. Thus, S352 is flagged dangling even though its underlying source is registered and admitted in the lane.
- **Unregistered URLs (S303 and S304)**: In contrast, S303 and S304 have no registered URL anywhere in `corpus/SOURCES.md`. Both were explicitly rejected during round-70 assimilation (`ScoutAdoption.md`).
- **Citation boundary**: While S303, S304, and S352 are cited in other repository markdown files (such as `corpus/lessons/round-70.md`), `id_resolver.py` strictly restricts its citation checking to `corpus/knowledge/**/*.md`.

## 6. Conformance

- Lane read-only: no git/jj mutation in `/home/vgpnk/Projects/shokunin/kake-shokunin`.
- No tools installed or upgraded (pacman paused; none needed).
- Scratch directory `/fast/scratch/hyaku/kake-r72/ScoutDangling/` cleaned up before completion.
