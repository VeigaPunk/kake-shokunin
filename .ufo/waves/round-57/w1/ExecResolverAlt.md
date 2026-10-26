# ExecResolverAlt

Independent second implementation of the round-57 C2 resolver (differential oracle). Written only from the
CLI-contract docstring of `.ufo/waves/round-57/c57_idresolver_gate.py` and `contract.md`/`contract.json`;
no other seat's resolver was opened. Stdlib only; no `--selftest` (out of scope for this seat). No files
outside this report and `ExecResolverAlt.files/` were written; no git/jj mutation; no tool installs.

## SCRIPT PATH:

`/home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-57/w1/ExecResolverAlt.files/alt_resolver.py`

Usage: `python3 -B alt_resolver.py --root <lane> [--revision <rev>] [--fleet <fleet root>]`.
Reads cited ids with `(?<![A-Za-z0-9_])S\d{3,}(?![A-Za-z0-9_])` from every `corpus/knowledge/**/*.md`
(revision mode: `git ls-tree -r` + one `git cat-file --batch`; never the working tree), registry ids from
`corpus/SOURCES.md` under `## Registry` (rows with 0-3 leading spaces before `|`, first cell fullmatching
`S\d{3,}`), and sibling ownership from `<fleet>/*-shokunin/` other than the lane (`git show
HEAD:corpus/SOURCES.md` when `.git` exists, else the file).

## RUNS:

All runs: `--root /home/vgpnk/Projects/shokunin/kake-shokunin --fleet /home/vgpnk/Projects/shokunin`.

(a) Lane working tree at the base (no `--revision`), 2026-10-25:
```
ids_cited=104 ids_resolved=104 dangling=0 owned_elsewhere=0 unowned=0
```
exit 0. (Same totals as the base revision itself, below — the knowledge tree was still at base content.)

