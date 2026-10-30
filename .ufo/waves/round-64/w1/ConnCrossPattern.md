# ConnCrossPattern — retained semantic-counter class

## Evidence and scope

Read-only static survey of `.ufo/waves/round-*/c*_*.py` and `scripts/` using the file glob and regex searches for `met`, substring membership, `json.loads`, and parsed `passed`/`ok` fields. Search hits are candidates, not automatically defects: substring matching is appropriate when literal quote occurrence is the stated property. No counter, fixture, tool selftest, or other runtime was executed. No frozen claim or receipt was modified.

**One concrete OTHER counter:** `/home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-62/c62_calibration.py:26-43` retains the marker-only calibration predicate:

- Lines 31-32 count S432/Disagree lines without interpreting their verdict.
- Lines 33-38 accept disconnected global substrings: the quote, `S432 §3.6`, `Round-62 correction`, `substantive located quote`, `round-61-verifier-spotcheck.md`, `## Gate`, `S432`, `Agree`, `Reject`, and `| S432 |`.
- Lines 39-41 combine those booleans and explicitly replace disagreement count with zero when markers pass: `unresolved = disagreements if not resolved else 0`; `met = unresolved == 0 and resolved`.
- Lines 9-15 enumerate all inputs. There is no retained raw blob, extraction recipe, digest pin, located-line derivation, or binding of the lesson to the actual spot-check verdict anywhere in this 53-line counter.

Committed-byte check, exact command:

```sh
git -C /home/vgpnk/Projects/shokunin/kake-shokunin ls-tree 4c8295fa5e3b628f1fdf3840299ae415c01849fb .ufo/waves/round-62/c62_calibration.py .ufo/waves/round-59/c59_axis_evidence.py
```

Exact output:

```text
100755 blob 59b0c26dfc728f26866e94bce39ab1aa57111238	.ufo/waves/round-59/c59_axis_evidence.py
100755 blob 484b2ebcd66d6646064721c636aa28eeec0825d1	.ufo/waves/round-62/c62_calibration.py
```

Also executed:

```sh
git -C /home/vgpnk/Projects/shokunin/kake-shokunin show 4c8295fa5e3b628f1fdf3840299ae415c01849fb:.ufo/waves/round-62/c62_calibration.py
```

Its output contains exactly these predicate lines (33-43 in the absolute file above):

```python
    correction = int(QUOTE in data["knowledge"] and "S432 §3.6" in data["knowledge"]
                     and "Round-62 correction" in data["knowledge"])
    criterion = int(CRITERION in data["quality"] and "round-61-verifier-spotcheck.md" in data["quality"])
    lesson_gate = int("## Gate" in data["lesson"] and "S432" in data["lesson"]
                      and "Agree" in data["lesson"] and "Reject" in data["lesson"])
    source_row = int("| S432 |" in data["sources"])
    resolved = correction == 1 and criterion == 1 and lesson_gate == 1 and source_row == 1
    unresolved = disagreements if not resolved else 0
    met = unresolved == 0 and resolved
    print(f"revision={rev} disagreements={disagreements} unresolved={unresolved} quote_correction={correction} criterion={criterion} lesson_gate={lesson_gate} source_row={source_row} met={str(met).lower()}")
    return 0 if met else 1
```

[INFERENCE, not an executed mutant] A nonempty spot blob `S432 Disagree`, a knowledge blob containing only QUOTE plus `S432 §3.6 Round-62 correction`, QUALITY containing only `substantive located quote round-61-verifier-spotcheck.md`, lesson containing only `## Gate\nS432 Agree Reject`, and SOURCES containing only `| S432 |` satisfy every predicate. The derived result is `disagreements=1 unresolved=0 ... met=true`, exit 0, despite no substantive resolution. QUOTE is the exact constant at line 16, not a fabricated replacement.

## Cross-surface implication and contradiction

A second surveyed transport surface illustrates why retaining the distinction matters: `/home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-59/c59_axis_evidence.py:296-305` recognizes a passing receipt by `met=True` OR an `EXIT=0` line and recognizes a tally by substring membership; lines 331-335 feed those checks into its own `met`. Its axis/section/pointer constraints are real, but do not independently execute the producer or establish its semantics. This is supporting evidence for a potential evidence-laundering path, **not** a demonstrated whole-counter bypass or a second proposed repair.

The frozen contract explicitly preserves old counters and re-runs round-63 counters for no-harm (`/home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-64/contract.md:133-139`). Thus “C1/C2 repaired here” and “the class remains in a retained predecessor” are compatible. A broader inference that every green historical counter now proves semantics would contradict the concrete c62 predicate. This finding alone does not refute round-64 C1 or C2 and does not establish a kill-rule breach.

## One bounded proposed move

In future evidence routing, keep frozen historical instruments untouched but classify c62 green receipts as **marker-consistency only**, never as independent semantic calibration support. Require the already available round-64 semantic witness when making the latter claim. This is a routing proposal only: no registry, score, contract, counter, receipt, or source file changed here.

Affected declared axes: calibration benefits by preventing marker-green promotion; operability and freshness need no tool/runtime/sidecar change. Runtime effect: none proposed. Contract effect: preserve historical predicates rather than silently strengthening them. Substrate effect: preserve committed bytes and receipt provenance. Verification effect: distinguish producer success from semantic evidence, including when receipts are consumed downstream.

Risks: routing labels could themselves become unverified prose; an allegedly independent witness must retain its revision and frozen-counter binding. Removing legacy evidence outright could lose honest historical context, so retain it with its narrower meaning. No no-harm outcome has been experimentally measured for this proposal.

## Verification and disposition

Attacked the semantics-binding interpretation of the retained round-62 counter through complete static predicate tracing. Finding: marker-only acceptance remains structurally present; runtime reproduction is unexercised. No judgment/admission of the round's claims is made.

Suggested owner verification, not run here: materialize the five marker-only blobs in an isolated, pre-existing committed fixture permitted by the owner; run the frozen c62 counter and record all output and exit status, then compare the semantic c64 counter on the same evidence. Do not alter either frozen instrument. A future routing control should also reject semantic promotion of c62-only receipts while retaining them as historical marker evidence.

No tools installed or upgraded. Only read-only Git commands were used. Own scratch directory was empty and removed before handoff; no fixtures, archives, or clones were created.
