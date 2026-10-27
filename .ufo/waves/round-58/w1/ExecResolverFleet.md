# ExecResolverFleet

C2 (operability) regression/adjacency scope: does the disclosed C2 fix to `scripts/id_resolver.py`
(fence-blind registry D1, git-quoted knowledge paths F1) change the result of any live fleet lane?

Tool under test = the lane's CURRENT (unfixed) tool, pinned to the committed blob:
`kake-shokunin` HEAD `cc8da1674d6e`, `git show HEAD:scripts/id_resolver.py | sha256sum` =
`25982446d2e647830269cfff0b4bebf7bf263dde57c4321d87eeb42f06461bee` (identical to the worktree file;
`git status --porcelain -- scripts/id_resolver.py` empty). All 21 fleet lanes that carry
`corpus/SOURCES.md` were scanned; every lane directory under `/home/vgpnk/Projects/shokunin/*-shokunin`
carries one (21 of 21 present).

Invocation per lane (read-only; no lane or fleet mutation):

    python3 -B /home/vgpnk/Projects/shokunin/kake-shokunin/scripts/id_resolver.py \
        --root /home/vgpnk/Projects/shokunin/<lane> --revision HEAD \
        --fleet /home/vgpnk/Projects/shokunin

## RUNS:

`kn` = knowledge paths at HEAD, `q` = those printed quoted, `freg` = fence blocks inside `## Registry`,
`fsrow` = `| S###` rows inside any fence. "summary" is the tool's last stdout line verbatim.

| lane | HEAD | exit | summary | freg | fsrow | kn | q |
|---|---|---|---|---|---|---|---|
| audio-shokunin | 7a2fcd4f0883 | 0 | ids_cited=15 ids_resolved=15 dangling=0 owned_elsewhere=0 unowned=0 | 0 | 0 | 18 | 0 |
| chousa-shokunin | 5b550133d79b | 1 | ids_cited=92 ids_resolved=91 dangling=1 owned_elsewhere=1 unowned=0 | 0 | 0 | 75 | 0 |
| game-dev-2d-shokunin | 7753d49b1667 | 0 | ids_cited=10 ids_resolved=10 dangling=0 owned_elsewhere=0 unowned=0 | 0 | 0 | 5 | 0 |
| game-dev-3d-shokunin | 89dd182b7094 | 0 | ids_cited=8 ids_resolved=8 dangling=0 owned_elsewhere=0 unowned=0 | 0 | 0 | 47 | 0 |
| kagi-shokunin | 69b61db46be4 | 0 | ids_cited=21 ids_resolved=21 dangling=0 owned_elsewhere=0 unowned=0 | 0 | 0 | 25 | 0 |
| kaidoku-shokunin | 6b9e64fe7e0d | 0 | ids_cited=107 ids_resolved=107 dangling=0 owned_elsewhere=0 unowned=0 | 0 | 0 | 136 | 0 |
| kake-shokunin | cc8da1674d6e | 0 | ids_cited=106 ids_resolved=106 dangling=0 owned_elsewhere=0 unowned=0 | 0 | 0 | 54 | 0 |
| kama-shokunin | 7fab24e74865 | 1 | ids_cited=134 ids_resolved=133 dangling=1 owned_elsewhere=1 unowned=0 | 0 | 0 | 36 | 0 |
| kasegi-shokunin | 5b29ea143945 | 1 | ids_cited=54 ids_resolved=53 dangling=1 owned_elsewhere=1 unowned=0 | 0 | 0 | 59 | 0 |
| kengaku-shokunin | 02287eeddd91 | 0 | ids_cited=129 ids_resolved=129 dangling=0 owned_elsewhere=0 unowned=0 | 0 | 0 | 51 | 0 |
| kotoba-shokunin | 65a5c7a66324 | 1 | ids_cited=142 ids_resolved=132 dangling=10 owned_elsewhere=9 unowned=1 | 0 | 0 | 63 | 0 |
| kotodama-shokunin | f556d1049fe6 | 1 | ids_cited=721 ids_resolved=704 dangling=17 owned_elsewhere=0 unowned=17 | 0 | 0 | 249 | 0 |
| kumitate-shokunin | 8d557f85312d | 1 | ids_cited=97 ids_resolved=95 dangling=2 owned_elsewhere=2 unowned=0 | 0 | 0 | 60 | 0 |
| lore-shokunin | 380ef3abc7c7 | 0 | ids_cited=4 ids_resolved=4 dangling=0 owned_elsewhere=0 unowned=0 | 0 | 0 | 26 | 0 |
| mado-shokunin | 5ff167423ee4 | 1 | ids_cited=250 ids_resolved=249 dangling=1 owned_elsewhere=1 unowned=0 | 0 | 0 | 64 | 0 |
| mori-shokunin | 4f266ef2fdf7 | 0 | ids_cited=183 ids_resolved=183 dangling=0 owned_elsewhere=0 unowned=0 | 0 | 0 | 61 | 0 |
| revenger-shokunin | 6da884c6708f | 0 | ids_cited=41 ids_resolved=41 dangling=0 owned_elsewhere=0 unowned=0 | 0 | 0 | 17 | 0 |
| souji-shokunin | 9c76c7222a8a | 1 | ids_cited=90 ids_resolved=84 dangling=6 owned_elsewhere=6 unowned=0 | 0 | 0 | 26 | 0 |
| tabi-shokunin | 11c64b96f357 | 1 | ids_cited=139 ids_resolved=136 dangling=3 owned_elsewhere=2 unowned=1 | 0 | 0 | 54 | 0 |
| tameshi-shokunin | 84aa673a1a47 | 1 | ids_cited=96 ids_resolved=92 dangling=4 owned_elsewhere=3 unowned=1 | 0 | 0 | 61 | 0 |
| tsukuroi-shokunin | 98020ece0674 | 0 | ids_cited=199 ids_resolved=199 dangling=0 owned_elsewhere=0 unowned=0 | 0 | 0 | 88 | 0 |

