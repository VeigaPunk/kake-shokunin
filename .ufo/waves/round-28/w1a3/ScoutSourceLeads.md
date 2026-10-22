# Scout — C2 registry hygiene (S036–S039, census, W04)

Seat: KakeR28a3.ScoutSourceLeads (leaf, freshness). Lane: /home/vgpnk/Projects/shokunin/kake-shokunin.
Read-only: no network, no installs, no tracked-file mutation; the only lane write is this report.
Sandbox: /fast/scratch/hyaku/kake-r28a3/w1/ScoutSourceLeads (clone + TMPDIR there).

## State timeline (the registry changed three times while I checked)

1. 35 rows S001–S035, `corpus/SOURCES.md` sha256 `3dafedf7b7a5d1ffaf9bef1526bd035ce643a1f77eb7322c394752a01822147b`.
2. L1 working-tree edit, 39 rows, sha256 `7d979a82d7e08c31adf5218f51e7b7306c3736dfbcb5bc73dfd867c12ae587dd` (uncommitted at the time).
3. L1 commit `e57f601bd0148bb7dce9052f0cade3fd11751375`; committed file sha256 `0470b804aa92f00db3ea642f92b3fc08856606b562929536a2ca9e2f3986ecf4`, 115 lines, tracked tree clean. Rows S036–S039 sit at lines 44–47, inside `## Registry` (line 5), before `## Paths` (line 49).

## Duplicate check — none of the four URLs was a row, rejected row, or lead

Pre-addition (state 1): `grep -n -E 'S03[6-9]' corpus/SOURCES.md` → no match, exit 1 (no row, no rejected row, no id reuse). `grep -n -E 'web\.dev/articles/vitals|defining-core-web-vitals-thresholds|docs/crux/(methodology|api)' corpus/SOURCES.md` → no match, exit 1 (not a row, not a rejected row, not a lead). Nearest neighbours are not matches: S018 is DebugBear (debugbear.com, tier C, rejected); the leads `web.dev: Optimize INP`, `W3C Event Timing`, `Chromium speed metrics changelog` are different pages.

Post-addition (state 3, committed): S036, S037, S038, S039 each occur once on a row-shaped line; each declared URL occurs exactly once in the file; all four rows are inside `## Registry`. Fleet-wide `grep -l` over `/home/vgpnk/Projects/shokunin/*-shokunin/corpus/SOURCES.md` matches only kake-shokunin, so no cross-lane `shared` report comes from these rows.

## Next-unused ids — confirmed at 35 rows

Extracting `| S(\d{3}) ` gave n=35, min=1, max=35, contiguous=True, duplicates=False — exactly S001…S035, so S036–S039 were the next unused ids, ascending, no reuse. Ids are per-lane: 13 sibling lane registries already carry S036–S039 for their own rows; validate and the C2 counter are per-file, and `shared` compares URLs, not ids.

## Census run — command, output, exit code

`cd /home/vgpnk/Projects/shokunin && bash scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin kake`

Run on all three states; identical output each time, exit 0:

```
kake	W04	S033 duplicate url www.rfc-editor.org/rfc/rfc9110.txt across scopes
kake	ok	/home/vgpnk/Projects/shokunin/kake-shokunin/corpus/SOURCES.md
```

`EXIT=0` every run (committed state: `VALIDATE_EXIT=0`). The four new rows introduce no E-code and no W-code. `ok` is printed only when the lane has no E-code, so `ok` + exit 0 is the clean verdict; W04 is pre-existing and unrelated to round 28.

## W04 for S033 — what it means

S028 and S033 both cite `https://www.rfc-editor.org/rfc/rfc9110.txt` under different scopes (empty-host validity of http(s) URIs; media-type grammar). The parser normalizes the URL (drop fragment, drop one trailing slash, drop scheme, lowercase host, keep path case) and names the later row, S033. W-codes never change exit status. S010 is `rfc9110.html#section-8.8`, whose fragment is stripped and whose path differs, so it is not in the collision. Distinct scopes are already the correct resolution; no action needed.

## How the census parses a registry row (add rows without breaking it)

Source: `/home/vgpnk/Projects/shokunin/scripts/sources-census.sh` (read-only), `row_pass`.

