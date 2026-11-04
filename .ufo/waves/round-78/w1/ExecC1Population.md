# ExecC1Population — C1 (calibration) implementation

**Verdict: C1 is implemented and green on the projected carrier** — `C1v1 revision=1729712e… rows=4 rows_with_population=4 undeclared=0 stale_populations=0 exact_mismatches=0 floor_violations=0 growth_tolerated=2 met=true` (exit 0). The base receipt re-runs byte-identically (`sha256 bb3ddcda58e3b317788f0102ab038b52ad84d1df64475e6972a66ef6e0d66c09`). All four rows now declare the population their checks scan, with provenance notes; the two `count_at_least` records stay dated floors and their carrier re-derivations are recorded in the notes; no exact record was stale.

## 1. Population assigned to each row, and why

| box | population | why |
|---|---|---|
| 1 | `{"kind":"file","path":"SKILL.md","count":1}` | all four checks (b1-ids/-tables/-registry/-checklist) declare `path: SKILL.md`; nothing else is read |
| 2 | `{"kind":"file","path":"LOG.md","count":1}` | all three checks (b2-rounds/-receipts/-missing) declare `path: LOG.md` |
| 3 | `{"kind":"file","path":"SKILL.md","count":1}` | both checks (b3-scripts/-invocations) declare `path: SKILL.md` |
| 4 | `{"kind":"files","dir":"corpus/knowledge","suffix":".md","exclude":["freshness-*.json"],"count":65}` | b4-lanes' own glob is `corpus/knowledge/*.md`; `freshness-*.json` is excluded by name and the exclude is inert under `suffix: ".md"` (kept as the A11 scope mirror) |

Box-4 count chain, measured with `git ls-tree -r --name-only <rev> corpus/knowledge | grep -c '\.md$'`:

- **63** at `a2cc5f51002433e11cc3d2f70e650a6c60ad5e68` — the round-77 record (so the old note's 63 was correct then, stale now);
- **64** at base `fe50945399a386b48678b1f2051fdbe8a77b10bd` and at lane HEAD `78711a628ad7e1c23cefcb9f9e345a0cc240c25b` (no `corpus/knowledge` delta between them);
- **65** at the round-78 carrier: 64 + ScribeMetaRobots' `corpus/knowledge/meta-robots-directives.md` (contract §C3 deliverable; confirmed by KakeR78). A pre-C3 carrier (64) is recorded red — `carrier-before-c3.txt`.

Ledger changes (file sha256 `828ab893e9e69693844bd8bd975cede3874473b42670af8010faf30a36f51adf`):

- new top-level `population-notation` documents the two accepted shapes, the exact-per-revision rule, the floor grading rule and the provenance revisions; the schema string is unchanged (`shonen-ledger/v1`).
- each row gained `population` and a provenance note. Box 3's population sentence was merged into its existing scope-limit note rather than added as a second `note` key (duplicate-key scan over the whole file: clean; row keys are `box,marker,title,status,scopes,population,note,checks`, plus `reason`/`flip` on box 2).
- box-4 check note and row note now state 63 → 64 → 65 with revisions; the stale “63” prose is corrected.

## 2. Observations re-measured under the counter's grading rule

Exact kinds — all re-derive exactly at base and carrier, so nothing was rewritten:

`b1-ids {ids:77,resolved:77,unresolved:0}` · `b1-tables 18` · `b1-registry 105` · `b1-checklist 1` · `b2-missing 1` · `b3-scripts 0` · `b3-invocations 0` · `b4-lanes 0`.

`count_at_least` floors — kept as recorded floors, dated measurement added to the row/check notes:

- `b2-rounds`: recorded 56 (a2cc5f51, highest round 76) → re-derived **57** at the carrier (the `## Round 77` section, `LOG.md:2608`). Growth, not drift.
- `b2-receipts`: recorded 98 (a2cc5f51) → re-derived **100** at the carrier (round-77 section adds two receipt paths). Growth, not drift.

The carrier run therefore reports `growth_tolerated=2`, `exact_mismatches=0`, `floor_violations=0` — the predicate does not count tolerated growth, and no floor was violated (nothing shrank).

## 3. Commands run (verbatim) and exit codes

```
# populations / provenance
git -C /home/vgpnk/Projects/shokunin/kake-shokunin rev-parse HEAD                      # 78711a628ad7e1c23cefcb9f9e345a0cc240c25b
git ls-tree -r --name-only a2cc5f51… corpus/knowledge | grep -c '\.md$'                # 63
git ls-tree -r --name-only fe509453… corpus/knowledge | grep -c '\.md$'                # 64
git ls-tree -r --name-only 78711a62… corpus/knowledge | grep -c '\.md$'                # 64
git diff --name-status fe509453… HEAD -- corpus/knowledge                              # (empty)

# base receipt re-run
python3 -B .ufo/waves/round-78/c78_shonen_population.py --root /home/vgpnk/Projects/shokunin/kake-shokunin --revision fe50945399a386b48678b1f2051fdbe8a77b10bd
# exit 1; cmp against controls/base-c1-population.txt → identical; both sha256 bb3ddcda…

# selftest
python3 -B .ufo/waves/round-78/c78_shonen_population.py --selftest --work /fast/scratch/hyaku/kake-r78/ExecC1Population/selftest2
# exit 0; selftest: 9/9 passed

# measure authority unchanged on the extended ledger (fixture revision)
python3 -B .ufo/waves/round-77/c77_shonen_ledger.py --root <fixture> --revision <fixture-rev>
# exit 1; only the two tolerated-growth findings above; 0 exact mismatches

# projected carrier (HEAD tree + edited ledger + C3 doc path)
git -C /home/vgpnk/Projects/shokunin/kake-shokunin archive HEAD | tar -x -C $S/carrier
cp <lane>/corpus/knowledge/shonen-ledger.json $S/carrier/corpus/knowledge/shonen-ledger.json
# (placeholder created at corpus/knowledge/meta-robots-directives.md; real file absent at cut time)
git -C $S/carrier init -q && git -C $S/carrier rev-parse --show-toplevel   # == $S/carrier
git -C $S/carrier -c user.name=fixture -c user.email=fixture@localhost commit -qm "c1 fixture"
# fixture rev 1729712e4ee5c2960bcad1c3d55fe8babbf9f1b7; knowledge .md count 65
python3 -B .ufo/waves/round-78/c78_shonen_population.py --root $S/carrier --revision 1729712e…
# exit 0; met=true (receipt controls/after-c1-population.txt)

# pre-C3 carrier (64 .md, declared 65)
python3 -B .ufo/waves/round-78/c78_shonen_population.py --root $S/prec3 --revision 86f424e3…
# exit 1; S1 box 4: declared=65 derived=64; stale_populations=1

# fabricated population (declared 999, derived 65)
python3 -B .ufo/waves/round-78/c78_shonen_population.py --root $S/fake --revision 731c17d8…
# exit 1; S1 box 4: declared=999 derived=65; rows_with_population=4; stale_populations=1
```

JSON integrity: `json.load` with an `object_pairs_hook` that rejects duplicate keys → clean; 4 rows; populations `[SKILL.md·1, LOG.md·1, SKILL.md·1, corpus/knowledge·.md·65]`.

## 4. Receipts (retained bytes, sha256)

- `controls/after-c1-population.txt` — pre-integration projected carrier, stdout + `exit=0`; `sha256 5d1cddb807884bf422b37047fdd33641339a40832e73f453d9dfb5e27047d4a1`. Construction and the integration re-cut command are recorded in `w1/ExecC1Population/README.txt`. **KakeR78 will re-cut this at the integration commit.**
- `w1/ExecC1Population/fake-population.txt` — fabricated count 999 → `stale_populations=1`; `sha256 037ed0fa…`.
- `w1/ExecC1Population/carrier-before-c3.txt` — 64-file carrier against declared 65 → `stale_populations=1`; `sha256 505f3b2e…`.
- `w1/ExecC1Population/selftest.txt` — 9/9, exit 0; `sha256 fed0ecd1…`.
- `w1/ExecC1Population/base-c1-population.rerun.txt` + `base-rerun-identity.txt` — byte-identical base receipt; `sha256 bb3ddcda…` both sides.
- `w1/ExecC1Population/sha256s.txt` — all receipt digests; `README.txt` — construction note.

## 5. Residual holes in the counter (reported, not fixed — predicate frozen)

1. **Population counts are graded exact while corpus counts are floors in this lane** (SKILL.md freshness section). Adding `corpus/knowledge/*.md` flips C1 red unless the ledger count moves in the same commit. KakeR78 accepted this as snapshot semantics and is adding the co-update as a round-78 QUALITY criterion. Flip for a later round: a floor/dirty population kind, or exclude-by-name for entries the round itself adds.
2. **The counter checks that the declared count re-derives, not that the declared kind/path is the surface the row's checks scan.** A row could declare `SKILL.md` while its checks read `LOG.md` and still be green if the count matches. Routed to round 79; flip: a row whose population kind/path disagrees with its checks' `path`/`params.glob` is red.
3. `classify()` recovers the check kind from `subject.split()[-1]`; a change in c77's subject format would route a floor finding to `exact` (conservative false red, never a permissive error). Also, two checks sharing an id across rows would collide in the kind map (last wins).
4. `regex_count` with `params.min` is a lower-bound shape but is graded exact; a growing `regex_count` would be a false red.

## 6. Coordination

- KakeR78 confirmed `count: 65` and that the C3 entry will be in the carrier; it re-cuts `controls/after-c1-population.txt` at the integration commit.
- ScribeProvince's dispatch still says “64 at the carrier” for SHONEN.md box 4; that is stale once `corpus/knowledge/meta-robots-directives.md` lands — the carrier line must say 65, or the integer must move to 64 in both places. I did not touch SHONEN.md.

## 7. Hygiene

Scratch `$HYAKU_SCRATCH/kake-r78/ExecC1Population` was deleted before yield (verified absent). No tool installs (nothing installed or upgraded; pacman untouched). No mutating git/jj command in the lane; the only commits were inside scratch fixtures after `git rev-parse --show-toplevel` was asserted to be the fixture dir. No write outside the lane paths above; `SHONEN.md`, the round-77 counter and other claims' files untouched. `corpus/knowledge/shonen-ledger.json` is the only tracked file changed; its sha256 is `828ab893e9e69693844bd8bd975cede3874473b42670af8010faf30a36f51adf`.
