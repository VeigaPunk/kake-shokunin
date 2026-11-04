# ScribeProvince — round 78, w1 (lane documentation state)

**Verdict: routed defect 2 is corrected append-only and the round-78 meta-robots state is documented;
the four `SHONEN.md` box lines restate measured populations with the markers unchanged.**
`PROVINCE.md` and `corpus/README.md` now record the round-77 sitemap move and the round-78
meta-robots contract and pending state; the C3 matrix receipt did not exist at write time, and neither
file claims a C3 result.

Seat: scribe (leaf). Lane `/home/vgpnk/Projects/shokunin/kake-shokunin`; lane HEAD
`78711a628ad7e1c23cefcb9f9e345a0cc240c25b`; round-78 base
`fe50945399a386b48678b1f2051fdbe8a77b10bd`. Every path below is absolute or lane-relative to that
root. No commit, checkout, reset, stash or other git/jj mutation; read-only `git show`/`ls-tree`/
`cat-file`/`log`/`status`/`rev-parse` only. No tool install or upgrade; pacman untouched; no network
call.

## 1. Edits, before → after (file:line)

| file | before | after |
|---|---|---|
| `PROVINCE.md` | 524 lines; ended at `PROVINCE.md:524` with the round-76 block; no round-77 correction, no round-78 block | 610 lines; `## Round-77 correction — sitemap containers and formats held (routed defect 2, 2026-11-03)` at `PROVINCE.md:526-556`; `## Round-78 meta-robots frontier step` at `PROVINCE.md:558-610`, with `**State at write time**` at `:596-610` |
| `corpus/README.md` | 522 lines; frontier ground-map table ended at `corpus/README.md:130` (`… CrUX origin membership … S438`); no r77 correction section; no r78 coverage section | 573 lines; new table row at `corpus/README.md:131` (`… Sitemap containers and formats … r77 (map row added r78) … S012 S447 S448`); `## Round-77 correction — sitemap containers and formats (2026-11-03, routed defect 2)` at `:525-544`; `## Coverage — round 78 (2026-11-03)` at `:546-573`, row at `:550`, state paragraph at `:563-573` |
| `SHONEN.md` | 12 lines; box bullets at `:6`, `:8`, `:10`, `:12` cited no population/revision and box 4 said `0 of 63` | 12 lines; same bullet positions restated (details below); markers at `:5` `[~]`, `:7` `[ ]`, `:9` `[~]`, `:11` `[~]` byte-identical |

Diffstat for the three owned files (`git diff --numstat -- PROVINCE.md SHONEN.md corpus/README.md`):
`86/0 PROVINCE.md`, `4/4 SHONEN.md`, `51/0 corpus/README.md` — insertions only outside the four
SHONEN bullet rewrites; no old PROVINCE/README line was altered.

SHONEN line changes:

- `SHONEN.md:6` (box 1): `… primary evidence \`SKILL.md\` — 77/77 …` → `… \`SKILL.md\` (population:
  that one file, byte-identical from the round-77 base \`a2cc5f51\` to the carrier \`78711a62\`) —
  re-measured at the carrier \`78711a62\`: 77/77 …`. Counts unchanged (77/77 ids, 18 tables, 105
  registry rows, 1 checklist heading).
- `SHONEN.md:8` (box 2): `56 round sections and 98 named wave-receipt paths` → `57 round sections and
  100 named wave-receipt paths (the row's recorded 56/98 date from \`a2cc5f51\`; both checks are
  \`count_at_least\` floors, so growth is not drift)`. The gap sentence (the absent
  `.ufo/waves/round-47/verification/offline-sweep-r46-verdict-time.txt`) and the flip sentence are
  kept; the `[ ]` marker is untouched.
- `SHONEN.md:10` (box 3): population/revision sentence added; `0 missing script or counter paths, 0
  missing \`python3 -B\` targets` unchanged; the scope-exclusion sentence is unchanged.
- `SHONEN.md:12` (box 4): `0 of 63 entries` → `0 of 65 entries` with the measured chain (65 in the
  worktree at `2026-11-03T23:44-03:00`; 64 at the committed lane HEAD `78711a62` and at the
  round-78 base `fe509453`; 63 at the base the row recorded, `a2cc5f51`) and the two re-derivation
  commands.

