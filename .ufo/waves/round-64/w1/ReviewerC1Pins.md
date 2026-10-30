# ReviewerC1Pins — C1 pin wiring review

Recommendation: the four evidence-byte pins hold under static review; do not interpret `pins=1` as binding every input or the spot-check verdict. One medium-severity semantic binding gap remains outside those four pins. No admission/settlement judgment is issued.

Axes: evidence identity, revision isolation, extraction equality, hostile-ledger reachability, verdict provenance.

## Findings, by severity

### Medium — spot-check reason is unpinned and never compared to the frozen verdict span

Evidence: `/home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-64/c64_calibration.py:193-198` reads the revision's spot-check but uses it only to count lines containing both `S432` and `Disagree`. `:90-95` excludes this file from `PIN_SHAS`. `:252-259` searches the lesson Gate for the constant `SPOT_VERDICT_SPAN`, not for the actual spot-check row's reason. `:267-270` then resolves the counted disagreement from that lesson gate. The currently retained reason is at `/home/vgpnk/Projects/shokunin/kake-shokunin/corpus/lessons/round-61-verifier-spotcheck.md:33`.

[INFERENCE, static counterexample, not executed] Keep all T0 files except replace `corpus/lessons/round-61-verifier-spotcheck.md` with exactly `S432 Disagree\n`. All four pinned bytes, recipe output, class, located span and other prose inputs are unchanged; `disagreements` remains 1; therefore the control flow preserves `pins=1`, `lesson_gate=1`, `unresolved=0`, and `met=true`, although the spot-check now contains no verdict reason at all. This contradicts the stronger claim that the Gate is bound to that revision's actual verdict span, not the narrow fact that four evidence blobs are pinned. Shared this boundary with ReviewerC1Predicate; no independent runtime reproduction is claimed here.

## Requested pin attacks

- **Same bytes at two Git paths:** no byte-evidence bypass found. `git_show` at `:104-110` uses `revision:rel`; `:200,206-208` hashes each returned blob against that path's constant. An extra copy at an unrelated path cannot satisfy a missing canonical path. Identical bytes at the required path legitimately satisfy byte identity; Git blob identity does not encode provenance. Symlink targets are not followed by this `git show` access: the symlink blob would itself have to equal the frozen content. Tree modes and external provenance are not checked, but neither is a changed-byte `pins=1` demonstrated by copying a blob.
- **Committed text versus recipe output:** `:225-229` passes the pinned raw bytes to the pinned recipe and requires both byte-for-byte equality with the committed text and equality with `TEXT_SHA`. `met` requires `recipe_rederive` at `:268`. No decoding/normalization-only equality or ledger-supplied digest substitutes for this comparison.
- **Pinned-but-hostile ledger:** the pinned ledger at `/home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-63/quote-class/quote-classes.json:1-18` is a JSON object with one S432 dictionary, expected paths/digests, `matchClass=collapsed-only`, and `locatedRawLines=6150-6154`. No duplicate-key or hostile row structure is present. `parse_ledger` at `:133-148` catches ordinary JSON/decode/shape errors, and `:220` supplies no ledger bytes at all when a pin fails. A different hostile JSON ledger cannot reach the `pins=1` branch without the excluded digest-collision premise. The parser does not generally validate all ledger fields, but the frozen full-ledger hash binds those fields here. The selected row's class and located range are separately checked at `:238-243`.
- **Worktree reads:** no evidence worktree read was found in `evaluate`: all nine evidence documents come through `git_show` at `:193,200-204`. The recipe module is read back from a fresh temporary file containing revision-materialized bytes (`:122-130,222-226`), not the repository's recipe path. The pinned recipe's `extract` at `/home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-63/quote-class/extract_text.py:60-64` only consumes its argument; the file-opening CLI at `:91-97` is not invoked by the counter. The counting command itself executes a filesystem counter, so instrument identity remains an external freeze obligation; `pins` does not self-hash the running counter. The selftest launches filesystem `__file__` (`c64_calibration.py:330-335`), not a revision-materialized counter. These are instrument/runtime trust boundaries, not evidence-path fallbacks.

## Unpinned inputs and residual risk

Revision-read but not digest-pinned: spot-check, knowledge correction, QUALITY criterion, round-64 lesson, SOURCES (`c64_calibration.py:77,86-89,193-204`). Their contents are predicate inputs, not protected by `pins=1`. Invocation root/revision, Git executable/config/object database, Python runtime/imports, and temporary-directory environment are also trusted inputs. The resolved revision OID from `rev-parse` is not captured: `:187` verifies the supplied expression and later calls reuse that expression (`:193,200-204`), so immutable full commit IDs are the reviewed use case; moving refs are not snapshot-isolated. No runtime/import/Git replacement or same-identity rerouting attack was executed, and no saturation claim is made. This counter has no resume-continuity path.

