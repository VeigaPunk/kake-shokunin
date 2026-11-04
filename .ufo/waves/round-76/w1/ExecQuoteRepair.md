# ExecQuoteRepair — C1 after-state (round 76, wave w1, attempt 1)

Seat: leaf executor. The lane checkout is read-only here; every write went to this wave dir or to a
`git clone --shared` in scratch. Base for every before-state: `a0491fcd041cbc3fff2c964ecf6268557e45a5c1`.
No tool was installed or upgraded (none needed); no model was named or passed.

**Amendments 3 and 4 apply** (`.ufo/waves/round-76/amendment-3.md` B1–B6 + B3-bis: population dedupe,
whole-line correction closure, correcting spans exempt only when they are base `T1`/`T2` findings, exact-text
append-only, `*.ready*` never a receipt; `amendment-4.md`: this round's own `base-c1-quote-truth*.txt` and
`ctl-*.txt` control files are never receipts). The repair was rebuilt against B3/B3-bis and measured on both
the seat's v0 counter and the amended hardened counter (§Appendix A).

## 1. Verdict

The C1 after-state is constructed and measured in a scratch clone:

```
$ python3 -B .ufo/waves/round-76/w1/ExecQuoteCounter/doc_quote_truth.py \
    --root . --revision 5529e836d5ed19d8797b3ba605e8b457f8ccd237 \
    --base a0491fcd041cbc3fff2c964ecf6268557e45a5c1 --rounds 75,76
C1v2 revision=5529e836 rows=26 receipt_files=10452 spans=30 exempted=8 corrections=7 findings=0 met=true
  missing corpus/lessons/round-76.md
exit=0
```

The same command with `--json` (`receipts/10-after-json.txt`) prints `"append_only": true`,
`"findings": []`, `"corrections": 7`, `"met": true`, exit 0. The L1's v0 `c76_quote_truth.py`
(sha256 `c9311780…`) prints the identical counts (`receipts/02-after-run.txt`).

`5529e836…` is a **scratch-clone commit**, not a lane revision: base tree + the three append blocks (§7).
The hash is not resolvable after this seat's scratch is removed; `receipts/04-diff.patch` reproduces it.

Seven correction rows close seven defects (one row per defective span; the `SCORECARD.md:4904` physical row
is one row, per amendment 3 §B6). Under the counter build that implements amendments 3+4 (pinned snapshot
`d8349b05…`, §Appendix A) the after tree measures `rows=23 receipt_files=10452 spans=41 exempted=7
corrections=7 findings=0 met=true`, exit 0; base measures `findings=7` (`rows=16`) and the no-repair tree —
base + this round's controls committed, nothing else — is **red with `findings=7`**, exit 1. The earlier
build (`63af0ede`, 22:01) printed `findings=8`/`exempted=8` because it still counted the `SCORECARD.md:4904`
duplicate; that build is superseded and its runs are kept as receipts 08/09.

## 2. Method

```sh
S=/fast/scratch/hyaku/kake-r76/ExecQuoteRepair
mkdir -p "$S/tmp"; export TMPDIR="$S/tmp"
git clone --shared /home/vgpnk/Projects/shokunin/kake-shokunin "$S/repo"
cd "$S/repo" && git checkout -q a0491fcd041cbc3fff2c964ecf6268557e45a5c1
git rev-parse HEAD   # a0491fcd041cbc3fff2c964ecf6268557e45a5c1 (asserted before any write)
```

`git rev-parse --show-toplevel` printed the clone path before every commit; the lane was only read
(`git show`, `ls-tree`, `hash-object`, `grep`).

Base under the 22:01 builds (`63af0ede` v2 / `c9311780` v0) — `findings=8`, exit 1, the eight lines of
`controls/base-c1-quote-truth.txt` (`receipts/01-base-run.txt` v0, `receipts/08-hardened-counter.txt` v2);
the amended build re-measures 7 (Appendix A):

