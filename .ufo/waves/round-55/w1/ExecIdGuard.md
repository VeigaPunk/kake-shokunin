# ExecIdGuard

Seat: leaf executor (round-55 W1, lane kake-shokunin, base `fcaf4b85ce32dbe2a88ce9924a4994e8cd93212d`).
Scope: replicate the assimilation id-collision guard, the guard proof and the quarantine slice from scratch,
then classify the colliding ids by document identity. Read-only on the lane; the only write is this report.

Scratch: `D=$(mktemp -d)` → `/tmp/tmp.3qTLtGFa3i`, `git -C "$D" init -q`,
`git -C "$D" rev-parse --show-toplevel` = `/tmp/tmp.3qTLtGFa3i` (matches `$D`). No commit, no identity,
no other repository touched. No pacman, no installs, no tool upgrades were needed (grep/comm/awk/cmp/sha256sum
were already present); nothing was installed, so there is no install record to file.

Inputs read (read-only), with sha256:

```
f4e6cc8830c1d963218a31e5745c0c892a30a83d0d758fcd412a5c201bdc517d  kake-shokunin/corpus/SOURCES.md (144364 B, 270 lines)
5f0cd4c4debc647f3d1e2a85519d4ae2b000d91dad49765514871fa502e9f0cc  shokuknow/merge/kake/SOURCES.append.md (126796 B)
5afe1810a6c3d62f37987b575a954f5b1197daa23005d4bb2f1d982f64bad833  shokuknow/.ufo/waves/corpus-expansion-1/absent-defect-register.md (375 lines)
```

`corpus/SOURCES.md` is byte-identical to the pinned pre-append mirror
`.ufo/waves/round-55/assimilation/pre-append/corpus/SOURCES.md` (same sha `f4e6cc88…`, 155 registry rows),
so the registry side of the intersection is measured at the pinned state.

## COMMANDS:

Run from `$D` (scratch). `L` = lane repo, `A` = `$L/.ufo/waves/round-55/assimilation`.

```sh
# 1. ids — the round's stated pattern (0–3 leading spaces)
grep -oE '^ {0,3}\|[[:space:]]*S[0-9]{3,}' $L/corpus/SOURCES.md | grep -oE 'S[0-9]+' | sort > reg-ids
grep -oE '^ {0,3}\|[[:space:]]*S[0-9]{3,}' /home/vgpnk/Projects/shokuknow/merge/kake/SOURCES.append.md \
  | grep -oE 'S[0-9]+' | sort > staged-ids
# 2. intersection
comm -12 reg-ids staged-ids > collisions
# 3. quarantine slice — the round's awk, verbatim
awk -F'|' -v l='kake' '$2 ~ ("`" l "`") && $3 ~ /round[0-9]+/ && $4 ~ /S[0-9]+/ {print $4, $5}' \
  /home/vgpnk/Projects/shokuknow/.ufo/waves/corpus-expansion-1/absent-defect-register.md > quarantine-slice
# 4. guard proof — fixture with the indented row, then both patterns
printf '| id | x |\n|---|---|\n  | S287 | indented |\n' > guard/fixture-reg.md
grep -oE '^ {0,3}\|[[:space:]]*S[0-9]{3,}' guard/fixture-reg.md | grep -oE 'S[0-9]+' | sort > guard/fixture-ids
grep -oE '^ {0,3}\|[[:space:]]*S[0-9]{3,}' guard/fixture-reg.md | grep -oE 'S[0-9]+' | sort > guard/fixture-collisions
grep -oE '^\|[[:space:]]*S[0-9]{3,}'        guard/fixture-reg.md | grep -oE 'S[0-9]+' | sort > guard/colzero-ids
# 5. comparison
sha256sum reg-ids staged-ids collisions quarantine-slice guard/fixture-*
cmp -s <mine> <lane artifact>            # per file, see COMPARISON
# 6. selectivity probes (boundary of the guard)
grep -cE '^ {0,3}\|[[:space:]]*S[0-9]{3,}' $L/corpus/SOURCES.md            # 155
grep -cE '^\|[[:space:]]*S[0-9]{3,}'      $L/corpus/SOURCES.md            # 155  (no indented rows today)
grep -cE '^ {0,3}\|[[:space:]]*S[0-9]{3,}' …/SOURCES.append.md            # 129
grep -cE '^\|[[:space:]]*S[0-9]{3,}'      …/SOURCES.append.md            # 129
```

