# ScribeReportMeasurements — report section draft (round-63, kake w1)

Scope: the report's **Before → after measurements** section only. One entry per
claim, exact counting command, measured/base revisions, and the committed
receipt lines pasted verbatim. No counter, control, fixture or receipt was
edited or re-run for this draft.

## Pins used by every measurement

| Pin | Value | Where verified |
|---|---|---|
| measured commit | `05b0d7f4b4a23513390f7b92547e2b0f1fccb06f` | `git ls-tree -r --name-only 05b0d7f4 -- .ufo/waves/round-63` lists both counters, both base receipts, both controls (`control-marker-fixture.txt`, `control-junk-fixture.txt`), `contract.md`, `quote-class/quote-classes.json`, `quote-class/S432.txt`, `quote-class/extract_text.py`, `sources/S432.live.html` |
| base (round-62 tip) | `13d4519818db28cd0aa912e49020659140d7b9fa` | `git merge-base --is-ancestor 13d45198 05b0d7f4` → exit 0 ("base is ancestor of measured") |
| counters' `BASE` constant | `13d4519818db28cd0aa912e49020659140d7b9fa` | `c63_calibration.py:40`, `c63_quote_tool.py:23` |
| after receipts commit | `7f77d12b370b42d0d724bd784bd1bfff47fff17b` ("round-63: green-after receipts at measured commit 05b0d7f4") | `git show --stat 7f77d12b` → only `after-c1.txt` + `after-c2.txt`, 8 insertions, nothing else |

Both counters and the tool resolve every input with
`git -C <root> show <revision>:<path>`, so the printed `revision=` is the tree
actually measured, not the working tree.

## Before → after measurements

### C1 — calibration (lowest owned axis, 2/10), contract §C1

Claim: the c62 counter family's marker-only false green is dead — every
`resolved` component is re-derived from committed bytes at the measured
revision.

Counting command (contract §C1, verbatim; `<commit>` substituted exactly as run):

```
python3 -B .ufo/waves/round-63/c63_calibration.py --root . --revision 05b0d7f4b4a23513390f7b92547e2b0f1fccb06f
```

Before — `13d4519818db28cd0aa912e49020659140d7b9fa` (`red-before`),
committed at `05b0d7f4` in `.ufo/waves/round-63/controls/base-c1.txt`:

```
# receipt: base C1 (red-before) — c63 semantics-binding counter at round-62 tip
$ python3 -B .ufo/waves/round-63/c63_calibration.py --root . --revision 13d4519818db28cd0aa912e49020659140d7b9fa
revision=13d4519818db28cd0aa912e49020659140d7b9fa disagreements=1 quote_correction=0 blobs_match=0 derived=unevaluable class_match=0 criterion=1 lesson_gate=0 source_row=1 unresolved=1 met=false
exit=1
```

After — measured commit, committed at `7f77d12b` in
`.ufo/waves/round-63/controls/after-c1.txt`:

```
# receipt: after C1 — c63 semantics-binding counter at measured commit 05b0d7f4b4a23513390f7b92547e2b0f1fccb06f
$ python3 -B .ufo/waves/round-63/c63_calibration.py --root . --revision 05b0d7f4b4a23513390f7b92547e2b0f1fccb06f
revision=05b0d7f4b4a23513390f7b92547e2b0f1fccb06f disagreements=1 quote_correction=1 blobs_match=1 derived=collapsed-only class_match=1 criterion=1 lesson_gate=1 source_row=1 unresolved=0 met=true
exit=0
```

Component deltas between the two receipts:

| Field | Base | Measured | Bound to (counter lines) |
|---|---|---|---|
| `disagreements` | 1 | 1 | count of S432 `Disagree` lines in `corpus/lessons/round-61-verifier-spotcheck.md` (unchanged — the disagreement is resolved by admitted class, not by editing the spot-check) |
| `quote_correction` | 0 | 1 | `[r63-correction` + frozen span + ledger path in `corpus/knowledge/response-header-expectations.md`, AND `blobs_match`, AND `class_match` (`c63_calibration.py:121-145`) |
| `blobs_match` | 0 | 1 | ledger `rawSha256`/`textSha256`/`quote` equal sha256 of the retained blobs at the revision (`:130-137`) |
| `derived` | `unevaluable` | `collapsed-only` | `classify()` run inline over the two blobs (`:59-67`, invoked `:138-141`; round-50 semantics) |
| `class_match` | 0 | 1 | `derived == "collapsed-only" == ledger.matchClass` (`:142-143`) |
| `criterion` | 1 | 1 | `corpus/QUALITY.md` names `X-Content-Type-Options`/`Content-Type`/`destination` (`:148-150`) |
| `lesson_gate` | 0 | 1 | `corpus/lessons/round-63.md` records the outside verdict + `collapsed-only` + author-side label (`:153-159`) |
| `source_row` | 1 | 1 | `^\|\s*S432\s*\|` in `corpus/SOURCES.md` (`:162`) |
| `unresolved` | 1 | 0 | `disagreements if not resolved else 0` (`:164-166`) |
| `met` / exit | `false` / 1 | `true` / 0 | `resolved = quote_correction and criterion and lesson_gate and source_row` (`:164`) |