```
C1v2 revision=a0491fcd rows=19 receipt_files=10452 spans=30 exempted=0 corrections=0 findings=8 met=false
  T1 SCORECARD.md:4892 files=18 mismatches=0 append_only=true met=true missing_frozen=0
  T1 SCORECARD.md:4892 mismatches=3 classes=E3 append_only=false missing_frozen=1
  T1 SCORECARD.md:4893 population=18 bound=18 mismatches=0 met=true missing_frozen=0
  T1 SCORECARD.md:4893 receipt: source=committed declared_valid=true
  T1 SCORECARD.md:4904 mismatches=0 met=true missing_frozen=0
  T1 SCORECARD.md:4904 mismatches=0 met=true missing_frozen=0
  T1 corpus/QUALITY.md:1499 files=15 append_only=false met=false
  T1 corpus/lessons/round-75.md:82 files=15 append_only=false met=false
```

The 4904 pair is one physical row scanned under two overlapping headings — the duplicate amendment 3 §B2
forbids and §B6 removes. Seven physical defects remain:
`SCORECARD.md:4892` ×2, `4893` ×2, `4904` ×1, `corpus/QUALITY.md:1499` ×1,
`corpus/lessons/round-75.md:82` ×1.

## 3. The seven defects and the seven correction rows

Each row names its defective span verbatim, quotes whole receipt line(s), names the receipt file:line, and
carries `[r76-correction 2026-11-03]`. Rows 1–5 are table rows in the new SCORECARD section; rows 6–7 are
the QUALITY and lesson bullets.

| # | Finding | Defective span (named verbatim) | Whole receipt line(s) quoted | Receipt | Correction row |
|---|---|---|---|---|---|
| 1 | `SCORECARD.md:4892` | `files=18 mismatches=0 append_only=true met=true missing_frozen=0` | `C1v1 revision=f87d14a9 rows=32 live=20 files=18 mismatches=0 classes=- append_only=true met=true missing_frozen=0` | `controls/after-c1-row-truth.txt:4` | `SCORECARD.md:4925` |
| 2 | `SCORECARD.md:4892` | `mismatches=3 classes=E3 append_only=false missing_frozen=1` | `C1v1 revision=153fa2a9eda8d95618697186feb18574cc7daae1 rows=27 live=15 files=15 mismatches=3 classes=E3 append_only=false met=false missing_frozen=1` | `controls/ctl-deletion-landed.txt:3` | `SCORECARD.md:4926` |
| 3 | `SCORECARD.md:4893` | `population=18 bound=18 mismatches=0 met=true missing_frozen=0` | `C2v1 revision=f87d14a949e1b5f8b4ec5807b75f22aa3e337353 population=18 bound=18 mismatches=0 met=true` **and** `population: derived=18 frozen=16 missing_frozen=0 beyond_frozen=2` | `controls/after-c2-receipts.txt:5-6` | `SCORECARD.md:4927` |
| 4 | `SCORECARD.md:4893` | `receipt: source=committed declared_valid=true` | `receipt: source=committed worktree=identical declared=abfbfaac58bcee2514490940d1b16365027a07c9 declared_match=false declared_valid=true` | `controls/after-c2-receipts.txt:7` | `SCORECARD.md:4928` |
| 5 | `SCORECARD.md:4904` | `mismatches=0 met=true missing_frozen=0` | `C1v1 revision=f87d14a9 rows=32 live=20 files=18 mismatches=0 classes=- append_only=true met=true missing_frozen=0` | `controls/after-c1-row-truth.txt:4` | `SCORECARD.md:4929` |
| 6 | `corpus/QUALITY.md:1499` | `files=15 append_only=false met=false` | `C1v1 revision=afc73a87759b4218d54369b583e021b6e800de73 rows=27 live=15 files=15 mismatches=2 classes=E3 append_only=false met=false` | `controls/ctl-deletion.txt:1` | `corpus/QUALITY.md:1524` |
| 7 | `corpus/lessons/round-75.md:82` | `files=15 append_only=false met=false` | same line as #6 **and** the landed control `C1v1 revision=153fa2a9eda8d95618697186feb18574cc7daae1 rows=27 live=15 files=15 mismatches=3 classes=E3 append_only=false met=false missing_frozen=1` | `controls/ctl-deletion.txt:1`, `controls/ctl-deletion-landed.txt:3` | `corpus/lessons/round-75.md:145` |

