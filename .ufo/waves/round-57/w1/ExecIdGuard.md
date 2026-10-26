# ExecIdGuard

Seat: leaf executor, round-57 W1. Scope: replicate the assimilation id-collision guard and the
quarantine slice from scratch in my own scratch repo, compare with the committed round-57 artifacts,
state same-document verdicts for the collisions, and pin the id-space facts for the renumber map.
Nothing in the lane was mutated except this report and `w1/ExecIdGuard.files/`. No pacman, no tool
install was needed (nothing to install), no labrat probe was used (this seat's inventory carries no
dispatch tool). All reads are pinned to the hashes in COMMANDS §7; the lane registry was still at the
pre-append state (`sha256 010af792…be81`, 158 rows) when read, so the append has not landed at read time.

## COMMANDS:

Scratch: `D=/tmp/execidguard.G2qCsK`; `git -C "$D" init -q`; `git -C "$D" rev-parse --show-toplevel`
printed `/tmp/execidguard.G2qCsK` (verified equal to `$D`). Every later git call named `-C "$D"`; no
commit was made. Full transcript with the exact argv and observed values:
`w1/ExecIdGuard.files/commands.txt`.

1. `grep -oE '^ {0,3}\|[[:space:]]*S[0-9]{3,}' corpus/SOURCES.md | grep -oE 'S[0-9]+' | sort` -> `reg-ids`
2. same pattern over `merge/kake/SOURCES.append.md` -> `staged-ids`; `comm -12 reg-ids staged-ids` -> `collisions`
3. `awk -F'|' -v l='kake' '$2 ~ ("`" l "`") && $3 ~ /round[0-9]+/ && $4 ~ /S[0-9]+/ {print $4, $5}' absent-defect-register.md` -> `quarantine-slice`
4. `cmp -s` of each replica against `.ufo/waves/round-57/assimilation/{reg-ids,staged-ids,collisions,quarantine-slice}`
5. guard fixtures: `  | S403 | x |` (0-3 spaces) and `    | S403 | x |` (4 spaces), each probed with the
   0-3-space pattern, the column-zero-only pattern and an unbounded ` *` pattern
6. guard on a scratch registry: `cp corpus/SOURCES.md` + append `  | S403 | x |`, then both patterns + `comm -12`
7. `grep -c` / `grep -c -F` of the S403/S408 ids and their document URLs in `corpus/SOURCES.md`
8. escaped-pipe-aware cell comparison (`re.split(r'(?<!\\)\|', row)`) of every collision row in both registries

Inputs at read time: `corpus/SOURCES.md` sha256 `010af7926a03788fa5f36371a0f9452ee3f3ee3c087977a455dc400bb3b5be81`
(273 lines, 158 rows, byte-identical to `assimilation/pre-append/corpus/SOURCES.md`);
`SOURCES.append.md` sha256 `5f0cd4c4debc647f3d1e2a85519d4ae2b000d91dad49765514871fa502e9f0cc` (135 lines);
lane HEAD `f7c98ff269286723077848f3caf1422c4004f46d`.

## COMPARISON:

| artifact | replica | committed | `cmp` | md5 (replica = committed) |
|---|---|---|---|---|
| `reg-ids` | 158 lines / 790 B | 158 / 790 | IDENTICAL | `b1ff10592de374a22de8e6c2854b8541` |
| `staged-ids` | 129 / 645 | 129 / 645 | IDENTICAL | `f6f2bbd0c8d6002c0e4be03aee5b1602` |
| `collisions` | 8 / 40 | 8 / 40 | IDENTICAL | `636715189e691c9eb3c3924f538c3ada` |
| `quarantine-slice` | 12 / 453 | 12 / 453 | IDENTICAL | `f19e980da6ab66a2f25ef5555a8f45e3` |

- Collisions, in sort order: S312 S329 S367 S372 S373 S374 S390 S409 — the eight ids the contract names.
- Neither id list has a duplicate (`sort -u` == `sort`: 158 and 129). Neither registry has a row the
  0-3-space pattern misses: the only unmatched `|`-leading lines are the two header rows (id row and
  `|---|` rule) in each file; `corpus/SOURCES.md` has no row indented 4+ spaces.
