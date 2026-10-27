# LabratC1Controls

Seat: labrat probe for the C1 counter (`.ufo/waves/round-59/c59_axis_evidence.py`, **VERSION 1**, frozen sha256
`95d23511d548a9c5fe5f76c201b002e931d9ecd55faca51c9c037c08d25be690`, = `contract.json.claims.C1.counterSha256v1`).
VERSION 1 was scored here; no claim was scored and no after-state was built in the lane.

## Method

Scratch clone `/fast/scratch/hyaku/kake-r59/LabratC1Controls/lane` (`git clone --shared` of the lane); each control is a
separate commit on top of the contract commit `45a92b64ac8a0f82dba369100e30682f14de81fb`, scored with the frozen counter:
`python3 -B .ufo/waves/round-59/c59_axis_evidence.py --root <clone> --revision <commit> --base fd6303ce5c14b3f892dec586297a942ab6e4193b [--json]`.
The lane repo, its Git index and its jj state were not touched (read-only `git show/log/status` only); the only lane
writes are this report and `.ufo/waves/round-59/w1/LabratC1Controls.files/`.

Baseline reproduced exactly: scoring the contract commit under `--base fd6303ce` gives `mismatches=16 unresolved=11
rows_no_receipt=3 receipts_off_axis=0 tallies_unfound=0 rows_no_tally=2 rows=3 scores_held=2 superseded_kept=0 met=False`,
exit 1 — identical to the committed `controls/base-c1-axis-evidence.txt`. (`--selftest` is a stub: "version 1 stub (wave 1
writes the fixture kill matrix); exit 2", exit 2.)

## CONTROLS:

34 controls, each its own commit. `met` is the counter's own verdict (exit 0 = met); counts are its `--json` fields.
`sup` = the three base cells appended verbatim outside the axis table (the claimed append-only step).

| control | exit | met | mism | unres | no_rcpt | off_axis | tally_miss | no_tally | scores | superseded |
|---|---|---|---|---|---|---|---|---|---|---|
| a-do-nothing | 1 | False | 16 | 11 | 3 | 0 | 0 | 2 | 2 | 0 |
| b-emptied-cells | 1 | False | 6 | 0 | 3 | 0 | 0 | 3 | 2 | 3 |
| b-emptied-cells-noappend | 1 | False | 6 | 0 | 3 | 0 | 0 | 3 | 2 | 0 |
| c-random-lane-file | 1 | False | 6 | 0 | 3 | 0 | 0 | 3 | 2 | 3 |
| c-random-lane-file-noappend | 1 | False | 6 | 0 | 3 | 0 | 0 | 3 | 2 | 0 |
| c2-random-lane-file-with-tally | 1 | False | 3 | 0 | 3 | 0 | 0 | 0 | 2 | 3 |
| d-fabricated-tally | 1 | False | 6 | 0 | 0 | 0 | 3 | 3 | 2 | 3 |
| d-fabricated-tally-noappend | 1 | False | 6 | 0 | 0 | 0 | 3 | 3 | 2 | 0 |
| e-off-axis-receipt | 1 | False | 3 | 0 | 0 | 3 | 0 | 0 | 2 | 3 |
| e-off-axis-receipt-noappend | 1 | False | 3 | 0 | 0 | 3 | 0 | 0 | 2 | 0 |
| **f-minimal-true** | **0** | **True** | 0 | 0 | 0 | 0 | 0 | 0 | 2 | 3 |
| g-minimal-true-no-append | 1 | False | 0 | 0 | 0 | 0 | 0 | 0 | 2 | 0 |
| h-nonreceipt-blob-under-round-dir | **0** | **True** | 0 | 0 | 0 | 0 | 0 | 0 | 2 | 3 |
| i1-r59-base-receipt-tally-3-3 | 1 | False | 12 | 0 | 3 | 3 | 3 | 3 | 2 | 3 |
| **i2-r59-after-receipt-with-r59-section** | **0** | **True** | 0 | 0 | 0 | 0 | 0 | 0 | 2 | 3 |
| j1-r59-base-receipt-tally-3-3-nosection | 1 | False | 12 | 0 | 3 | 3 | 3 | 3 | 2 | 3 |
| j2-r59-after-receipt-no-r59-section | 1 | False | 6 | 0 | 3 | 3 | 0 | 0 | 2 | 3 |
| k-r59-base-receipt-with-r59-section | 1 | False | 6 | 0 | 0 | 0 | 3 | 3 | 2 | 3 |
| l-off-axis-receipt-only | 1 | False | 8 | 0 | 3 | 3 | 1 | 1 | 2 | 3 |
| m-r59-after-receipt-section-not-naming-axis | 1 | False | 6 | 0 | 3 | 3 | 0 | 0 | 2 | 3 |
| n-tally-from-unrelated-blob | **0** | **True** | 0 | 0 | 0 | 0 | 0 | 0 | 2 | 3 |
| o-r59-base-receipt-rows-3-3 | 1 | False | 6 | 0 | 0 | 0 | 3 | 3 | 2 | 3 |
| p-r59-base-receipt-tally-16-16 | **0** | **True** | 0 | 0 | 0 | 0 | 0 | 0 | 2 | 3 |
| q-mirror-receipt-bad-tally | **0** | **True** | 0 | 0 | 0 | 0 | 0 | 0 | 2 | 3 |
| r-r59-contract-as-receipt | **0** | **True** | 0 | 0 | 0 | 0 | 0 | 0 | 2 | 3 |
| s1-seat-report-path-nonexistent | 1 | False | 12 | 3 | 3 | 0 | 3 | 3 | 2 | 3 |
| s2-real-seat-report-as-receipt | **0** | **True** | 0 | 0 | 0 | 0 | 0 | 0 | 2 | 3 |
| t-counter-source-as-receipt | 1 | False | 6 | 0 | 0 | 0 | 3 | 3 | 2 | 3 |
| u-base-cells-one-char-changed | 1 | False | 0 | 0 | 0 | 0 | 0 | 0 | 2 | 2 |
| v1-decoy-plus-real-table-also-edited | **0** | **True** | 0 | 0 | 0 | 0 | 0 | 0 | 2 | 3 |
| v2-decoy-real-table-untouched | **0** | **True** | 0 | 0 | 0 | 0 | 0 | 0 | 2 | 3 |
| w-real-axis-table-only-no-append | 1 | False | 3 | 0 | 1 | 0 | 1 | 1 | 2 | 0 |
| y-r59-receipt-outside-controls-dir | **0** | **True** | 0 | 0 | 0 | 0 | 0 | 0 | 2 | 3 |
| z-decoy-only-no-append-no-section | **0** | **True** | 0 | 0 | 0 | 0 | 0 | 0 | 2 | 3 |