What each correction restores (the observed field the claim skipped):
1. `classes=-` between `mismatches=0` and `append_only=true`; 2. `met=false` between `append_only=false`
and `missing_frozen=1`; 3. the C2 line ends at `met=true` — `missing_frozen=0` belongs to the next
derived-population line, so the claim spliced two lines into one; 4. `worktree=identical`, the declared
revision and `declared_match=false`; 5. `classes=- append_only=true`; 6.–7. `mismatches=2 classes=E3`
between `files=15` and `append_only=false`. No verdict moves: C1 met at the tip, C2 met, deletion is still
not a repair (`append_only=false`).

## 4. The exact whole receipt lines used (pasted, as requested)

Six distinct lines, nine uses. All six are quoted **trimmed** (amendment 3 §B3(b): exact equality with a
receipt line after trimming leading/trailing whitespace); the two lines that are indented in the receipt are
shown here with their original indentation, and the blocks quote them without it.

```
C1v1 revision=f87d14a9 rows=32 live=20 files=18 mismatches=0 classes=- append_only=true met=true missing_frozen=0        # .ufo/waves/round-75/controls/after-c1-row-truth.txt:4
C1v1 revision=153fa2a9eda8d95618697186feb18574cc7daae1 rows=27 live=15 files=15 mismatches=3 classes=E3 append_only=false met=false missing_frozen=1        # .ufo/waves/round-75/controls/ctl-deletion-landed.txt:3
C2v1 revision=f87d14a949e1b5f8b4ec5807b75f22aa3e337353 population=18 bound=18 mismatches=0 met=true        # .ufo/waves/round-75/controls/after-c2-receipts.txt:5
  population: derived=18 frozen=16 missing_frozen=0 beyond_frozen=2        # .ufo/waves/round-75/controls/after-c2-receipts.txt:6  (two leading spaces in the receipt; quoted trimmed)
  receipt: source=committed worktree=identical declared=abfbfaac58bcee2514490940d1b16365027a07c9 declared_match=false declared_valid=true        # .ufo/waves/round-75/controls/after-c2-receipts.txt:7  (two leading spaces; quoted trimmed)
C1v1 revision=afc73a87759b4218d54369b583e021b6e800de73 rows=27 live=15 files=15 mismatches=2 classes=E3 append_only=false met=false        # .ufo/waves/round-75/controls/ctl-deletion.txt:1
```

Every quote was interpolated from those bytes by a generator that read the receipt files
(`gen_blocks.py`, scratch), never retyped; the two indented lines are trimmed by `.strip()` on read.

## 5. Amendment 3 B3 / B3-bis compliance

