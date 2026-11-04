# MutC — round 77, wave w1 (kake lane)

Seat: mutation tester (leaf). Scope: one plausible defect at a time against the two round-77
instruments — `scripts/sitemap_audit.py` (C2 tool), `.ufo/waves/round-77/c77_sitemap_matrix.py`
(C2 counter), `.ufo/waves/round-77/c77_shonen_ledger.py` (C1 counter). Every mutant was applied to a
scratch copy; the lane checkout was read-only; no subagent, no network, no `git`/`jj` write, no tool
install or upgrade, no model named or passed. Scratch root `S=/fast/scratch/hyaku/kake-r77/MutC`
(deleted after this report was written; every number below is transcribed from the receipts that
lived there).

## 0. Bytes scored

The instruments moved while this seat ran (three tool builds, two ledger builds, one case-file
rename). Only the final pin is scored; §5 records the intermediate reds with their digests, because
a report that quotes an earlier build cannot be reproduced from these bytes.

|Role|Path|sha256|Bytes|mtime|
|---|---|---|---|---|
|C2 tool **scored**|`scripts/sitemap_audit.py`|`f767af770652437d7af18c693dff7cafd64d7f79c38cec36a20e6c4e0bbe9176`|32325|2026-11-03 22:56:28|
|C2 tool selftest **scored**|`scripts/sitemap_audit_selftest.py`|`f22e0a67d777ce80ce2d1099520f50f98016c28901e77b7cb5e4b73c386b9c89`|81651|2026-11-03 22:56:42|
|C2 matrix **scored**|`.ufo/waves/round-77/c77_sitemap_matrix.py`|`5c6eacba266068845144ba59c8e7099cc22fee10ca95c0ab78019ba33d21afce`|29677|2026-11-03 22:49:41|
|C1 counter **scored**|`.ufo/waves/round-77/c77_shonen_ledger.py`|`2d66e5af30b90f50875ac820879430b55f0c344e3c4965b6bcc203a3567a4396`|48343|2026-11-03 22:58:42|
|C2 cases|`.ufo/waves/round-77/cases/`|20 case dirs, 62 files|1.7 MB|g01 file renamed 22:5x (§5 F4)|
|C2 constants|`.ufo/waves/round-77/consts/`|4 tools + README|—|stable since 22:45|

Earlier snapshots seen and superseded (times from `stat`): tool `16ea784f…` (22:46) → `98cdb926…`
(22:51) → `742c2ab1…` (22:51) → `f767af77…` (22:56); selftest `19b265ce…` → `82a587e3…` →
`f22e0a67…`; ledger `a9eef8bd…` (v1, 22:46) → `2d66e5af…` (v2, 22:58). Cases: `g01`'s file was
renamed `sitemap.xml.gz` → `sitemap.xml.bin` (same bytes, same expectation) between 22:49 and 22:53.

Drift check after every mutant run, all four instruments against the pinned copies:

```
$ sha256sum scripts/sitemap_audit.py scripts/sitemap_audit_selftest.py \
    .ufo/waves/round-77/c77_sitemap_matrix.py .ufo/waves/round-77/c77_shonen_ledger.py
scripts/sitemap_audit.py                                SAME
scripts/sitemap_audit_selftest.py                       SAME
.ufo/waves/round-77/c77_sitemap_matrix.py               SAME
.ufo/waves/round-77/c77_shonen_ledger.py                SAME
```

## 1. Detectors and pristine baselines

All commands run from the lane root with `TMPDIR=$S/tmp`, `python3 3.14.8`, `-B` everywhere; tool
runs are bounded by the counter's 300 s timeout. `$T` is the pinned tool copy.