Control identities (`r59` = a round-59 receipt file also committed):

- **(a)** do-nothing: base SCORECARD unchanged → 16 mismatches, exit 1. Reproduces the committed base receipt.
- **(b)** three evidence cells emptied → `rows_no_receipt=3`, `rows_no_tally=3` → 6 mismatches, exit 1.
- **(c)** each cell replaced by one random existing lane file path (not a receipt): `corpus/knowledge/free-read-verbs.md`,
  `corpus/knowledge/freshness-sweep.md`, `corpus/knowledge/receipt-integrity.md` → `rows_no_receipt=3` → exit 1.
- **(c2)** same, but each cell also states a tally that *does* occur in the cited file (`18/21`, `60/60`, `27/27`) → the
  tally atom passes (`rows_no_tally=0`), the receipt atom still fires → 3 mismatches, exit 1.
- **(d)** on-axis receipt cited but a fabricated tally `99/99` → `tallies_unfound=3`, `rows_no_tally=3` → exit 1.
- **(e)** a correct-looking cell that *also* cites a receipt of a round with no claim on that axis (round 53 → operability/
  calibration; round 54 → freshness) → `receipts_off_axis=3` → 3 mismatches, exit 1.
- **(f)** minimal-true: each cell = one on-axis receipt + one tally from it, old cells appended verbatim at EOF → **exit 0**.
- **(g)** (f)'s cells but old cells not kept → `superseded_kept=0` → exit 1 (append-only atom bites).
- **(u)** base cells appended with one character changed in each → `superseded_kept=2` → exit 1 (verbatim check is strict).
- **(h/q)** cell cites a **non-receipt blob that merely lives under `.ufo/waves/round-58/`** — the round-58 assimilation
  mirror `SCORECARD.md` — with tally `117/117` (`q` used `12/12`, also present) → **exit 0**.
- **(n)** receipt and tally come from *different* cited blobs (receipt = round-58 control, tally from an unrelated corpus
  file) → **exit 0**.
- **(p)/(k)** cite the round-59 **base** control receipt — the file recording `mismatches=16 … met=False` — with the
  tally `16/16` inside it, plus a `## Round 59` SCORECARD section naming the axes → **exit 0**.