`receipts/05-correction-validation.txt` classifies **every** claim-bearing span on **every** correction row
by the B3-bis rule ("not a whole receipt line is exempt only when the identical span is a base T1/T2
finding"):

```
== A. claimy spans on every correction row, classified (amendment 3 B3 / B3-bis)
  SCORECARD.md:4925  NAMED_DEFECT + WHOLE_RECEIPT_LINE
  SCORECARD.md:4926  NAMED_DEFECT + WHOLE_RECEIPT_LINE
  SCORECARD.md:4927  NAMED_DEFECT + WHOLE_RECEIPT_LINE + WHOLE_RECEIPT_LINE
  SCORECARD.md:4928  NAMED_DEFECT + WHOLE_RECEIPT_LINE
  SCORECARD.md:4929  NAMED_DEFECT + WHOLE_RECEIPT_LINE
  corpus/QUALITY.md:1524       NAMED_DEFECT + WHOLE_RECEIPT_LINE
  corpus/lessons/round-75.md:145  NAMED_DEFECT + WHOLE_RECEIPT_LINE + WHOLE_RECEIPT_LINE
  totals: whole_lines=9 named_defects=7 contiguous_fragments=0 fabricated=0
  strict B3-bis reading (only whole lines + named defects on every row): True
```

Consequence: no correction row carries an incidental claimy fragment at all — every observed token other
than the named defect is written as plain text, never backticked, so B3(c) has nothing to reject. Closure
is 1:1 (section B of the same receipt): each of the seven base findings is named verbatim by exactly one
row (the duplicated 4904 instance is named by row 5). Section C: all six defective spans have **0** hits
across the 10,452 committed receipts at the measured revision, so `findings=0` can only come from the
correction exemption, not from a receipt that happens to contain the fragment.

## 6. Append-only evidence

```
$ git diff --numstat a0491fcd..HEAD -- SCORECARD.md corpus/QUALITY.md corpus/lessons/round-75.md
18      0       SCORECARD.md
15      0       corpus/QUALITY.md
11      0       corpus/lessons/round-75.md

$ git diff --diff-filter=D --name-only a0491fcd..HEAD
(no output = no deleted file)

$ git diff --numstat … | awk '$2 != 0'
(no output = zero deleted lines: no historical line rewritten)
```

44 insertions, 0 deletions (`receipts/03-append-only-numstat.txt`); every hunk is a `+` block at end of
file; the counter's own conjunct prints `"append_only": true`. The three lane files are still byte-identical
to base, so the blocks apply to the lane verbatim:

```
SCORECARD.md                worktree=e032e2a5… base=e032e2a5… same=yes
corpus/QUALITY.md           worktree=2dfcb363… base=2dfcb363… same=yes
corpus/lessons/round-75.md  worktree=f78369f8… base=f78369f8… same=yes
```

## 7. Deliverables (apply verbatim, append-only)

| File | Block | bytes | sha256 |
|---|---|---|---|
| `SCORECARD.md` | `blocks/scorcard-append.md` (18 lines) | 3,131 | `6a486359ac3d53d2f60852a7fba109b89e58f70bd53bce003fcbcc8089dd9767` |
| `corpus/QUALITY.md` | `blocks/quality-append.md` (15 lines) | 1,145 | `625857db4e34e0744e80ae33b65c470990c21b2f15084ca4668293d7d07c920d` |
| `corpus/lessons/round-75.md` | `blocks/lesson-append.md` (11 lines) | 1,063 | `a28a5e5fd5adc98dfec5b3b9d5da19941cab914c72aefb00ef3cca9bef525dd1` |

`receipts/04-diff.patch` (`bf10eaed…`) is the same change as a unified diff. Each block starts with one
blank line and is appended to end of file (`cat >>`), or apply the patch (`git apply`) — same bytes.
`receipts/11-patch-reproduction.txt` proves the delivered patch alone reproduces the after-state: a fresh
`git clone --shared`, `git apply 04-diff.patch`, commit → the three blobs are byte-identical to the working
clone (`c6425d8d…`, `91c5fdab…`, `2ec39606…`) and both counters report
`rows=26 … exempted=8 corrections=7 findings=0 met=true`, exit 0, at the patch-built revision.

- SCORECARD: new level-two `## Round 75 — quote corrections (appended round 76)` — one paragraph, one
  5-column table, five data rows.
- QUALITY: new level-two `## Round-76 criterion — quoted receipts are whole` — one bullet with the
  admit/reject rule and the whole `ctl-deletion.txt:1` line.
- round-75 lesson: new level-two `## Corrections` — one bullet naming the deletion-control defect, quoting
  both control lines, and stating the historical bullet is not rewritten.

## 8. Risks and defects

**R1 — CLOSED by amendment 4 (was: the C1 target is reachable with no repair at all).** Receipts include
any file under a `controls/` directory, and the round-76 controls are the counter's before-state output
lines: each finding line ends with the very span it reports. Probe on the 22:01 builds
(`receipts/06-launder-probe.txt`, `receipts/09-launder-probe-hardened.txt`): branch from `a0491fcd`, copy
`.ufo/waves/round-76/controls/*.txt`, commit, **no correction anywhere**:

```
$ python3 -B .ufo/waves/round-76/w1/ExecQuoteCounter/doc_quote_truth.py --root . --revision HEAD --base a0491fcd --rounds 75,76
C1v2 revision=HEAD rows=19 receipt_files=10461 spans=30 exempted=0 corrections=0 findings=0 met=true
exit=0
```

and the control receipt carries every span verbatim, e.g.
`base-c1-quote-truth.txt:2:  T1 SCORECARD.md:4892 files=18 mismatches=0 append_only=true met=true missing_frozen=0`
(`receipts/07-launder-spans-in-control-receipt.txt` lists all six). Amendment 4 now excludes
`.ufo/waves/round-76/controls/base-c1-quote-truth*.txt` and `ctl-*.txt` from the receipt universe, and the
amended build re-measures the same tree **red**: `receipt_files=10455 … findings=7 met=false`, exit 1
(Appendix A / `receipts/13-amendment4-verification.txt`). The probe receipts remain as the record of the
defect as it stood before the amendment.

**R2 — CLOSED by the amended build.** The 22:01 build (`63af0ede`) printed `rows=19 … findings=8` with
`SCORECARD.md:4904` twice (`receipts/08-hardened-counter.txt`), where amendment 3 §B6 records **7** and
forbids duplicate findings from one physical row. The build that implements B1/B2/B6 prints `rows=16 …
findings=7` at base and `rows=23 … findings=0` after (Appendix A); three successive builds
(`c013f269`, `a12f9611`, `d8349b05`) gave the same three verdict lines.

**R3 — `corpus/lessons/round-76.md` does not exist at the measured revision** (`missing` notice, not a
finding). When it lands its rows join the population: re-run at the final tip; a bad quote there is a new
finding, not a regression of this repair.

**R4 — the exemption is still keyed by substring presence** (`any(span in c["text"] …)`), so a correction
row exempts any span it merely mentions, even though the amended build now also checks correction-row spans
(`spans_checked` counts them; `exempted=7` are exactly the seven named findings). This repair's rows name
exactly one defect each and use whole lines otherwise, so the weakness is not exercised; row 3's defective
span does contain row 5's span as a substring, which is why `05-correction-validation.txt` lists two rows
for the 4904 span. Informational for this landing; a stricter counter could require the named span to sit
in a designated "defective" position.

**R5 — `--work` is not used by either counter's measurement path** (v0 uses it only for `--selftest`; the
v2 CLI accepts it but this run passed `--root`/`--revision` only). Nothing was written outside the clone and
`TMPDIR`; stated so the L1 does not expect a `--work` in the reproduction command.