|Id|Detector|Command|Pristine result|
|---|---|---|---|
|D1|C2 matrix (frozen form)|`python3 -B $M --root . --tool $T --cases $C --consts $K --work $W --json-out out.json`|`C2 revision=worktree cases=20 decided=20 correct=20 wrong=0 constants_failed=4/4 met=true`, rc 0|
|D2|independent per-case oracle (does not import the counter)|`python3 percase.py --tool $T --cases $C`|`PERCASE tool=sitemap_audit.py cases=20 ok=20 wrong=0`, rc 0|
|D3|delivered tool selftest|`python3 -B $SELFTEST --tool $T`|`PASS 271/271`, rc 0|
|D4|C1 counter selftest|`python3 -B $L --selftest --work $W`|`selftest: 26/26 passed`, rc 0|
|D5|C1 counter on seven planted trees served by a fake read-only `git` (plain directories; no repository is written)|`python3 ledger_run.py --counter $L --root fixtures/<name>`|see table below|
|D6|matrix-counter selftest|`python3 -B $M --work $W --selftest`|`selftest 14/14 passed`, rc 0|
|D7|base-tool fixture for D6-mutants|`python3 -B $M --root . --tool tools/base_sitemap_audit.py …`|`correct=2 wrong=18 constants_failed=4/4 met=false`, rc 1|
|D8|three-failing-constants fixture (3 real constants + an oracle that replays `expect.json`)|`python3 -B $M --tool tools/oracle.py --consts consts3 …`|`cases=20 decided=20 correct=20 wrong=0 constants_failed=3/4 met=false`, rc 1|
|D9|crashing-tool fixture|`python3 -B $M --tool tools/crash.py …`|`cases=20 decided=0 correct=0 wrong=0 constants_failed=4/4 met=false`, rc 1|

D5 fixtures (C1 v2 schema, `{"id","kind","path","params","observed"}`; the counter prints the same
fields the frozen line names; `revision=aaaa…` is the fake 40-hex revision):

|Fixture|Pristine line|rc|
|---|---|---|
|`clean` (2 evidenced + 2 gap, markers `~ ~ ␠ ␠`)|`boxes=4 evidenced=2 gap=2 unexamined=0 mismatches=0 met=true`|0|
|`all-evidenced`|`boxes=4 evidenced=4 gap=0 unexamined=0 mismatches=0 met=true`|0|
|`holds-contradict` (recorded `observed=false`, `holds=true`, path exists)|`boxes=4 evidenced=3 gap=0 unexamined=0 mismatches=1 met=false`|1|
|`empty-checks` (4 rows, `checks: []`)|`boxes=4 evidenced=0 gap=0 unexamined=4 mismatches=8 met=false`|1|
|`x-no-verifier` (`[x]`, evidenced row, no `verifier`)|`boxes=4 evidenced=3 gap=0 unexamined=1 mismatches=2 met=false`|1|
|`duplicate-row` (two valid rows for box 1)|`boxes=4 evidenced=3 gap=0 unexamined=0 mismatches=1 met=false`|1|
|`blank-no-ledger` (four `[ ]`, no ledger)|`boxes=4 evidenced=0 gap=0 unexamined=4 mismatches=0 met=false`|1|

`blank-no-ledger` reproduces amendment 1 A1's frozen base line exactly; the live base run on the
scored counter is the same line at `a2cc5f51`:

```
$ python3 -B .ufo/waves/round-77/c77_shonen_ledger.py --root . \
    --revision a2cc5f51002433e11cc3d2f70e650a6c60ad5e68 --work $W/base-final
C1 revision=a2cc5f51002433e11cc3d2f70e650a6c60ad5e68 boxes=4 evidenced=0 gap=0 unexamined=4 mismatches=0 met=false
exit 1
```

Detector agreement was checked on unfixed bytes before any mutant was scored: on the round-39 tool,
D1 and D2 print the same population (`correct=2 wrong=18` / `ok=2 wrong=18`), so a per-case
attribution from D2 is the same comparison D1 makes. D1/D3/D4/D6 are green before every mutation, so
every red below is caused by the mutant and not by the baseline.

## 2. `scripts/sitemap_audit.py` mutants (D1+D2+D3)