Digests after writing (`sha256sum`, 2026-11-03T23:47-03:00): `PROVINCE.md`
`1b1d215ef21c4e86922c11f2d855823fe9ae313f3b2b738956b1554622296e31` (610 lines), `SHONEN.md`
`30053141a71cf9b66fc36db039edd30b291581c7c8677f62a8b681a48f7e7e7d` (12 lines), `corpus/README.md`
`110e7ccb53f7a13ff1c22c09bd50cf91d60ab3625ac980dd2fe9aa72ff54cd1a` (573 lines).

## 2. Round-77 routed defect 2 — what the correction states and its evidence

The old lines stay in place and are named as historical: `PROVINCE.md:328` (round-38 "Still open …
sitemaps …"), `PROVINCE.md:342-343` (round-39 "Still open: gzip, live fetch, text/RSS sitemaps,
robots cross-submission …"), and the README `Untouched ground` bullet "Sitemap gzip, text/RSS
sitemaps, robots `Sitemap:` cross-submission" (read at `corpus/README.md:161-162` before the row
insertion; the new prose names the bullet by text, not line, because the insertion shifts it).

What moved, with the entry and the tool as evidence:

- Entry `corpus/knowledge/sitemap-formats.md` — `git cat-file -s` = 13,214 bytes; sha256
  `72b20b1f9a424546c9a2d0ad3cc4ced489926156a49e1f3e8d6ec1cd8410025f`, identical at `3db64e09` and
  `78711a62`; cites S012 (re-opened), S447 (RFC 1952) and S448 (RFC 4287).
- Tool `scripts/sitemap_audit.py` at `3db64e09` — 32,325 bytes; sha256
  `f767af770652437d7af18c693dff7cafd64d7f79c38cec36a20e6c4e0bbe9176`, identical at `78711a62`;
  gzip container by magic `1f 8b` (never the name, cap after expansion), plain text, RSS 2.0, Atom
  1.0, `format_unsupported`. The delivered selftest reports `PASS 271/271` (235 round-39 + 36
  round-77 declarations; `grep -c 'add("r77_'` on
  `git show 3db64e09:scripts/sitemap_audit_selftest.py` → 36). I quote that tally from
  `.ufo/waves/round-77/w1/ExecSitemapFormats.md` §3 and the verifier §2 C2; **I did not run it**.
- Matrix `.ufo/waves/round-77/controls/after-c2-matrix.txt`:
  `C2 revision=3db64e09550c9f8309f6c1077f9f7df6243cb446 cases=20 decided=20 correct=20 wrong=0
  constants_failed=4/4 met=true`, exit 0; base
  `.ufo/waves/round-77/controls/base-c2-matrix-v2.txt` `correct=2 wrong=18
  constants_failed=4/4 met=false`, exit 1.
- Admission: `corpus/lessons/round-77-verifier-spotcheck.md` §2 C2 ("Verdict: improved"), §5
  expansion (knowledge `.md` files 63 → 64), §7 `CLOSURE kake r77 status=ok admitted=true`; §6
  defect 2 is this routed defect.
- README frontier ground map: row added for `knowledge/sitemap-formats.md` (r77), rows
  `S012 S447 S448`, dated `(map row added r78)`.

## 3. Round-78 block — what it says

Both files state only what `.ufo/waves/round-78/contract.md` §C3 fixes: the
`kake-meta-robots-manifest/v1` shape, local-HTML-only reads, ASCII-case-insensitive `name` matching,
`<head>`-only placement (`meta_robots_tag_outside_head`), comma tokenization with trimmed
case-insensitive tokens, the full directive vocabulary, `none`/`all` expansion, the cross-element
most-restrictive merge, findings that never enter the effective set
(`meta_robots_invalid_value`, `meta_robots_unknown_directive`), the `["follow","index"]` default,
sorted `expect.effective`/`expect.findings` comparison (`meta_robots_expected_mismatch`), exits
0/1/2/64, `--selftest` ≥ 40, the g01–g24 case families (≥ 20 cases) and the predicate
`met <=> cases == decided and correct == cases and constants_failed == 4`, with four degenerate
constants that must each fail at least one case.

