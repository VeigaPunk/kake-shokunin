# ExecIdGuard

Replication of the round-56 assimilation id-collision guard and the kake quarantine slice, rebuilt from scratch in a
private scratch repo (`mktemp -d` → `/tmp/tmp.g1BbNBe0B1`, `git init -q`, `rev-parse --show-toplevel` == that path).
Evidence files: `.ufo/waves/round-56/w1/ExecIdGuard.files/` (fixtures, guard outputs, `commands.txt`).
Lane state untouched: no writes outside this report and its `.files/`, no git/jj mutation.

## COMMANDS:

Registry ids (lane, read-only):
```
grep -oE '^ {0,3}\|[[:space:]]*S[0-9]{3,}' corpus/SOURCES.md | grep -oE 'S[0-9]+' | sort
```
Staged ids (shokuknow, read-only):
```
grep -oE '^ {0,3}\|[[:space:]]*S[0-9]{3,}' /home/vgpnk/Projects/shokuknow/merge/kake/SOURCES.append.md \
  | grep -oE 'S[0-9]+' | sort
```
Collisions:
```
comm -12 <reg-ids> <staged-ids>
```
Quarantine slice:
```
awk -F'|' -v l='kake' '$2 ~ ("`" l "`") && $3 ~ /round[0-9]+/ && $4 ~ /S[0-9]+/ {print $4, $5}' \
  /home/vgpnk/Projects/shokuknow/.ufo/waves/corpus-expansion-1/absent-defect-register.md
```
Byte comparison: `cmp -s` + `sha256sum` per artifact. Full transcript: `ExecIdGuard.files/commands.txt`.

## COMPARISON:

| artifact | reproduced | bytes | lines | sha256 (reproduced) | vs `.ufo/waves/round-56/assimilation/` |
|---|---|---|---|---|---|
| `reg-ids` | 156 | 780 | 156 | `7f458d3d…acc90dd` | byte-identical (`cmp -s` rc 0) |
| `staged-ids` | 129 | 645 | 129 | `3938ec94…3828f9deb` | byte-identical |
| `collisions` | 8 | 40 | 8 | `a443d89d…def8ea9a0` | byte-identical |
| `quarantine-slice` | 12 | 453 | 12 | `6d92f440…c15d2d63a` | byte-identical |

Counts and bytes match exactly on all four artifacts; no id repeats inside either set (156 rows → 156 ids, 129 rows →
129 ids), so dedupe is not masking anything.
Set arithmetic: 148 registry ids absent from staged; 121 staged ids absent from registry. Staged range S287–S415.
Collision ids: S312 S329 S367 S372 S373 S374 S390 S409.

Source pins: `corpus/SOURCES.md` = sha256 `cc402e4b…5e6c50e`, 145418 bytes — equals `mirror-pin.json` and the
`pre-append/corpus/SOURCES.md` copy (both pin fields verified True), so the registry read here is the pinned pre-append
registry, not a build-edited one. Append source sha256 `5f0cd4c4…2e9f0cc`.

Quarantine derivation fidelity: the register holds 13 lines whose lane cell is `` `kake` ``. Twelve satisfy the
`round[0-9]+` + `S[0-9]+` condition; the excluded line is `| `kake` | 9 |` (register line 242), a per-lane count row,
not a row of either defect table. Nine slice rows come from the `payload-absent` table (S142 S143 S148 S156 S161 S193
S194 S195 S206); three (S154 S178 S184) come from the second table (`| lane | round | id | why it was not checked |
cited source |`, header line 265), whose class cell is the sentence "the cited source could not be fetched, so no quote
was checked". Observed register defect, not corrected here: in that second table the id cell carries a stray trailing
backtick (`S154\``, `S178\``, `S184\``), which is why the derived slice shows `S154\`` etc. None of the 12 slice ids
occurs in the lane registry (0 occurrences each) and none intersects the collision set.

## GUARD PROOF:

Fixture `ExecIdGuard.files/fixture-indented-registry.md`:
```
| id | source |
|---|---|
  | S287 | x |
```
- 0–3-space pattern `^ {0,3}\|[[:space:]]*S[0-9]{3,}` → reports `S287` (`guard-0to3.out`, 1 line; raw `grep -c` = 1, rc 0).
- Column-zero-only pattern `^\|[[:space:]]*S[0-9]{3,}` → reports nothing (`guard-col0.out`, 0 bytes; raw `grep -c` = 0, rc 1).