- **(o)** same receipt but a `3/3` tally *not* in it → `tallies_unfound=3` → exit 1.
- **(r)** cites **the round-59 frozen contract itself** (`.ufo/waves/round-59/contract.md`, which contains `21/21`) as the
  round-59 receipt → **exit 0**. **(y)** round-59 receipt placed **outside** `controls/` → **exit 0**.
- **(s2)** cites a **wave seat report** (`.ufo/waves/round-58/w1/ExecSourceLive.md`, tally `155/155`) → **exit 0**.
  **(s1)** the same shape with a path that does not exist → `unresolved=3` → exit 1 (the resolve atom works).
- **(t)** cites the counter's own source as the receipt → the source has no `21/21` → exit 1.
- **(i1)/(j1)** round-59 base receipt with a `3/3` tally, with/without a `## Round 59` section → 12 mismatches, exit 1.
- **(i2)/(j2)/(m)/(l)** a round-59 **after**-receipt (a real `controls/` file whose body carries `3/3`): **(i2)** with a
  `## Round 59` section naming the three axes → **exit 0**; **(j2)** without the section → `rows_no_receipt=3` +
  `receipts_off_axis=3`; **(m)** section present but its table does not name the axes → same off-axis failure;
  **(l)** off-axis-only receipt → 8 mismatches. So a round-59 receipt is only honoured when SCORECARD carries a
  `## Round 59` section whose table names that axis — a coupling worth knowing before the build.
- **(v1)/(v2)/(z)** a **decoy axis table prepended before the real one**: v1 takes the *first* table with the header, so the
  decoy is scored and the real (still broken) table is never read → **exit 0** with base defects still in the file
  (verified: `z` still contains `/tmp/kake-r17/…` and `cli.mjs:935` under the decoy).
- **(w)** correct cells, no append → `superseded_kept=0` → exit 1.

## READING:

**The hypothesis is confirmed for the five named cheap controls, and (f) MEETing is the claim's stated limit, not a
counter hole.** (a)-(e) all exit 1 with the correct disagreement counters: v1's tally atom, receipt-axis atom,
append-only atom and score-freeze atom all fire. (f) is the claimed work minimally — one on-axis receipt plus one tally
taken from that receipt, old cells kept verbatim — and the contract explicitly carves that out ("What the counter does
not test: whether a cited receipt supports the score (reviewer-checked)"). So (f) MEETing is the intended reviewer-checked
limit. **Three holes sit one level below the assignment's five, and each lets a build reach exit 0 while the claimed work
was never done.** These are the material findings.

1. **The receipt atom is "any blob under `.ufo/waves/round-<N>/`", not "a receipt."** v1's check is
   `re.match(r"^\.ufo/waves/round-(\d+)/", f)` plus an on-axis section lookup. It never requires the blob to *be* a
   receipt (a `controls/` measurement output), never requires it under `controls/`, never requires it to be new in this
   round, and never reads what it says. So **(h)** a round-58 assimilation *mirror* of SCORECARD.md counts as the receipt;
   **(s2)** a *wave seat report* counts; **(r)** the round-59 *frozen contract* counts; **(y)** a round-59 file outside
   `controls/` counts. Cheapest of these: cite the round-59 contract file you were handed, with the `21/21` it already
   contains — `rows_no_receipt` and `rows_no_tally` both pass with **no measurement of any kind performed**.
2. **The tally need not come from the receipt.** v1 searches the tally in *every* resolved blob the cell mentions
   (`bodies = [... for b in blobs]`), not in the cited receipt. **(n)** cites a real on-axis receipt and states `18/21`,
   which occurs only in an unrelated corpus file → met. The counter cannot tell "this receipt says 14/14" from "some file I
   also named says 18/21". The code matches its own docstring ("a resolved blob pointer of the same cell") — the defect is
   that the atom is stated at cell granularity rather than receipt granularity.
3. **A stale round's receipt is accepted as the current round's receipt.** **(p)/(k)** cite the round-59 *base* receipt —
   the file recording `mismatches=16 … met=False` — with the `16/16` inside it plus a `## Round 59` section naming the
   axes → met=True. v1 never reads the receipt's result. With holes 1+3 the cheapest end-to-end green needs **no run of
   the counter at all**: cite the frozen base receipt, cite the `16/16` it contains, add the round-59 section, keep the old
   cells verbatim.

Two further observations:

4. **The scored table is the first table with the header, not the lane's axis table.** **(v2)/(z)** prepend a decoy
   `| Axis | Score | Evidence pointer | Last change |` table; v1 scores the decoy and never reads the real one, so a build
   leaving the genuine axis table pointing at `/tmp/kake-r17/…` and `cli.mjs:935` still exits 0 (defects verified still
   present in the file).
5. **v1 never checks that a receipt's own result is positive.** (t) fails only incidentally (the counter source has no
   `21/21`); (o) fails only because its fabricated `3/3` is absent. A receipt recording `met=False` is accepted if it
   contains any `A/B` string.

