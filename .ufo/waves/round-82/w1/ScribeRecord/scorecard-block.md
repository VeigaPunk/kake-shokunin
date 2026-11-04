## Round 82 — measured claims (author-side; closure owns admission)

Frozen contract `.ufo/waves/round-82/contract.md` at
`082b7dd39053e5f96ca6c463da47a3e4d83d4580`, frozen before any seat ran; no amendment, and no
predicate, item, target or kill rule moved after the freeze. Base
`419866015b1f58e01f061cde9a77d490653d3c76`; measured carrier `<rev>`. Wave `w1`: one v1 wave, 13
requested seats inside the run-15 band 8–16 — scout 2, executor 3, scribe 3, reviewer 2, critic 1,
mutation-tester 1, connector 1; requested attack share 4/13 = 30.8 % over the run-15 directive's
roles {reviewer, critic, mutation-tester, labrat}. The L1 held the planner seat, as the validator
forbids `planner` as a swarm role. Scores held: operability 10 HOLD, freshness 10 HOLD, calibration
2 HOLD.

| Claim | Axis | Before → after | Counting command | Evidence/verdict |
|---|---|---|---|---|
| C1 the round-81 routed-defect queue closes | calibration 2→2 HOLD | base `41986601`: `C1v1 revision=419866015b1f58e01f061cde9a77d490653d3c76 items=8 open=8 closed=0 met=false`, exit 1 (`.ufo/waves/round-82/controls/base-c82-defect-queue.txt`) → carrier `<rev>`: `C1v1 revision=<rev> items=8 open=0 closed=8 met=true`, exit 0 (`.ufo/waves/round-82/controls/after-c1.txt`) | `python3 -B .ufo/waves/round-82/c82_defect_queue.py --root . --revision <rev>` | measured met; counter selftest `selftest: 11/11 passed`, exit 0 (`controls/c82-selftest-c1.txt`), one green tree per item, one mutant per item and a missing-tree fixture; junk control `open=8 closed=0 met=false`, exit 1 (`controls/ctl-c82-junk-queue.txt`), whose lesson asserts all eight closed in prose and whose junk tree is rebuilt deterministically by `junk_tree_build.py` (two runs, `tree_sha256=d9302da6…`); D6's supersession row is `corpus/QUALITY.md` §Round 82 and D7's gate receipt is `controls/after-c1-ledger-gate.txt` (`events=40 undisclosed=0 … met=true`, exit 0) |
| C2 a second dated capture feeds a capture-to-capture drift gate (capability) | freshness 10→10 HOLD | base `41986601`: `C2v1 revision=419866015b1f58e01f061cde9a77d490653d3c76 declared=3 surfaces_a=3 surfaces_b=0 manifest_ok=0 receipts_ok=0 order_ok=0 floor_ok=0 determinism=0 record_equal=0 selftest_ok=0 met=false`, exit 1 (`controls/base-c82-capture-delta.txt`) → carrier `<rev>`: `C2v1 revision=<rev> declared=3 surfaces_a=3 surfaces_b=3 manifest_ok=1 receipts_ok=1 order_ok=1 floor_ok=1 determinism=1 record_equal=1 selftest_ok=1 met=true`, exit 0 (`controls/after-c2.txt`) | `python3 -B .ufo/waves/round-82/c82_capture_delta.py --root . --revision <rev>` | measured met; the record is `controls/after-c2-delta.txt` — the tool's stdout with no command line — and the counter re-derives it byte-for-byte at the revision; capture A is the round-81 tree, capture B the round-82 tree, three declared `ds4cc.com` surfaces in each; identical-capture control `order_ok=0 floor_ok=0 met=false`, exit 1 (`controls/ctl-c82-identical-capture.txt`); tampered control (real capture B with one body byte flipped, post-data and disclosed) `receipts_ok=0 met=false`, exit 1 (`controls/ctl-c82-tampered-capture.txt`) |

Move log (round 82):

| Round | Axis | Before | After | Evidence |
|---|---|---|---|---|
| 82 | calibration (HOLD 2) | `open=8 closed=0 met=false` at `41986601`; eight routed round-81 defects, three of them stale numbers in filed prose (a claimed-but-unlanded registry cell, a mislabelled measured revision, a superseded byte count) | `open=0 closed=8 met=true` at `<rev>`; every item decided by a conjunct over lane bytes — S433's two cells re-read, the round-81 receipt's own revision token matched, the fleet commit's two report blobs compared, the seat record's byte count re-derived, the two dead receipt paths probed absent, the `corpus/QUALITY.md` row superseding the stale `18/18` tally, the round-82 ledger gate receipt, the round-80 lesson's `[r82-correction` line | `.ufo/waves/round-82/c82_defect_queue.py`; `controls/base-c82-defect-queue.txt` → `controls/after-c1.txt`; `controls/ctl-c82-junk-queue.txt`; `controls/c82-selftest-c1.txt`; `corpus/QUALITY.md` §Round 82; `controls/after-c1-ledger-gate.txt` |
| 82 | freshness (HOLD 10) | `surfaces_b=0 met=false` at `41986601`: no second capture, no delta record, no drift gate; capture A had been audited once but never compared to a later instant | two dated captures of the same three declared surfaces (capture A from round 81, capture B under `.ufo/waves/round-82/capture/`), every receipt verified against its retained body, and an offline delta whose record re-derives from committed bytes at a pinned revision; identical-capture and one-byte-flipped controls both read `met=false` | `scripts/capture_delta.py`; `.ufo/waves/round-82/population/`; `.ufo/waves/round-82/capture/`; `controls/after-c2-delta.txt`; `controls/after-c2.txt`; `controls/ctl-c82-identical-capture.txt`; `controls/ctl-c82-tampered-capture.txt` |

### Demonstrated repertoire, round 82

| Capability | What it can do | Evidence pointer | First-working round |
|---|---|---|---|
| Capture-to-capture drift gate | Verifies every receipt in two dated capture trees against its retained body (GET, integer status in 100..599, byte count equal to the retained body, body sha256 equal to the receipt digest, RFC 3339 fetch time, not truncated), prints one stable line per surface in the union plus `surfaces=… identical=… changed=… added=… removed=…`, and re-derives the whole record from committed bytes at a measured revision; offline by construction (no socket call in the file), with an identical-capture control and a one-byte-flipped control that both read `met=false` | `scripts/capture_delta.py`; `.ufo/waves/round-82/c82_capture_delta.py`; `controls/base-c82-capture-delta.txt` → `controls/after-c2.txt`; `controls/after-c2-delta.txt`; `controls/ctl-c82-identical-capture.txt`; `controls/ctl-c82-tampered-capture.txt` | 82 |

Stated limits, not claimed closed: C1's row conjuncts are textual by necessity — a records-only
tree with arithmetically correct numbers can reach `open=0`, so the non-author closure is what
catches a transcription; D3 reads the fleet repo's history because the filed round-81 report is a
fleet file outside this round's write scope. C2 decides the chain, not the property: it proves two
dated captures and a reproducible delta over committed bytes, not that any surface is correct, not
that a future change would be detected, and not that a capture came from a socket — a well-formed
fabrication with real digests passes, so provenance is the capture transcript
(`w1/ExecCapture/capture-run.txt`). Freshness stays HOLD at 10 and is not re-measured live; the
capture B instants and the registry/census after-state are recorded in `controls/census-after.txt`
and the capture receipts, not inferred here.
