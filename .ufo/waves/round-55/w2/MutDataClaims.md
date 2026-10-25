# MutDataClaims

ATTACKS: whether the two round-55 counters notice damage to the DATA they judge, at revision
a7a548e102b71bd16b0a6ddafa469393a2c98b69 — C1 `.ufo/waves/round-55/c55_readme_index.py` vs
`corpus/README.md` §Coverage map + `corpus/knowledge/`; C2 `.ufo/waves/round-55/c55_quote_truth.py`
vs `corpus/SOURCES.md` rows S372/S373/S418, `corpus/lessons/round-55.md` §Gate,
`.ufo/waves/round-55/sources/` (S372/S373/S418.html + receipts.json), and
`.ufo/waves/round-55/assimilation/validate/`. 15 data mutants (8 C1, 7 C2), each in its own
disposable scratch clone; both counters run on every mutant.

## Baseline and method (commands run)

- Baseline: `D0=$(mktemp -d /tmp/mutbase.XXXXXX) && git clone -q --no-hardlinks
  /home/vgpnk/Projects/shokunin/kake-shokunin "$D0" && git -C "$D0" checkout -q a7a548e102b71…`,
  then `python3 -B "$D0/.ufo/waves/round-55/c55_readme_index.py" --root "$D0" --revision
  a7a548e102b71…` → `index_mismatches=0 knowledge_files=49 met=True`, `EXIT=0`; and
  `c55_quote_truth.py --root "$D0" --revision a7a548e102b71…` → `8/8 met=True`, `EXIT=0`.
  Selftests in the same clone (`--selftest`, cwd=$D0): C1 `35/35`, C2 `50/50`, both exit 0.
  Baseline green ⇒ every non-zero exit below is attributable to the mutant, not the environment.
- Per mutant: `bash /tmp/runmut.sh Mxx`, which runs `D=$(mktemp -d /tmp/mutMxx.XXXXXX) && git clone
  -q --no-hardlinks /home/vgpnk/Projects/shokunin/kake-shokunin "$D" && git -C "$D" checkout -q
  a7a548e102b71… && python3 /tmp/mut.py Mxx "$D" && git -C "$D" add -A && git -C "$D"
  -c user.name=mut -c user.email=mut@local commit -qm "w2 mutant Mxx (scratch clone only)"`, then
  both counters as `--root "$D" --revision <clone commit>`. Setup failure exits 9 before any
  counter runs. `/tmp/mut.py` asserts every replacement target occurs exactly once (count==1) and
  prints the after-sha256 of each touched path. Identity `mut <mut@local>` was used only inside
  the scratch clones; the lane repo's index and jj state were never touched (no
  add/commit/stash/checkout/reset/pull/push against the lane; only read-only `show`/`ls-tree`).
- Survivor rule applied: attacked counter exit 0 ⇒ SURVIVOR. The other counter's exit is recorded
  but not judged (disjoint surface: C1 reads README+knowledge tree, C2 reads registry/lesson/
  sources/validate; C1-mutants leaving C2 at 0 and vice versa are expected).
