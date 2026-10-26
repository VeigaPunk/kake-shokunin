# MutIdResolver
Round-57 W2 mutation battery over `scripts/id_resolver.py` (read at `git show 4b8c73050470ada9e6583f3b12d659d1bed6a17f:scripts/id_resolver.py`, sha256 `2bee5a8fa08efb43…`; worktree file byte-identical before and after — confirmed by running). Detector: mutant's `--selftest` run directly, plus `.ufo/waves/round-57/c57_idresolver_gate.py --root <mutant clone> --revision <mutant commit> --fleet /home/vgpnk/Projects/shokunin`. Baseline (both, pristine, confirmed by running): selftest `selftest: 33/33` exit 0; gate 5/5, G1–G5 PASS, exit 0. Each mutant: single anchor replacement (count asserted = 1), committed as `scripts/id_resolver.py` on a mktemp clone of the lane (`user.name=selftest`), scratch dir removed in `finally`. 31 mutants run, all confirmed by running. Gate note: every killed run had gate rc=1 with G2 the first failing condition; G3–G5 were not separately probed for selftest-killed mutants (G2 failing is itself a kill: `run_selftest` exit ≠ 0 or last line rejected).

## MUTANTS:
| ID | Single-point mutation | Selftest | Gate | Verdict |
|---|---|---|---|---|
| M01 | ID_RE drop lookahead `(?![A-Za-z0-9_])` | 31/33 (decoy S500x) | rc1, G2 | killed by selftest |
| M02 | ID_RE drop lookbehind `(?<![A-Za-z0-9_])` | 31/33 (decoy AS500) | rc1, G2 | killed by selftest |
| M03 | ID_RE `\d{3,}`→`\d{2,}` | 31/33 (decoy S12) | rc1, G2 | killed by selftest |
| M04 | ID_RE `\d{3,}`→`\d{4,}` | 10/33 (all indent/4-digit cases) | rc1, G2 | killed by selftest |
| M05 | ID_RE `_` dropped from both lookaround classes | 33/33 | rc0 | SURVIVED both |
| M06 | ROW_RE ` {0,3}`→` {0,4}` (4-space rows become rows) | 32/33 (4-spaces-is-code) | rc1, G2 | killed by selftest |
| M07 | ROW_RE ` {0,3}`→` {0,2}` (3-space rows ignored) | 31/33 (indent-3, S200 owners) | rc1, G2 | killed by selftest |
| M08 | drop `sid = m.group(1).strip()` | 33/33 | rc0 | SURVIVED both (equivalent, see below) |
| M09 | ID_CELL_RE drop `$` anchor (`^S\d{3,}$`→`^S\d{3,}`) | 33/33 | rc0 | SURVIVED both |
| M10 | SECTION_END_RE `^#{1,2}\s`→`^#\s` (h2 no longer ends section) | 32/33 (section-end case) | rc1, G2 | killed by selftest |
| M11 | REGISTRY_HEADING_RE drop trailing `\s*$` | 33/33 | rc0 | SURVIVED both |
| M12 | drop `line = raw.rstrip("\r")` | 33/33 | rc0 | SURVIVED both (equivalent, see below) |
| M13 | `parse_registry` `splitlines()`→`split("\n")` | 33/33 | rc0 | SURVIVED both |
| M14 | sibling suffix `"-shokunin"`→`"shokunin"` | 33/33 | rc0 | SURVIVED both |
| M15 | drop lane exclusion `realpath(path)==lane_real` | 32/33 (realpath case) | rc1, G2 | killed by selftest |
| M16 | sibling git test rc==0→rc==1 (file even for git repos) | 33/33 | rc0 | SURVIVED both |
| M17 | `lane_registry` ignores `--revision`, reads worktree file | 31/33 (revision-reads-old-blobs) | rc1, G2 | killed by selftest |
| M18 | `knowledge_bodies` ignores `--revision`, walks worktree | 32/33 (revision-reads-old-blobs) | rc1, G2 | killed by selftest |
| M19 | revision-branch `ls-tree` filter drops `.endswith(".md")` | 33/33 | rc0 | SURVIVED both |
| M20 | owners `sorted(...)`→`sorted(..., reverse=True)` | 29/33 (owners order) | rc1, G2 | killed by selftest |
| M21 | url-match: `matched = owners` (URL check removed) | 30/33 (url-match-absent) | rc1, G2 | killed by selftest |
| M22 | url-match scans first citing file only (`paths[:1]`) | 33/33 | rc0 | SURVIVED both |
| M23 | drop `u.rstrip(".,;:")` on registry URLs | 33/33 | rc0 | SURVIVED both |
| M24 | `owned_elsewhere` counts `row[3]` (url-match) not `row[2]` | 31/33 (two-siblings summary) | rc1, G2 | killed by selftest |
| M25 | `unowned` = `len(rows)` (not `len(rows)-owned`) | 31/33 (id-held-by-none) | rc1, G2 | killed by selftest |
| M26 | exit invert: `Result(0 if dangling else 1)` | 20/33 (all clean/dangling status cases) | rc1, G2 | killed by selftest |
| M27 | `_err` status 2→1 (unevaluable) | 30/33 (all exit-2 cases) | rc1, G2 | killed by selftest |
| M28 | usage exit 64→2 | 32/33 (usage-error case) | rc1, G2 | killed by selftest |
| M29 | selftest last line `selftest:`→`selftest ` (no colon) | 33/33 ok, line `selftest 33/33` | rc1, **G2 FAIL** | killed by gate G2 only |
| M30 | dangling ids `sorted(...)`→`reverse=True` (line order) | 33/33 | rc0 | SURVIVED both |
| M31 | drop `sibling_registry` final `return {}` (None for registry-less sibling) | 32/33 (TypeError in sibling-without-registry) | rc1, G2 | killed by selftest |