## 9. What the L1 should do, in order

1. Append the three blocks (or `git apply receipts/04-diff.patch`) to the lane. Files are unchanged since
   base, so this is a clean append.
2. Measure with the amended build (§Appendix A): at the applied tip expect
   `rows=23 … exempted=7 corrections=7 findings=0 met=true`, exit 0; at base / on the no-repair tree expect
   `findings=7 met=false`, exit 1 (amendment 4 keeps the do-nothing control red, so the green is not
   vacuous).
3. After `corpus/lessons/round-76.md` lands, re-run at the final tip (R3).

## 10. Limits

- One counter predicate over one population; the semantic readings in §3 are human judgments on the same
  bytes, not additional measurements.
- `met=true` is a scratch-revision measurement; the lane has no commit from this seat (leaf, no
  commit/push/deploy).
- Unrun here: the counters' `--selftest` suites, and every lane-level gate (`c73_wave_pointers.py`, the
  registry gates). The parent owns post-integration gates.

## 11. Receipts

| File | Content | sha256 |
|---|---|---|
| `receipts/01-base-run.txt` | v0 at base: 8 findings, exit 1 (tool sha256 + exact command) | `7f5dba4a331f4c32ad03abcfc1d991f3e4d5a6031dbc931dd6f763d0cf9a687e` |
| `receipts/02-after-run.txt` | v0 at after: 0 findings, exit 0 | `f0d62353ada6f2b3b74d103dbc08b14b0092060b4ab6fed92598eaebabc1de3a` |
| `receipts/03-append-only-numstat.txt` | numstat, deletion filter, zero-deleted-lines check | `3f31830be606ad39914759756dddd602b6d444568e12c99eede46adcf8c7f527` |
| `receipts/04-diff.patch` | three-file unified diff | `bf10eaed7ac60467d54945d5f6f8efb3c078bdee87ca7ca697ba6e04cc520cf6` |
| `receipts/05-correction-validation.txt` | B3-bis span classification, closure map, 0 receipt hits | `5ac8d17c594dcd8ee84bb32885ac98158bd6a0d1b1674b5d78ca9af316960fba` |
| `receipts/06-launder-probe.txt` | laundering probe under v0 | `61cc6c2ec01deaf150b10cbda38d2aa253b47511c91095278b34892ae4bb2589` |
| `receipts/07-launder-spans-in-control-receipt.txt` | all six spans inside `controls/base-c1-quote-truth.txt` | `0944dfd8a8f0a572923aead08c5d67f823f063bd52cdcc17882c7f45a7344b32` |
| `receipts/08-hardened-counter.txt` | delivered v2 at base and after, with sha256 + size | `44cf8e692b7d4c7cf0e57a65cc434c3c9a95655e919f20cf9e8c7942f95c2c9d` |
| `receipts/09-launder-probe-hardened.txt` | laundering probe under the delivered v2 | `8846e650708ff6f40f75284c98587fd7ebe89a173ce0dd45751abd5ab4857c8c` |
| `receipts/10-after-json.txt` | v2 `--json` at after: `append_only=true`, `findings=[]`, `met=true` | `210c70a0857d39d6133a8b6232964ea762755c7cb6ed080da58298411811dc03` |
| `receipts/11-patch-reproduction.txt` | fresh clone + `git apply` of `04-diff.patch`: byte-identical blobs, both counters `findings=0 met=true` exit 0 | `e107a8c9c4da8c886596490a8cac96ca545ac6c5fcb41cd306aa2ed93bd3030a` |
| `receipts/12-amended-build-base-after.txt` | amended build at base + after + no-repair (first run, build `a12f9611`) | `ba6364d6fe220402210333f02d34d22df2e74f0945ab89d5e06e5be8cf8c1460` |
| `receipts/13-amendment4-verification.txt` | pinned snapshot `d8349b05` (41,600 B, 994 lines): base 7, after 0, no-repair 7; blob hashes; control file list | `854b495551b35d6454fa9d3ce912d6f1146a74dc42cab43d9461bd33b46434b2` |