- Scope: counted only between a level-2 heading whose trimmed text is exactly `Registry` (0–3 leading spaces) and the next `## ` or top-level `# ` heading. 4+ leading spaces are code, ignored. Append at the end of the table, before `## Paths`.
- Shape: line must start and end with `|`; split on `|` must give NF=13 (11 cells); E01 prints `NF-2`. No `|` inside any cell; one physical line per row.
- Cells: id, source, kind, tier, scope, anchor, teaches, status, opened, recheck, used-by.
- id `^S[0-9]{3,}$`, unique (E02/E03). kind enum spec|docs|paper|code|tool|dataset|talk|book|community|own-work (E05). tier A|B|C (E06). status queued|mined|rejected (E07; `watch` is invalid).
- opened: real ISO calendar date, not later than today UTC (E08). recheck: ISO date, `^[0-9]+d$`, or symbolic `^[A-Za-z][A-Za-z0-9 _-]*$`; `90d`, `on-release`, `6 months` pass, `2027-01` gives E09.
- URL: first `https?://[^\s|]+` in the source cell; fragment and one trailing `/` stripped, scheme stripped, host lowercased. Same URL + same scope → E04 unless teaches contains `supersedes S###`; same URL + new scope → W04 on the later row.
- tier A + community → E10; W01 tier-C mined with real used-by; W02 rejected with teaches under 8 characters; W03 mined with used-by `—`.
- E11 (separate pass, mined rows only): every comma-separated used-by path must exist relative to the lane root; `—` and empty are skipped. Both targets exist now: `corpus/knowledge/field-performance-cwv.md`, `corpus/lessons/round-28.md`.
- E12: any row-shaped line (`^| S###|`) outside `## Registry` is an error — never paste a row into Paths, Search log or Leads.
- Exit: 1 on any E-code, 0 with W-codes only, 2 on missing registry or usage error.

Self-check: `bash /home/vgpnk/Projects/shokunin/scripts/sources-census.sh selftest` (TMPDIR in scratch) → 96 checks `killed`, 0 survived, `selftest ok`, exit 0.

## The C2 counter is a second, independent parser

`.ufo/waves/round-28/c2_source_count.py` ignores section boundaries: it scans every line, does `line.strip().strip("|").split("|")`, requires exactly 11 cells with `cells[0] == id`, and takes the first match. It then demands exact cells: `cells[3] == "A"`, `cells[7] == "mined"`, `cells[8] == "2026-10-22"`, `cells[10]` containing `corpus/knowledge/field-performance-cwv.md`; the URL in `cells[1]` must match `re.escape(url) + r"(?![\w/-])"` — no trailing `/`, `-` or word character right after it (` —` or ` |` is fine). Keep exactly one row per id.

It also needs entry lines 1–3 to start `source:`, `verified-at: 2026-10-22`, `recheck:`; each id as a whole-word token in the entry; and one `## Gate` line per id in `corpus/lessons/round-28.md` carrying the id, the URL, `accessed 2026-10-22`, and exactly one curly-quoted excerpt of 1–25 words.

## Evidence at the committed head

- `python3 -B .ufo/waves/round-28/c2_source_count.py --root . --revision HEAD` → `passed 4 / 4`, `COUNTER_EXIT=0` (all three files committed at `e57f601b`).
- Census validate on the committed tree → exit 0, W04 line only (above).
- An earlier sandbox dry-run on a copy of the uncommitted tree (clone commit `4f8dee2`) also scored 4/4; superseded by the real commit.

## Commands and exit codes

1. `bash scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin kake` → 0 (three states).
2. `bash /home/vgpnk/Projects/shokunin/scripts/sources-census.sh selftest` (TMPDIR in scratch) → 0.
3. `grep -n -E 'S03[6-9]' corpus/SOURCES.md` (state 1) → 1, no match.
4. `grep -n -E 'web\.dev/articles/vitals|defining-core-web-vitals-thresholds|docs/crux/(methodology|api)' corpus/SOURCES.md` (state 1) → 1, no match.
5. `grep -l -E 'web\.dev/articles/vitals|defining-core-web-vitals-thresholds|docs/crux/(methodology|api)' /home/vgpnk/Projects/shokunin/*-shokunin/corpus/SOURCES.md` → only kake-shokunin.
6. `python3 -B .ufo/waves/round-28/c2_source_count.py --root . --revision HEAD` → 0, 4/4.
7. `git show HEAD:corpus/SOURCES.md | sha256sum` → `0470b804…`, equal to the working-tree hash.

## Not verified

- No URL was fetched (not my seat); row scopes/teaches and the entry's quotes were not checked against the pages — only registry shape and the two parsers' contracts.
- Post-addition snapshots may go stale if the registry is edited again; the head I checked is `e57f601b`.
- The counter's 4/4 proves contract shape at that commit, not claim truth; judgement stays with the non-author closure.