## COMPARISON:

Every replicated artifact is byte-identical (`cmp -s` silent, equal sha256, equal line and byte counts).

| artifact | mine lines/bytes | mine sha256 | lane lines/bytes | lane sha256 | cmp |
|---|---|---|---|---|---|
| `reg-ids` | 155 / 775 | `5dfcf4fab40f8f4ecdef113e2b9661adf3fefb85188a8ca03366eae72e95d57c` | 155 / 775 | same | IDENTICAL |
| `staged-ids` | 129 / 645 | `3938ec94ee29d52d27e6192603a9c30b9bfee3a8969600c7207478c3828f9deb` | 129 / 645 | same | IDENTICAL |
| `collisions` | 8 / 40 | `a443d89dc53a6ad4d6c8d6c7204116f378bdd479620dcbb95a02a92def8ea9a0` | 8 / 40 | same | IDENTICAL |
| `quarantine-slice` | 12 / 453 | `6d92f4408c7482e59fb93c2085676f7d9c4fedb687bcfd501060f63c15d2d63a` | 12 / 453 | same | IDENTICAL |

Collisions content reproduced exactly (sorted, one id per line): `S312 S329 S367 S372 S373 S374 S390 S409` — 8 ids,
matching the contract's ledger. Registry 155 ids, staged 129 ids, staged ids absent from the registry = 120
(`S287`–`S415` minus the 8 collisions plus nothing else; `S380` and `S418` are both absent from the lane registry).

Quarantine slice reproduced exactly: 12 rows — 9 `payload-absent` (`S142 S143 S148 S156 S161 S193 S194 S195 S206`)
and 3 unreachable-source rows (`S154 S178 S184`). Filter selectivity checked: the register holds 13 lines matching
`` `kake` ``; the 13th is the summary line `| \`kake\` | 9 |`, correctly excluded by the `round[0-9]+` / `S[0-9]+`
guards. Neither slice id set intersects the registry ids or the staged ids (`comm -12` empty both ways), consistent
with the contract's "none adopted this round, none appended".

Two register-side observations, reported not remediated (external substrate is read-only):
- The register's own summary table says `` | `kake` | 9 | ``, but the lane has 12 defect rows; the 9 counts
  `payload-absent` only, the 3 `unreachable` rows are outside the summary count.
- Rows for `S154`, `S178`, `S184` carry a stray trailing backtick in the id cell (`S154\``, `S178\``, `S184\``);
  the awk copies it through verbatim, which is why those three slice lines print the class sentence in the
  position where the other nine print `` `payload-absent` ``.

## GUARD PROOF:

Fixture `guard/fixture-reg.md` (43 B, sha `29589c39…`), rows: header, separator, then `  | S287 | indented |`
(two leading spaces, inside the 0–3 window).

| pattern | ids reported | verdict |
|---|---|---|
| `^ {0,3}\|[[:space:]]*S[0-9]{3,}` (round pattern) | `S287` (1 id) | catches the indented row |
| `^\|[[:space:]]*S[0-9]{3,}` (column-zero only) | none (0 ids, empty file) | blind to the indented row |

Both are byte-identical to the lane's `assimilation/guard-proof/`: `fixture-reg.md` 43 B `29589c39e02406f899921f9fb07c0098ab633ad29c54d830f3a3ba0e587e277b`,
`fixture-ids` 5 B `c464fc55900f6cd91a757e374fcd13af2845edb7d7b85ae0da93e009b2427cb6`,
`fixture-collisions` 5 B (same sha) — all `MATCH` by `cmp -s`.

