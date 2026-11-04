<!-- DRAFT for L1 integration — delete this comment block before appending.

Placeholders this draft leaves for the L1 (all after-state, none invented here):
  <<carrier>>      the measured carrier revision (40 hex) named by the after receipts
  <<after-c1>>     the `C1v1 revision=… items=6 open=0 closed=6 met=true` line
                   `c83_defect_queue.py --revision <carrier>` prints
  <<after-c2>>     the `C2v1 revision=… … met=true` line
                   `c83_drift_class.py --revision <carrier>` prints
  <<verdict-c1>>   one sentence: measured met, exit code, selftest tally, junk-control line
  <<verdict-c2>>   one sentence: measured met, exit code, classifier record, control-pair line

Every number below that is not a placeholder was read from a committed file named beside it.
-->

## Round 83 — measured claims (author-side; closure owns admission)

Frozen contract `.ufo/waves/round-83/contract.md` at
`64b7199281e5457df0e08652977f698c4f34f46e`, frozen before any seat ran; no amendment, and no
predicate, item, target or kill rule moved after the freeze. Base
`826b0061f233ce1dffb9bd6874abc1342a864247`; measured carrier `<<carrier>>`. Wave `w1`: one v1
wave, 14 requested seats inside the run-15 band 8–16 — scout 2, executor 4, scribe 3, reviewer 2,
mutation-tester 2, critic 1; requested attack share 5/14 = 35.7 % over the run-15 directive's roles
{reviewer, critic, mutation-tester, labrat}. The L1 held the planner seat, as the validator forbids
`planner` as a swarm role. Scores held: operability 10 HOLD, freshness 10 HOLD, calibration 2 HOLD.

| Claim | Axis | Before → after | Counting command | Evidence/verdict |
|---|---|---|---|---|
| C1 the round-82 routed-defect queue closes | calibration 2→2 HOLD | base `826b0061`: `C1v1 revision=826b0061f233ce1dffb9bd6874abc1342a864247 items=6 open=6 closed=0 met=false`, exit 1 (`.ufo/waves/round-83/controls/base-c83-defect-queue.txt`, whose last line reads `base_c1_exit=1`) → carrier `<<carrier>>`: `<<after-c1>>` (`.ufo/waves/round-83/controls/after-c1.txt`) | `python3 -B .ufo/waves/round-83/c83_defect_queue.py --root . --revision <<carrier>>` | <<verdict-c1>>; counter selftest `selftest: 9/9 passed`, exit 0 (`.ufo/waves/round-83/controls/c83-selftest-c1.txt`) — one green tree per item, one mutant per item and a missing-tree fixture; junk control `open=6 closed=0 met=false`, exit 1 (`.ufo/waves/round-83/controls/ctl-c83-junk-queue.txt`) over the tree rebuilt from `junk-tree.json` |
| C2 the drift gate's header changes are classified and the verdict re-derives (capability) | freshness 10→10 HOLD | base `826b0061`: `C2v1 revision=826b0061f233ce1dffb9bd6874abc1342a864247 declared=3 surfaces_a=3 surfaces_b=3 receipts_ok=1 diffs=14 validator=0 representation=0 unknown=0 verdict=same-object record_equal=0 determinism=0 control_ok=0 tool_offline=0 selftest_ok=0 tool_absent=1 met=false`, exit 1 (`.ufo/waves/round-83/controls/base-c83-drift-class.txt`, whose last line reads `base_c2_exit=1`) → carrier `<<carrier>>`: `<<after-c2>>` (`.ufo/waves/round-83/controls/after-c2.txt`) | `python3 -B .ufo/waves/round-83/c83_drift_class.py --root . --revision <<carrier>>` | <<verdict-c2>>; counter selftest `selftest: 9/9 passed`, exit 0 (`.ufo/waves/round-83/controls/c83-selftest-c2.txt`); the classifier's own record `.ufo/waves/round-83/controls/after-c2-classes.txt` prints three surface lines plus `summary surfaces=3 diffs=14 per_request=14 validator=0 representation=0 policy=0 unknown=0 verdict=same-object` at the frozen captures; the control pair must classify `# control=verdict=representation-changed validator=1`, and the identical-pair tree must read `control_ok=0 met=false`, exit 1 (`.ufo/waves/round-83/controls/ctl-c83-control-class.txt`) |

