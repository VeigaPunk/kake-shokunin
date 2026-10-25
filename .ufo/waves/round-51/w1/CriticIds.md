# CriticIds — the id-collision evidence, attacked (round 51, wave 1)

Verdict: the overlap is **neither resolved nor correctly noted**. It is misdescribed. The
three ids named in `corpus/lessons/round-51.md:60-67` are the lane's own ids, not ids in any
package snapshot I can read; the committed staged list is a round-49 carry-over anchored to
nothing; and the overlap that actually exists is by **URL**, including the two rows this
round adopted.

## Counterexample

Take the staged package at the path the wave brief names,
`/home/vgpnk/Projects/shokuknow/merge/kake/SOURCES.append.md` (working-tree mtime
2026-10-24 23:33:20 -0300, **129 rows S287–S415**, parsed with the census pattern
`^ {0,3}\|[[:space:]]*S[0-9]{3,}`):

- id intersection with the live lane registry (145 ids, S001–S286): **0**.
- URL intersection: **10 pairs**, and it covers exactly the ground the note names —
  S310↔S273 (crawl-budget), S311↔S274 (reduce-crawl-rate), S323↔S286 (troubleshoot),
  S299↔S262 (canonicalization), S300↔S263 (googlebot), plus S287/S288/S289↔S137/S138/S139,
  S296↔S080, S399↔S249.

Committed package HEAD `8b94c5c1` (2026-10-24 11:02:02 -0300, **97 rows S137–S233**): also
**0** id intersection, 9 URL pairs — S149↔S262, S150↔S263, S160↔S273, S161↔S274,
S173↔S286, S137/S138/S139↔S137/S138/S139.

So `S273`, `S274`, `S286` exist as ids in **neither** package state. They are the lane's ids
for URLs the package stages as S160/S161/S173. And the committed scratch that produced the
note — `.ufo/waves/round-51/assimilation/staged-ids`, 121 ids S250–S370 — is byte-identical
to rounds 49 and 50 (`diff -q` → identical), differs from round-48's (115 ids S137–S251),
and matches no revision of the package: over the 5 commits reachable for
`merge/kake/SOURCES.append.md` the row count is 76/80/85/93/97 (all S137–S233), and
`git log -S S370 -- merge/kake/SOURCES.append.md` returns nothing.

## Resolved or merely noted?

Merely noted — and the note is unanchored, stale, and unenforced.

1. **Internally consistent, externally unanchored.** `comm -12` of the two committed lists
   reproduces `assimilation/collisions` byte-for-byte. The defect is the input: neither
   `reg-ids` nor `staged-ids` records a path, revision, mtime, sha256 or command for the
   staged side. The package working tree moved at 23:33:20, ten minutes after the lane's
   last commit (9d13768, 23:23:07) — the object that was checked no longer exists at the
   path a later round will read.
2. **The wrong key.** The census detects duplicates two ways: id (`E03`,
   `scripts/sources-census.sh:641`) and URL+scope with literal scope equality (`E04`,
   `:649`); differing scope is only a warning (`W04`, `:645`). Measured against the live
   registry:
   - today's package row S310 appended verbatim (shape-repaired) → **exit 0**, one
     `W04 S310 duplicate url … crawl-budget across scopes`;
   - the same row with the lane's exact S273 scope → `E04 … within scope` (exit 1).
   Consequently the two rows **this round adopted** (S262, S263) are already duplicate URLs
   against the staged package (S299/S300 today; S149/S150 at HEAD), while the lesson claims
   "no citation had to be re-pointed". True for ids, false for URL identity.
3. **The guard is half-proven.** `guard/guard-collisions` is non-empty (S262) on the
   indented fixture and `guard/guard-col0` is empty — that shows the *pattern* catches
   indentation. But round-51 committed no guard-side staged list (round-49 had
   `guard-staged-ids` and `guard-wide-ids`), so `guard-collisions` cannot be re-derived from
   the committed guard files.