Score: 31 run — 19 killed by selftest (gate G2 corroborates), 1 killed by gate only (M29/G2 — the `--selftest` last-line format is checked by no selftest case, exactly the contract clause the gate owns), 11 survived both (35%).

## SURVIVORS:
All confirmed by running (selftest 33/33, gate 5/5 exit 0 on each).
- **M05 underscore lookaround** — no fixture places `_` adjacent to an id (`S777_`/`_S777`); `S_777` in the gate decoy list never exercises the class (S is followed by `_`, not a digit, so the quantizer rejects it regardless).
- **M08 cell-strip drop** — EQUIVALENT, no fixture can kill it: ROW_RE's `\s*([^|]*?)\s*\|` already backstops leading/trailing whitespace out of the captured cell (Python `\s` ≡ `str.strip()` set), so `.strip()` is dead defensive code. Coverage finding, not a contract change; recommend deleting it or leaving with a comment.
- **M09 ID_CELL_RE `$`** — registry cells like `S777x` are never tested; `match` with a dropped `$` registers `S777` from a malformed cell.
- **M11 heading `\s*$`** — no fixture has trailing text on the `## Registry` heading (`## Registry (legacy)`).
- **M12 `rstrip("\r")`** — EQUIVALENT, no fixture can kill it: `str.splitlines()` already consumes `\r` (lone or in `\r\n`) as a boundary, so no split line can retain a trailing `\r`. Dead code; the CRLF guarantee actually lives in `splitlines()`.
- **M13 `split("\n")` for CRLF** — every fixture's CRLF rows end in `| — |\r` where URL_RE's `\s`/`|` exclusions already stop before the `\r`, and heading regexes absorb `\r` via `\s*$`; only lone-`\r` (classic-Mac) endings distinguish the two.
- **M14 `-shokunin` suffix** — no fixture creates a sibling matching `"shokunin"` but not `"-shokunin"` (`shokunin`, `fooshokunin`); the mutant discovers extra siblings.
- **M16 sibling HEAD vs file** — killed only by a dirty sibling: no selftest case and no gate fixture commit a sibling repo whose HEAD registry differs from its working-tree file. (G4 passes because the real fleet siblings' files match HEAD today — timing-fragile, not structural.)
- **M19 revision-branch `.md` filter** — the gate's G3 runs tools without `--revision`, exercising only the working-tree branch's separate `.md` filter; the `ls-tree` branch filter is covered by no fixture, and the real corpus has no non-`.md` file under `corpus/knowledge/` at either probed revision.
- **M22 url-match first-file-only** — no fixture quotes an owner URL only in a citing file that is not first in sorted order.
- **M23 URL punctuation rstrip** — every fixture row places the URL mid-cell before ` |`, so `.,;:` trimming never fires; no fixture ends a source cell with the URL followed by punctuation.
- **M30 DANGLING line order** — the gate compares `sorted(tool_lines)` (order-insensitive) and no selftest case asserts multi-id `render()` order, so reversed output order is invisible to both detectors.

## PROPOSED FIXTURES:
Selftest `@fixture`-style cases (names per `_cases()` style) that kill the 9 killable survivors:
- `decoy S777_ (trailing underscore) is not an id` — body `"Not an id: S777_.\n"`; also `decoy _S777 is not an id`. Kills M05.
- `registry cell S777x is not a registry id` — lane registry row `| S777x | https://e.example/7 | … |`, knowledge cites `S777`; expect dangling/unowned (summary `(1,0,1,0,1)`). Kills M09 (M08 in table).
- `registry heading with trailing text is not the Registry section` — heading `## Registry (legacy)` over valid rows; id must stay dangling. Kills M11 (M10 in table).
- `lone-CR registry rows` — `_registry(..., eol="\r")` variant; rows must still resolve. Kills M13 (M12 in table).
- `sibling without a dash suffix is not a sibling` — `siblings={"shokunin": [("S777", …)]}` (or `fooshokunin`); expect owners `[]`. Kills M14 (M13 in table).
- `sibling read at HEAD not the dirty worktree` — `_repo` sibling committed with the id in `corpus/SOURCES.md`, then file rewritten without it (uncommitted); owner must still be found. Kills M16 (M15 in table).
- `non-markdown knowledge file at a revision is ignored` — `case_revision_reads_old_blobs`-style repo fixture plus committed `corpus/knowledge/notes.json` containing an id, queried via `--revision`; expect it uncited. Kills M19 (M18 in table).
- `url-match scans every citing file` — two files `a.md` (no URL) and `b.md` (quotes owner URL); expect `url-match` to name the owner. Kills M22 (M21 in table).
- `url-match ignores punctuation after a registry URL` — registry source cell ends `… https://a.example/101. | …` while the body quotes the bare URL; expect match. Kills M23 (M22 in table).
- `dangling lines render in id order` — two dangling ids (e.g. S101 before S200); assert `render()` line order, not just set equality. Kills M30 (M29 in table).
No fixture is proposed for M08/M12-equivalents (table M08, M12): they are equivalent mutants — the honest fix is deleting the dead `.strip()` / `rstrip("\r")`, not new tests.

## Restoration:
No file outside my own report was written; no git/jj state of the lane, siblings, or fleet was mutated (scratch work only: mktemp clones + tempdir fixtures). Evidence (confirmed by running): lane `scripts/id_resolver.py` sha256 `2bee5a8fa08efb432d946465f361db169e6572a9cfe5697f6de3ffd6f3bdfba5` before and after — equal to the revision blob; scratch clone `/tmp/mutid_base` same hash before/after the battery (`unchanged=True` from the driver); all 32 mutant scratch dirs removed (`/tmp/mutid-*` count 0 after run); remaining lab artifacts (`/tmp/mutid_base`, driver, result JSON, baseline captures) deleted after this report. No tools were installed or upgraded; no pacman was run.

VERDICT: 31 single-point mutants — 20 killed (19 by selftest, M29 by gate G2 only), 11 survived both (9 killable by proposed fixtures, 2 equivalent dead-code mutants); baseline 33/33 + gate 5/5; original bytes untouched.