End-to-end: scratch registry = `corpus/SOURCES.md` + the staged S287 row re-indented to two spaces, then the full
`reg-ids` → `comm -12` pipeline against the staged set.
- 0–3-space guard: 157 ids, 9 collisions `S287 S312 S329 S367 S372 S373 S374 S390 S409`
  (`scratch-collisions-0to3.out`).
- Column-zero-only guard: 156 ids, 8 collisions — S287 silently missing (`scratch-collisions-col0.out`).

Bound (why the pattern is 0–3 and not 0–∞): a 4-space-indented `    | S287 | x |` fixture
(`fixture-4space-registry.md`) is reported by neither the 0–3 pattern (`guard-0to3-on-4space.out`, empty) nor the
column-zero-only pattern, while an unbounded `^ *\|…` variant does report it (`guard-unbounded-on-4space.out`). The
guard is therefore exact for the 0–3 indentation contract and blind beyond it.
Today both live inputs are flush-left: 0 indented S-rows and 156 column-zero rows in `corpus/SOURCES.md`; 0 indented
rows in `SOURCES.append.md`.

## SAME-DOCUMENT TABLE:

Compared cell 3 (source) of each colliding row in both files; all eight source cells are byte-equal, so every collision
is the SAME document re-listed, not a different source reusing an id.

| id | primary URL (identical in both) | same document? | row fields that differ |
|---|---|---|---|
| S312 | https://ziyuan.baidu.com/college/courseinfo?id=267&page=15 | YES | scope, anchor, teaches, opened, recheck, used-by |
| S329 | https://ziyuan.baidu.com/college/courseinfo?id=1399 | YES | scope, anchor, teaches, opened, recheck, used-by |
| S367 | https://info-search.yahoo.co.jp/archives/002852.php | YES | scope, anchor, teaches, opened, recheck, used-by |
| S372 | https://info-search.yahoo.co.jp/archives/002849.php | YES | scope, anchor, teaches, opened, recheck, used-by |
| S373 | https://info-search.yahoo.co.jp/archives/002850.php | YES | anchor, opened, recheck, used-by (scope/teaches equal) |
| S374 | https://info-search.yahoo.co.jp/archives/002851.php | YES | scope, teaches, opened, recheck, used-by (anchor equal) |
| S390 | https://ziyuan.baidu.com/wiki/990 | YES | anchor, opened, recheck, used-by (scope/teaches equal) |
| S409 | https://ziyuan.baidu.com/wiki/1021 | YES | teaches, opened, recheck, used-by (scope/anchor equal) |

No collision id differs in document. All eight differ in `opened` and in the `recheck` cell: the staged copies carry a
live `curl` command, the registry rows carry a bare interval. Opened dates: registry all `2026-10-25`; staged
`2026-10-23` (S312, S329) and `2026-10-24` (the other six, including S367). `status` is `mined` on both sides for all
eight. Staged rows also carry a second URL inside the recheck command (2 URL occurrences vs 1 in the registry row).

## NEXT ID:

Max id in the lane registry is **S418**; the next unused id is **S419** (= max + 1).
```
grep -oE '^ {0,3}\|[[:space:]]*S[0-9]{3,}' corpus/SOURCES.md | grep -oE 'S[0-9]+' | sort | tail -1
# -> S418
```
Registry tail by id: S409, S416, S417, S418 (S410–S415 unused, but max+1 is the stated rule). S419 and S420 occur 0
times in `corpus/SOURCES.md`, matching `mirror-pin.json` `adoptedAbsent: ["S419","S420"]`.

Staged ids S375, S376, S388, S389, S387 do not occur in the lane registry (0 occurrences each, both by row-start
extraction and by raw substring count); each occurs once in `SOURCES.append.md`. They are staged-only, so they can be
adopted without an id collision.

Checks not run: none of the above is unrun — every number here comes from a command executed in this seat, transcript in
`ExecIdGuard.files/commands.txt`. No pacman, no tool install, no lane test/build run.

VERDICT: All four assimilation artifacts reproduce byte-for-byte (156/129/8/12 rows; 780/645/40/453 bytes); the 0–3-space guard catches an indented S287 that the column-zero pattern misses; all 8 collisions are the same document with divergent metadata; lane max id is S418 so the next unused id is S419, and staged S375/S376/S387/S388/S389 are registry-absent.