Refusals are stated: `X-Robots-Tag` response headers (owned by `scripts/response_snapshot.py` /
`scripts/header_audit.py`), rendering/rendered DOM, crawler behaviour, whether any live property
carries a correct declaration, and ranking/indexing outcomes. Both files say no live property was
measured, no network call was made, and publishing stays operator-owned.

## 4. What I could not state, and why

1. **The C3 matrix receipt.** At 2026-11-03T23:46-03:00 the counter
   `.ufo/waves/round-78/c78_meta_robots_matrix.py` had appeared, but
   `.ufo/waves/round-78/controls/after-c3-matrix.txt` did not exist, and the tool/entry were still
   being rewritten (see §5). The docs therefore name the receipt as **pending** and claim no
   `cases`/`decided`/`correct`/`constants_failed` value.
2. **C1's committed-carrier measurement.** `c78_shonen_population.py` reads the ledger from the
   revision (`git show <rev>:corpus/knowledge/shonen-ledger.json`), so at `78711a62` it still sees
   the old ledger: `rows_with_population=0 undeclared=4 met=false`, exit 1, although the worktree
   ledger now declares all four populations (box 4 count 65). The only green receipt,
   `.ufo/waves/round-78/controls/after-c1-population.txt`, measures fixture revision
   `1729712e4ee5c2960bcad1c3d55fe8babbf9f1b7`, not the lane; I did not run it.
3. **Any verdict/admission for C1/C2/C3.** Not on disk and not this seat's claim; the docs assert
   none.
4. **Box-4 population at a committed carrier.** No committed revision carries 65 yet. Measured
   chain: 63 at `a2cc5f51`, 64 at `fe509453`, 64 at `78711a62`, 65 in the worktree once
   `corpus/knowledge/meta-robots-directives.md` landed. `SHONEN.md:12` states the 65 with the
   revision chain rather than silently replacing the base value.

## 5. Caveat owed to the L1: point-in-time digests moved under me

The C3 entry and tool were rewritten while I measured: entry `202fdee7…` (20,503 B, ~23:44:2x) →
`4dac2a16…` (20,604 B, mtime 23:44:46) → `da328e56…` (23:46:23); tool `c5bd4d8c…` (62,119 B,
23:44:57) → `d32fb580…` (23:46:23). I first wrote the state paragraphs citing an intermediate digest,
then removed every C3 digest and selftest tally rather than ship a number that was already
superseded. The docs now cite presence plus the carrier re-cut as the measurement. A `selftest 83/83
passed` (exit 0) was observed on the 23:45 bytes (`c5bd4d8c…`) but is deliberately **not** claimed
for the carrier. The L1 should re-cut both the digest and the tally at the integration commit.

## 6. Commands used to re-measure every count I wrote (verbatim, exit status)

From `/home/vgpnk/Projects/shokunin/kake-shokunin`, `S=/fast/scratch/hyaku/kake-r78/ScribeProvince`,
`TMPDIR=$S/tmp`:

