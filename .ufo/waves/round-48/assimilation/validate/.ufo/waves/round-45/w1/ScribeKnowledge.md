# ScribeKnowledge — C1 knowledge entry draft (`corpus/knowledge/receipt-integrity.md`)

Seat `kake-r45.ScribeKnowledge` (wave 1, build). Axes: **operability** (the entry must give an
operator a rule that rejects a bad receipt on sight), **freshness** (provenance trio + a recheck
command that exists and runs). No product code, judge, commit, or corpus file touched: the corpus is
L1-write-only this wave, so the entry is a draft under `drafts/`.

## What I did

1. Read the round-44 evidence: `.ufo/waves/round-44/w2/ReviewCounterContract.md` (§Defect 1(a)–(c)),
   the frozen v1 driver `.ufo/waves/round-44/c44_audit.py`, and the frozen counter's receipt-writing
   paths in `.ufo/waves/round-44/c44_count_v5.py`.
2. Re-read the v2 gate as built by the sibling seat (`.ufo/waves/round-45/c45_audit.py`, uncommitted
   at writing) so the entry's "binding rule" describes the shipped predicate, not the prose spec.
3. Opened the S133 source (`subprocess` docs) once, read-only, for the `returncode` passage.
4. Wrote the draft with: the three defect classes each carrying a round-44 evidence pointer; the
   v2 five-clause validity gate; the do-nothing reachability note; opinion marked as opinion; every
   count with its command; and the registry-status dependency.

## Decisive command output (verbatim)

```
$ sha256sum .ufo/waves/round-44/c44_audit.py
8ee2c8bf9333206963236b023048ae2b560bbec703adef4d448bd5529c2d0c75  .ufo/waves/round-44/c44_audit.py

$ python3 -B .ufo/waves/round-44/c44_audit.py --selftest
SELFTEST PASS: class and mixed-key witnesses pass, legacy/timing-only and no-class witnesses fail
SELFTEST_EXIT=0

$ grep -cE "^\*\*\([abc]\) " .ufo/waves/round-44/w2/ReviewCounterContract.md
3

$ grep -cE "^\|[[:space:]]*S[0-9]{3,}[[:space:]]*\|" corpus/SOURCES.md ; grep -oE … | tail -1 ; grep -c S133 corpus/SOURCES.md
132
| S132
0
```

Witness-split re-derivation over both files named `after-v5.json` (the entry's counts section):

```
.ufo/waves/round-44/verification/claim/after-v5.json witnessed=23/27 ok=False build_met=3/3 class_only=22 mixed=1 met=4 other=0
.ufo/waves/round-44/verification/claim/after-final/after-v5.json witnessed=27/27 ok=True build_met=3/3 class_only=26 mixed=1 met=0 other=0
```

v2 gate as built (read, not run): `.ufo/waves/round-45/c45_audit.py:68-86` is one
`receipt_validity(receipt, exit_code, mtime_bounds, counter_sha)` returning
`(False, "counter_error")` for exit ∉ {0,1}; `(False, "tool_absent")` for `note == "tool absent"`;
`(False, "stale_receipt")` for counter-sha mismatch, missing `seed`, or mtime outside
`[started_ns-1s, finish_ns+1s]`; manifest written before spawning (`:223-227`), non-empty outdir
refused (`:201-203`), invalid rows excluded from witness and not-met counts (`:101,105,111,115`).

Recheck command exists and accepts the stages (`--help`, read-only):

```
usage: c45_matrix.py [-h] --stage {before,after} [--with-honest]
```

## Named attack — verdict

**PASS on the draft's operability criterion**: every one of the three defect classes carries a
`file:line` site in the frozen bytes plus an executed round-44 probe pointer (§1(a) `:41-55`, §1(b)
`:57-71`, §1(c) `:73-96` of the review); the v2 rule is stated as the five clauses the shipped
predicate actually implements; the do-nothing note states the direction of reachability (v1
reachable → v2 not), so an operator can decide a future receipt.

**Gap, stated rather than papered over**: I did not run `c45_matrix.py --stage before|after` — it
writes `.ufo/waves/round-45/verification/matrix/`, outside my write path, and `ExecMatrixRunner`
owns it. The draft therefore quotes the frozen declaration's before/after figures and the round-44
receipts, not a round-45 measurement.

## Findings

1. **Two receipts share the name `after-v5.json`, and they disagree.** The frozen C2(c) sentence
   ("22 class-only + 1 mixed + 4 met") re-derives from
   `verification/claim/after-v5.json` (23/27 witnessed, `ok=False`), while the later
   `verification/claim/after-final/after-v5.json` re-derives 26/1/0 (27/27 witnessed, `ok=True`),
   which is what the round-45 C1 declaration's "27/27 witnessed, build 3/3" refers to. The sibling
   draft `drafts/witness-split-sentence.md` reports the 26/1/0 figure and calls the 22/1/4 statement
   wrong; on the bytes, both numbers are right — for different files. Any future citation of "the
   round-44 claim receipt" must name the file. Verbatim counts above; I did not resolve which file
   the frozen sentence intended (that is the canonical judge's call).
2. **S133 is not in this lane's registry yet.** `corpus/SOURCES.md` holds 132 rows, last id `S132`,
   and `grep -c S133` → 0. The draft's `source:` cites S133, which the L1 must land with the entry
   (the sibling `ScribeSourcesGate` seat drafts that row). Recorded in the draft's own
   "Registry status" section so the dependency is visible in the entry, not just here.
3. **Round-44's three probes are the review's, not mine.** The draft says so explicitly; probes A/B
   are classifier-shape probes and probe C is an end-to-end planted-receipt run — all executed by
   `kake-r44.ReviewCounterContract`, none re-run by this seat.
4. **Fixture provenance is real-counter sourced.** Each fixture README states its receipt's origin
   (`after-final/tools/headtail-V1.json`, `build-1.json`), so the entry's "a receipt copied byte-for-
   byte" phrasing matches what the fixtures actually do.

## Files written

- `.ufo/waves/round-45/drafts/receipt-integrity.md` — the entry draft (8,373 bytes; provenance trio
  one line per field, matching `corpus/knowledge/claim-count-derivation.md`).
- `.ufo/waves/round-45/w1/ScribeKnowledge.md` — this report.
- Scratch `/fast/scratch/hyaku/kake-r45/ScribeKnowledge/` created; no temp files needed.

No tool installed or upgraded (python3 3.14.8 and coreutils already present; pacman paused and
untouched). No write outside the draft path, scratch, and this report.

## Unrun / out of scope

- `c45_matrix.py --stage before|after` — unrun (owned by `ExecMatrixRunner`; writes outside my path).
- v2 `--selftest` — unrun (owned by `ExecDriverV2`).
- No verdict on C1 itself; the entry documents the mechanism and its evidence pointers only.