- Quarantine slice: 12 lines, `grep -cE 'S[0-9]+'` = 12, so every line carries an S-id (requirement met).
  The slice is drawn from two register sections: 9 rows from `## Rows` (lines 83–91, class
  `payload-absent`, ids S142 S143 S148 S156 S161 S193 S194 S195 S206) and 3 rows from
  `## Rows whose quotes were NEVER CHECKED` (lines 319–321, ids S154 S178 S184, whose class cell is the
  sentence "the cited source could not be fetched, so no quote was checked", i.e. class `unreachable`
  per the register's legend).
- The 3 unreachable rows print with a stray trailing backtick in the id cell (`S154\``, `S178\``,
  `S184\``) because that table's id cell is written as an unclosed code span; the committed slice has
  the same bytes, so this is a faithful replication of a formatting defect in the upstream register,
  not a derivation error. The ids are still readable and carry `S` + digits.
- The register holds 13 `` `kake` `` rows; the predicate keeps 12. The excluded row is line 242,
  `| \`kake\` | 9 |`, the lane-total row of the register's `## By lane` section (no round, no id) —
  correct exclusion, not a dropped defect row.
- Note on the carried proof: `assimilation/guard-proof/commands.txt` (carried from round 56) records
  `156 780` for `reg-ids`. The live registry is now `158 790`, and my replica of the *current* registry
  is `158 790`/`IDENTICAL`. So the carried line is a round-56 measurement against a smaller registry,
  not a mismatch with the artifacts committed this round.

## GUARD PROOF:

Fixture A (`fixture-indented-S403.md`, 52 B) — registry shape plus the indented row `  | S403 | x |`
(2 leading spaces, inside the 0-3 window):

| probe | pattern | output | verdict |
|---|---|---|---|
| 0-3-space | `^ {0,3}\|[[:space:]]*S[0-9]{3,}` | `S403` (1 line) | reports the indented row |
| column-zero only | `^\|[[:space:]]*S[0-9]{3,}` | empty (0 lines) | reports nothing |
| unbounded | `^ *\|[[:space:]]*S[0-9]{3,}` | `S403` | also matches — cannot bound the indent |

Fixture B (`fixture-4space-S403.md`, 54 B) — same row at 4 spaces: the 0-3 pattern returns **empty**,
the unbounded ` *` pattern returns `S403`. So the 0-3 bound is exactly what keeps the guard on the
registry's documented shape while tolerating the 0-3 indent a staged append may carry; the two probes
differ only on the indented input, which is the discriminating case the assignment names.

Scratch registry proof (`registry-with-indented-S403.md` = `corpus/SOURCES.md` + the appended line):

- 0-3-space pattern -> 159 ids / 795 B; `comm -12` with `staged-ids` -> **9** collisions / 45 B,
  `S312 S329 S367 S372 S373 S374 S390 S403 S409` — the indented S403 is caught as a collision.
- column-zero-only pattern -> 158 ids / 790 B; `comm -12` -> **8** collisions / 40 B, S403 absent.
- The column-zero outputs are byte-identical to the committed `reg-ids` and `collisions`
  (md5 `b1ff1059…`, `636715…`), which independently confirms that (a) the committed artifacts were
  produced by the column-zero-capable read of the current registry, and (b) no row of the committed
  registry sits outside column zero today.
- Consequence for the round: an indented adoption of staged S403 would have entered the registry as a
  collision only under the 0-3-space form, and the round-57 map deliberately avoids that by renumbering
  to S421/S422.

Saved under `w1/ExecIdGuard.files/`: `fixture-indented-S403.md`, `fixture-4space-S403.md`,
`guard-0to3-on-indented.out` (`S403`), `guard-col0-on-indented.out` (0 B), `guard-0to3-on-4space.out`
(0 B), `guard-unbounded-{on-indented,on-4space}.out`, `scratch-registry-append-line.txt`,
`scratch-reg-ids-0to3`, `scratch-collisions-0to3`, `scratch-reg-ids-col0`, `scratch-collisions-col0`,
the four replicas (`*.replica`) and `commands.txt`. The 147 KB scratch registry copy was not saved; it
is one `cp` + one `printf` in `commands.txt`.

## SAME-DOCUMENT TABLE:

URL cell = registry cell 3 (`source`, the `title — URL` cell); comparison used an escaped-pipe-aware
split, so the staged `recheck` cells' escaped `\|` do not shift columns. Each colliding row's source
cell is byte-identical between the two registries, and its URL set is equal (each row carries exactly
one URL).

| id | document URL (both registries) | verdict |
|---|---|---|
| S312 | `https://ziyuan.baidu.com/college/courseinfo?id=267&page=15` | SAME document |
| S329 | `https://ziyuan.baidu.com/college/courseinfo?id=1399` | SAME document |
| S367 | `https://info-search.yahoo.co.jp/archives/002852.php` | SAME document |
| S372 | `https://info-search.yahoo.co.jp/archives/002849.php` | SAME document |
| S373 | `https://info-search.yahoo.co.jp/archives/002850.php` | SAME document |
| S374 | `https://info-search.yahoo.co.jp/archives/002851.php` | SAME document |
| S390 | `https://ziyuan.baidu.com/wiki/990` | SAME document |
| S409 | `https://ziyuan.baidu.com/wiki/1021` | SAME document |

8 of 8 are the same document; **0 differ**. The rows are not byte copies of each other — the titles,
`kind`, `tier` and `status` agree, but the staged row differs from the lane row in 4–6 of the other
cells (scope, anchor, teaches, opened, recheck, used-by), e.g. S374 differs only in scope/teaches/
opened/recheck, S373 only in anchor/opened/recheck/used-by. So the collision is a *document* collision
with re-worded prose: a title- or row-bytes-based duplicate check would have missed it, a URL-based one
catches all eight. Consequence: adopting any of these staged rows would have added a second row for a
document the lane already holds, which is exactly what the guard forbids; the two adopted rows
(S403, S408) are not in this set.

## NEXT ID:

- S403 in the lane registry: `grep -cE '^ {0,3}\|[[:space:]]*S403[[:space:]]*\|'` = **0**; the token
  `S403` occurs **0** times anywhere in `corpus/SOURCES.md`. S408 likewise **0** / **0**.
- Lane id space: 158 distinct ids, `S001`–`S420`; max = **S420**; the space is sparse (S140–S248 and
  other blocks are unused), so the *lowest* unused id overall is **S140** — "next unused" in the round's
  sense is max+1, not lowest-gap.
- Next unused id after the max = **S421**; **S422** is also free. Both are absent from the lane registry
  (`S421 reg=0`, `S422 reg=0`) and from `staged-ids` (`S421 staged=0`, `S422 staged=0`), so neither the
  lane nor the staged append can collide with the renumber map; `grep -cE 'S421|S422' collisions` = 0.
- Staged document URLs of the two adopted rows, `grep -c -F` in `corpus/SOURCES.md`:
  `https://ziyuan.baidu.com/college/articleinfo?id=3458` -> **0**;
  `https://ziyuan.baidu.com/wiki/867` -> **0**. Path fragments alone also return 0
  (`college/articleinfo?id=3458` -> 0, `wiki/867` -> 0), so no lane row holds either document under
  another URL form.
- Cross-check with the retained bodies: `sources/receipts.json` pins S421 to
  `https://ziyuan.baidu.com/college/articleinfo?id=3458` and S422 to `https://ziyuan.baidu.com/wiki/867`
  — the same URLs the staged S403/S408 rows cite, so the renumber map moves a document the lane does
  not yet hold to the two free ids.

Risks / limits: the facts above are pinned to the registry hash `010af792…be81` (158 rows); if the W1
build seat appends S421/S422 while the wave runs, "S421 unused" becomes stale by construction — the
check is valid at that hash, and re-running step 6 of `commands.txt` against a later tree re-derives it.
I did not inspect whether any lane knowledge file already cites S403/S408 (outside this assignment);
the registry-level check above is what was asked and what was run. No claim in this report rests on an
unrun check.

VERDICT: All four committed artifacts replicate byte-identically from scratch (158/790, 129/645, 8/40, 12/453), the 0-3-space guard reports the indented S403 while column-zero reports nothing (and the scratch-registry run turns 8 collisions into 9), all 8 collisions are the same document by URL, and S403/S408 plus their URLs are absent from a registry whose max id is S420 with S421/S422 free.