(b) `3994101dba28896830604fd0b08c7f00faca8ed6` (round-52 verifier commit):
```
DANGLING S367 cited-by=corpus/knowledge/yahoo-japan-rel-nofollow-semantics.md owners=kotodama-shokunin url-match=-
DANGLING S372 cited-by=corpus/knowledge/yahoo-japan-rel-nofollow-semantics.md owners=kotodama-shokunin url-match=-
DANGLING S373 cited-by=corpus/knowledge/baidu-friendly-crawl-guidance.md,corpus/knowledge/yahoo-japan-rel-nofollow-semantics.md owners=kotodama-shokunin url-match=-
DANGLING S390 cited-by=corpus/knowledge/baidu-friendly-crawl-guidance.md,corpus/knowledge/baidu-mobile-matching-error-causes.md owners=kotodama-shokunin url-match=-
DANGLING S409 cited-by=corpus/knowledge/baidu-friendly-crawl-guidance.md,corpus/knowledge/baidu-mobile-matching-error-causes.md owners=kotodama-shokunin url-match=-
ids_cited=99 ids_resolved=94 dangling=5 owned_elsewhere=5 unowned=0
```
exit 1. Exactly the five expected ids, each owned by kotodama-shokunin; no other id dangles; `url-match=-`
for all five (no citing file quotes kotodama's registry URL for those ids).

(c1) `fd91527a286086c1f4e6d4f44f715a907f041b5d` (round-53 repair):
```
ids_cited=99 ids_resolved=99 dangling=0 owned_elsewhere=0 unowned=0
```
exit 0.

(c2) `e48354b7c26bb6dc544ab6bbdc534fabe0daf7b6`:
```
ids_cited=102 ids_resolved=102 dangling=0 owned_elsewhere=0 unowned=0
```
exit 0.

(c3) `28fa0b23e699303725aba2727094531f5e44494d` (base):
```
ids_cited=104 ids_resolved=104 dangling=0 owned_elsewhere=0 unowned=0
```
exit 0.

Exit-code matrix (same script): missing `--root` → 64; unknown option → 64; `--help` → 0; unresolved
revision → 2 (`unevaluable: revision deadbeef unresolved`, no stdout); lane without `corpus/SOURCES.md`
→ 2; lane registry present but no knowledge file → 2.

Fixture parity (extra, run in `/tmp` via `c57_idresolver_gate.build_fixture()`, gate-owned fixture):
```
DANGLING S101 cited-by=corpus/knowledge/sub/bad.md owners=alpha-shokunin url-match=alpha-shokunin
DANGLING S200 cited-by=corpus/knowledge/sub/bad.md owners=alpha-shokunin,beta-shokunin url-match=-
DANGLING S0300 cited-by=corpus/knowledge/sub/bad.md owners=alpha-shokunin url-match=-
DANGLING S777 cited-by=corpus/knowledge/sub/bad.md owners=- url-match=-
ids_cited=6 ids_resolved=2 dangling=4 owned_elsewhere=3 unowned=1
```
exit 1; parsed output equals `EXPECT_FIXTURE` and `EXPECT_SUMMARY` exactly. Clean variant (bad.md removed):
`ids_cited=2 ids_resolved=2 dangling=0 owned_elsewhere=0 unowned=0`, exit 0.

## CONTRACT AMBIGUITIES:

Each was decided from the docstring text plus the gate's G3 expectations (which pin several of them); the
ones the fixture does not pin are marked `[UNPINNED]` and are the likely divergence points.

1. **Token inside a URL** — counted. The contract says "every token `S` + 3 or more digits (word-bounded)";
   no context filter is specified, so a match inside `https://…/S123` counts. No such token exists in the
   lane knowledge at any of the five revisions (checked by grep), so this is `[UNPINNED]` in practice.
2. **Range `S001-S007` / `S001–S006`** — both endpoints counted as separate ids (hyphen/en dash are not
   word characters). The lane knowledge uses such ranges (e.g. `publish-channels.md:2`, `static-canonical-
   preflight.md:54`); treating the range as one token would change `ids_cited`.
3. **Heading id `S1`** — not a match: fewer than 3 digits. Ids in headings with 3+ digits (`### … (S036)`)
   are ordinary citations and count.
4. **Fenced code block** — scanned, not skipped (no exclusion in the contract; 46 fence lines exist in
   `corpus/knowledge`). No S### token currently sits inside a fence, so `[UNPINNED]`.
5. **Distinct vs occurrences** — `ids_cited` counts distinct ids (pinned by the fixture: S001 appears twice
   in `good.md`, total is 6 not 7); `cited-by` lists each file once.
6. **`cited-by` order** — `[UNPINNED]`; chosen as lexicographic sort of root-relative POSIX paths, comma
   separated with no space.
7. **DANGLING line order** — `[UNPINNED]`; chosen as ascending numeric id (`int(id[1:])`, then string), so
   S0300 < S367. The gate parses into a dict, so order is invisible to G3/G4/G5.
8. **`url-match` semantics** — the docstring names the column but not its rule. Decided from the fixture:
   a lane appears when it **owns** the id and at least one of that lane's registry source URLs for the id
   is a verbatim substring of the citing file(s)' text (whole file, not a window around the citation). A
   non-owner lane whose URL happens to appear is not listed (`[UNPINNED]` — untested by the fixture).
9. **Which URLs a sibling "has" for an id** — `[UNPINNED]`; taken as every `https?://…` occurrence in the
   row's source (second) cell, trailing `.,;:"'` trimmed; duplicate registry rows for one id merge their
   URL lists.
10. **Registry section boundary** — rows are collected from `## Registry` until the next level-2 heading;
    `###` subsections do not close it. Rows with 4+ leading spaces are skipped (indented code).
11. **Registry cell strictness** — `[UNPINNED]`; the first cell must fullmatch `S\d{3,}` after stripping
    whitespace (no backticks/links/bold unwrapping). A decorated cell therefore does not resolve.
12. **Sibling with no readable registry** — skipped (contributes no ownership), not unevaluable. Sibling
    repos are read at live HEAD even when `--revision` is given (contract says so explicitly).
13. **Unevaluable set** — the parenthetical lists three causes; treated as non-exhaustive: an unreadable
    `--fleet` root and a `git` failure while reading the revision also exit 2 (`[UNPINNED]`).
14. **`--root` requiredness** — the CLI block brackets `--revision`/`--fleet` but not `--root`, so `--root`
    is required; omitting it is usage (64). The gate always supplies it, so this cannot diverge in G3-G5.
15. **`--selftest`** — deliberately absent here (assignment scope). Invoking it yields 64; a differential
    harness must exclude it from comparison.

## ORACLE USE:

Procedure for the seat that diffs the two implementations (primary `scripts/id_resolver.py` in a clean
clone of the measured revision vs this file, both run with `python3 -B` and a minimal env):

1. Same five targets, same order: working tree (no `--revision`), then `3994101`, `fd91527`, `e48354b7`,
   `28fa0b2`, all with `--root <lane> --fleet /home/vgpnk/Projects/shokunin`.
2. Compare **stdout bytes and exit code** per target (`diff <(A) <(B)`; compare `$?` separately). Do not
   normalize away whitespace — the summary line's spacing is part of the contract.
3. Canonicalize only if both sides emit the same line set in a different order: sort `DANGLING` lines and
   compare as sets, and record that a reorder divergence occurred (my order is numeric-ascending, see
   ambiguity 7). Totals must match exactly as `ids_cited/ids_resolved/dangling/owned_elsewhere/unowned`.
4. Expected anchors: `3994101` must produce exactly S367 S372 S373 S390 S409 with owner
   `kotodama-shokunin` and `dangling=5` exit 1; `fd91527` and both later revisions must produce
   `dangling=0` exit 0 with `ids_cited` 99 / 102 / 104 respectively (working tree currently 104).
5. Third, independent check both sides against the gate's own G3 fixture: import
   `c57_idresolver_gate.build_fixture()` in a throwaway dir and require both tools to reproduce
   `EXPECT_FIXTURE`/`EXPECT_SUMMARY` (this alt does, exactly). This catches a primary tool that hardcodes
   the real-fleet answer.
6. A stdout diff is a finding, not a verdict: adjudicate by the docstring + fixture and list the
   ambiguities above that the diff touches. Divergences are expected only on the `[UNPINNED]` items
   (ordering, url-match for non-owners, decorated registry cells, missing fleet root) or on `--selftest`
   (excluded). Any divergence on the four pinned runs is a real defect in one of the two.
7. My run does not replace a `--selftest` N>=16 (G2): it certifies the resolver's observable behavior, not
   the primary tool's own selftest count.

VERDICT: Independent alt resolver matches the contract on all five assigned runs (3994101 → the exact five ids, owner kotodama-shokunin, exit 1; all later revisions and the working tree → dangling=0, exit 0) and reproduces the gate's G3 fixture exactly.