## Appendix A — amendment 4 re-verification (amended counter build)

Requested by the L1 after amendment 4 froze: re-verify the after-state on a build that applies amendments
3 (B1/B2/B6) and 4, and confirm the no-repair tree is red. Counter: `doc_quote_truth.py` as iterated by its
seat. Because the lane file changed three times during this check, the numbers below were taken with a
**pinned snapshot**: `sha256 d8349b053edef7a8a91c3398e60fac443a7979a63a56087ffac122542ab42bc5`, 41,600 B,
994 lines, byte-identical to the lane file at snapshot time (`diff -q` silent). Three successive builds
(`c013f269`, `a12f9611`, `d8349b05`) produced the same three verdict lines; receipts 12 and 13.

Trees (all `git clone --shared` of the lane, `git rev-parse --show-toplevel` asserted before every commit):

- **base**: `a0491fcd`;
- **after**: base + `blocks/scorcard-append.md`, `blocks/quality-append.md`, `blocks/lesson-append.md`
  (blobs `c6425d8daa8e224d5225b353e1953fc23ec551cd`, `91c5fdab205b0f9b71d5977afa8bc48eabba720d`,
  `2ec3960635b4a77c773d8f1fb1cc1a29c566fbf3` — the same bytes as `receipts/04-diff.patch`);