**Cross-check against the counter currently being edited in the lane working tree** (`.ufo/waves/round-59/c59_axis_evidence.py`,
uncommitted, sha256 `1d04f19da1b47041642c99969498a948353f53acdc6d6869c8cb177f06a1ec02`; read-only, not mine, not
committed). Scored on my commits it rejects (n), (r), (y), (p), (k), (o), (i2), (j2), (m), (l), (v1), (v2), (z): it
narrows the tally atom to the receipt, requires the round section to be preserved verbatim from the base revision, and
adds `tables == 1`. It **still accepts (h), (q), (s2)** — a non-receipt blob under a round dir is still an on-axis
receipt. That is the same hole as (1). A one-line tightening closes it and keeps the true positives: requiring the receipt
path to match `^\.ufo/waves/round-(\d+)/controls/` turns (h), (q), (s2), (r), (y) into failures while (f) and the
recommended shape stay green (measured; patch receipts in the `.files/` tree). Whether to adopt it is the L1's call — the
assignment states the counter is VERSION 1 and this seat is read-only.

Note for the L1's own build: v2's round-section coupling means a round-59 receipt is honoured only if the measured
SCORECARD carries a `## Round 59` section whose base-revision text is preserved verbatim and whose table names the axis
(control **i2** is green under v1; under v2 it is not, because the round-59 section does not exist in the base revision).
Whichever counter version the L1 freezes, the after-cells must be paired with the matching SCORECARD section.

**A shape green under v1, under v2, and under the tightened patch** (measured, commit `e069d9083cff`): each cell cites a
real round-58/round-56 `controls/` after-receipt with the tally that receipt itself contains (`14/14`, `8/8`, `19/19`), a
`## Round 59` section naming the three axes is appended, and the three base cells are appended verbatim. Exit 0 under all
three. If the L1 builds C1 this way the hole set need not be closed first — but the honest-build hole (3) still lets a
*cheaper* build in, so a green C1 must be reviewed against "which receipt, produced by which run".

**Risk note on this seat's evidence.** All 34 controls are synthetic states I authored in a scratch clone; none is a
claim, none is a measured after-state, and no receipt here was produced by a real C1 run. The "recommended shape" finding
is about the counter's arithmetic, not about the truth of any claim. No round-59 after-state was scored, so nothing here
says whether the C1 claim is or is not met.

**Open questions for the L1.** (i) Should the receipt atom require `controls/` — deciding whether (h)/(s2)/(r)/(y) are
holes or reviewer territory? My measurement says the one-line tightening separates them cleanly; I did not modify the lane
counter. (ii) Should the receipt be required to be *new* (absent at base) and to record `met=True`? Both are single-atom
additions; the second rejects (p)/(k)/(o) and (s2) while keeping (f) green. (iii) The contract's scope statement ("a
receipt of a round with no claim on the axis fails") suggests the author intended receipts to be receipts; the atom does
not enforce it. If (h)/(s2)/(r) are in-scope reviewer checks, that should be recorded explicitly — (r) otherwise makes
the counter green with **zero** measurement performed.

**Receipts.** `.ufo/waves/round-59/w1/LabratC1Controls.files/` — `manifest.json` (all 34 controls, commits, counts),
`<control>.json` (each `--json` run verbatim), `<control>.txt` (each plain-text run with argv and exit code),
`build_controls{,2,3,4}.py` (builders), plus the two v1 patch scripts and the in-flight v2 copy used for the cross-check.

Tooling: nothing was installed or upgraded for this seat (only `python3` 3.14 and `git`, both already present), so per
the operator directive of 2026-10-19 there is no tool/version/channel entry. `pacman` was not run.

VERDICT: v1 rejects all five named cheap controls (a)-(e) with the correct disagreement counters and (f) MEETs as the
claim's stated reviewer-checked limit, but three unexercised holes remain — any blob under a round dir counts as a
receipt (the round-59 contract itself is green, with no measurement), the tally may live outside the cited receipt, and
the round-59 *base* receipt (which records met=False) is accepted as the after-receipt; the in-flight v2 working-tree
counter closes the last two and the decoy-table hole but still accepts a non-receipt blob as a receipt.