Falsifier control (same counter, marker-only fixture), committed at `05b0d7f4`
in `.ufo/waves/round-63/controls/control-marker-fixture.txt`:

```
# receipt: marker-only false-green control (round-62 routed-defect fixture, corpus copied byte-exact from committed .ufo/waves/round-62/controls/false-green-fixture/corpus)
# fixture: scratch git repo, top-level verified, rev 7833be888760bc7878857aa39362792b02e3ab07
$ python3 -B .ufo/waves/round-62/c62_calibration.py --root <fixture> --revision <rev>  # old counter, family defect
revision=7833be888760bc7878857aa39362792b02e3ab07 disagreements=1 unresolved=0 quote_correction=1 criterion=1 lesson_gate=1 source_row=1 met=true
exit=0
$ python3 -B .ufo/waves/round-63/c63_calibration.py --root <fixture> --revision <rev>  # repaired counter
revision=7833be888760bc7878857aa39362792b02e3ab07 disagreements=1 quote_correction=0 blobs_match=0 derived=unevaluable class_match=0 criterion=0 lesson_gate=0 source_row=1 unresolved=1 met=false
exit=1
```

Junk-marker control, committed at `05b0d7f4` in
`.ufo/waves/round-63/controls/control-junk-fixture.txt`:

```
# receipt: junk-marker control — adversarial marker planting without retained blobs/ledger
# fixture: scratch git repo rev 7da479c28d206a9733cf2012b6ea434c4dab450f
$ python3 -B .ufo/waves/round-63/c63_calibration.py --root <fixture> --revision <rev>
revision=7da479c28d206a9733cf2012b6ea434c4dab450f disagreements=1 quote_correction=0 blobs_match=0 derived=unevaluable class_match=0 criterion=1 lesson_gate=1 source_row=1 unresolved=1 met=false
exit=1
```

Reading: both controls carry `met=false` under c63; the marker control
additionally shows the *old* c62 counter printing `met=true` on the same bytes —
the routed defect is preserved as history and the repair is receipt-visible,
not asserted.

### C2 — operability (HOLD 10), contract §C2

Claim: the committed quote-class tool runs its frozen 4-case selftest at the
measured revision.

Counting command (contract §C2, verbatim; `<commit>` substituted exactly as run):

```
python3 -B .ufo/waves/round-63/c63_quote_tool.py --root . --revision 05b0d7f4b4a23513390f7b92547e2b0f1fccb06f
```

Before — base, committed at `05b0d7f4` in
`.ufo/waves/round-63/controls/base-c2.txt`:

```
# receipt: base C2 (red-before) — quote-tool counter at round-62 tip
$ python3 -B .ufo/waves/round-63/c63_quote_tool.py --root . --revision 13d4519818db28cd0aa912e49020659140d7b9fa
revision=13d4519818db28cd0aa912e49020659140d7b9fa present=0 selftest=unevaluable met=false
exit=1
```

After — measured commit, committed at `7f77d12b` in
`.ufo/waves/round-63/controls/after-c2.txt`:

```
# receipt: after C2 — quote-tool counter at measured commit 05b0d7f4b4a23513390f7b92547e2b0f1fccb06f
$ python3 -B .ufo/waves/round-63/c63_quote_tool.py --root . --revision 05b0d7f4b4a23513390f7b92547e2b0f1fccb06f
revision=05b0d7f4b4a23513390f7b92547e2b0f1fccb06f present=1 selftest=4/4 frozen_cases=ok met=true
exit=0
```

Field deltas: `present` 0→1 (`git show <rev>:scripts/quote_class.py`
resolves at measured, absent at base); `selftest` `unevaluable`→`4/4`
(subprocess `--selftest --json` run from the lane root against the extracted
blob); `frozen_cases` absent→`ok` (all four frozen ids
`inline_raw_substring`, `markup_collapsed_only`, `absent_everywhere`,
`s432_real` present, `passed`, and `derived == expected`,
`c63_quote_tool.py:25-30,77-85`); `met` false→true, exit 1→0.