- **no-repair**: base + the lane's `.ufo/waves/round-76/controls/*.txt` committed verbatim, nothing else.

```
$ python3 -B counter-snapshot.py --root . --revision a0491fcd... --base a0491fcd --rounds 75,76
C1v2 revision=a0491fcd rows=16 receipt_files=10452 spans=25 exempted=0 corrections=0 findings=7 met=false
  T1 SCORECARD.md:4892 files=18 mismatches=0 append_only=true met=true missing_frozen=0
  T1 SCORECARD.md:4892 mismatches=3 classes=E3 append_only=false missing_frozen=1
  T1 SCORECARD.md:4893 population=18 bound=18 mismatches=0 met=true missing_frozen=0
  T1 SCORECARD.md:4893 receipt: source=committed declared_valid=true
  T1 SCORECARD.md:4904 mismatches=0 met=true missing_frozen=0
  T1 corpus/QUALITY.md:1499 files=15 append_only=false met=false
  T1 corpus/lessons/round-75.md:82 files=15 append_only=false met=false
exit=1

$ python3 -B counter-snapshot.py --root . --revision 04f18d3c... --base a0491fcd... --rounds 75,76
C1v2 revision=04f18d3c rows=23 receipt_files=10452 spans=41 exempted=7 corrections=7 findings=0 met=true
  missing corpus/lessons/round-76.md
exit=0

$ python3 -B counter-snapshot.py --root . --revision 65e9994b... --base a0491fcd --rounds 75,76
C1v2 revision=65e9994b rows=16 receipt_files=10455 spans=25 exempted=0 corrections=0 findings=7 met=false
  ... same seven findings as base
exit=1
```

Reading:

- **base is 7**, `rows=16` (one row per physical line: the `SCORECARD.md:4904` duplicate is gone), so
  §B2/§B6 are implemented and §B1's 7–40-char revision citations are no longer counted as claims
  (`spans=25`, down from 30).
- **after is 0** with `exempted=7 corrections=7`: the build now checks correction-row spans
  (`spans_checked` 25 → 41, i.e. +16 = 9 whole-line quotes + 7 named defects), and every one of them is
  either a whole receipt line or the named base finding — nothing on a correction row is fabricated.
- **no-repair is RED at 7**, exit 1, `receipt_files=10455` = 10,452 + the three non-excluded round-76
  control files (`census-before.txt`, `harm-base.txt`, `sweep-r76.txt`); the six
  `base-c1-quote-truth*.txt` / `ctl-*.txt` files are excluded by amendment 4. This is the do-nothing control
  the round needs, and it shows the green in the after-state is carried by the repairs.

`receipts/13-amendment4-verification.txt` holds these lines, the snapshot hash/size, the after-tree blob
hashes, and the committed control-file list; `receipts/12-…` holds the first (pre-snapshot) run of the same
three lines under build `a12f9611`.

**Amendment 7 note (receipt counts are build-dependent).** The `receipt_files` values above (10,452 base /
after, 10,455 no-repair) were printed by build `d8349b05` and earlier. Amendment 7 §F1 restores a closed
round's seat receipts (`.ufo/waves/round-75/w1/…`) to the universe — only the newest measured round's seat
tree is excluded — so a build implementing F1 will print a different receipt count, and §F2 records that the
base stays `findings=7`. The counts are therefore build-specific; the evidence is the verdict lines, which
amendment 7 leaves unchanged: base `findings=7 met=false` exit 1, after `findings=0 met=true` exit 0,
no-repair tree `findings=7 met=false` exit 1.
