# ScoutC62Defect — round-63 w1 report

**Seat:** ScoutC62Defect (leaf scout; no subagent dispatch)
**Item:** Re-derive the round-62 marker-only false-green from committed bytes only; confirm the documented reproduction inputs are intact. No re-runs performed.
**Verdict:** The documented reproduction inputs are INTACT — all five fixture corpus files are byte-identical (sha256) to the hashes recorded in the round-62 defect receipt, all are committed in the fleet at the measured commit `05b0d7f4b4a23513390f7b92547e2b0f1fccb06f`, and the working tree is clean. The false-green mechanism re-derives statically, exactly as documented.

Fleet root for all paths below: `/home/vgpnk/Projects/shokunin/kake-shokunin` (measured commit `05b0d7f4b4a23513390f7b92547e2b0f1fccb06f`).

## 1. Receipt under test

`/home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-62/controls/counter-false-green-l1.txt` (committed, blob `e64e284ca7ea21db1b1a70bd0c8785001d837f46` at the measured commit; working tree clean).

Receipt claims, summarized:
- An ephemeral fixture repo (scratch root `/fast/scratch/hyaku/kake-r62/L1CounterProbe/fixture`, fixture commit `6e5a16076d8c73feff41b7af2159bef9fe1046c8`) was built by copying the committed corpus `.ufo/waves/round-62/controls/false-green-fixture/corpus/`, committing it, and running `python3 -B .ufo/waves/round-62/c62_calibration.py --root "$D" --revision "$REV"`.
- Observed: `source_file_present=no`; `disagreements=1 unresolved=0 quote_correction=1 criterion=1 lesson_gate=1 source_row=1 met=true`; exit 0 — a false green: marker strings satisfy the counter while the S432 `Disagree` line remains and no S432 source body exists.
- Receipt records sha256 for 5 fixture input files.

## 2. Fixture corpus integrity — sha256 match (all 5/5)

Command (cwd `/home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-62/controls/false-green-fixture`):

```
$ sha256sum corpus/lessons/round-61-verifier-spotcheck.md corpus/knowledge/response-header-expectations.md corpus/QUALITY.md corpus/lessons/round-62.md corpus/SOURCES.md
0a9a034861b19ba9f0c2b49adb9e9c394b406816a63dc458b1b8ee62668405c3  corpus/lessons/round-61-verifier-spotcheck.md
635089aadf398ea2b17799494c5a0e209af3f87a4459234e71892d29351ba6b6  corpus/knowledge/response-header-expectations.md
373b9d254dff8668f9ae273e3f24ec87ff9b52f2c862ebabd158d76ad64d0457  corpus/QUALITY.md
d7033c6dc40448844e9c652900fb54298de8af539c8e45819e29d377bb1a8923  corpus/lessons/round-62.md
a27f4338e565e5231b48adb49c24f759612f8827927cd80cf838462ff4dd8d2b  corpus/SOURCES.md
```

| File | Receipt sha256 | Measured sha256 | Match |
|---|---|---|---|
| corpus/lessons/round-61-verifier-spotcheck.md | 0a9a0348…8405c3 | 0a9a0348…8405c3 | ✓ |
| corpus/knowledge/response-header-expectations.md | 635089aa…1ba6b6 | 635089aa…1ba6b6 | ✓ |
| corpus/QUALITY.md | 373b9d25…64d0457 | 373b9d25…64d0457 | ✓ |
| corpus/lessons/round-62.md | d7033c6d…b1a8923 | d7033c6d…b1a8923 | ✓ |
| corpus/SOURCES.md | a27f4338…4dd8d2b | a27f4338…4dd8d2b | ✓ |

## 3. Committed-state evidence (fleet git)

From cwd `/home/vgpnk/Projects/shokunin/kake-shokunin`:

```
$ git ls-tree -r 05b0d7f4b4a23513390f7b92547e2b0f1fccb06f -- .ufo/waves/round-62/controls/false-green-fixture/
100644 blob ba2f59fb2f75e6f2dd9c93adbef716cd32ccd730  .../corpus/QUALITY.md
100644 blob f875daebccb1d26961e3e0cbe412fe6fc70bc39e  .../corpus/SOURCES.md
100644 blob b9633cad90ff3b4b39714646cd0b2419776f4cfa  .../corpus/knowledge/response-header-expectations.md
100644 blob f3c99fc7901e8330d16fea275bf8591ace4f7ce  .../corpus/lessons/round-61-verifier-spotcheck.md
100644 blob 85efbb538655a0ef704aa13432b15322e8a85aec  .../corpus/lessons/round-62.md

$ git ls-tree 05b0d7f4b4a23513390f7b92547e2b0f1fccb06f .ufo/waves/round-62/controls/counter-false-green-l1.txt
100644 blob e64e284ca7ea21db1b1a70bd0c8785001d837f46  .ufo/waves/round-62/controls/counter-false-green-l1.txt

$ git status --porcelain .ufo/waves/round-62/controls/false-green-fixture/ ; git status --porcelain .ufo/waves/round-62/controls/counter-false-green-l1.txt
(empty — clean)
```

All five corpus blobs, plus the receipt, are in the measured commit tree; nothing is modified, untracked, or stale in the working tree. The fixture was introduced by commit `a5a0c444` ("round-62: retain counter false-green falsifier"), which is on the ancestry leading to the measured commit (`git log --oneline -1 05b0d7f4 -- <fixture-dir>` returned `a5a0c444`).

## 4. Static re-derivation of the false-green (no re-run, bytes only)

Frozen counter `.ufo/waves/round-62/c62_calibration.py` (committed, mode 100755, blob `484b2ebcd66d6646064721c636aa28eeec0825d1`; working tree clean). Walking its logic over the committed corpus bytes:

1. `disagreements` = lines in spot-check containing "S432" and "Disagree". Fixture `corpus/lessons/round-61-verifier-spotcheck.md` (60 B): `| S432 / Fetch | Admit | url | Disagree | generic lead-in |` → **disagreements=1**. The recorded round-61 S432 disagreement is present.
2. `quote_correction` = knowledge blob contains the exact QUOTE string AND "S432 §3.6" AND "Round-62 correction". Fixture `corpus/knowledge/response-header-expectations.md` (154 B): `Round-62 correction S432 §3.6 response header can be used to require checking of a response’s Content-Type header against the destination of a request` (curly apostrophe U+2019, byte-exact per sha256) → **quote_correction=1**.
3. `criterion` = quality blob contains "substantive located quote" and "round-61-verifier-spotcheck.md". Fixture `corpus/QUALITY.md` (57 B): `substantive located quote round-61-verifier-spotcheck.md` → **criterion=1**.
4. `lesson_gate` = lesson blob contains "## Gate", "S432", "Agree", "Reject". Fixture `corpus/lessons/round-62.md` (26 B): `## Gate S432 Agree Reject` → **lesson_gate=1**.
5. `source_row` = sources blob contains "| S432 |". Fixture `corpus/SOURCES.md` (18 B): `| S432 | source |` → **source_row=1**.
6. `resolved = all(quote_correction, criterion, lesson_gate, source_row)` → True. **`unresolved = disagreements if not resolved else 0` → 0**: the single recorded disagreement is zeroed out precisely because the markers are green. `met = unresolved == 0 and resolved` → **met=true**, exit 0.

The static output line `disagreements=1 unresolved=0 quote_correction=1 criterion=1 lesson_gate=1 source_row=1 met=true` is identical to the receipt's observed line. Note also that the counter has no source-body check at all — its only "source" evidence is the `| S432 |` marker row; no retained S432 source file exists anywhere in the corpus (directory listing shows exactly the five files), consistent with the receipt's independently observed `source_file_present=no`. The falsification is therefore faithfully reproducible from committed bytes: marker-token-only corpus → green calibration despite the live disagreement.

## 5. Gaps / caveats

- The ephemeral fixture commit hash `6e5a16076d8c73feff41b7af2159bef9fe1046c8` lives only in the deleted scratch repo (`scratch_cleanup=clean` per receipt) and cannot be re-derived from the fleet. It is not needed: the recipe is deterministic (`cp -a` of the committed corpus + `git add` + commit), and the committed corpus bytes hash-match the receipt, so any faithful re-execution rebuilds equivalent content.
- Per seat instructions I did not execute the counter; the mechanism re-derivation in §4 is static, from committed counter source + committed corpus bytes only.

## 6. Lane compliance

- Read-only against the fleet; wrote only this Report at the seat-specified path `.ufo/waves/round-63/w1/ScoutC62Defect.md`.
- No subagent dispatch, no commits, no git/jj mutation, no re-runs, no fixture creation, no installs (nothing to record).
- Frozen claim, counters, receipts, and the round-62 corpus untouched.