The before-state is structural, not incidental: at
`13d4519818db28cd0aa912e49020659140d7b9fa`,
`git ls-tree -r --name-only 13d45198 -- .ufo/waves/round-63 scripts/quote_class.py`
prints nothing (exit 0, zero paths), and `corpus/lessons/round-63.md` is absent
from the base tree while `corpus/lessons/round-63.md` exists at `05b0d7f4`.

## Artifact provenance (hashed, read-only)

`sha256sum` of the worktree files and `git show 05b0d7f4:<path> | sha256sum`
agree for every frozen artifact below (worktree == measured blob):

| Path | sha256 at measured commit | Expected value |
|---|---|---|
| `.ufo/waves/round-63/c63_calibration.py` | `bcd16f680da2594040a897803ddefa82ff13679ebe458dd6f6ff6c957ea3fc91` | matches |
| `.ufo/waves/round-63/c63_quote_tool.py` | `9fcbfad06fe6abed2b23556894879491204a1ef4d2b9f3cf194a9a3aeaa7f01e` | matches |
| `.ufo/waves/round-63/quote-class/quote-classes.json` | `5f48e26be27975ee55702cac1e1b20b61f3bd5906910c865f5192bd7e010c42d` | matches |
| `scripts/quote_class.py` | `431e75e8fee2c913c6fa74aebbf7cb2e678f139a1a37b3d38994d1bb22841f14` | matches (post freeze-note value) |
| `.ufo/waves/round-63/quote-class/S432.txt` | `8b90d096d2653ce57025e25c5bee5c63df66692e15ef8579371032da6f542a69` | equals ledger `textSha256` |
| `.ufo/waves/round-61/sources/S432.html` | `63b0a018753c330adf1e40417524eb70ea02d4d3e123bcb39b6770f23bad911b` | equals ledger `rawSha256` |

Ledger `quote-classes.json` row `S432`: `matchClass=collapsed-only`,
`locatedRawLines=6150-6154`. Independent substring check of the frozen span
(`"The \`X-Content-Type-Options\` response header … destination of a request."`):
`grep -Fc` on the raw HTML → `0` hits; on `S432.txt` → `1` hit — i.e. the span
is collapsed-only, which is why C1 derives `collapsed-only` rather than
`raw-substring`.

Receipt files themselves: `after-c1.txt` =
`d825d214be22b443887523c5905a1808ad3e8d51cf396be800c52943ca523952`,
`after-c2.txt` =
`999dacde6cb01c03d32c15cae97a92d62574830eae1a375e689e75a0681dc20b`, each
identical between worktree and `7f77d12b:<path>`.

Marker-control input integrity: the five corpus files under
`.ufo/waves/round-62/controls/false-green-fixture/` hash at `05b0d7f4` to
exactly the values recorded in
`.ufo/waves/round-62/controls/counter-false-green-l1.txt`
(`0a9a0348…`, `635089aa…`, `373b9d25…`, `d7033c6d…`, `a27f4338…`), so the
control was fed the same bytes that produced the round-62 defect.

## Known limits of this section

1. **Receipt commit is one commit after the measured commit.** `after-c1.txt` /
   `after-c2.txt` are empty at `05b0d7f4` and land in `7f77d12b`; that commit
   changes only those two files (8 insertions), so the measured tree is
   untouched by receipt capture.
2. **Fixture revisions are scratch-only.** `7833be888760bc7878857aa39362792b02e3ab07`
   and `7da479c28d206a9733cf2012b6ea434c4dab450f` exist in deleted
   `/fast/scratch/hyaku/...` repos; only the receipts and the byte-identical
   committed corpus survive. The control lines are receipt evidence, not
   re-derivable from this tree without rebuilding the fixtures.
3. **No committed stub-tool control receipt.** C2's stub rejection is
   code-level (`c63_quote_tool.py:77-85` requires all four frozen case ids,
   `passed`, `derived == expected`, `total == passed == 4`), not
   receipt-demonstrated. C1's adversarial control does have a receipt
   (`control-junk-fixture.txt`).
4. **Nothing was re-run.** All before/after numbers above are pasted from the
   committed receipts; I verified artifact hashes and revision ancestry only.
   No claim here rests on a fresh execution of either counter.
5. **`disagreements=1` persists after the fix.** The S432 `Disagree` line is
   still counted; the resolution is the admitted `collapsed-only` class plus
   the correction block, so `unresolved` drops to 0 without the spot-check
   being edited (no-harm: spot-check untouched).