One hunk each unless named; applied with an exact-span patcher that refuses a partial match; applied
to a fresh copy of the pinned blob, never to the lane file. `out` is the mutant's sha256 prefix;
`restored` is `sha256(copy after restore) == sha256(pinned)`.

|Id|Mutation|Matrix line after the mutation|Selftest after|D2 wrong cases|Verdict|out / restored|
|---|---|---|---|---|---|---|
|S1a|dispatch the container on `path.endswith(".gz")` instead of `magic == GZIP_MAGIC` (G2)|`cases=20 decided=20 correct=18 wrong=2 constants_failed=4/4 met=false` rc 1|`PASS 265/271` (`r77_gzip_magic_reads_body`, `r77_gzip_name_plain_body`)|`g01, g04`|**killed** (D1, D2, D3)|`1831737d0dedda05` / true|
|S1b|remove the magic check entirely: never decompress|`correct=16 wrong=4` rc 1|`PASS 266/271` (`r77_gzip_magic_reads_body`, `r77_gzip_decompressed_too_large`)|`g01, g02, g03, t06`|**killed**|`ebdfa2c007c3330b` / true|
|S2|apply the 52,428,800 limit to the compressed file (`os.path.getsize`) and read the expanded body unbounded (G1)|`correct=19 wrong=1` rc 1|`PASS 270/271` (`r77_gzip_decompressed_too_large`)|`g02`|**killed**|`3947eebdd8e75503` / true|
|S3|accept a relative text URL: drop `text_url_not_absolute` (T1)|`correct=19 wrong=1` rc 1|`PASS 269/271` (`r77_text_relative_url`, `r77_text_scheme_url`)|`t03`|**killed**|`6043ba0f8ff35e59` / true|
|S4|drop the 50,000-entry text check (`if False`)|`correct=19 wrong=1` rc 1|`PASS 270/271` (`r77_text_too_many_entries`)|`t05`|**killed**|`a58c89404627bd25` / true|
|S5|drop the feed missing-link finding in both `_audit_rss` and `_audit_atom`|`correct=18 wrong=2` rc 1|`PASS 269/271` (`r77_rss_missing_link`, `r77_atom_link_without_href`)|`a02, r02`|**killed** (both ids proved separately)|`6861e655e700ba5f` / true|
|S6|treat a malformed RSS `<pubDate>` as clean (`_valid_feed_date` → `True`)|`correct=19 wrong=1` rc 1|`PASS 270/271` (`r77_rss_bad_pubdate`)|`r03`|**killed**|`b34bb8502855dac5` / true|
|S6b|treat a malformed Atom `<updated>` as clean (`not _valid_lastmod(...)` → `False`)|`correct=19 wrong=1` rc 1|`PASS 270/271` (`r77_atom_bad_updated`)|`a03`|**killed**|`08d4cb36a03636fb` / true|
|S7|return `(None, set())` for a root outside `urlset/sitemapindex/rss/feed` (X1)|`correct=19 wrong=1` rc 1|`PASS 270/271` (`r77_root_html_unsupported`)|`d01`|**killed**|`11bf20fa3957a83a` / true|
|S8|catch `BaseException` at the entry point and `sys.exit(0)`|`correct=8 wrong=12` rc 1|`PASS 71/271` (`cli_single_document_findings`, `cli_no_args`, …)|`a02 a03 d01 g02 g03 r02 r03 r04 t02 t03 t04 t05`|**killed** (it also swallows `SystemExit`, so every non-clean verdict collapses to 0)|`6cb52e4f8736a944` / true|
|S8e|catch `Exception` (not `BaseException`) at the entry point and `sys.exit(0)`|`correct=20 wrong=0 … met=true` rc 0|`PASS 271/271`|none|**survived** — see §5 F1|`b2f38a008b89e422` / true|

Notes on the kills that are easy to overstate:

- `S1a` fails two cases because the matrix now decides G2 in both directions (`g01` is gzip bytes
  under a non-`.gz` name, `g04` is plain XML under a `.gz` name); a name dispatcher cannot pass both.
  Before the `g01` rename (pin of 22:49) the same mutant was red on `g04` only.
- `S2`'s first attempt at the literal mutation (bounded read kept, limit skipped for compressed) is
  not equivalent: the expanded body is truncated at 52,428,801 bytes, the XML parse fails, and `g02`
  still goes red — but for `xml_malformed`, not for the size rule. The recorded mutant removes both
  the compressed-size-limit substitution and the bounded read, so `g02` is clean 0 and the kill is
  unambiguous.
- `S6` and `S6b` are separate because the tool validates RSS `<pubDate>` with `_valid_feed_date`
  (RFC 822 or sitemap form) and Atom `<updated>` with `_valid_lastmod`; one mutation of
  `_valid_feed_date` leaves `a03` green, which is why the pair is reported.

## 3. `c77_sitemap_matrix.py` mutants (D6+D7+D8+D9)

|Id|Mutation|D6 selftest|Independent fixture|Verdict|out / restored|
|---|---|---|---|---|---|
|M1|`judge()`: a 0/1 case with the right exit and the wrong finding set is correct (`and True`)|`selftest 13/14 passed`, FAIL `empty-findings-constant-killed (failed=[])`|D7 (base tool): `correct=12 wrong=8`, where D2's independent count is `wrong=18`; D8: `constants_failed=2/4`|**killed**|`5d703f7e9c4a13f2` / true|
|M2|`met` requires three failing constants instead of all four (`>= CONSTANT_COUNT - 1`)|`13/14 passed`, FAIL `surviving-constant-not-counted (constants_failed=3 survivors=['survivor.py'])`|D8: `correct=20 wrong=0 constants_failed=3/4 met=true` (pristine: `met=false`)|**killed**|`52640fb3aa2985e6` / true|
|M3|compare exit codes only, in both the 0/1 and the input-fault branch|`10/14 passed`; FAILs `empty-findings-constant-killed`, `exit-two-needs-error-status`, `wrong-input-fault-code-rejected`, `mixed-fault-finding-rejected`|D7: `correct=12 wrong=8` vs independent `wrong=18`; D8: `constants_failed=2/4`|**killed** (four independent selftest checks)|`709b82d1b6975734` / true|
|M4|`tally()`: `decided = len(results)` (undecided counts as decided)|counter raised `AssertionError` in `tally` (`assert correct + wrong == decided`), no line, rc 1|D9: same `AssertionError`, stdout empty|**killed** (fails closed: no line rather than a wrong line)|`4ade8b7806376d1a` / true|

M4's crash is the counter's own invariant doing its job; it is recorded as a kill because the
observable output differs from pristine (pristine D9 prints `decided=0 … met=false`), but the failure
mode is a traceback with rc 1 rather than a silently green line.

## 4. `c77_shonen_ledger.py` mutants (D4+D5)