- Discarded runs: five earlier invocations (ids D01–D05) failed inside `/tmp/mut.py` (KeyError:
  function names are M01…, ids passed were D01…) BEFORE any commit; the `C1_EXIT=1`/`C2_EXIT=2`
  lines they printed were shell artifacts (mutator's own exit; empty `--revision` usage error) and
  are not counter results. No mutant was applied in those runs.

## MUTANTS

| id | edit (all inside its own scratch clone) | C1 exit | C2 exit | observed detector output (attacked counter) |
|---|---|---|---|---|
| M01 | README fleet-registry row Coverage cell → `TBD` | 1 | 0 | C1 `index_mismatches=1 met=False`, `thin=1: fleet-registry.md` |
| M02 | drift-detection row Coverage ← publish-channels row's text | 1 | 0 | C1 `index_mismatches=2 met=False`, `thin=1: drift-detection.md` + `duplicate=1` |
| M03 | delete `corpus/knowledge/fleet-registry.md` | 1 | 0 | C1 `deleted=1` + `dangling=1: knowledge/fleet-registry.md`; knowledge_files 49→48 |
| M04 | fleet-registry.md H1 `registry`→`register` | 1 | 0 | C1 `head_changed=1: fleet-registry.md` |
| M05 | add unindexed `corpus/knowledge/zzz-unindexed-mutant.md` | 1 | 0 | C1 `unindexed=1: zzz-unindexed-mutant.md`; knowledge_files 49→50 |
| M06 | append a second `## Coverage map` heading to README | 2 | 0 | C1 refuses: `expected exactly one '## Coverage map' section, found 2` (EXIT=2, unevaluable — not a pass) |
| M07 | fleet-registry row Entry → `knowledge/fleet-registry-gone.md` | 1 | 0 | C1 `unindexed=1: fleet-registry.md` + `dangling=1: knowledge/fleet-registry-gone.md` |
| M08 | swap Entry cells: fleet-registry ↔ vault-properties rows | 1 | 0 | C1 `thin=1: fleet-registry.md` (vault side not flagged — see observations) |
| M09 | one character inside a quoted span of EACH entry (S372 一→二; S373 で→に; S418 っ→つ) | 0 | 1 | C2 `6/8 met=False`: C5 "not a raw substring of the retained body" ×3 + C7 "validated scratch entry differs from the landed entry" ×3 |
| M10 | Gate quote S372 lengthened `…みなされます` → `…みなされます。ただし` (24→27 units, still a raw body substring) | 0 | 1 | C2 `7/8 met=False`: C5 `Gate quote is 27 units, expected 6 to 25` — pure ceiling hit, no substring note |
| M11 | Gate quote S372 one character 限→域 | 0 | 1 | C2 `7/8 met=False`: C5 "Gate line quotes … which is not a raw substring of the retained body" |
| M12 | remove S418's registry row from `corpus/SOURCES.md` | 0 | 1 | C2 `2/8 met=False`: C3 "no registry row", C4 "no usable registry row", C5 title′′, C6 "no registry URL", C7 byte-equality, C8 `registry rows 155 != mirror rows 155 + 1` |
| M13 | S372 `teaches` cell `unrestricted`→`unrestricted-mutant` | 0 | 1 | C2 `5/8 met=False`: C3 "a cell other than used-by differs from the base row" + C7 byte-equality + C8 "append-only: … != mirror bytes" |
| M14 | receipts.json S418 `sha256` 2b146a…→3b146a… | 0 | 1 | C2 `7/8 met=False`: C6 "receipt sha256 3b146a… != body 2b146a…" |
| M15 | remove `.ufo/waves/round-55/assimilation/validate/` (153 files, 27901 deletions) | 0 | 1 | C2 `7/8 met=False`: C7 "append-block validation receipt is incomplete" |

## SURVIVORS

None. 15/15 mutants were noticed by the counter whose data they damage: 14 exit 1 (predicate not
met), M06 exit 2 (counter refuses to evaluate rather than score a two-section map). No counter
returned exit 0 on data it judges.

## WHAT EACH SURVIVOR MEANS FOR THE CLAIM

No survivors, so no survivor findings. The kills support the claim that both counters notice
damage to the data they judge, for these 15 probes: C1's thin/duplicate/head_changed/deleted/
unindexed/dangling terms each fired on their targeted damage class, and its two-section guard
refuses to score (exit 2) instead of silently reading the wrong section; C2's quote-truth (C5),
row-shape (C3), used-by (C4), receipt-pin (C6), validate-before-append (C7) and mirror-bytes (C8)
conditions each fired on their targeted damage class. Observations (not survivors): (a) M08's
swap was caught by one side only — the fleet-registry coverage cell still shares a 5+-letter word
with vault-properties.md's head, so a swap pair whose cells share vocabulary with both swapped
heads is a residual path worth a future probe; (b) M10 shows the ceiling check fires on units
alone (the lengthened span stayed a raw substring), so the 25-unit ceiling is enforced
independently of quote fabrication; (c) M12 additionally shows C5/C6 degrade gracefully to
explicit fail notes (empty title / no registry URL) rather than crashing.

## Restoration evidence

All mutation bytes lived in disposable /tmp clones (tasking declares each mutant its own clone
commit); the lane repo received no write from this seat except this report file. Before-hashes =
`git -C <lane> show a7a548e102b71…:<path> | sha256sum`; after-hashes as printed by `/tmp/mut.py`.

| path | before (a7a548e) | after (mutant) |
|---|---|---|
| corpus/README.md | ea3e34b3bfcbced846c072bc36d68979cc489e1b226a0e9382f4d21fbd260c90 | M01 3dd3139ca2347a58…; M02 6ec823223094e192…; M06 96192957deecbf59…; M07 7807c33907333423…; M08 32724ab73f67bf65… |
| corpus/knowledge/fleet-registry.md | 4bd960f082e43fd1a4d5e40c02503d304e72b983f8df2f4fef920a1d331a4cd1 | M03 removed; M04 227e9c02d127d948a91faf56caa88eb76098672bca213bbff89c95c538bc785a |
| corpus/knowledge/yahoo-japan-robots-txt-refusal-rules.md | a86a3e62847e8b2db35d4f0c0fea7ab212fbffb7e05b16250647745c17f38d12 | M09 b41f0ba829419fa4551487bb00fa49b909de88de79dcdfc620fc5fcf0f57c869 |
| corpus/knowledge/yahoo-japan-robots-pattern-syntax.md | 1ad1f5b138ca661b51322f65c99a23ca82b9103173e6c63cccc5430763745818 | M09 000e5d9604a829ce6de50a8aaa4c3252b59854f3601665b530273ac0f25245b3 |
| corpus/knowledge/yahoo-japan-robots-txt-basics.md | bc5a3098eccc870a1e9e15bb1b81d4009a3be3484c0cfc565826b5b5da2f7062 | M09 d0309f97670330fe29e5be1495062120605aa24d0912c761f3cd6c5a7ff90baa |
| corpus/lessons/round-55.md | 33c38d71a1fc4e9f2ee6b3a375920e27f2b1e0fecf6e62e0d1fee4e70eb4ed3f | M10 d8c84cd4709d11adb29c7459185ac3355a30ce658a5f288eccf9f17957bd4058; M11 2de7f5d3b86f8c1866776ef1f141e50c0da0c5f7d76c63bf6dbbf161353266aa |
| corpus/SOURCES.md | cc402e4b559528170fe71ba09b6ad3be663a8f9d5ce9f36caeaed5ea45e6c50e | M12 7727f64ddfb139702d9a9c64c9f75121cfcb7d2840105d03c2a950b0e9e81f8d; M13 192173252459247b68d49fc265fa50a303c489b43088eb11d3b95e484d08cee0 |
| .ufo/waves/round-55/sources/receipts.json | c85a7d18585ae330f935d337afbd08f03c386ce8037fd5161bc401a53151b18e | M14 a496d17cd996dd482d5b6d3ef8e779d03abac4dc3adfc89eb45317d915a79d64 |
| .ufo/waves/round-55/assimilation/validate/ | 153 files present at a7a548e (`git ls-tree -r --name-only … \| wc -l` → 153) | M15 removed (diff --shortstat: `153 files changed, 27901 deletions(-)`) |
| corpus/knowledge/zzz-unindexed-mutant.md | absent | M05 added, 8d29e5486df96a23e7b18f1bdf282117d5ee66b8e875ceab49fd5eff0f907384 |

Clone commits measured (dir = REV): M01 /tmp/mutM01.h0wYeq = 08413329a1f51050d3ebe8e1ca0a3ec747752cbe;
M02 /tmp/mutM02.Ui8s8v = aacd1eb81eb74f05be57286ede60872f2fc85ff3; M03 /tmp/mutM03.YjnBnu =
f1ab5ec830b078c28a548f2eea597509238744d9; M04 /tmp/mutM04.VDhfgF =
44b411a5b960367ea15e3a980ebb261bcfc4dd03; M05 /tmp/mutM05.P07O2P =
96da5310421286fe702ba9e61b548d53e28596e6; M06 /tmp/mutM06.M4s56S =
6fcf4032189c2a7cbc5d2031a5ca0ac517775d86; M07 /tmp/mutM07.u8E0EV =
4f93d7568994a606f04cab3dbf4a7603b59dbf36; M08 /tmp/mutM08.TNIgBn =
0ebbc63b15671195aec4ee51872318d0adafa176; M09 /tmp/mutM09.Yj452v =
49814ee983e8d5fd17d150c95dcebc4638392ebb; M10 /tmp/mutM10.Fr2Qcq =
a73bbc8e88a0802f73e325e3b3a4cc5bd1e023ee; M11 /tmp/mutM11.4wKLCd =
6acd311ed9e77494d0fadb7dae8417285ec4970b; M12 /tmp/mutM12.4s3JKC =
9bd8e368c5a3d6f034fb6b95d719bba4bff8f6a3; M13 /tmp/mutM13.jjfOXD =
94e2b923a3311297a81c2e5f1dbee86cba2f3487; M14 /tmp/mutM14.qgFo6a =
f4923d807db420411ebfdb038c3b4fb64cf68b00; M15 /tmp/mutM15.WJfmSn =
42934a9f4f753416e9d3decae41790a6af2dad3a.

Tooling: nothing installed or upgraded (python3 + git sufficed; pacman untouched per the
host-wide pause). No credential material, session tokens, `op://` refs or private URLs used or
recorded.

VERDICT: 15/15 data mutants detected (14 exit 1, M06 exit 2 unevaluable), 0 survivors — both counters notice damage to the data they judge at a7a548e102b71bd16b0a6ddafa469393a2c98b69.