Move log (round 83):

| Round | Axis | Before | After | Evidence |
|---|---|---|---|---|
| 83 | calibration (HOLD 2) | `open=6 closed=0 met=false` at `826b0061`; the six defects the non-author round-82 closure routed at the round-82 report, lesson and evidence chain — an attack population that settled 0/7, wave-prose character counts printed as bytes, an instrument rebind with no committed receipt, an erratum that named kinds instead of quoting the superseded text, five open counter-mutation survivors, and a Gate summary that named a category the lesson never filed | `<<after-c1>>` at `<<carrier>>`; every item carried by a state conjunct re-derived from a non-lesson file — the wave accounting re-derived from spec+results, UTF-8 `output_bytes` per settled seat, the `instrument_receipts.py --check` receipt, the fleet commit's removed report lines quoted back into the lesson, the executable killer suite `distinguished=5/5`, and the round-83 `corpus/QUALITY.md` criterion line — plus a row conjunct in `corpus/lessons/round-83.md` for each item | `.ufo/waves/round-83/c83_defect_queue.py`; `controls/base-c83-defect-queue.txt` → `controls/after-c1.txt`; `controls/ctl-c83-junk-queue.txt`; `controls/c83-selftest-c1.txt` |
| 83 | freshness (HOLD 10) | `tool_absent=1 met=false` at `826b0061`: the round-82 drift gate compared status, body sha256 and the header mapping but never classified a changed header, so a changed `etag` and a changed `date` read alike | `<<after-c2>>` at `<<carrier>>`; every changed header between capture A and capture B classified against the frozen class table as per-request / validator / representation / policy / unknown, a surface `representation-changed` on status, body sha256 or any validator/representation/unknown change, and the whole verdict re-derived offline from committed bytes with a determinism pair, an identical-pair control and a control pair that must classify `representation-changed` with `validator>=1` | `scripts/header_change_class.py`; `.ufo/waves/round-83/c83_drift_class.py`; `controls/after-c2-classes.txt`; `controls/base-c83-drift-class.txt` → `controls/after-c2.txt`; `controls/ctl-c83-control-class.txt`; `controls/c83-selftest-c2.txt` |

### Demonstrated repertoire, round 83

| Capability | What it can do | Evidence pointer | First-working round |
|---|---|---|---|
| Header-change classifier | Reads two dated capture trees of the declared surfaces and verifies each receipt against its retained body (GET, integer status 100..599, byte count equal to the body, body sha256 equal to the receipt digest, not truncated); canonicalises each surface's header list (lower-cased name, repeated values joined with `, `); classifies every changed header against the frozen class table as `per-request`, `validator`, `representation`, `policy` or `unknown`, with `unknown` decisive by design so a change is never waved through silently; prints one line per surface in declared order plus `summary surfaces=… diffs=… per_request=… validator=… representation=… policy=… unknown=… verdict=…`; a surface is `representation-changed` when status or body sha256 differs or any changed header is validator/representation/unknown, otherwise `same-object`. Offline by construction (no `socket`, `urllib`, `requests` or `http.client` reference outside the docstring), selftested, and exercised by a control pair that must classify `representation-changed` with `validator>=1` | `scripts/header_change_class.py`; `.ufo/waves/round-83/c83_drift_class.py`; `.ufo/waves/round-83/controls/after-c2-classes.txt`; `.ufo/waves/round-83/controls/ctl-c83-control-class.txt`; `.ufo/waves/round-83/controls/after-c2.txt` | 83 |

Stated limits, not claimed closed: both scores are held — C1 and C2 move evidence, not the scalar,
so calibration stays 2 and freshness stays 10. C1's row conjuncts are textual by necessity (a Gate
summary is prose; a records-only tree with arithmetically correct numbers can reach `open=0`), and
the D6 criterion is read from one physical line, so a paraphrase that never contradicts the lesson
passes; the non-author closure is what catches a mis-transcription. C2 decides the capture chain,
not the property: it proves two committed capture trees and a reproducible classification, not that
any surface is correct, not that a future change would be detected, and not that a capture came
from a socket — a well-formed fabrication with real digests passes, so provenance stays the capture
transcript. The class table is frozen by header name, so a changed header outside it is `unknown`
and decisive by design, and a `policy` header whose new value changes freshness semantics still
reads `policy`. Freshness is not re-measured live this round.
