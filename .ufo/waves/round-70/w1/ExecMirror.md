# ExecMirror — round 70 W1 (kake lane, attempt 1)

Base for every measurement: `e5f6fd9e4c243d092160bc74e8bea24256087173`. Append machinery built
and attacked; **nothing was appended to the lane**; no tracked file, no git/jj mutation, no
shokuknow write. Scratch `/fast/scratch/hyaku/kake-r70/ExecMirror` removed before yield.

## Delivered (all new, under `.ufo/waves/round-70/w1/ExecMirror/`)

- `guard.sh` (executable, sha256 `f9dde457…347a`) — `<registry.md> <staged-rows.md> <outdir>`;
  ids via `grep -oE '^ {0,3}\|[[:space:]]*S[0-9]{3,}' | grep -oE 'S[0-9]+' | sort` for both,
  `comm -12` → collisions; prints `registry-ids=N staged-ids=M collisions=K`; exit 0 clean,
  1 collision, 2 usage.
- `reg-ids` (175), `staged-ids` (129), `collisions` (8) from the real base-vs-staged run.
- `normalized-row.md` (sha256 `72d755b3…b845`), `staged-S352-row.txt` (`4d0ff087…082c`),
  `prose-recheck-row.md` (`1c261c89…1e74`).
- `measure.txt` — every command, output and exit code; six retained census logs
  (`gate-*.log`); fixture logs.

## Attacks and verdicts (all run)

| # | Attack | Verdict |
|---|---|---|
| A1 | Guard able-to-fail: fixture git repo from base `SOURCES.md`, real `S433` row prefixed by two leading spaces + staged row with that id | **PASS** — `collisions=1` (`S433`), exit 1; toplevel asserted `= $D` before first commit |
| A2 | Guard negative control: same registry, staged `S999` (absent) | **PASS** — `collisions=0`, exit 0 (discriminates) |
| A3 | Real collision run: base registry vs `shokuknow/merge/kake/SOURCES.append.md` | 8 collisions: `S312 S329 S367 S372 S373 S374 S390 S409`; exit 1. **Staged `S352` does NOT collide** (`reg-ids` 0, `collisions` 0) — see Finding 1 |
| A4 | Next-unused-id scan past reg-ids+staged-ids from lane max `S437` | `S438` (explicit loop, not arithmetic; absent from both lists) |
| A5 | Raw staged S352 row verbatim into a base mirror | **FAILS as required** — `E01 S352 fields=12` (NF=14 due to escaped pipe) + `E11` shifted used-by; exit 1 |
| A6 | Second fixture row, prose recheck `2026-10-23 — re-verify …` (13 fields, no pipes) | **FAILS as required** — `E09 S439 recheck=2026-10-23 — re-verify …`; exit 1 |
| A7 | Normalized row (`S438`, `180d`, `2026-11-03`) in the same mirror | **PASS** — 16 baseline W04 only, `file ok`, exit 0 |
| A8 | Unmodified base copy through the same gate | **PASS** — 16 W04, exit 0 |
| A9 | Corpus-only extraction (`git archive … corpus`) then validate | exit 1, 17 × `E11` on pre-existing rows — mirror root lacks `scripts/`, `SCORECARD.md`, `.ufo/`, `SKILL.md` (all present at base). Gate re-run on a full base-revision mirror; recorded as the path-resolution limit of `--file` |

## Normalization result

Staged row → normalized row: `S352→S438`, `opened 2026-10-24→2026-11-03`, recheck
`180d — \`curl … \| grep …\` -> 1 (ran 2026-10-24)` → `180d`, used-by unchanged
`corpus/knowledge/crux-bigquery-origin-membership.md`. Normalized row: NF=13, exactly 12
structural pipes, zero backslashes, zero escaped pipes, `status mined`, all other cells
byte-identical to the staged row.

## Findings

1. **Contract §10 premise falsified by measurement.** The frozen contract states "staged id S352
   collides with the lane registry's S352". At `e5f6fd9e` the lane registry is 175 rows,
   `S001`–`S437` with holes (`S140`–`S249`, …) and `S352` appears **nowhere** in `SOURCES.md`
   (`grep -n 'S352'` → none) nor in its history (`git log -S'| S352 |'` → 0 commits). The 8
   measured collisions are all other ids. The adopted id is still `S438` because the contract's
   next-unused rule governs, but the collision half of the renumber rationale does not hold and
   must not be reported as proven.
2. **Whole-file guard exit 1.** Run over the full staged file the guard refuses (8 unrelated
   collisions). Only the single-row adoption path is collision-free; the guard must be run per
   adopted row, or the 8 ids resolved first.
3. **Gate copy is not adoption text.** The mirror's entry is the verbatim staged file
   (`source: S352`, `verified-at: 2026-10-24`, prose recheck); it exists only for the E11 path
   check. Contract C2(a) requires the tip entry to name `S438`, `verified-at: 2026-11-03` and
   `recheck: 180d`.

## Risks / blockers

- No blocker for the append machinery: guard proven able to fail, normalized row passes the
  real census gate (exit 0, warnings only), base copy clean.
- Risk carried to L1: the contract's S352-collision sentence and the report's renumber map must
  be amended to state S352 was unused at base; adopting `S438` remains correct.
- Tooling: none installed or upgraded (pacman untouched).

## Exact retained evidence

`measure.txt` (full transcript), `gate-full-base.log`, `gate-full-normalized.log`,
`gate-raw-staged-row.log`, `gate-prose-recheck-row.log`, `gate-corpus-only-*.log`,
`fixture-positive.log`, `fixture-negative.log`, `fixture-collisions.txt`, plus the three row
files and `reg-ids`/`staged-ids`/`collisions`.