|Id|Mutation|D4 selftest|D5 fixture that changes|Verdict|out / restored|
|---|---|---|---|---|---|
|L1|trust the ledger: skip `observation-differs` and take `bool(check.get("holds", True))` as the verdict instead of `_verdict`|`23/26 passed`; FAILs `a5-06-observed-contradicts-derivation`, `threshold-below-min`|`holds-contradict`: `met=false` → `met=true` (mismatches 1 → 0)|**killed**|`ad88566231284122` / true|
|L2|allow `checks: []` at the schema gate only|`25/26 passed`, FAIL `empty-checks: unexamined=0 != 1`|`empty-checks`: `unexamined=4 mismatches=8` → `unexamined=0 mismatches=4`, `met=false` in both|**killed on the printed line; the verdict is defended** — the second gate `all_pass = all(verdicts) if verdicts else False` still emits `status-unsupported`, so the claim could not have been greened by this single change|`27b05cd74e842723` / true|
|L2b|L2 plus `all_pass = … if verdicts else True`|`25/26 passed`, FAIL `empty-checks: met=True != False`|`empty-checks`: `met=true`, `evidenced=4` (pristine `met=false`)|**killed** (the printed line and the verdict both flip; the fixture class is the right one)|`8013ca2eb6c70d18` / true|
|L3|drop the `[x]`-needs-verifier rule at both gates (schema and evaluation)|`25/26 passed`, FAIL `x-without-verifier: met=True != False`|`x-no-verifier`: `met=false` → `met=true`, `mismatches 2 → 0`|**killed**|`71293f647ae59ef5` / true|
|L4|duplicate rows: last valid row wins (`by_box[box] = [row]`)|`25/26 passed`, FAIL `duplicate-row: met=True != False`|`duplicate-row`: `met=false` → `met=true`|**killed**|`07cb5d62d155ce7d` / true|

L1's fixture carries `holds: true` over a recorded `observed` that the path contradicts — exactly the
laundering shape amendment 2 A3 closes. L3 is the case that the v1 counter's selftest missed (its
`x-without-verifier` fixture also carried a marker-disagreement, so it stayed red for another reason
and the rule could be removed without a red); the v2 selftest's `x-without-verifier` case now isolates
it, and the planted tree isolates it independently.

## 5. Survivors, coverage findings, and instrument observations

**F1 — S8e survived both frozen detectors; the missing case is an output-channel fault.**
`except Exception: sys.exit(0)` at `__main__` is inert for every input that reaches `main`, because
`main` already wraps manifest loading (`f767af77` lines 863–866) and the whole check loop (lines
877–886) in `except Exception` and returns `input_invalid` at exit 2. The one path that escapes is a failure while
emitting the document, after those handlers. Measured with a closed read end (a full-size output
piped into `head -c 0`, `t05` case):

```
$ python3 -B $T --manifest cases/t05/manifest.json 2>err | head -c 0
pristine rc=1   stderr: BrokenPipeError: [Errno 32] Broken pipe
$ python3 -B mutants/S8e.py --manifest cases/t05/manifest.json 2>err | head -c 0
S8e rc=0        stderr: (empty)
```

So the mutant is reachable but outside the frozen population: the 20-case matrix and the 271-case
selftest never close stdout. The case the instrument should have had is a "tool output cannot be
written" probe (or a one-line statement that output-channel faults are out of scope); neither the
matrix nor the selftest names that boundary today. The verdict is **survived within the frozen
detectors, not equivalent**.

**F2 — L2 shows the ledger counter is defended in depth on the empty-`checks` shape.** Removing the
schema non-empty gate alone moves `unexamined` but not `met`; only removing the second gate (L2b)
greens the box. Recorded as a strength, and as the reason the table separates L2 from L2b.

**F3 — intermediate instrument states were red; the scored bytes are green.** These are the exact
reds seen while pinning (each was reproduced at the time and is not reproducible from the final
bytes):

- Matrix, tool `16ea784f…`/`98cdb926…` of 22:46–22:51: `cases=20 decided=20 correct=18 wrong=2
  constants_failed=4/4 met=false`, wrong on `g02` (tool emitted `sitemap_too_large`, case expects
  amendment A5's `too_large`) and `g03` (tool emitted `gzip_corrupt`, case expects amendment A6's
  `gzip_invalid`).
- Matrix counter `5c6eacba` against the case set as it stood before 22:49:45 refused to run —
  `c77_sitemap_matrix: cannot evaluate: …/cases/g03: an exit-2 case must name its input-fault error
  code`, rc 2, no printed line — because `g03/expect.json` still had `"findings": []`. The case was
  corrected to `["gzip_invalid"]` at 22:49:45 and the counter then ran.