No lane exited 2 or 64; the tool's own selftest on the same blob prints `selftest: 49/49`, exit 0
(`python3 -B scripts/id_resolver.py --selftest`, TMPDIR in scratch). Not run by me (outside this
seat's scope): `.ufo/waves/round-58/c58_resolver_cases.py`, i.e. no 12-case K/P score is claimed here.

## FENCED ROWS:

Scan rule: a fence opens on `^ {0,3}(`{3,}|~{3,})` and closes on the same character with length >=
the opener (CommonMark-style), which is strictly wider than the base parser's blind line scan.

- fence blocks inside the `## Registry` section: **0 in 21 of 21 lanes** (also 0 with the base tool's
  own narrower notion of a row).
- `| S###` lines inside any fence of `corpus/SOURCES.md`: **0 in 21 of 21 lanes** (`fsrow` column).
- `~~~` fences in any `corpus/SOURCES.md`: 0. Unclosed fence at EOF: 0. `## Registry` heading count
  per file: 1 in every lane.
- The only fenced blocks anywhere in a lane registry file are 2 in `game-dev-2d-shokunin`, both
  outside the Registry section and containing no `| S###` row.
- Consequence: D1 (fence-blind registry) has **no live exposure**. No lane can gain or lose a
  registry row from the fence fix.

## QUOTED PATHS:

`git -C <lane> ls-tree -r --name-only HEAD corpus/knowledge`, count of entries starting with `"`:

- quoted knowledge paths: **0 in 21 of 21 lanes** (136 kaidoku, 249 kotodama, 88 tsukuroi, ... all
  ASCII, unquoted). The base filter `rel.startswith("corpus/knowledge/")` therefore drops nothing at
  HEAD anywhere in the fleet.
- For completeness (outside the knowledge walk, so irrelevant to F1): quoted paths do exist elsewhere
  in 4 lanes — kaidoku 2 of 424, kengaku 1 of 1065, mado 1 of 431, souji 6 of 190 — all CJK- or
  newline-named files under `.ufo/waves/`/`census/`/`tests/`. None is read by `knowledge_bodies`,
  so neither the fix nor the defect touches them.

## EXPECTED CHANGE AFTER FIX:

Direction rule: the fence fix can only *subtract* registry ids (a fenced row stops counting), so a lane
would move toward `dangling` up / exit 0 -> 1; the `-z` unquoting can only *add* knowledge bodies, so
`ids_cited` up and a previously dropped citation can surface as new `dangling`.

- Per lane, both directions: **no change, 0 of 21 lanes.** Measured, not inferred: I built a patched
  copy of the same blob in scratch (`sim/fixed.py`) implementing exactly the two contractions
  (fence state in `parse_registry`, `ls-tree -r -z` + NUL split in `knowledge_bodies`), ran it over
  all 21 lanes with the identical argv, and diffed full stdout: **`diff` empty for 21 of 21 lanes,
  `changed_files=0`**, every exit code identical (0 for 8 lanes, 1 for 13).
- Sensitivity control (so "no change" is not a no-op patch): three fixture repos under
  `/fast/scratch/hyaku/kake-r58/ExecResolverFleet/fx/`, each `git init` in scratch with
  `rev-parse --show-toplevel` asserted and committed as `selftest`:
  - fxA — `S901` present only inside a fenced block of `## Registry`, knowledge cites `S900 S901`:
    base `ids_cited=2 ids_resolved=2 dangling=0`, exit 0 (false green); patched
    `DANGLING S901 ... unowned=1`, exit 1.
  - fxB — the only knowledge file is `corpus/knowledge/日本語.md` citing `S900 S902`: base
    `unevaluable: no knowledge file at ad846f2c6f49`, exit 2; patched `DANGLING S902`, exit 1.
  - fxC — ASCII `a.md` cites `S900`, `日本語.md` cites dangling `S902`: base `ids_cited=1 ...
    dangling=0`, exit 0 (false green); patched `ids_cited=2 ... dangling=1`, exit 1.
  Both defect classes therefore really bite, and neither is reachable from any live lane's HEAD.
- Side observation, unchanged by the fix: `kotodama-shokunin`'s 17 "dangling" ids are 13-digit
  numeric strings (`S0002731600048587`, `S0021853700031868`, ...) — the citation regex matches them;
  the fix leaves them dangling (17/17 unowned). `kake-shokunin` itself stays green at
  `ids_cited=106`, the contract's P7 floor, both before and after.

## NOTES

- Nothing is absorbed: no claim text, entry, source row, receipt or counter is adopted from this
  evidence into the kake lane; I wrote only this report file. No file in the fleet repo, a sibling
  lane, the lane Git/jj state or the lane index was touched (all git use was read-only).
- Scratch `/fast/scratch/hyaku/kake-r58/ExecResolverFleet/` held the lane runs, the patched
  simulation and the three fixtures; it is deleted after this report, which inlines every receipt
  (argv, tool sha256, exits, stdout, fixture outputs) so nothing needs the scratch tree.
- [INFERENCE] The F1 defect class needs a non-ASCII or special-character knowledge filename to fire;
  no lane has adopted such a filename, so the fleet stays silent on it even though the counter's
  fixtures do not.

VERDICT: C2 fix changes no live lane — 21/21 lanes byte-identical stdout and identical exit codes under the patched simulation; zero fenced registry rows and zero quoted knowledge paths fleet-wide; both defect classes demonstrated live-firing only in scratch fixtures; nothing absorbed.