## Commands and observed output

All commands used read-only Git access to the lane. Let the following displayed commands stand literally, including their absolute paths:

```sh
git -C /home/vgpnk/Projects/shokunin/kake-shokunin diff 1a48131577ba82c967650561be34e8dba909432a 4c8295fa5e3b628f1fdf3840299ae415c01849fb -- .ufo/waves/round-64/c64_calibration.py
```

Observed summary: `.ufo/waves/round-64/c64_calibration.py | 449 ++++++++++++++++++++++++`; `1 file changed, 449 insertions(+), 0 deletions(-)`. The measured source was also read with:

```sh
git -C /home/vgpnk/Projects/shokunin/kake-shokunin show 4c8295fa5e3b628f1fdf3840299ae415c01849fb:.ufo/waves/round-64/c64_calibration.py
```

The following five exact commands each produced the SHA shown immediately below:

```sh
git -C /home/vgpnk/Projects/shokunin/kake-shokunin show 4c8295fa5e3b628f1fdf3840299ae415c01849fb:.ufo/waves/round-64/c64_calibration.py | sha256sum
5489eb2f3ac498e0383d841c677f036231fbf6933717d8da447f3193ff088adf  -
git -C /home/vgpnk/Projects/shokunin/kake-shokunin show 4c8295fa5e3b628f1fdf3840299ae415c01849fb:.ufo/waves/round-61/sources/S432.html | sha256sum
63b0a018753c330adf1e40417524eb70ea02d4d3e123bcb39b6770f23bad911b  -
git -C /home/vgpnk/Projects/shokunin/kake-shokunin show 4c8295fa5e3b628f1fdf3840299ae415c01849fb:.ufo/waves/round-63/quote-class/S432.txt | sha256sum
8b90d096d2653ce57025e25c5bee5c63df66692e15ef8579371032da6f542a69  -
git -C /home/vgpnk/Projects/shokunin/kake-shokunin show 4c8295fa5e3b628f1fdf3840299ae415c01849fb:.ufo/waves/round-63/quote-class/quote-classes.json | sha256sum
5f48e26be27975ee55702cac1e1b20b61f3bd5906910c865f5192bd7e010c42d  -
git -C /home/vgpnk/Projects/shokunin/kake-shokunin show 4c8295fa5e3b628f1fdf3840299ae415c01849fb:.ufo/waves/round-63/quote-class/extract_text.py | sha256sum
6b0a88cddfa3b712e8fdbe69c4c2803c816490cd43893972dfe0d39d5f362405  -
```

Existing receipt, not my execution: `/home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-64/controls/after-c1.txt:1-3` records:

```text
$ python3 -B .ufo/waves/round-64/c64_calibration.py --root . --revision 4c8295fa5e3b628f1fdf3840299ae415c01849fb (measured revision T0, contract .ufo/waves/round-64/contract.md §C1)
revision=4c8295fa5e3b628f1fdf3840299ae415c01849fb disagreements=1 pins=1 pin_drift=none recipe_rederive=1 ledger_state=ok derived=collapsed-only class_match=1 located=6150-6154 quote_correction=1 criterion=1 lesson_gate=1 source_row=1 unresolved=0 met=true
exit=0
```

## Verification gaps and bounds

`read xd://lsp` returned `No such tool: xd://lsp`; no language server/status/references/definition/diagnostics device was available. Findings use source control-flow review, not semantic-tool proof. Reviewer role prohibits invoking another runtime, so no Python counter, mutant, selftest, build, or fixture commit was executed. No tools were installed. No lane artifact except this report was written. Seat scratch was created at `/fast/scratch/hyaku/kake-r64/ReviewerC1Pins` and removed before yielding.

Self-evaluation: accuracy 4/5 (static inference explicitly distinguished from execution); completeness 4/5 (all four requested attacks inspected, runtime reproduction prohibited); clarity 4/5 (separate finding/trust boundaries); actionability 4/5 (one-file exact counterexample supplied); conciseness 4/5 (command transcripts retained for evidence). Overall 4.0/5. Highest-impact next verification belongs to the main agent: reproduce the single-line spot-check replacement with the frozen counter and immutable revision. Would the user agree? Likely, provided this remains a scoped static recommendation rather than a reproduced kill claim.