Coverage boundary of the guard, measured (not in the lane artifact): a row indented four spaces or with a tab
before `|` is reported by **neither** pattern (`^ {0,3}` caps at three; `^ *` finds it). Today neither real file
has any indented row — 0–3-space count equals column-zero count in both (155 = 155 registry, 129 = 129 staged) —
so the guard is currently non-load-bearing and no live id is being missed; the gap only matters if a future
append indents by ≥4 spaces or a tab.

## SAME-DOCUMENT TABLE:

URL cell compared byte-for-byte between the lane row (`corpus/SOURCES.md`) and the staged row
(`merge/kake/SOURCES.append.md`); line numbers are 1-based.

| id | lane line | staged line | URL (both, identical string) | document verdict |
|---|---|---|---|---|
| S312 | 156 | 32 | `https://ziyuan.baidu.com/college/courseinfo?id=267&page=15` | SAME document |
| S329 | 155 | 49 | `https://ziyuan.baidu.com/college/courseinfo?id=1399` | SAME document |
| S367 | 157 | 87 | `https://info-search.yahoo.co.jp/archives/002852.php` | SAME document |
| S372 | 158 | 92 | `https://info-search.yahoo.co.jp/archives/002849.php` | SAME document |
| S373 | 159 | 93 | `https://info-search.yahoo.co.jp/archives/002850.php` | SAME document |
| S374 | 154 | 94 | `https://info-search.yahoo.co.jp/archives/002851.php` | SAME document |
| S390 | 160 | 110 | `https://ziyuan.baidu.com/wiki/990` | SAME document |
| S409 | 161 | 129 | `https://ziyuan.baidu.com/wiki/1021` | SAME document |

Different documents among the 8 collisions: **none (0 of 8)**. Each pair also carries the same source title
before the URL (e.g. `百度搜索资源平台 — 平台工具使用手册（移动适配）`, `Yahoo!検索 インフォセンター — サイト単位、ディレクトリ単位での巡回の拒否設定 1`),
so identity does not rest on the URL alone. The rows are not textually equal — they differ in prose/status cells
(`scope,anchor,teaches,opened,recheck,used-by` for S312/S329/S367/S372; `anchor,opened,recheck,used-by` for
S373/S390; `scope,teaches,opened,recheck,used-by` for S374; `teaches,opened,recheck,used-by` for S409) — but a
differing description cell is not a different document.

Consequence for the renumber map: since all 8 collisions are the same document, **no colliding staged id is
eligible for renumbering**; the staged rows must resolve to the existing lane rows (contract's
`staged S372/S373 -> existing lane rows S372/S373`). The round's only renumber, `staged S380 -> S418`, concerns a
staged id that is not a collision (S380 and S418 are both absent from the lane registry) and whose document
`https://info-search.yahoo.co.jp/archives/002885.php` appears nowhere in `corpus/SOURCES.md`
(`grep -c '002885' corpus/SOURCES.md` = 0; staged count = 1; `S418` in staged = 0) — it is a lane-id choice for a
document the lane lacked, so the same-document rule does not block it.

Unrun / not claimed: no quote-truth or coverage-map counter was run (C1/C2 belong to their own seats); no git or jj
state was inspected beyond `rev-parse` in the scratch repo; the register's external fix (summary count, stray
backticks) was not attempted. Nothing in this report is a verdict on the entries' content.

VERDICT: reg-ids/staged-ids/collisions/quarantine-slice and the guard-proof fixtures all reproduce byte-identically; the 0–3-space pattern reports S287 on the indented fixture while the column-zero pattern reports nothing; all 8 collisions (S312 S329 S367 S372 S373 S374 S390 S409) are the same document in both registries, so no collision is eligible for renumbering and the only legitimate renumber is the non-colliding S380 -> S418.