- Tool selftest `19b265ce` against tool `742c2ab1`: `PASS 266/267`, FAIL
  `r77_root_html_with_doctype_unsupported` (the tool had moved the doctype gate ahead of the root gate
  per A9; the case still expected `format_unsupported`). Scored selftest `f22e0a67` with tool
  `f767af77` is `PASS 271/271`.
- C1 v1 counter `a9eef8bd` on the base revision printed
  `… unexamined=4 mismatches=4 met=false`, contradicting amendment 1 A1's frozen
  `mismatches=0`; its selftest case `missing-ledger` pinned `"mismatches": 4` (v1 line 927–929). The
  scored v2 counter prints `mismatches=0` at `a2cc5f51` (line quoted in §1) and zeroes the
  blank-marker path deliberately (`if box["marker"] in ("~", "x")` guards `marker-without-row`).

**F4 — the `g01` fixture was renamed mid-wave to make G2 two-directional.** `sitemap.xml.gz` →
`sitemap.xml.bin` with identical bytes and expectation (`cases/README.md` says so at lines 54–58).
This strengthens the `g01`/`g04` pair against name-based dispatch; the S1a row records both kills.

**F5 — no mutant exposed a green-turning gap in the scored population.** All 11 C2-tool mutants, 4
matrix-counter mutants and 5 ledger-counter mutants are killed by the frozen detectors except S8e,
whose reachability is outside the population (F1). No case expectation needed changing, and no
mutation reported `met=true` where the pristine reported `met=false` without its own detector also
going red (M2's `met=true` on D8 is the intended kill; `met=true` there is against a three-failing
constant set, not the shipped one).

## 6. Restoration and scratch evidence

Every mutant was applied to `$S/mutants/<id>.py` from the pinned blob, then run: the 11 C2-tool and
5 C1 copies passed an explicit `compile(bytes, path, "exec")` check before their detectors ran, and
all 4 matrix-counter copies executed (M1–M3 printed a line, M4 raised its own `AssertionError`), so
every one of the 20 is syntactically live. After the run each copy was overwritten again from the
pinned blob with `python3 restore.py <pinned> <mutant>`, which printed `identical: true`. The pinned copies were
never edited: after the last mutant the four lane files still hash to the §0 digests (drift check
above). Mutant digests (sha256) are in the tables; the pristine digests are in §0.

Scratch `S=/fast/scratch/hyaku/kake-r77/MutC` (pinned copies, fixtures, fake `git`, mutants,
receipts, work dirs) was removed with `rm -rf -- "$S"` after this report was written. Nothing was
written outside `S` and this file: the lane checkout, `.ufo/state/`, `MANIFEST.json`, the fleet repo
and every sibling lane were untouched.

## 7. Re-run recipe

```sh
S=/fast/scratch/hyaku/kake-r77/MutC; mkdir -p "$S"; cd <lane>
# 1. pin the four instruments + cases + consts into $S/pin, sha256sum them
# 2. detectors, pristine: matrix / percase / tool selftest / ledger selftest
python3 -B .ufo/waves/round-77/c77_sitemap_matrix.py --root . --tool $S/pin/sitemap_audit.py \
  --cases $S/pin/cases --consts $S/pin/consts --work $S/work/base --json-out $S/receipts/base.json
python3 -B $S/pin/sitemap_audit_selftest.py --tool $S/pin/sitemap_audit.py
python3 -B .ufo/waves/round-77/c77_shonen_ledger.py --selftest --work $S/work/lst
python3 -B .ufo/waves/round-77/c77_shonen_ledger.py --root . \
  --revision a2cc5f51002433e11cc3d2f70e650a6c60ad5e68 --work $S/work/lbase
# 3. one mutant: exact-span replace on a copy, then the three C2 detectors or the seven C1 trees
# 4. restore from the pinned blob and compare sha256 with the pinned digest
```

The per-mutant spans are in §2–§4; each is a single semantic change (S2, S5, L1, L3 and L2b carry
two hunks of the same change, named where applied).