```
$ git rev-parse HEAD
78711a628ad7e1c23cefcb9f9e345a0cc240c25b                                     # exit 0

$ git ls-tree -r --name-only a2cc5f51 -- corpus/knowledge | grep -c '\.md$'
63                                                                           # exit 0
$ git ls-tree -r --name-only fe509453 -- corpus/knowledge | grep -c '\.md$'
64                                                                           # exit 0
$ git ls-tree -r --name-only 78711a62 -- corpus/knowledge | grep -c '\.md$'
64                                                                           # exit 0
$ ls corpus/knowledge/*.md | wc -l
65                                                                           # exit 0 (worktree, C3 entry present)

$ python3 -B .ufo/waves/round-77/c77_shonen_ledger.py \
    --root /home/vgpnk/Projects/shokunin/kake-shokunin \
    --revision 78711a628ad7e1c23cefcb9f9e345a0cc240c25b --json
C1 revision=78711a628ad7e1c23cefcb9f9e345a0cc240c25b boxes=4 evidenced=3 gap=0 \
  unexamined=0 mismatches=2 met=false
  finding: observation-differs box 2 b2-rounds — recorded 56 but re-derived 57
  finding: observation-differs box 2 b2-receipts — recorded 98 but re-derived 100
                                                                             # exit 1; boxes 1/3/4 agree, no exact mismatch
$ python3 -B .ufo/waves/round-78/c78_shonen_population.py \
    --root /home/vgpnk/Projects/shokunin/kake-shokunin \
    --revision 78711a628ad7e1c23cefcb9f9e345a0cc240c25b
C1v1 revision=78711a628ad7e1c23cefcb9f9e345a0cc240c25b rows=4 rows_with_population=0 \
  undeclared=4 stale_populations=0 exact_mismatches=0 floor_violations=0 growth_tolerated=2 met=false
                                                                             # exit 1 (revision blob is the pre-r78 ledger)

$ python3 -B scripts/meta_robots_audit.py --selftest --work $S/mr-selftest
selftest 83/83 passed                                                        # exit 0 (bytes sha256 c5bd4d8c…, 23:45)

$ git show 3db64e09:scripts/sitemap_audit.py | sha256sum
f767af770652437d7af18c693dff7cafd64d7f79c38cec36a20e6c4e0bbe9176  -           # exit 0
$ git show 3db64e09:corpus/knowledge/sitemap-formats.md | sha256sum
72b20b1f9a424546c9a2d0ad3cc4ced489926156a49e1f3e8d6ec1cd8410025f  -           # exit 0
$ git cat-file -s 3db64e09:scripts/sitemap_audit.py
32325                                                                        # exit 0
$ git cat-file -s 78711a62:corpus/knowledge/sitemap-formats.md
13214                                                                        # exit 0
$ git show 3db64e09:scripts/sitemap_audit_selftest.py | grep -c 'add("r77_'
36                                                                           # exit 0

$ ls -d .ufo/waves/round-78/cases/*/ | wc -l
34                                                                           # exit 0 (case directories at 23:46)

$ sha256sum PROVINCE.md SHONEN.md corpus/README.md
1b1d215e…  PROVINCE.md   (610 lines)
30053141…  SHONEN.md     (12 lines)
110e7ccb…  corpus/README.md  (573 lines)                                     # exit 0
$ git diff --numstat -- PROVINCE.md SHONEN.md corpus/README.md
86  0  PROVINCE.md
4   4  SHONEN.md
51  0  corpus/README.md                                                      # exit 0
$ git status --porcelain=v1 -- PROVINCE.md SHONEN.md corpus/README.md
 M PROVINCE.md
 M SHONEN.md
 M corpus/README.md                                                          # exit 0; no other path written by this seat
```

## 7. Routed observations (reported, not judged)

1. **Case-set population vs the contract's enumeration.** The landed case set has 34 directories:
   the contract's g01–g24 families plus lettered/extension variants (`g08b`, `g12a`–`g12d`,
   `g16b`, `g19b`, `g25`, `g26a`, `g26b`, `g27`). The contract says "one case each unless a family
   says otherwise; ≥ 20 cases" and enumerates g01–g24; whether the extra ids are in-population is
   the C3 owner's declaration, not mine. Reported for the L1's integration read.
2. **Line-number shift in `corpus/README.md`.** The r77 map row was inserted at `:131`, so every
   line below it moved by +1. The new prose therefore cites the `Untouched ground` bullet by its
   text and `PROVINCE.md` by its unchanged absolute line numbers.
3. **`SHONEN.md` box-2 counts moved because `LOG.md` changed in round 77 after the ledger's
   derivation.** `b2-rounds` 56 → 57 and `b2-receipts` 98 → 100 are `count_at_least` growth, which
   C1's grading tolerates; the box stays `[ ]` because `b2-missing` is still 1 (the round-47
   receipt is absent at the revision) and the flip is unchanged.

## 8. Hygiene

- Scratch tree `/fast/scratch/hyaku/kake-r78/ScribeProvince` was used only for `TMPDIR`, the c77
  JSON capture and the tool selftest; it is removed with `rm -rf` before yield (verified absent
  afterwards). Nothing was left in `/tmp`.
- No file outside `PROVINCE.md`, `SHONEN.md`, `corpus/README.md` and this report was written by this
  seat; `considerthese/`, `SCORECARD.md`, `LOG.md`, `SKILL.md`, the ledger, the registry, `.ufo/state/`
  and `MANIFEST.json` were read only or not touched.
- No tool installed or upgraded; no pacman transaction; no network call.