4. **Nothing enforces it.** Neither `c51_wave_ledger.py` nor `c51_quote_truth.py` mentions
   `collisions`, `staged-ids` or `reg-ids` (grep: no matches). C1 can score 3/3 with the
   collision scratch wrong; the claim lives only in prose.

## What breaks if a later round adopts the staged rows under those ids

Measured with the real validator and the frozen counters, not argued:

- **Shape first.** 96 of 129 working-tree rows carry the staged `recheck` prose with a
  literal pipe (`180d — \`curl … | grep -c …\``), giving NF=14 → `E01 … fields=12`
  (`sources-census.sh:636`). Because E01 `next`s, **E03 is never printed** for that row: a
  raw append of the package's S273-relabelled row yields E01 only. The duplicate-id guard
  is disabled in precisely the form the package supplies.
- **After shape repair**, appending under S273 → `E03 S273 duplicate id`, exit 1.
- **In-place adoption** (replace the lane's S273 cells, keep the id) →
  `sources-census.sh validate` **exit 0**. A mined row is silently re-pointed to a different
  scope, different teaches and `opened 2026-10-23` with no finding at all.
- **Prior frozen counters flip**, because every staged row carries `opened 2026-10-23` while
  the lane's rules require `2026-10-24`:
  - `c49_quote_truth.py` R1: `2/2 met=True` → **`1/2 met=False`, `FAIL S273: opened=2026-10-23`**
    (reproduced in a throwaway repo at three revisions: in-place, raw duplicate append,
    normalized duplicate append; S274 follows the same rule);
  - `c50_quote_class.py` R4: `3/3 met=True` → **`2/3 met=False`, `FAIL S286: opened=2026-10-23`**.
- **Two rows for one id** make "the row" ambiguous: the counter read the appended row. It
  also breaks the `sort | uniq -d` invariant round-50's scratch asserted for the registry.

## Impacted axes

- **freshness** — the note reports a package state that cannot be re-opened; and the round's
  own two admissions are already duplicate URLs against the staged package (S299/S300 now,
  S149/S150 at HEAD). That is a live coverage defect, not a future risk.
- **operability** — the collision check is read by no counter, its staged input is unpinned
  and identical to the previous two rounds' copy, and the census's only id guard (E03) is
  defeated by the package's own row shape.

## Smallest safe correction

1. Nothing to undo this round: `git show 5591557 -- corpus/SOURCES.md` adds only S262 and
   S263, so no staged row was adopted.
2. Pin the staged read: record `path@commit`, the file sha256, its mtime and the extraction
   command, and re-derive the staged id list against the commit each round — never the dirty
   working tree (it moved at 23:33:20 tonight while the wave was open). If the campaign is
   mid-write, the honest staged set is the commit's, and its intersection is empty.
3. Intersect on **URL as well as id** and report both separately, each staged row paired with
   the lane id that already holds its URL.
4. Make it a C1 ledger condition (e.g. L4) so a stale or unanchored staged read fails the
   round, and commit the guard's staged side (`guard-staged-ids`) as round 49 did.
5. For any future adoption from staged: assign a **fresh** lane id, never a held one; strip
   the recheck prose to `180d`; never carry the staged `opened` into a row a frozen counter
   pins to `2026-10-24`.

## Scratch evidence I relied on

Committed lane bytes: `.ufo/waves/round-51/assimilation/{reg-ids (143, S001–S286),
staged-ids (121, S250–S370), collisions (3)}`, `assimilation/guard/{guard-registry.md,
guard-reg-ids, guard-collisions, guard-col0, guard-col0-ids}`; `.ufo/waves/round-{48,49,50}/
assimilation/staged-ids`; `corpus/lessons/round-51.md:60-67`, `round-50.md:35`;
`corpus/SOURCES.md`; `.ufo/waves/round-49/c49_quote_truth.py`;
`.ufo/waves/round-50/c50_quote_class.py`; `scripts/sources-census.sh:636,641,645,649`.

External read-only: `shokuknow/merge/kake/SOURCES.append.md` (working tree and
`git show 8b94c5c1:merge/kake/SOURCES.append.md`), package `git rev-list` over 5 commits.

Working copies used: `/tmp/pkg-head.md`, `/tmp/lane-ids.txt`, `/tmp/ext-ids.txt`,
`/tmp/staged-file.txt`, `/tmp/recomp.txt`, `/tmp/fxroot2` (symlink farm plus a real copy of
the registry), `/tmp/k49` (throwaway git repo used to run both frozen counters at several
revisions). These are disposable; every number above is rebuildable from committed or
read-only bytes with the commands below, so no finding rests on `/tmp` surviving.

```
# staged ids / registry ids / the collision set
git -C /home/vgpnk/Projects/shokuknow show 8b94c5c1:merge/kake/SOURCES.append.md > /tmp/pkg-head.md
grep -oE '^ {0,3}\|[[:space:]]*S[0-9]{3,}' corpus/SOURCES.md | grep -oE 'S[0-9]+' | sort   # 145
grep -oE '^ {0,3}\|[[:space:]]*S[0-9]{3,}' /tmp/pkg-head.md | grep -oE 'S[0-9]+' | sort     # 97
grep -oE 'S[0-9]+' .ufo/waves/round-51/assimilation/staged-ids | sort                       # 121
comm -12 <(sort .ufo/waves/round-51/assimilation/reg-ids) <(sort .ufo/waves/round-51/assimilation/staged-ids)
diff -q .ufo/waves/round-50/assimilation/staged-ids .ufo/waves/round-51/assimilation/staged-ids

# URL-level intersection: row id = column 2, source URL = first https?:// token in column 3
# (id ∩ = 0; url ∩ = 10 pairs against the working tree, 9 against 8b94c5c1)

# adoption matrix: a REAL copy of the lane with the registry swapped, never a symlink
cp -as /home/vgpnk/Projects/shokunin/kake-shokunin /tmp/fx2 && rm /tmp/fx2/corpus/SOURCES.md
cp corpus/SOURCES.md /tmp/fx2/corpus/SOURCES.md        # then append/replace one row in /tmp/fx2
bash /home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --today 2026-10-25 \
  --file /tmp/fx2/corpus/SOURCES.md

# frozen counters: throwaway repo with corpus/ and .ufo/waves/round-{49,50}
git init /tmp/k49 && cp -a corpus /tmp/k49/ && cp -a .ufo/waves/round-49 /tmp/k49/.ufo/waves/
python3 -B .ufo/waves/round-49/c49_quote_truth.py --root /tmp/k49 --revision <rev>
python3 -B .ufo/waves/round-50/c50_quote_class.py --root /tmp/k49 --revision <rev>
```

No tool installs or upgrades were needed, and no evidence here is a rebuilt file: every figure
comes from committed lane bytes, the package's committed blob `8b94c5c1`, or the commands
above. This report cites **no** round-35 scratch path (grep: 0), so the round-35 scratch
relocation does not affect it — verified from the worktree, not from a peer message:
`mado-shokunin/.ufo/waves/round-35/scratch` is absent, `scratch-evidence` is present with 59
seat dirs and 261 tracked files at `4efaf63`.

## Disclosure

Early in the review a `cp -as` fixture made `/tmp/fxroot/corpus/SOURCES.md` a symlink to the
lane registry, and two mutation writes followed it into the real file. `git diff` showed
exactly three changed lines, all mine (an inserted S149 row, an appended S160 row, an S286
replacement). The file was restored from `git show HEAD:corpus/SOURCES.md`; the diff for
`corpus/SOURCES.md` is now empty and both sides hash to
`4ea81a5ae79029cbb7ec424a51ec1d31e06650f5072d8c58cea878f558449fe3`. No other lane file was
touched; the later experiments used a detached real copy.
